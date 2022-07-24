import re
import uuid
import random
import copy
from typing import Any, Dict, Tuple, Union, List, Optional
from utils import (
    is_coref_valid,
    get_code,
    get_context_id,
    get_keys,
    get_value_context_id,
    get_var,
    get_var_value,
    substitute_code,
    substitute_text,
    substitute_var,
)
from fake_data.faker import fake


def sample(
    key: str,
    name: str,
    grammar: Dict,
    program_stack: Dict,
    context: Dict,
    idx: Optional[str] = None,
) -> Dict:
    context["id"] = get_context_id()
    if re.search(rf"faker_.*", key):
        value = sample_from_faker(key=key)
    else:
        value = sample_from_grammar(
            key=key,
            grammar=grammar,
            program_stack=program_stack,
            context=context,
            idx=idx,
        )

    value["final"] = True
    program_stack[value["uuid"]] = value

    return value


def sample_from_faker(key: str) -> dict:
    func_names = key.split("faker_")[1]
    value = None
    for func_name in func_names.split(" "):
        result = getattr(fake, func_name)()
        value = result if value is None else f"{value} {result}"
    value = normalize_result(value, key)
    return value


def normalize_result(
    result: Optional[Union[str, dict]], key: str, context: Optional[Dict] = None
):
    value = result if isinstance(result, dict) else dict()
    value["uuid"] = key + "_" + str(uuid.uuid4()).split("-")[0]
    value["text"] = result["text"] if isinstance(result, dict) else result
    value["template_text"] = value["text"]
    value["code"] = get_code(value)
    value["template_code"] = value["code"]
    value["var"] = get_var(value, [])
    value["key"] = key
    value["final"] = False
    value["args"] = dict()
    if context:
        value["context"] = context
    return value


def sample_from_grammar(
    key: str,
    grammar: Dict,
    program_stack: Dict,
    context: Dict,
    idx: Optional[str] = None,
) -> Dict:
    value = sample_value(key, grammar, program_stack, context=context)
    if not value["final"]:
        child_keys = get_keys(value["text"] + value["code"], index=idx)
        for child_name, child_key, child_idx in child_keys:
            subcontext = dict()
            subcontext["parent"] = context
            context["children"] = (
                [*context["children"], subcontext]
                if "children" in context
                else [subcontext]
            )
            # sample child value
            child = sample(
                key=child_key,
                name=child_name,
                idx=child_idx,
                grammar=grammar,
                program_stack=program_stack,
                context=subcontext,
            )

            value["args"][child_name] = child

            value["text"] = substitute_text(
                text=value["text"], key=child_name, value=child["text"]
            )

            # var_value = child["var"] or value["var"] or f"${{{key}:var}}"
            # if child_idx and not var_value.startswith("$"):
            #     var_value = var_value + child_idx

            var_value = get_var_value(
                name=child_name,
                parent_var=value["var"],
                child_var=child["var"],
                index=child_idx,
            )

            value["var"] = substitute_var(
                var=value["var"],
                key=child_key,
                name=child_name,
                var_value=var_value,
            )

            # replace child value and var in parent with child value and var
            value["code"] = substitute_code(
                code=value["code"],
                var=value["var"],
                key=child_key,
                name=child_name,
                code_value=child["code"],
                var_value=var_value,
                child_var=child["var"],
            )

            # d["var"] = d["var"] or new_var
            # d["code"], d["var"] = substitute_code(code=d["code"], key=k, value=dd["code"], var=d["var"])

            # d["code"] = substitute_code(code=d["code"], key=k, repl=dd["code"])

            # if d["var"]:
            #     repl_var = d["var"]
            #     #(
            #         # dd["var"] if "var" in dd and dd["var"] is not None else d["var"] #get_var(dd, [])
            #     # )
            #     d["var"], d["code"] = substitute_var(var=d["var"],
            #                                          code=d["code"],
            #                                          key=k,
            #                                          repl=repl_var)
    return value


def sample_value(
    key: str,
    data: Dict,
    program_stack: Dict,
    context: Dict,
    k: int = 1,
    options: Dict = {},
) -> Dict[str, Any]:
    defaultOptions = {"reuse_key": True}
    options = {**defaultOptions, **options}

    if not options["reuse_key"]:
        return sample_random_value(key=key, data=data, k=k, context=context)
    else:
        value = get_value_from_program_stack(
            key=key, program_stack=program_stack, context=context
        )
        if value:
            return value
        else:
            return sample_random_value(key=key, data=data, k=k, context=context)


def sample_random_value(
    key: str, data: dict, context: Dict, k: int = 1
) -> Dict[str, Any]:
    population = get_entries_for_key(key, data, context)
    weights = [item["weight"] if "weight" in item else 1.0 for item in population]
    results = random.choices(population, weights, k=k)
    result = results[0]
    d = normalize_result(result, key, context)
    d = copy.deepcopy(d)
    return d


def get_value_from_program_stack(
    key: str, program_stack: Dict, context: Dict
) -> Optional[Dict[str, Any]]:
    value = None
    values = []
    for k in program_stack:
        v = program_stack[k]
        if (
            v['key'] == key
            and is_coref_valid(v)
            and get_value_context_id(v) != context['parent']['id']
        ):
            values.append(v)
    if len(values) > 0:
        value = values[0]
    return value


def get_entries_for_key(key: str, data: dict, context: Dict) -> List[dict]:
    entries = []
    if key in data:
        entries = copy.deepcopy(data[key])
    elif len([k for k in data.keys() if re.search(k, key)]) > 0:
        k = [k for k in data.keys() if re.search(k, key)][0]
        entries = copy.deepcopy(data[k])
        try:
            params_str = re.search(k, key).group(1) if re.search(k, key) else None
        except:
            params_str = None

        if params_str:
            for item in entries:
                param_values = list(map(lambda x: x.strip(), params_str.split(",")))
                params = dict()
                # obj is a special text key in the param
                params["obj"] = param_values[0]
                params["obj"] = (
                    params["obj"][:-1]
                    if item.get("num") == "sg" and params["obj"].endswith("s")
                    else params["obj"]
                )
                # var is a special code key in the param
                params["var"] = param_values[0]
                # rest of the params
                if len(param_values) > 1:
                    for param in param_values[1:]:
                        [k, v] = param.split("=")
                        params[k.strip()] = (
                            v.strip()
                            if not v.strip().startswith("$")
                            else f"${{{v.strip()[1:]}}}"
                        )
                text_keys = get_keys(item["text"], key_pattern=r"\$([^\s\{\}}]+)")
                for k in text_keys:
                    item["text"] = re.sub(
                        re.escape(f"${k[0]}"), params.get(k[0], ""), item["text"], 1
                    )
                code_keys = get_keys(item["code"], key_pattern=r"\$([^\s\,\(\)\{\}]+)")
                for k in code_keys:
                    item["code"] = re.sub(
                        re.escape(f"${k[0]}"), params.get(k[0], ""), item["code"], 1
                    )  # item["code"].replace(f"${k[0]}", params.get(k[0], ""))
    return entries


def substitute_text2(text: str, key: str, repl: str) -> str:
    new_text = re.sub(rf"\${{{key}}}", repl, text, 1)
    return new_text


def substitute_code2(code: str, key: str, repl: str) -> str:
    if re.search(rf"\n\s*\${{{key}}}", code):
        indent = code.split(f"${{{key}}}")[0].split("\n")[-1]
        # indent
        repl = re.sub(rf"\n", f"\n{indent}", repl)
    new_code = re.sub(rf"\${{{key}}}", repl, code, 1)
    if not re.match(r".*[\=|\(].*", new_code) and re.match(r'.*".*', new_code[1:-1]):
        new_code = re.sub(r'"', "", new_code)
        new_code = f'"{new_code}"'
    return new_code


def substitute_var2(var: str, code: str, key: str, repl: str) -> Tuple[str, str]:
    new_var = var
    new_code = code
    if f"{key}:var" in code or f"${{{key}:var}}" == var or re.search(rf"faker_.*", key):
        new_code = re.sub(rf"\${{{key}:var}}", repl, code)
        new_var = re.sub(rf"\${{{key}:var}}", repl, var) if var else repl
    return new_var, new_code
