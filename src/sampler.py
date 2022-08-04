import re
import uuid
import random
import copy
from typing import Any, Dict, Deque, Tuple, Union, List, Optional
from collections import deque
from key import Key
from entity import Entity
from utils import (
    get_context_id,
    get_keys,
    get_value_context_id,
    normalize_result,
)
from fake_data.faker import fake


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


def sample(
    key: Key,
    grammar: Dict,
    program_stack: Deque,
    context: Dict = dict(),
    options: Dict = dict(),
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
            context=context,
        )

        # otherwise continue and sample children
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

                entity.children[child_key.key] = child
                child.parent = entity

                if len(child_keys) > 1:
                    program_stack.append(child)

    # check if this entity can have a co-reference source
    coref_source_entity = sample_coreference(
        coref_entity=entity, program_stack=program_stack
    )
    if coref_source_entity:
        # flag this entity to be a co-ref of a given source
        if coref_source_entity not in coref_source_entity.coreference_entities:
            coref_source_entity.coreference_entities.append(coref_source_entity)
        coref_source_entity.coreference_entities.append(entity)
        entity.coreference_entities = coref_source_entity.coreference_entities

    entity.final = True

    return entity


def sample_coreference(coref_entity: Entity, program_stack: Deque[Entity]) -> Optional[Entity]:
    """
    This method sample a value by key from a the program stack.

    If the coreference flag is switched on then try to coreference and return the source entity along with a
    corefered valued
    steps:
    1. extract the sampled value type
    2. Iterate over the program stack to find the most recent element with type (1)
    3. check if this value should be coreferenced
    4. If all conditions in (3) are met then
        a. Copy source entity to be the coreffed entity
        b. Update the coreffed entity to have a coreffed value
        c. Update the source entity to have a corefenced value
    """
    if not coref_entity.can_corefernce():
       return None
    
    source_entity = None
    for entity in program_stack:
        if entity.is_coreference_with(coref_entity):
            source_entity = entity
            break
    return source_entity


def sample_from_faker(key: Key) -> Entity:
    func_names = key.key.split("faker_")[1]
    result = None
    for func_name in func_names.split(" "):
        value = getattr(fake, func_name)()
        result = value if not result else f"{value} {result}"

    norm_result = normalize_result(result, key)
    entity = Entity(**norm_result)
    return entity


def sample_from_grammar(
    key: Key,
    grammar: Dict,
    context: Dict,
) -> Entity:
    value = sample_random_value(key=key, data=grammar, context=context)
    norm_result = normalize_result(result=value, key=key, context=context)
    entity = Entity(**norm_result)
    return entity


# def sample_value(
#     key: Key,
#     grammar: Dict,
#     program_stack: Dict,
#     context: Dict,
#     k: int = 1,
#     options: Dict = {},
# ) -> Dict[str, Any]:
#     """
#     This method sample a value by key from a given grammar k times.

#     If the coreference flag is switched on then try to coreference and return the source entity along with a
#     coreffed valued
#     steps:
#     1. extract the sampled value type
#     2. check if this value should be coreferenced:
#         a. Another entity of the same type is present in the program stack
#         b. The candidate source entity is not in a conjunction
#         c. The source entity does not share the same parent as the current entity
#         d. No other source type is previously coreferenced
#     3. If all conditions in (2.) are met then
#         a. Copy source entity to be the coreffed entity
#         b. Update the coreffed entity to have a coreffed value
#         c. Update the source entity to have a corefenced value
#     """
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
    value = copy.deepcopy(result)
    return value
