import re
import uuid
from typing import List, Tuple, Optional, Dict
import inflect


def is_coref_valid(value: Dict) -> bool:
    valid = "coref_valid" in value and value["coref_valid"]
    return valid


def get_keys(
    value: str, index: Optional[str] = None, key_pattern: str = r"\$\{([^{}]+)\}"
) -> List[Tuple[str, str, Optional[str]]]:
    # find all keys enclosed in ${}
    items = re.findall(key_pattern, value)
    items = list(dict.fromkeys(items))  # remove duplicates while preserving order
    # filter out var keys ${*:var}
    keys = [item for item in items if not item.endswith(":var")]
    # split indexed keys as in ${*.1} and ${*.2}...
    index_prefix = f"{index}_" if index is not None else ""
    results = [
        (
            item,
            item.split(".")[0],
            (index_prefix + str(item.split(".")[1]))
            if len(item.split(".")) > 1
            else None,
        )
        for item in keys
    ]
    return results


def get_code(d: dict) -> str:
    code = d["code"] if "code" in d else d["text"]
    # should_format = d['format'] if 'format' in d else True
    # if should_format and isinstance(code, str) and not code.startswith('"') and not re.search(r'\$\{.*\}|\=|\n', code):  # type: ignore
    # code = re.sub(r'"', '', code)
    # code = f'"{code}"'
    # elif should_format and code.startswith('"') and code.endswith('"'):
    #     new_code = re.sub(r"\"", "", code[1:-1])
    #     code = new_code #f'"{new_code}"'

    code = str(code).strip()
    return code


def get_context_id() -> str:
    context_id = str(uuid.uuid4()).split("-")[0]
    return context_id


def get_value_context_id(value) -> Optional[str]:
    value_context_id = None
    if (
        "context" in value
        and "parent" in value["context"]
        and "id" in value["context"]["parent"]
    ):
        value_context_id = value["context"]["parent"]["id"]
    return value_context_id


def get_var(value: dict, context: List[str]) -> Optional[str]:
    if "var" in value and value["var"] is not None:
        var = value["var"]

    # elif 'code' in d and d['code'].startswith('"'):
    #     var = re.sub(r'"|^and$|^or$|^the$', '', d['code']).strip()
    #     var = re.sub(r'\s+', '_', var)
    #     var = '_'.join([(x if re.match(r"[-+]?\d+$", x) is None else inflect.engine().number_to_words(x)) for x in var.split('_')])
    #     var = re.sub(r'-', '_', var)
    #     var = re.sub(r'\:', '', var)
    #     var = var.lower()
    else:
        var = None

    return var


def get_var_value(
    name: str, parent_var: str, child_var: str, index: Optional[str] = None
) -> str:
    var_value = f"${{{name}:var}}"

    # if parent has var value and parent type is identical to child type then:
    #   set var value to parent var value --and replace child var value in child code
    if (
        parent_var
        and (parent_var == child_var or child_var is None)
        and not parent_var.startswith("$")
    ):
        var_value = parent_var
    # else if child has var value then
    #   set var value to child var value
    elif child_var:
        var_value = child_var

    if index and not var_value.startswith("$"):
        var_value += index

    return var_value


def to_text(value: dict, index: Optional[str] = None) -> str:
    text = value["template_text"]
    child_keys = get_keys(value["text"] + value["code"], index=index)
    for child_name, _, child_idx in child_keys:
        child_value = value["args"][child_name]

        text = substitute_text(
            text=text, key=child_name, value=to_text(child_value, index=child_idx)
        )

    return text


def to_code(value: dict, index: Optional[str] = None) -> str:
    code = value["template_code"]
    child_keys = get_keys(value["text"] + value["code"], index=index)
    for child_name, child_key, child_idx in child_keys:
        child_value = value["args"][child_name]

        var_value = child_value["var"] or value["var"] or f"${{{child_key}:var}}"
        if child_idx and not var_value.startswith("$"):
            var_value = var_value + child_idx

        code = substitute_code(
            code=value["code"],
            var=value["var"],
            key=child_key,
            name=child_name,
            code_value=to_code(child_value, index=child_idx),  # child_value["code"],
            var_value=var_value,
        )
    return code


def substitute_text(text: str, key: str, value: str) -> str:
    new_text = text
    if value:
        escaped_key = re.escape(key)
        new_text = re.sub(rf"\${{{escaped_key}}}", value, new_text)

    new_text = re.sub(rf"\s+", " ", new_text, 1)
    return new_text


def substitute_code(
    code: str,
    var: str,
    key: str,
    name: str,
    code_value: str,
    var_value: Optional[str],
    child_var: Optional[str] = None,
) -> str:  # Tuple[str, str]:
    new_code = code
    # new_var = var

    # get indentation
    escaped_regex = re.escape(f"${{{key}}}")
    if re.search(rf"\n\s*{escaped_regex}", new_code):
        indent = new_code.split(f"${{{key}}}")[0].split("\n")[-1]
        # indent
        code_value = re.sub(rf"\n", f"\n{indent}", code_value)

    # replace child var in parent with var value
    if var_value and child_var and var_value != child_var:
        escaped_regex = re.escape(f"{child_var} =")
        code_value = re.sub(escaped_regex, f"{var_value} =", code_value)

    # replace child key with child code
    escaped_regex = re.escape(f"${{{name}}}")
    new_code = re.sub(escaped_regex, code_value, new_code)

    # replace child key in parent with child code
    if code_value:
        escaped_regex = re.escape(f"${{{name}}}")
        new_code = re.sub(escaped_regex, code_value, new_code)

    # replace child var in parent with var value
    if var_value:
        escaped_regex = re.escape(f"${{{name}:var}}")
        new_code = re.sub(escaped_regex, var_value, new_code)
        # escaped_regex = re.escape(f"${{{name}:var}}")
        # if re.search(escaped_regex, new_code):
        #     new_code = re.sub(escaped_regex, var_value, new_code)
        #     new_var = var_value if var == f"${{{name}:var}}" else new_var
        # else:
        #     escaped_regex = re.escape(f"${{{key}:var}}")
        #     new_code = re.sub(escaped_regex, var_value, new_code)
        #     new_var = var_value if var == f"${{{key}:var}}" else new_var

    return new_code  # , new_var


def substitute_var(var: str, key: str, name: str, var_value: Optional[str]) -> str:
    new_var = var

    if new_var and var_value:
        escaped_regex_name = re.escape(f"${{{name}:var}}")
        escaped_regex_key = re.escape(f"${{{key}:var}}")
        if re.search(escaped_regex_name, new_var):
            new_var = var_value if var == f"${{{name}:var}}" else new_var
        elif re.search(escaped_regex_key, new_var):
            new_var = var_value if var == f"${{{key}:var}}" else new_var

    return new_var
