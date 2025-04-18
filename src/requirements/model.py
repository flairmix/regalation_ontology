# src/requirements/model.py

from pydantic import BaseModel
from typing import List, Optional

class ObjectProperty(BaseModel):
    property_name: str
    target: str  # id другого объекта

class PropertyEntry(BaseModel):
    name: str
    value: Optional[float] = None
    unit: Optional[str] = None

class ObjectInstance(BaseModel):
    id: str
    class_name: str
    properties: Optional[List[PropertyEntry]] = []
    relations: Optional[List[ObjectProperty]] = []

class CheckEntry(BaseModel):
    type: str  # например, Check_property_value_greater
    target: Optional[str] = None  # id объекта или свойства
    unit: Optional[str] = None
    value: Optional[float] = None

class ConditionEntry(BaseModel):
    type: str  # например, Condition_component_exist
    target: Optional[str] = None  # id объекта или свойства


class Requirement(BaseModel):
    id: str
    objects: List[ObjectInstance]
    conditions: List[ConditionEntry] = []
    checks: List[CheckEntry]