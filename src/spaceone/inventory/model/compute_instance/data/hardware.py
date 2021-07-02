from schematics import Model
from schematics.types import StringType, IntType, FloatType, ListType


class HardWare(Model):
    core = IntType(default=0)
    memory = FloatType(default=0.0)
    cpu_model = ListType(StringType)