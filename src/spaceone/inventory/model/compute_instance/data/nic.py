from schematics import Model
from schematics.types import StringType, IntType, ListType, DictType, ModelType


class NICTags(Model):
    vnic_id = StringType(serialize_when_none=False)
    hostname_label = StringType(serialize_when_none=False)


class NIC(Model):
    device_index = IntType()
    nic_type = StringType(choices=("Primary", "Secondary"))
    ip_addresses = ListType(StringType())
    cidr = StringType()
    mac_address = StringType()
    public_ip_address = StringType()
    tags = ModelType(NICTags, default={})