from schematics import Model
from schematics.types import StringType


class VCN(Model):
    display_name = StringType()
    id = StringType()
    cidr_block = StringType()
