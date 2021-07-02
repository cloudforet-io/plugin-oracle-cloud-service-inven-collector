from schematics.types import ModelType, StringType, ListType ,PolyModelType

from spaceone.inventory.model.compute_instance.data.server import ServerData
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField,\
                                                                  EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

from spaceone.inventory.model.compute_instance.data.disk import Disk
from spaceone.inventory.model.compute_instance.data.nic import NIC
from spaceone.inventory.model.compute_instance.data.oracle_cloud import  Tags

'''
Instance
'''
compute_instance = ItemDynamicLayout.set_fields('Compute Instance', fields=[
    TextDyField.data_source('Account', 'data.account'),
    TextDyField.data_source('Compartment', 'data.compartment.compartment_name'),
    TextDyField.data_source('Instance ID', 'data.compute.instance_id'),
    TextDyField.data_source('Instance Name', 'data.instance_name'),
    EnumDyField.data_source('Instance State', 'data.compute.instance_state', default_state={
        'safe': ['RUNNING'],
        'warning': ['PENDING', 'STOPPING'],
        'disable': ['SHUTTING-DOWN'],
        'alert': ['STOPPED']
    }),
    TextDyField.data_source('Instance Type', 'data.compute.instance_type'),
    TextDyField.data_source('Image', 'data.compute.image'),
    TextDyField.data_source('Launch Mode', 'data.oracle_cloud.launch_mode'),
    TextDyField.data_source('Boot Volume Type', 'data.oracle_cloud.boot_volume_type'),
    TextDyField.data_source('Primary IP Address', 'primary_ip_address'),
    ListDyField.data_source('IP Addresses', 'ip_addresses',
                            default_badge={'type': 'outline'}),
    TextDyField.data_source('Region', 'region_code'),
    TextDyField.data_source('Availability Domain', 'data.compute.ad'),
    TextDyField.data_source('Fault Domain', 'data.oracle_cloud.fault_domain'),
    ListDyField.data_source('Security Groups', 'data.security_group',
                            default_badge={'type': 'outline',
                                           'delimeter': '<br>',
                                           'sub_key': 'security_group_name'},
                            reference={'resource_type': 'inventory.CloudService',
                                       'reference_key': 'data.security_group_id'}),
    TextDyField.data_source('Key Pair', 'data.compute.keypair'),
    DateTimeDyField.data_source('Launched At', 'data.compute.launched_at')

])

compute_instance_vcn = ItemDynamicLayout('VCN', fields=[
    TextDyField.data_source('VCN Name', 'data.vcn.display_name'),
    TextDyField.data_source('VCN ID', 'data.vcn.id', reference={
        'resource_type': 'inventory.CloudService',
        'reference_key': 'data.id'
    }),
    TextDyField.data_source('Subnet Name', 'data.subnet.name'),
    TextDyField.data_source('Subnet ID', 'data.subnet.id', reference={
        'resource_type': 'inventory.CloudService',
        'reference_key': 'data.id'
    })
])

compute_instance_pool = ItemDynamicLayout('Instance Pool', fields=[
    TextDyField.data_source('Instance Pool', 'data.instance_pool.display_name'),
    TextDyField.data_source('Instance Pool ID', 'data.instance_pool.id', reference={
        'resource_type': 'inventory.CloudService',
        'reference_key': 'data.id'
    }),
    TextDyField.data_source('Instance Configuration ID', 'data.instance_pool.instance_configuration_id', reference={
        'resource_type': 'inventory.CloudService',
        'reference_key': 'data.instance_configuration_id'
    }),
    TextDyField.data_source('Size', 'data.instance_pool.size')
])

instance = ListDynamicLayout.set_layouts('Compute Instance', layouts=[compute_instance, compute_instance_vcn,
                                                                      compute_instance_pool])

disk = TableDynamicLayout.set_fields('Disk', root_path='disks', fields=[
    TextDyField.data_source('Index', 'device_index'),
    TextDyField.data_source('Name', 'device'),
    SizeField.data_source('Size(GB)', 'size', options={
        'display_unit': 'GB',
        'source_unit': 'GB'
    }),
    TextDyField.data_source('Volume ID', 'tags.volume_id'),
    TextDyField.data_source('Volume_type', 'disk_type'),
    TextDyField.data_source('VPUS per GB', 'tags.vpus_per_gb'),
    TextDyField.data_source('IOPS', 'tags.iops')
])

nic = TableDynamicLayout.set_fields('NIC', root_path='nics', fields=[
    TextDyField.data_source('Index', 'device_index'),
    TextDyField.data_source('MAC Address', 'mac_address'),
    ListDyField.data_source('IP Addresses', 'ip_addresses', options={'delimiter': '<br>'}),
    TextDyField.data_source('CIDR', 'cidr'),
    TextDyField.data_source('Public IP', 'public_ip_address'),
    TextDyField.data_source('Hostname Label', 'tags.hostname_label')
])

security_group = TableDynamicLayout.set_fields('Security Groups', root_path='data.security_group', fields=[
    EnumDyField.data_source('Direction', 'direction', default_badge={
        'indigo.500': ['inbound'], 'coral.600': ['outbound']
    }),
    TextDyField.data_source('Name', 'security_group_name', reference={
        'resource_type': 'inventory.CloudService',
        'reference_key': 'data.security_group_name'
    }),
    EnumDyField.data_source('Protocol', 'protocol', default_outline_badge=['ALL', 'TCP', 'UDP', 'ICMP']),
    TextDyField.data_source('Port Range', 'port'),
    TextDyField.data_source('Remote', 'remote'),
    TextDyField.data_source('Description', 'description')
])

lb = TableDynamicLayout.set_fields('LB', root_path='data.load_balancer', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Endpoint', 'endpoint'),
    EnumDyField.data_source('Type', 'type', default_badge={
        'indigo.500': ['NLB'], 'coral.600': ['LB']
    }),
    ListDyField.data_source('Protocol', 'protocol', options={'delimiter': '<br>'}),
    ListDyField.data_source('Scheme', 'scheme', default_badge={
        'indigo.500': ['public'], 'coral.600': ['private']
    })
])

tags = TableDynamicLayout.set_fields('Oracle Tags', root_path='data.oracle_cloud.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
])

compute_instance_metadata = CloudServiceMeta.set_layouts([instance, tags, disk, nic, security_group, lb])


class ComputeInstanceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compute')
    cloud_service_type = StringType(default='Instance')
    data = ModelType(ServerData)
    _metadata = ModelType(CloudServiceMeta, default=compute_instance_metadata, serialize_name='metadata')
    name = StringType()
    tags = ListType(ModelType(Tags))
    nics = ListType(ModelType(NIC))
    disks = ListType(ModelType(Disk))
    primary_ip_address = StringType(default='')
    ip_addresses = ListType(StringType())
    server_type = StringType(default='VM')
    os_type = StringType(choices=('LINUX', 'WINDOWS'))


class ComputeInstanceResponse(CloudServiceResponse):
    resource = PolyModelType(ComputeInstanceResource)
    resource_type = StringType(default='inventory.Server')

