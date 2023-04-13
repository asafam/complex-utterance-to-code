import re
import random
import copy
import json

from typing import Dict, Deque, List, Optional
from synthetics.utils import load_grammar
from synthetics.key import Key
from synthetics.entity import Entity
from synthetics.utils import (
    get_context_id,
    get_keys,
    get_labels,
    normalize_data,
)
from synthetics.data_generator.faker import get_faker


def get_entries_for_key(key: Key, data: dict) -> List[dict]:
    entries = []
    # checks if the key is in the data
    if key.key in data:
        entries = copy.deepcopy(data[key.key])
    # checks if the key is a regex in the data
    elif (
        len(
            [
                k
                for k in data.keys()
                if re.search(k, key.key)  # and key.key.endswith(":text")
            ]
        )
        > 0
    ):
        k = [k for k in data.keys() if re.search(k, key.key)][0]
        entries = copy.deepcopy(data[k])
        try:
            params_str = (
                re.search(k, key.key).group(1) if re.search(k, key.key) else None
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
                            if not v.strip().startswith("{")
                            and not v.strip().endswith("}")
                            else f"${v.strip()}"
                        )
                text_keys = get_keys(value=item["text"], label_regex=r"\$([^\s\{\}}]+)")
                for k, _ in text_keys:
                    item["text"] = re.sub(
                        re.escape(f"${k.key}"), params.get(k.key, ""), item["text"], 1
                    )
                code_keys = get_keys(
                    value=item["code"], label_regex=r"\$([^\s\,\(\)\{\}]+)"
                )
                for k, _ in code_keys:
                    item["code"] = re.sub(
                        re.escape(f"${k.key}"), params.get(k.key, ""), item["code"], 1
                    )  # item["code"].replace(f"${k[0]}", params.get(k[0], ""))
    return entries


def sample_key(key: Key, grammar: Dict, **kwargs) -> Entity:
    if re.search(rf"faker_.*", key.key):
        # faker dynamic key
        entity = sample_from_faker(key=key, **kwargs)
    else:
        # generic dynamic key (not faker)
        entity = sample_from_grammar(key=key, grammar=grammar, **kwargs)

    return entity


def sample(
    key: Key = Key("utterance"),
    grammar: Dict = None,
    grammar_dir: str = "config/grammar",
    options: Dict = dict(),
    **kwargs,
) -> Entity:
    default_options = {"sample_children": True}
    options = {**default_options, **options}

    if not grammar:
        grammar = load_grammar(grammar_dir=grammar_dir)

    # sample key
    entity = sample_key(key=key, grammar=grammar, **kwargs)

    # sample sub-keys if entity can be further sampled

    text_labels = get_labels(entity.text, ignore_regex="[^\[]\:\w+")
    code_labels = get_labels(entity.code, ignore_regex="[^\[]\:\w+")

    labels = list(dict.fromkeys(text_labels + code_labels))
    for label in labels:
        if label not in entity.key_entity_map:
            sub_key = Key(label=label)
            params_regex = r"(?<=\[).+?(?=\])"
            params = (
                json.loads(
                    re.search(params_regex, sub_key.label).group(0).replace("'", '"')
                )
                if re.search(params_regex, sub_key.label)
                else {}
            )

            sub_entity = sample(key=sub_key, grammar=grammar, **params)
            entity.map_key_entity(sub_key, sub_entity)
        sub_entity.text_index = (
            text_labels.index(label) if label in text_labels else None
        )
        sub_entity.code_index = (
            code_labels.index(label) if label in code_labels else None
        )

    return entity


def sample_(
    key: Key,
    grammar: Dict,
    sentence_stack: Deque,
    context: Dict = dict(),
    options: Dict = dict(),
    **kwargs,
) -> Entity:

    context["id"] = get_context_id()
    context["key"] = key.key
    if re.search(rf"faker_.*", key.key):
        # faker dynamic key
        entity = sample_from_faker(key=key)
    else:
        # generic dynamic key (not faker)
        entity = sample_from_grammar(
            key=key, grammar=grammar, context=context, **kwargs
        )

        # sample children
        if options.get("sample_children"):
            # recursively sample the nested keys
            labels = get_labels

            keys = entity.get_keys()
            for key, params in enumerate(keys):
                # update the context
                subcontext = dict()
                subcontext["parent"] = context
                context["children"] = (
                    [*context["children"], subcontext]
                    if "children" in context
                    else [subcontext]
                )

                # sample child value
                sub_entity = sample(
                    key=key,
                    grammar=grammar,
                    sentence_stack=sentence_stack,
                    context=subcontext,
                    **params,
                )

                entity.add_sub_entity(key, sub_entity)

                if len(keys) > 1:
                    sentence_stack.append(child)

    # check if this entity can have a co-reference source
    coref_source_entity = sample_coreference(
        coref_entity=entity, sentence_stack=sentence_stack
    )
    if coref_source_entity:
        # flag this entity to be a co-ref of a given source
        if coref_source_entity not in coref_source_entity.coreference_entities:
            coref_source_entity.coreference_entities.append(coref_source_entity)

        child_idx = next(
            (
                i
                for i, e in enumerate(coref_source_entity.coreference_entities)
                if e.parent == entity and e.get_type() == entity.get_type()
            ),
            -1,
        )
        if (
            child_idx != -1
            and coref_source_entity.coreference_entities[child_idx].key.key
            != coref_source_entity.key.key
        ):
            coref_source_entity.coreference_entities[
                child_idx
            ].coreference_entities = []
            coref_source_entity.coreference_entities[child_idx] = entity
            entity.coreference_entities = coref_source_entity.coreference_entities
        elif child_idx == -1:
            coref_source_entity.coreference_entities.append(entity)
            entity.coreference_entities = coref_source_entity.coreference_entities

    entity.final = True

    return entity


def sample_coreference(
    coref_entity: Entity, sentence_stack: Deque[Entity]
) -> Optional[Entity]:
    """
    This method sample a value by key from a the sentence stack.

    If the coreference flag is switched on then try to coreference and return the source entity along with a
    corefered valued
    steps:
    1. extract the sampled value type
    2. Iterate over the sentence stack to find the most recent element with type (1)
    3. check if this value should be coreferenced
    4. If all conditions in (3) are met then
        a. Copy source entity to be the coreffed entity
        b. Update the coreffed entity to have a coreffed value
        c. Update the source entity to have a corefenced value
    """
    if not coref_entity.can_corefernce():
        return None

    source_entities = [
        entity for entity in sentence_stack if entity.is_coreference_with(coref_entity)
    ]
    source_entities_coref = source_entities[-1] if source_entities else None
    return source_entities_coref


def sample_from_faker(key: Key, seed: Optional[int] = None) -> Entity:
    fake = get_faker(seed=seed)
    func_names = key.key.split("faker_")[1]
    result = None
    for func_name in func_names.split(" "):
        value = getattr(fake, func_name)()
        result = value if not result else f"{value} {result}"

    norm_result = normalize_data(result, key)
    entity = Entity(**norm_result)
    return entity


def sample_from_grammar(
    key: Key,
    grammar: Dict,
    # context: Dict,
    seed: Optional[int] = None,
    **kwargs,
) -> Entity:
    data = sample_random_value(key=key, data=grammar, seed=seed)
    norm_result = normalize_data(data=data, key=key, context={}, **kwargs)
    entity = Entity(**norm_result)
    return entity


# def sample_value(
#     key: Key,
#     grammar: Dict,
#     sentence_stack: Dict,
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
#     value = get_value_from_sentence_stack(
#         key=key, sentence_stack=sentence_stack, context=context
#     )
#     if value:
#         return value
#     else:
#         return sample_random_value(key=key, data=data, k=k, context=context)


def sample_random_value(
    key: Key,
    data: dict,
    k: int = 1,
    default_divider: str = "|",
    seed: Optional[int] = None,
) -> Dict:
    if seed:
        random.seed(seed)

    population = (
        get_entries_for_key(key, data)
        if default_divider not in key.key
        else key.key.split(default_divider)
    )
    weights = [item["weight"] if "weight" in item else 1.0 for item in population]
    results = random.choices(population, weights, k=k)
    result = results[0]
    value = copy.deepcopy(result)
    return value
