from schematics import Model
from schematics.types import StringType


class Subnet(Model):
    name = StringType()
    id = StringType()
    cidr_block = StringType()
    subnet_domain_name = StringType()