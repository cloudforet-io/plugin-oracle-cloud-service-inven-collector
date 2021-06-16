from schematics import Model
from schematics.types import StringType, DateTimeType, ListType, BooleanType, ModelType, DictType


class ComputeTags(Model):
    image_id = StringType()
    firmware = StringType()
    id = StringType()


class Compute(Model):
    keypair = StringType()
    ad = StringType()
    instance_state = StringType()
    launched_at = DateTimeType()
    instance_id = StringType(default='')
    instance_name = StringType(default='')
    account = StringType()
    image = StringType()
    instance_type = StringType()
    security_groups = ListType(DictType(StringType()))
    tags = ModelType(ComputeTags, default={})
