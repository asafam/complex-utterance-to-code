import pandas as pd
from typing import Union


def load_data(file_path):
    df = pd.read_csv(file_path)

    df.fillna("", inplace=True)
    df["text_lang_rep"] = (
        "Text: " + df["text"].astype(str) + "\nLang rep: " + df["lang_rep"].astype(str)
    )
    df["lang_rep_pretty"] = df["lang_rep"]
    df["lang_rep"] = df["lang_rep"].str.replace(r"\s+", " ", regex=True)
    df["code_rep_pretty"] = df["code_rep"]
    df["code_rep"] = df["code_rep"].str.replace(r"\s+", " ", regex=True)

    print("shape = ", df.shape)

    return df


def load_test_data(
    test_file_path="data/eval_complex_utterance_to_code_with_intermediate_82_20230519.csv.gz",
    id_labels=["test_id", "sample_id", "sample_minor_id"],
    sorted=True,
    sample_frac=1,
    random_state=42,
):
    test_df = load_data(file_path=test_file_path)
    test_df["sample_id"] = test_df["sample_id"].astype(str)
    test_df = test_df.sample(frac=sample_frac, random_state=random_state).reset_index(
        drop=True
    )

    if id_labels:
        test_df.set_index(id_labels, inplace=True)
        if sorted:
            test_df.sort_index(inplace=True)

    print("test_df", test_df.shape)
    return test_df
  

def split_dataset_train_test(
    df: pd.DataFrame,
    test_size: Union[float, int],
    random_state: int = None,
    reset_index: bool = True,
):
    df = df.sample(frac=1, random_state=random_state)

    total_rows = df.shape[0]
    train_size = (
        (int(total_rows * (1 - test_size)))
        if test_size <= 1
        else (total_rows - test_size)
    )

    # Split data into test and train
    train_df = df[0:train_size]
    test_df = df[train_size:]

    train_df.reset_index(drop=True, inplace=True)
    test_df.reset_index(drop=True, inplace=True)
    return train_df, test_df


def get_dataset_args(
    tokenizer, 
    selected_model_flavour_params,
    dataset_args_keys_mask = ["input_prefix", "input_label", "target_label"],
    max_input_length = 512,
    max_target_length = 512
):
    selected_model_dataset_args = {key: selected_model_flavour_params[key] for key in dataset_args_keys_mask}

    base_dataset_args = dict(
        tokenizer=tokenizer,
        max_input_length = max_input_length,
        max_target_length = max_target_length,
    )
    dataset_args = {**base_dataset_args, **selected_model_dataset_args}
    return dataset_args