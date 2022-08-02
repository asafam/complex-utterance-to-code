import re
import uuid
from collections import Counter
from typing import List, Union, Tuple, Optional, Dict
from key import Key


def get_root_entity(entity: Dict) -> Optional[Dict]:
    if entity.get("type"):
        return entity

    root_entity = None
    for arg in entity.get("children", {}).keys():
        arg = entity["children"].get(arg)
        root_entity = get_root_entity(arg)
        if root_entity:
            break

    return root_entity


def get_keys(
    value: str, index: Optional[str] = None, key_pattern: str = r"\$\{([^{}]+)\}"
) -> List[Key]:
    # find all keys enclosed in ${}
    items = re.findall(key_pattern, value)
    items = list(dict.fromkeys(items))  # remove duplicates while preserving order
    # filter out var keys ${*:var}
    key_items = [item for item in items if not item.endswith(":var")]
    # split indexed keys as in ${*.1} and ${*.2}...
    index_prefix = f"{index}_" if index is not None else ""
    counter = Counter([key_item.split(".")[0] for key_item in key_items])
    keys = [
        Key(
            key=item,
            key_type=item.split(".")[0],
            index=(index_prefix + str(item.split(".")[1]))
            if len(item.split(".")) > 1
            else None,
            count=counter[item.split(".")[0]],
        )
        for item in key_items
    ]
    return keys


def get_code(d: dict) -> str:
    code = d["code"] if "code" in d else d["text"]
    code = str(code).strip()
    return code


def get_context_id() -> str:
    context_id = str(uuid.uuid4()).split("-")[0]
    return context_id


def get_value_context_id(value) -> Optional[str]:
    value_context_id = value.get("context", {}).get("parent", {}).get("id")
    return value_context_id


def get_var(value: dict, context: List[str]) -> Optional[str]:
    if "var" in value and value["var"] is not None:
        var = value["var"]
    else:
        var = None

    return var


def get_var_value(key: Key, parent_var: str, child_var: str) -> str:
    var_value = f"${{{key.key}:var}}"

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

    if key.index and not var_value.startswith("$"):
        var_value += key.index

    return var_value


def normalize_result(
    result: Optional[Union[str, dict]], key: Key, context: Optional[Dict] = None
):
    value = result if isinstance(result, dict) else dict()
    value["uuid"] = key.key + "_" + str(uuid.uuid4()).split("-")[0]
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


def substitute_text(text: str, key: Key, value: str, options: Dict = {}) -> str:
    default_options = {
        "strip": True,
    }
    options = {**default_options, **options}

    new_text = text
    if value:
        escaped_key = re.escape(key.key)
        new_text = re.sub(rf"\${{{escaped_key}}}", value, new_text)

    # post processing
    if options["strip"]:
        new_text = re.sub(rf"\s+", " ", new_text, 1)

    return new_text


def substitute_code(
    code: str,
    key: Key,
    code_value: str,
    var_value: Optional[str],
    child_var: Optional[str] = None,
    options: Dict = {},
) -> str:
    default_options = {
        "remove_redundant_rows": True,
        "strip": True,
    }
    options = {**default_options, **options}

    new_code = code

    # get indentation
    escaped_regex = re.escape(f"${{{key.key_type}}}")
    if re.search(rf"\n\s*{escaped_regex}", new_code):
        indent = new_code.split(f"${{{key.key_type}}}")[0].split("\n")[-1]
        # indent
        code_value = re.sub(rf"\n", f"\n{indent}", code_value)

    # replace child var in parent with var value
    if var_value and child_var and var_value != child_var:
        # child_var = ... with var_value = ...
        escaped_regex = re.escape(f"{child_var} =")
        code_value = re.sub(escaped_regex, f"{var_value} =", code_value)

        # {key_type:var} = ... with var_value = ...
        escaped_regex = re.escape(f"${{{key.key_type}:var}}")
        code_value = re.sub(escaped_regex, var_value, code_value)

    # replace child key with child code
    escaped_regex = re.escape(f"${{{key.key}}}")
    new_code = re.sub(escaped_regex, code_value, new_code)

    # replace child key in parent with child code
    if code_value:
        escaped_regex = re.escape(f"${{{key.key}}}")
        new_code = re.sub(escaped_regex, code_value, new_code)

    # replace child var in parent with var value
    if var_value:
        escaped_regex = re.escape(f"${{{key.key}:var}}")
        new_code = re.sub(escaped_regex, var_value, new_code)

    # post processing
    if options["remove_redundant_rows"]:
        new_code = "\n".join(
            [
                r
                for r in new_code.split("\n")
                if "=" not in r or (r.split("=")[0].strip() != r.split("=")[1].strip())
            ]
        )

    if options["strip"]:
        new_code = "\n".join([r for r in new_code.split("\n") if r != "__DELETE__"])

    return new_code


def substitute_var(var: str, key: Key, var_value: Optional[str]) -> str:
    new_var = var

    if new_var and var_value:
        escaped_regex_name = re.escape(f"${{{key.key}:var}}")
        escaped_regex_key = re.escape(f"${{{key.key_type}:var}}")
        if re.search(escaped_regex_name, new_var):
            new_var = var_value if var == f"${{{key.key}:var}}" else new_var
        elif re.search(escaped_regex_key, new_var):
            new_var = var_value if var == f"${{{key.key_type}:var}}" else new_var

    return new_var
