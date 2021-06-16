from schematics import Model
from schematics.types import StringType


class Domain(Model):
    domain = StringType()
    fqdn = StringType()