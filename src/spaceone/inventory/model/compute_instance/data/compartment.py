from schematics import Model
from schematics.types import StringType


class Compartment(Model):
    compartment_name = StringType()
    compartment_id = StringType()
    tenancy_id = StringType()