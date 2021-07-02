from schematics import Model
from schematics.types import StringType, IntType


class InstancePool(Model):
    id = StringType()
    display_name = StringType()
    instance_configuration_id = StringType()
    size = IntType()