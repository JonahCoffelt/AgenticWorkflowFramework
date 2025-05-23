from typing import Any
from .data_validation import validate_string


class Resource():
    name: str
    """"""
    value: Any
    """"""
    
    def __init__(self, name: str, value: Any):
        """
        Container for a single resource in the context.
        Essentially stored as a key-value pair. 
        Args:
            name: str
                Used to identify the resource
            value
        """
        
        self.name = name
        self.value = value

    @property
    def name(self) -> str: return self._name
    @property
    def value(self) -> Any: return self._value

    @value.setter
    def value(self, value: Any):
        self._value = value
    @name.setter
    def name(self, value: str):
        self._name = validate_string(value)

    def __repr__(self):
        return f'<Resource | {self.name} : {self.value} >'