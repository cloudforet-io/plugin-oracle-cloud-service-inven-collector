from schematics.types import ListType, StringType, BooleanType
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource


class CloudServiceType(CloudServiceTypeResource):
    name = StringType(default="Instance")
    provider = StringType(default='oracle_cloud')
    group = StringType(default='ComputeInstance')
    labels = ListType(StringType(), serialize_when_none=False, default=["Compute"])
    tags = {
        'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/oci/OCI_icon_VM.svg'
    }
    is_primary = BooleanType(default=True)
    is_major = BooleanType(default=True)
    service_code = StringType(default="Instance")
    resource_type = StringType(default="inventory.Server")

