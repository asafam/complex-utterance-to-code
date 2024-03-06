from typing import List, Union, Optional, TypeVar, Generic
import os
import pandas as pd
import numpy as np
import ast
import math
import glob
from representations.tree.tree import Tree
from representations.builders.ast.tearers.tearer_factory import TearerFactory
import tokenize
from nltk.translate import bleu_score
from nltk.translate.bleu_score import SmoothingFunction
from sklearn import metrics
import signal
from contextlib import contextmanager
from tqdm.auto import tqdm
import re
tqdm.pandas()


def clean_output(output: str) -> str:
    if output is None:
        return None

    cleaned_output = output

    cleaned_output = re.sub(".*```(python|py)", "```", cleaned_output)
    x = cleaned_output.split("```")
    cleaned_output = x[1 if (len(x) > 1) else 0]

    regex_strings_to_remove = ['^Code:\n', '^Dense ast:\n', '^.*Dense AST:\n']
    for regex_string_to_remove in regex_strings_to_remove:
        cleaned_output = re.sub(regex_string_to_remove, "", cleaned_output, flags=re.DOTALL)

    return cleaned_output


def parse_code_rep_to_code(code_rep: str, rules_enabled: bool = False, verbose: str = "Fatal") -> str:
    try:
        tree = Tree.unparse(code_rep)
        tearer = TearerFactory().get_tearer(tree.root_node, rules_enabled=rules_enabled)
        asdl = tearer.tear(tree.root_node)
        code = ast.unparse(asdl)
    except Exception as e:
        if verbose == "Error":
            print(f"[Error] failed to prase code rep to code:\n", e)
        code = ""
    finally:
        return code


def build_test_code(
    code: str,
    imports: str,
    test: str,
    code_embed_str: str = "# end code block to test",
    fail_on_error: bool = False,
    verbose: str = "Fatal",
):
    if not code:
        return None

    try:
        code_insert_idx = test.find(code_embed_str)
        program_code = imports
        program_code += "\n"
        program_code += test[:code_insert_idx]
        program_code += code
        program_code += "\n"
        program_code += test[code_insert_idx:]
    except Exception as e:
        if verbose == "Error":
            print("[ERROR] Failed to unparse code rep to code\n", e)
        if fail_on_error:
            raise e
        program_code = ""
    finally:
        return program_code


def tokenize_source(code):
    file_path = "/tmp/example.py"

    with open(file_path, "w") as text_file:
        text_file.write(code)

    with open(file_path, "rb") as f:
        tokens_gen = tokenize.tokenize(f.readline)

        tokens = [token.string for token in tokens_gen]

    os.remove(file_path)
    return tokens


class TimeoutException(Exception):
    pass


def signal_handler(signum, frame):
    raise TimeoutException("Timed out!")


def suppressed_print(*args, **kwargs):
    pass


def suppressed_input(*args, **kwargs):
    return ''


def suppressed_sleep(*args, **kwargs):
    time.sleep(2)

def suppressed_scheduler_run(*args, **kwargs):
    pass


def eval_code(code: str):
    test_results = {}

    if not code:
        test_results["code_failure"] = 1
    elif any([(illegal_str in code) for illegal_str in ["import time", "import sched", "import pygame", "from time import"]]):
        test_results["execution_failure"] = 1
    else:
        try:
            local_scope = {
                'print': suppressed_print,
                'input': suppressed_input,
                'time.sleep': suppressed_sleep,
                'scheduler.run': suppressed_scheduler_run
            }
            signal.signal(signal.SIGALRM, signal_handler)
            time_limit = 1
            signal.alarm(time_limit)
            exec(code, local_scope)
            signal.alarm(0)

            test_results = local_scope.get("test_results", {})
            test_results["execution_success"] = test_results.get("execution_success", 0) + 1
        except AssertionError as e:
            test_results["assertion_failure"] = test_results.get("assertion_failure", 0) + 1
        except TimeoutException as e:
            test_results["execution_failure"] = test_results.get("execution_failure", 0) + 1
            print(code[code.index("# start code block to test"):code.index("# end code block to test")])
            print(e)
        except Exception as e:
            test_results["execution_failure"] = test_results.get("execution_failure", 0) + 1

    code_failure = test_results.get("code_failure", 0)
    assertion_failure = test_results.get("assertion_failure", 0)
    execution_failure = test_results.get("execution_failure", 0)
    execution_success = test_results.get("execution_success", 0)
    correct = test_results.get("correct", 0)
    incorrect = test_results.get("incorrect", 0)
    total = (correct + incorrect) or math.inf
    accuracy = (1 - code_failure) * (correct / total)

    results = dict(
        code_failure=code_failure,
        execution_success=execution_success,
        execution_failure=execution_failure,
        assertion_failure=assertion_failure,
        correct=correct,
        incorrect=incorrect,
        accuracy=accuracy,
    )

    return results


def generate_predictions(
    df,
    experiment_params,
    gold_column,
    id_labels,
    file_path=None,
    n=1,
    batch_size=4,
    num_workers=8,
    output_column="output",
):
    outputs = []
    targets = []
    ns = []
    ids = {}

    for id_label in id_labels:
        ids[id_label] = []

    filtered_df = df[df[output_column].isna()] if output_column in df else df # generate predictions only for
    unique_df = filtered_df.drop_duplicates(subset=id_labels)

    if unique_df.empty:
        return df


    # create a tokenizer and load the model
    model_name = experiment_params.get("model_name")
    pretrained_model_path = experiment_params.get("pretrained_model_path")
    tokenizer = load_tokenizer(
        model_name=model_name,
        pretrained_model_name_or_path=pretrained_model_names_mapping[model_name]
    )
    model = load_model(
        model_name=model_name,
        pretrained_model_name_or_path=pretrained_model_path
    )
    model.eval()

    # load the dataset
    strategy = experiment_params.get("strategy")
    strategy_params = strategies_params[strategy]
    dataset_args = get_dataset_args(tokenizer, strategy_params)
    max_length = dataset_args['max_target_length']

    if experiment_params.get("model_name") in [Model.CodeLlama7b]:
      dataset_args["strategy"] = strategy
      dataset = ComplexPromptCodeDataset(data=unique_df, **dataset_args)
      # dataset = get_dataset(df=unique_df, tokenizer=tokenizer, strategy=experiment_params.get("strategy"))
    else:
      dataset = ComplexUtteranceCodeDataset(data=unique_df, **dataset_args)

    dataloader = DataLoader(dataset, batch_size=batch_size, num_workers=num_workers)

    for batch in tqdm(dataloader):
        outs = model.generate(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
            max_length=max_length,
            do_sample=n>1,
            num_return_sequences=n
        )

        output = [tokenizer.decode(out, skip_special_tokens=True) for out in outs]
        target = [t.strip() for t in list(np.repeat(batch[gold_column], n))]

        outputs.extend(output)
        targets.extend(target)
        ns.extend(list(np.arange(n)) * (batch["input_ids"].shape[0]))
        for id_label in id_labels:
            ids[id_label].extend(list(np.repeat(batch[id_label], n)))

        preds_df = pd.DataFrame({
            **{
                output_column: outputs,
                "target": targets,
                "n": ns,
            },
            **ids
        })

        if file_path:
            preds_df['sample_id'] = preds_df['sample_id'].astype('int64')
            df['sample_id'] = df['sample_id'].astype('int64')

            # preds_df = (df.set_index(id_labels)).merge(preds_df, on=id_labels, how='left')

            # Merge the DataFrames
            suffix_preds = '_preds'
            merged_df = pd.merge(df, preds_df, on=id_labels, how='left', suffixes=('', suffix_preds))

            # Update 'n' and 'output' in df where they are None
            for column in preds_df.columns:
              merged_column = f"{column}{suffix_preds}"
              if merged_column in merged_df:
                merged_df[column] = merged_df[column].combine_first(merged_df[merged_column])
                merged_df.drop(merged_column, axis=1, inplace=True)
            preds_df = merged_df

            # preds_df = df.merge(preds_df, on=id_labels, how='left')
            preds_df.to_csv(file_path)
            # total_preds_count = preds_df['sample_id'].nunique()
            # generated_preds_count = preds_df[preds_df[output_column].notna()]['sample_id'].nunique()
            # pending_preds_count = preds_df[preds_df[output_column].isna()]['sample_id'].nunique()
            # print(f"Generated {generated_preds_count} / {total_preds_count} ({(100. * generated_preds_count / total_preds_count):.0f}%) and saved to {file_path}")

    return preds_df


def humaneval_accuracy_score(
    n,
    ks,
    data: pd.DataFrame,
    code_column_name: str = "pred_code",
    score_id_labels: Union[str, List[str]] = ["sample_id", "sample_minor_id"],
    score_column_name: str = "accuracy",
    soft=True
):
    test_codes = data.apply(
        lambda x: build_test_code(
            code=x[code_column_name], imports=x["imports"], test=x["test"]
        ),
        axis=1,
    )
    print("In humaneval_accuracy_score...")
    test_results = test_codes.progress_apply(lambda test_code: eval_code(test_code))
    test_results_df = pd.DataFrame.from_records(
        test_results.values, index=test_results.index
    )
    results = []
    for soft in [False, True]:
      for k in [1, 10]:
        test_scores_df = test_results_df.copy().reset_index()
        projected_score_column_name = score_column_name + '_projected'
        test_scores_df[projected_score_column_name] = test_scores_df[score_column_name].apply(lambda x: x if (soft or(x == 1.0)) else 0)
        scores = (
            test_scores_df
            .groupby(score_id_labels)
            .apply(lambda x: x[projected_score_column_name].sum())
            .apply(lambda c: pass_at_k(n=n, c=c, k=k))
        )
        score = scores.mean()
        # print(f"len = {scores.shape[0]}, mean = {scores.sum() / scores.shape[0]}, score = {score}")
        print(f"Humaneval: n={n}\tk = {k}\tsoft = {soft}\tlen = {scores.shape[0]}\tscore = {score}")
        result = dict(score=score, n=n, k=k, soft=soft, results=test_results_df)
        results.append(result)
    return results


def bleu_accuracy_score(
    data: pd.DataFrame,
    generated_column="generated_code",
    gold_column="code",
    score_id_labels1: Union[str, List[str]] = ["sample_id", "sample_minor_id", "n"],
    score_id_labels2: Union[str, List[str]] = ["sample_id", "sample_minor_id"],
    score_column_name: str = "bleu_score",
):
    eval_results = data.apply(
        lambda x: eval_bleu(x[gold_column], x[generated_column]), axis=1
    )
    eval_results_df = eval_results.to_frame("bleu_score")
    test_scores = (
        eval_results_df.reset_index(drop=False)
        .groupby(score_id_labels1)[score_column_name]
        .mean()
    )
    score = (
        test_scores.reset_index(drop=False)
        .groupby(score_id_labels2)[score_column_name]
        .max()
        .mean()
    )
    return dict(score=score, results=eval_results_df)


def pass_at_k(n, c, k):
    """
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@$k$
    """
    if (n - c) < k:
        return 1.0
    score =  1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))
    return score


def eval_bleu(code, generated_code):
    if not code or not generated_code:
        return 0

    hypothesis = tokenize_source(code)

    try:
        reference = tokenize_source(generated_code)
    except:
        return 0

    n = max(min(len(hypothesis), 4), 1)
    weight = 1 / n
    weights = (weight,) * n
    smoothing_function = SmoothingFunction().method4
    score = bleu_score.sentence_bleu(
        [reference], hypothesis, weights=weights, smoothing_function=smoothing_function
    )
    return score


def model_eval(
    n,
    ks,
    results_df=None,
    results_file_path=None,
    output_column="output",
    gold_column="code",
    code_column="generated_code",
    should_clean_output=True,
    parse_to_code=False,
    parse_rules_enabled=False,
    compute_humanval=True,
    compute_bleu=True,
    force_parse_code_rep_to_code=True,
):
    results_df = (
        pd.read_csv(results_file_path) if results_file_path else results_df.copy()
    )
    results_df['sample_minor_id'].fillna('a', inplace=True)
    results_df = results_df.loc[:, ~results_df.columns.str.contains('^Unnamed')]
    results_df.set_index(['sample_id', 'sample_minor_id', 'n'], inplace=True)
    results_df.sort_index(inplace=True)

    if should_clean_output:
        results_df[output_column] = results_df[output_column].apply(clean_output) # clean the output from prompt strings

    if parse_to_code:
        print(f"Parsing rep code to code ({results_df[results_df[code_column].isna()].shape[0] if (code_column in results_df) else results_df.shape[0]})")
        results_df[code_column] = results_df.progress_apply(
            lambda x: x[code_column] if (not force_parse_code_rep_to_code and (code_column in x) and x[code_column]) else parse_code_rep_to_code(x[output_column], rules_enabled=parse_rules_enabled),
            axis=1
        )
    else:
        results_df[code_column] = results_df[output_column]


    # results_df["test"] = results_df["test"].str.replace(
    #     "= next(iterator)", "= next(iterator, None)", regex=True
    # )
    # results_df[code_column] = results_df[code_column].str.replace(
    #     " = ContentType.", " = MessageContentType.", regex=True
    # )
    # results_df[code_column] = results_df[code_column].str.replace(
    #     "Message.", "Messages.", regex=True
    # )
    results_df[code_column] = results_df[code_column].str.replace('=  =', '=')

    humaneval_results = (
        humaneval_accuracy_score(n=n, ks=ks, data=results_df, code_column_name=code_column)
        if compute_humanval
        else {}
    )

    bleu_results = (
        bleu_accuracy_score(
            data=results_df, generated_column=code_column, gold_column=gold_column
        )
        if compute_bleu
        else {}
    )

    result = dict(
        humaneval=humaneval_results,
        bleu=bleu_results
    )
    return result


def eval_generated_code(
    df,
    experiment_params,
    target_label,
    id_labels,
    n,
    file_path=None,
    output_column="output",
    gold_column="code",
    force_generate_predictions=False,
    should_generate_predictions=True,
    should_model_eval=True,
    batch_size=4
):
    file_exists = file_path and os.path.exists(file_path)
    if file_exists:
      print(f"Loading results from {file_path}")

    preds_df = pd.read_csv(file_path) if file_exists else df

    total_preds_count = preds_df['sample_id'].nunique()
    pending_preds_count = preds_df[preds_df[output_column].isna()]['sample_id'].nunique() if output_column in preds_df else preds_df['sample_id'].nunique()
    generated_preds_count = preds_df[preds_df[output_column].notna()]['sample_id'].nunique() if output_column in preds_df else 0
    print(f"Generated {generated_preds_count} / {total_preds_count} ({(100. * generated_preds_count / total_preds_count):.0f}%)")

    should_generate_predictions = should_generate_predictions and pending_preds_count > 0
    if force_generate_predictions or should_generate_predictions:
        print(f"Generating {pending_preds_count} results...")
        preds_df = generate_predictions(
            df=preds_df,
            experiment_params=experiment_params,
            n=n,
            file_path=file_path,
            gold_column=target_label,
            id_labels=id_labels,
            batch_size=batch_size
        )

    if file_path:
        results_df = pd.read_csv(file_path)
        results_df = results_df.loc[:, ~results_df.columns.str.contains('^Unnamed')]
    else:
        results_df = preds_df

    return results_df


def eval_test_data(
    experiment_params,
    test_df,
    n,
    ks = [1, 10],
    results_file_path=None,
    output_column="output",
    gold_column="code",
    force_generate_predictions=False,
    should_generate_predictions=True,
    should_model_eval=True,
    batch_size=4,
    force=False
):
    # selected model params
    strategy = experiment_params.get("strategy")
    strategy_params = strategies_params[strategy]
    target_label = strategy_params.get('target_label')
    parse_code = (target_label in ['code_rep', 'code_rep_raw'])
    parse_rules_enabled = (target_label == 'code_rep_raw')
    slug = strategy_params.get('slug')

    id_labels = ['sample_id'] #['test_id', 'sample_id', 'sample_minor_id']

    print(f"model_id = {model_id}")
    print(f"slug = {slug}")
    print(f"n = {n}")
    print(f"")

    results_df = eval_generated_code(
        df=test_df,
        experiment_params=experiment_params,
        n=n,
        target_label=target_label,
        id_labels=id_labels,
        gold_column=gold_column,
        file_path=results_file_path,
        force_generate_predictions=force_generate_predictions,
        should_generate_predictions=should_generate_predictions,
        should_model_eval=should_model_eval,
        batch_size=batch_size
    )

    results = None
    if should_model_eval:
        results = model_eval(
            n=n,
            ks=ks,
            results_df=results_df,
            parse_to_code=parse_code,
            parse_rules_enabled=parse_rules_enabled,
            compute_humanval=True,
            compute_bleu=False,
            output_column=output_column,
            gold_column=gold_column,
        )
    return results