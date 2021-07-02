from schematics import Model
from schematics.types import ModelType, StringType, ListType


class Tags(Model):
    key = StringType(deserialize_from='Key')
    value = StringType(deserialize_from='Value')


class OracleCloud(Model):
    fault_domain = StringType()
    launch_mode = StringType(choices=('PARAVIRTUALIZED', 'SR-IOV'))
    boot_volume_type = StringType(serialized_when_none=False)
    network_type = StringType()
    tags = ListType(ModelType(Tags))

