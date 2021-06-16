from schematics import Model
from schematics.types import  ModelType, ListType, StringType
from spaceone.inventory.model.compute_instance.data import OS, OracleCloud, SecurityGroup, Compute, LoadBalancer, \
    VCN, Subnet, InstancePool, NIC, Compartment, Domain, Disk, HardWare
from spaceone.inventory.libs.schema.cloud_service import CloudServiceMeta


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value ")


class ServerData(Model):
    os = ModelType(OS)
    oracle_cloud = ModelType(OracleCloud)
    compartment = ModelType(Compartment)
    hardware = ModelType(HardWare)
    security_group = ListType(ModelType(SecurityGroup))
    compute = ModelType(Compute)
    domain = ModelType(Domain)
    load_balancer = ListType(ModelType(LoadBalancer))
    vcn = ModelType(VCN)
    subnet = ModelType(Subnet)
    instance_pool = ModelType(InstancePool, serialize_when_none=False)

