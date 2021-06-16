from schematics import Model
from schematics.types import StringType, IntType, BooleanType, ModelType, FloatType


class DiskTags(Model):
    volume_id = StringType(serialize_when_none=False)
    vpus_per_gb = StringType()
    iops = IntType(serialize_when_none=False)


class Disk(Model):
    device_index = IntType()
    device = StringType()
    disk_type = StringType(default="BlockVolume")
    size = FloatType()
    tags = ModelType(DiskTags, default={})