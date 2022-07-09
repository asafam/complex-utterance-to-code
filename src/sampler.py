import re
import random
import copy
from typing import Dict, Tuple, Union, List, Optional
from utils import get_code, get_keys, get_var
from fake_data.faker import fake


def sample(key: str, name: str, program_stack: Dict, grammar: Dict) -> Dict:
    if re.search(rf"faker_.*", key):
        result = sample_from_faker(key=key)
    else:
        result = sample_from_grammar(
            key=key, program_stack=program_stack.copy(), grammar=grammar
        )

    program_stack[name] = result

    return result


def sample_from_faker(key: str) -> dict:
    func_names = key.split("faker_")[1]
    value = None
    for func_name in func_names.split(" "):
        result = getattr(fake, func_name)()
        value = result if value is None else f"{value} {result}"
    value = normalize_result(value, key)
    return value


def normalize_result(result: Optional[Union[str, dict]], key: str):
    value = result if isinstance(result, dict) else dict()
    value["text"] = result["text"] if isinstance(result, dict) else result
    value["code"] = get_code(value)
    value["var"] = get_var(value, [])
    value["key"] = key
    return value


def sample_from_grammar(key: str, program_stack: Dict, grammar: Dict) -> Dict:
    d = sample_random_value(key, grammar)
    child_keys = get_keys(d["text"] + d["code"])
    for child_name, child_key, child_idx in child_keys:
        dd = sample(
            key=child_key, name=child_name, program_stack=program_stack, grammar=grammar
        )
        d["text"] = substitute_text(text=d["text"], key=child_name, value=dd["text"])
        var = dd["var"] or d["var"] or f"${{{key}:var}}"
        if child_idx:
            var = var + child_idx
        d["code"] = substitute_code(
            code=d["code"], key=child_key, name=child_name, value=dd["code"], var=var
        )
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

    return d


def sample_random_value(key: str, data: dict, k=1) -> dict:
    population = get_entries_for_key(key, data)
    weights = [item["weight"] if "weight" in item else 1.0 for item in population]
    results = random.choices(population, weights, k=k)
    result = results[0]
    d = normalize_result(result, key)
    d = copy.deepcopy(d)
    return d


def get_entries_for_key(key: str, data: dict) -> List[dict]:
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
                        params[k.strip()] = v.strip() if not v.strip().startswith('$') else f'${{{v.strip()[1:]}}}'
                text_keys = get_keys(item['text'], key_pattern=r'\$([^\s\{\}}]+)')
                for k in text_keys:
                    item["text"] = re.sub(re.escape(f"${k[0]}"), params.get(k[0], ""), item["text"], 1) 
                code_keys = get_keys(item['code'], key_pattern=r'\$([^\s\,\(\)\{\}]+)')
                for k in code_keys:
                    item["code"] = re.sub(re.escape(f"${k[0]}"), params.get(k[0], ""), item["code"], 1) #item["code"].replace(f"${k[0]}", params.get(k[0], ""))
    return entries


def substitute_text(text: str, key: str, value: str) -> str:
    new_text = text
    if value:
        escaped_key = re.escape(key)
        new_text = re.sub(rf"\${{{escaped_key}}}", value, new_text, 1)
    
    new_text = re.sub(rf"\s+", " ", new_text, 1)
    return new_text


def substitute_code(
    code: str, key: str, name: str, value: str, var: Optional[str]
) -> str:
    new_code = code

    # get indentation
    escaped_regex = f"${{{key}}}"
    if re.search(rf"\n\s*{escaped_regex}", code):
        indent = code.split(f"${{{key}}}")[0].split("\n")[-1]
        # indent
        value = re.sub(rf"\n", f"\n{indent}", value)

    # replace keys in code
    if value:
        escaped_regex = re.escape(f"${{{name}}}")
        new_code = re.sub(escaped_regex, value, new_code, 1)

    if var:
        escaped_regex = re.escape(f"${{{key}:var}}")
        new_code = re.sub(escaped_regex, var, new_code, 1)
        escaped_regex = re.escape(f"${{{name}:var}}")
        new_code = re.sub(escaped_regex, var, new_code, 1)

    return new_code


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


def substitute_var(code: str, var: str, key: str, repl: str) -> Tuple[str, str]:
    new_code = code
    new_var = var
    if f"${{{key}:var}}" in code:
        new_code = re.sub(rf"\${{{key}:var}}", repl, code)
        new_var = re.sub(rf"\${{{key}:var}}", repl, var) if var else repl

    return new_code, new_var


def substitute_var2(var: str, code: str, key: str, repl: str) -> Tuple[str, str]:
    new_var = var
    new_code = code
    if f"{key}:var" in code or f"${{{key}:var}}" == var or re.search(rf"faker_.*", key):
        new_code = re.sub(rf"\${{{key}:var}}", repl, code)
        new_var = re.sub(rf"\${{{key}:var}}", repl, var) if var else repl
    return new_var, new_code
