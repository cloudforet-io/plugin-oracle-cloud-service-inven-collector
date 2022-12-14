from schematics import Model
from schematics.types import StringType, IntType, DictType, ListType, ModelType


class LoadBalancerTags(Model):
    lb_id = StringType()


class LoadBalancer(Model):
    type = StringType(choices=('LB', 'NLB'))
    endpoint = StringType()
    port = ListType(IntType())
    name = StringType()
    protocol = ListType(StringType())
    scheme = StringType(choices=('public', 'private'))
    tags = ModelType(LoadBalancerTags, default={})