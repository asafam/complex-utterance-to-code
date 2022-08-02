import re
import uuid
import random
import copy
from typing import Any, Dict, Deque, Tuple, Union, List, Optional
from collections import deque
from key import Key
from entity import Entity
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
    key: Key,
    grammar: Dict,
    program_stack: Deque,
    context: Dict = dict(),
    options: Dict = {},
) -> Entity:
    default_options = {"sample_children": True}
    options = {**default_options, **options}

    context["id"] = get_context_id()
    if re.search(rf"faker_.*", key.key):
        entity = sample_from_faker(key=key)
    else:
        entity = sample_from_grammar(
            key=key,
            grammar=grammar,
            program_stack=program_stack,
            context=context,
        )

        if options["sample_children"]:
            # recursively sample the nested keys
            child_keys = entity.get_keys()
            for child_key in child_keys:
                # update the context
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
                    grammar=grammar,
                    program_stack=program_stack,
                    context=subcontext,
                )

                entity.children[child_key] = child

    entity.final = True
    program_stack.append(entity)

    return entity


def sample_from_faker(key: Key) -> Entity:
    func_names = key.key.split("faker_")[1]
    result = None
    for func_name in func_names.split(" "):
        value = getattr(fake, func_name)()
        result = value if not result else f"{value} {result}"

    norm_result = normalize_result(result, key)

    entity = Entity(
        key=key,
        text=norm_result["text"],
        code=norm_result["code"],
        var=norm_result["var"],
    )  # result if value is None else f"{value} {result}"
    # value = normalize_result(value, key)
    return entity


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


def sample_from_grammar(
    key: Key,
    grammar: Dict,
    program_stack: Dict,
    context: Dict,
) -> Entity:
    value = sample_value(key, grammar, program_stack, context=context)
    if not value["final"]:
        # child_keys = get_keys(value["text"] + value["code"], index=key.index)
        # for child_key in child_keys:
        for child_key in value["children"]:
            # subcontext = dict()
            # subcontext["parent"] = context
            # context["children"] = (
            #     [*context["children"], subcontext]
            #     if "children" in context
            #     else [subcontext]
            # )
            # # sample child value
            # child = sample(
            #     key=child_key,
            #     grammar=grammar,
            #     program_stack=program_stack,
            #     context=subcontext,
            # )

            # value["args"][child_key] = child
            child = value["children"][child_key]

            value["text"] = substitute_text(
                text=value["text"], key=child_key, value=child["text"]
            )

            # var_value = child["var"] or value["var"] or f"${{{key}:var}}"
            # if child_idx and not var_value.startswith("$"):
            #     var_value = var_value + child_idx

            var_value = get_var_value(
                key=child_key,
                parent_var=value["var"],
                child_var=child["var"],
            )

            value["var"] = substitute_var(
                var=value["var"],
                key=child_key,
                var_value=var_value,
            )

            # replace child value and var in parent with child value and var
            value["code"] = substitute_code(
                code=value["code"],
                key=child_key,
                code_value=child["code"],
                var_value=var_value,
                child_var=child["var"],
            )

    return value


def sample_value(
    key: Key,
    grammar: Dict,
    program_stack: Dict,
    context: Dict,
    k: int = 1,
    options: Dict = {},
) -> Dict[str, Any]:
    """
    This method sample a value by key from a given grammar k times.

    If the coreference flag is switched on then try to coreference and return the source entity along with a
    coreffed valued
    steps:
    1. extract the sampled value type
    2. check if this value should be coreferenced:
        a. Another entity of the same type is present in the program stack
        b. The candidate source entity is not in a conjunction
        c. The source entity does not share the same parent as the current entity
        d. No other source type is previously coreferenced
    3. If all conditions in (2.) are met then
        a. Copy source entity to be the coreffed entity
        b. Update the coreffed entity to have a coreffed value
        c. Update the source entity to have a corefenced value
    """
    default_options = {"sample_children": True}
    options = {**default_options, **options}

    context["id"] = get_context_id()
    if re.search(rf"faker_.*", key.key):
        value = sample_from_faker(key=key)
    else:
        value = sample_from_grammar(
            key=key,
            grammar=grammar,
            program_stack=program_stack,
            context=context,
        )

        if options["sample_children"]:
            # recursively sample the nested keys
            child_keys = get_keys(value["text"] + value["code"], index=key.index)
            for child_key in child_keys:
                # update the context
                subcontext = dict()
                subcontext["parent"] = context
                context["children"] = (
                    [*context["children"], subcontext]
                    if "children" in context
                    else [subcontext]
                )
                # sample child value
                child = sample_value(
                    key=child_key,
                    grammar=grammar,
                    program_stack=program_stack,
                    context=subcontext,
                )

                value["children"][child_key] = child

    # if not options["reuse_key"]:
    #     return sample_random_value(key=key, data=data, k=k, context=context)
    # else:
    #     value = get_value_from_program_stack(
    #         key=key, program_stack=program_stack, context=context
    #     )
    #     if value:
    #         return value
    #     else:
    #         return sample_random_value(key=key, data=data, k=k, context=context)


def sample_random_value(
    key: Key, data: dict, context: Dict, k: int = 1
) -> Dict[str, Any]:
    population = get_entries_for_key(key, data, context)
    weights = [item["weight"] if "weight" in item else 1.0 for item in population]
    results = random.choices(population, weights, k=k)
    result = results[0]
    value_orig = normalize_result(result, key, context)
    value = copy.deepcopy(value_orig)
    return value


def get_value_from_program_stack(
    key: Key, program_stack: Dict, context: Dict
) -> Optional[Dict[str, Any]]:
    value = None
    values = []
    for k in program_stack:
        v = program_stack[k]
        if (
            v["key"].key == key.key
            and v["key"].index is None
            and is_coref_valid(v)
            and get_value_context_id(v) != context["parent"]["id"]
            and "coref_context_id" in v
            and v["coref_context_id"] != context["parent"]["id"]
        ):
            values.append(v)
    if len(values) > 0:
        value = values[0]
        values[0]["coref_context_id"] = context["parent"]["id"]
    return value


def get_entries_for_key(key: Key, data: dict, context: Dict) -> List[dict]:
    entries = []
    if key.key_type in data:
        entries = copy.deepcopy(data[key.key_type])
    elif len([k for k in data.keys() if re.search(k, key.key_type)]) > 0:
        k = [k for k in data.keys() if re.search(k, key.key_type)][0]
        entries = copy.deepcopy(data[k])
        try:
            params_str = (
                re.search(k, key.key_type).group(1)
                if re.search(k, key.key_type)
                else None
            )
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
                        re.escape(f"${k.key}"), params.get(k.key, ""), item["text"], 1
                    )
                code_keys = get_keys(item["code"], key_pattern=r"\$([^\s\,\(\)\{\}]+)")
                for k in code_keys:
                    item["code"] = re.sub(
                        re.escape(f"${k.key}"), params.get(k.key, ""), item["code"], 1
                    )  # item["code"].replace(f"${k[0]}", params.get(k[0], ""))
    return entries
