import uuid
import re
from key import Key
from utils import (
    get_keys,
    get_var_value,
    substitute_code,
    substitute_text,
    substitute_var,
)
from typing import Optional, Dict, List


class Entity:
    def __init__(
        self,
        key: Key,
        text: str,
        code: str,
        var: str,
        final: bool = False,
        parent: Optional["Entity"] = None,
        context: Dict = {},
        **kwargs,
    ) -> None:
        self.key = key
        self.text = text
        self.template_text = text
        self.code = code
        self.template_code = code
        self.var = var
        self.children = dict()
        self.context = context
        self.uuid = self._generate_uuid()
        self.final = final
        self.type = None
        self.parent = parent
        self.coreference_text = None
        self.coreference_entities = []
        self.shown = False

        for k, v in kwargs.items():
            setattr(self, k, v)

    def can_corefernce(self) -> bool:
        result = self.coreference_text is not None
        return result

    def get_context_id(self) -> Optional[str]:
        context_id = self.context.get("parent", {}).get("id")
        return context_id

    def get_keys(self) -> List[Key]:
        keys = get_keys(value=self.text + self.code, index=self.key.index)
        return keys

    def get_type(self) -> Optional[str]:
        if self.type:
            return self.type

        var_type = None
        for child_key in self.children:
            child = self.children[child_key]
            var_type = child.get_type()
            if var_type:
                break

        return var_type

    def get_var(self):
        if self.var is not None and not self.var.startswith("$"):
            return self.var

        var = None
        for child_key in self.children:
            child = self.children[child_key]
            var = child.get_var()
            if var:
                break
        return var

    def is_coreference_with(self, coref_entity: "Entity") -> bool:
        """
        This method checks if this entity can coreference with a given entity.
        All of the following conditions should be met:
        * Another entity of the same type is present in the program stack
        * The candidate source entity is not in a conjunction
        * The source entity does not share the same parent as the current entity
        * No other source type is previously coreferenced
        """
        result = (
            self.get_type() == coref_entity.get_type()  # coref to the same type
            and self.coreference_text is not None  # has a text value for co-referencing
            # and coref_entity.type
            # is not None  # the source is a top level - todo!!! need to find a better way
            and self.key.count == 1  # source entity is not brought in conjunction
            and self.get_context_id()
            != coref_entity.get_context_id()  # entity and coref do not share the same parent
            # and v.get("coref_context_id") != context.get("parent", {}).get("id")
        )
        return result

    def to_text(self, options: Dict = dict()) -> str:
        default_options = {"print_stack": []}
        options = {**default_options, **options}
        if self.coreference_text and self._is_coreference_mentioned(
            options["print_stack"]
        ):
            options["print_stack"].append(self.uuid)
            return self.coreference_text

        child_keys = get_keys(value=self.text, index=self.key.index)
        for child_key in child_keys:
            child = self.children[child_key.key]

            self.text = substitute_text(
                text=self.text, key=child_key, value=child.to_text(options)
            )

        options["print_stack"].append(self.uuid)

        text = self.text
        return text

    def to_code(self, options: Dict = dict()) -> str:
        default_options = {"print_stack": []}
        options = {**default_options, **options}
        if self.coreference_text and self._is_coreference_mentioned(
            options["print_stack"]
        ):
            options["print_stack"].append(self.uuid)
            return "__DELETE__"

        child_keys = get_keys(value=self.code, index=self.key.index)
        for child_key in child_keys:
            child = self.children[child_key.key]

            var_value = get_var_value(
                key=child_key,
                parent_var=self.var,
                child_var=child.get_var(),
            )

            self.var = substitute_var(
                var=self.var,
                key=child_key,
                var_value=var_value,
            )

            # replace child value and var in parent with child value and var
            self.code = substitute_code(
                code=self.code,
                key=child_key,
                code_value=child.to_code(options),
                var_value=var_value,
                child_var=child.var,
            )

        options["print_stack"].append(self.uuid)

        code = self.code
        return code

    def _generate_uuid(self) -> str:
        value = self.key.key + "_" + str(uuid.uuid4()).split("-")[0]
        return value

    def _is_coreference_mentioned(self, print_stack: List[str]) -> bool:
        """
        This method checks whether any of the coreference entities in
        the coreference segment were already mentioned (and therefore
        we would probably like to list this entity by its coreference
        value)"""
        result = len(self.coreference_entities) > 0 and any(
            [
                (coref_entity.uuid in print_stack)
                for coref_entity in self.coreference_entities
            ]
        )
        return result

    # def _is_top_level_coreference(self):
    #     result = self.coreference_text is not None and not (self.parent and self.get_type() == self.parent.get_type() and self.parent._is_top_level_coreference())

    def __repr__(self) -> str:
        return self.key.key
