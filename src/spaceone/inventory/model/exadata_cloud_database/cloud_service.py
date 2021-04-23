# Created By Seungho
from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.exadata_cloud_database.data import CloudExadataInfra, CloudVMCluster, DatabaseSoftwareImage, Backup, Database

from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField,\
                                                                  EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
ExadataInfrastructure
'''
exadata_infra_base = ItemDynamicLayout.set_fields('General Info', fields=[
    TextDyField.data_source('Display Name', 'data.display_name'),
    TextDyField.data_source('Id', 'data.id'),
    EnumDyField.data_source('Lifecycle State', 'data.lifecycle_state', default_state={
        'safe': ['AVAILABLE'],
        'warning': ['UPDATING', 'TERMINATING', 'MAINTENANCE_IN_PROGRESS'],
        'alert': ['TERMINATED', 'FAILED']
    }),
    TextDyField.data_source('Availability Domain', 'data.availability_domain'),
    TextDyField.data_source('Compartment', 'data.compartment_name'),
    TextDyField.data_source('Shape', 'data.shape'),
    TextDyField.data_source('Version', 'data.version'),
    TextDyField.data_source('Compute Count', 'data.compute_count'),
    TextDyField.data_source('Storage Count', 'data.storage_count'),
    SizeField.data_source('Total Storage Size', 'data.total_storage_size_in_gbs', options={
        'display_unit': 'GB',
        'source_unit': 'GB'
    }),
    SizeField.data_source('Available Storage Size', 'data.available_storage_size_in_gbs', options={
        'display_unit': 'GB',
        'source_unit': 'GB'
    }),
    TextDyField.data_source('Maintenance Window' 'data.maintenance_window.display'),
    DateTimeDyField.data_source('Created', 'data.time_created')
])

exadata_last_maintenance_run = ItemDynamicLayout.set_fields('Last Maintenance Run', root_path='data.last_maintenance_run'
                                                            , fields=[
        TextDyField.data_source('Display', 'maintenance_display'),
        TextDyField.data_source('Id', 'id'),
        EnumDyField.data_source('State', 'lifecycle_state', default_state={
            'safe': ['SUCCEEDED'],
            'warning': ['SCHEDULED', 'IN_PROGRESS',
                        'SKIPPED', 'UPDATING', 'DELETING'],
            'alert': ['FAILED', 'DELETED', 'CANCELED']
        }),
        TextDyField.data_source('Description', 'description'),
        TextDyField.data_source('Target Resource Id', 'target_resource_type'),
        TextDyField.data_source('Target Resource Type', 'target_resource_type'),
        TextDyField.data_source('Maintenance Type', 'maintenance_type'),
        TextDyField.data_source('Maintenance Subtype', 'maintenance_subtype'),
        TextDyField.data_source('Alert', 'maintenance_alert'),
        DateTimeDyField.data_source('Time Scheduled', 'time_scheduled'),
        DateTimeDyField.data_source('Time Started', 'time_started'),
        DateTimeDyField.data_source('Time Ended', 'time_ended')
    ])

exadata_next_maintenance_run = ItemDynamicLayout.set_fields('Next Maintenance Run', root_path='data.next_maintenance_run'
                                                            , fields=[
        TextDyField.data_source('Display', 'maintenance_display'),
        TextDyField.data_source('Id', 'id'),
        EnumDyField.data_source('State', 'lifecycle_state', default_state={
            'safe': ['SUCCEEDED'],
            'warning': ['SCHEDULED', 'IN_PROGRESS',
                        'SKIPPED', 'UPDATING', 'DELETING'],
            'alert': ['FAILED', 'DELETED', 'CANCELED']
        }),
        TextDyField.data_source('Description', 'description'),
        TextDyField.data_source('Target Resource Id', 'target_resource_type'),
        TextDyField.data_source('Target Resource Type', 'target_resource_type'),
        TextDyField.data_source('Maintenance Type', 'maintenance_type'),
        TextDyField.data_source('Maintenance Subtype', 'maintenance_subtype'),
        TextDyField.data_source('Alert', 'maintenance_alert'),
        DateTimeDyField.data_source('Time Scheduled', 'time_scheduled'),
        DateTimeDyField.data_source('Time Started', 'time_started'),
        DateTimeDyField.data_source('Time Ended', 'time_ended')
    ])

exadata_maintenance_meta = ListDynamicLayout.set_layouts('Maintenance Run', [exadata_last_maintenance_run,
                                                                             exadata_next_maintenance_run])

exadata_vm_cluster_meta =\
    TableDynamicLayout.set_fields('Exadata VM Clusters',
                                  root_path='data.list_cloud_vm_cluster', fields=[
            TextDyField.data_source('Display Name', 'display_name'),
            EnumDyField.data_source('State', 'lifecycle_state', default_state={
                'safe': ['AVAILABLE'],
                'warning': ['PROVISIONING', 'UPDATING',
                            'TERMINATING','MAINTENANCE_IN_PROGRESS'],
                'alert': ['TERMINATED', 'FAILED']
            }),
            TextDyField.data_source('Compartment', 'compartment_name'),
            TextDyField.data_source('Availability Domain', 'availability_domain'),
            TextDyField.data_source('CPU Core Count', 'cpu_core_count'),
            DateTimeDyField.data_source('Created', 'time_created')
        ])

exadata_tag = TableDynamicLayout.set_fields('Tags', root_path='data.freeform_tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

exadata_infra_meta = CloudServiceMeta.set_layouts([exadata_infra_base, exadata_vm_cluster_meta,
                                                  exadata_maintenance_meta, exadata_tag])

'''
ExadataVMCluster
'''
vm_cluster_base = ItemDynamicLayout.set_fields('General Info', fields=[
    TextDyField.data_source('Display Name', 'data.display_name'),
    TextDyField.data_source('Cluster Name', 'data.cluster_name'),
    EnumDyField.data_source('State', 'lifecycle_state', default_state={
        'safe': ['AVAILABLE'],
        'warning': ['PROVISIONING', 'UPDATING',
                    'TERMINATING','MAINTENANCE_IN_PROGRESS'],
        'alert': ['TERMINATED', 'FAILED']
    }),
    TextDyField.data_source('Id', 'data.id'),
    TextDyField.data_source('Availability Domain', 'data.availability_domain'),
    TextDyField.data_source('Compartment', 'data.compartment_name'),
    TextDyField.data_source('Cloud Exadata Infrastructure Id', 'data.cloud_exadata_infrastructure_id'),
    TextDyField.data_source('Shape', 'data.shape'),
    TextDyField.data_source('CPU Core Count', 'data.cpu_core_count'),
    TextDyField.data_source('Node Count', 'data.node_count'),
    SizeField.data_source('Storage Size','data.storage_size_in_gbs', options={
        'display_unit': 'GB',
        'source_unit': 'GB'
    }),
    TextDyField.data_source('Storage Percentage', 'data.data_storage_percentage'),
    TextDyField.data_source('System Version', 'data.system_version'),
    TextDyField.data_source('License Model', 'data.license_model'),
    TextDyField.data_source('GI Version', 'data.gi_version'),
    TextDyField.data_source('Time Zone', 'data.time_zone'),
    ListDyField.data_source('SSH Public Key', 'data.ssh_public_keys', options={
        'delimiter': '<br>'
    }),
    DateTimeDyField.data_source('Created', 'data.time_created')
])

vm_cluster_network = ItemDynamicLayout.set_fields('Network', fields=[
    TextDyField.data_source('Subnet Id', 'data.subnet_id'),
    TextDyField.data_source('Backup Subnet Id', 'data.backup_subnet_id'),
    ListDyField.data_source('NSG Id', 'data.nsg_ids', options={
        'delimiter': '<br>'
    }),
    ListDyField.data_source('Backup NSG Id', 'data.backup_network_nsg_ids', options={
        'delimiter': '<br>'
    }),
    TextDyField.data_source('Hostname Prefix', 'data.hostname'),
    TextDyField.data_source('Host Domain Name', 'data.domain'),
    TextDyField.data_source('SCAN DNS Name', 'data.scan_dns_name'),
    TextDyField.data_source('SCAN DNS record Id', 'data.scan_dns_record_id'),
    ListDyField.data_source('SCAN IP Id', 'data.scan_ip_ids', options={
        'delimiter': '<br>'
    }),
    ListDyField.data_source('VIP Id', 'data.vip_ids', options={
        'delimiter': '<br>'
    })
])

vm_cluster_database = TableDynamicLayout.set_fields('Database', root_path='data.list_database', fields=[
    TextDyField.data_source('Name', 'db_name'),
    EnumDyField.data_source('State', 'lifecycle_state', default_state={
        'safe': ['AVAILABLE'],
        'warning': ['PROVISIONING', 'UPDATING',
                    'BACKUP_IN_PROGRESS', 'UPGRADING', 'TERMINATING'],
        'alert': ['TERMINATED', 'RESTORE_FAILED', 'FAILED']
    }),
    TextDyField.data_source('Database Unique Name', 'db_unique_name'),
    TextDyField.data_source('Workload Type'),
    DateTimeDyField.data_source('Created', 'time_created')
])

vm_cluster_node = TableDynamicLayout.set_fields('Node', root_path='data.list_db_node', fields=[
    TextDyField.data_source('Name', 'hostname'),
    EnumDyField.data_source('State', 'lifecycle_state', default_state={
        'safe': ['AVAILABLE'],
        'warning': ['PROVISIONING', 'UPDATING', 'STOPPING', 'STARTING', 'TERMINATING'],
        'alert': ['STOPPED', 'TERMINATED', 'FAILED']
    }),
    TextDyField.data_source('Vnic Id', 'vnic_id'),
    TextDyField.data_source('Fault Domain', 'fault_domain'),
    TextDyField.data_source('Storage Size(GB)', 'software_storage_size_in_gb'),
    DateTimeDyField.data_source('Created', 'time_created')
])

vm_cluster_update_history = \
    TableDynamicLayout.set_fields('Update History', root_path='data.list_update_history', fields=[
        TextDyField.data_source('Update Id', 'update_id'),
        TextDyField.data_source('Action', 'update_action'),
        TextDyField.data_source('Type', 'update_type'),
        EnumDyField.data_source('State', 'lifecycle_state', default_state={
            'safe': ['SUCCEEDED'],
            'warning': ['IN_PROGRESS'],
            'alert': ['FAILED']
        }),
        DateTimeDyField.data_source('Started', 'time_started'),
        DateTimeDyField.data_source('Completed', 'time_completed')
    ])

vm_cluster_update =\
    TableDynamicLayout.set_fields('Update', root_path='data.list_update', fields=[
        TextDyField.data_source('Id', 'id'),
        EnumDyField.data_source('State', 'lifecycle_state', default_state={
            'safe': ['SUCCEEDED'],
            'warning': ['IN_PROGRESS'],
            'alert': ['FAILED']
        }),
        TextDyField.data_source('Type', 'update_type'),
        TextDyField.data_source('Last Action', 'last_action'),
        ListDyField.data_source('Available Actions', 'available_actions', options={
            'delimiter': '<br>'
        }),
        TextDyField.data_source('Version', 'version'),
        DateTimeDyField.data_source('Released', 'time_released')
    ])

vm_cluster_tag = TableDynamicLayout.set_fields('Tags', root_path='data.freeform_tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

vm_cluster_meta = CloudServiceMeta.set_layouts([vm_cluster_base, vm_cluster_network,
                                                vm_cluster_node, vm_cluster_database,
                                                vm_cluster_update_history, vm_cluster_update,
                                                vm_cluster_tag])

'''
Database
'''
vm_db_base = ItemDynamicLayout.set_fields('General Info', fields=[
    TextDyField.data_source('DB Name', 'data.db_name'),
    TextDyField.data_source('Id', 'data.id'),
    TextDyField.data_source('Compartment Id', 'data.compartment_id'),
    EnumDyField.data_source('State', 'data.lifecycle_state',
                            default_state={
                                'safe': ['AVAILABLE'],
                                'warning': ['PROVISIONING', 'UPDATING',
                                            'BACKUP_IN_PROGRESS', 'UPGRADING', 'TERMINATING'],
                                'alert': ['TERMINATED', 'RESTORE_FAILED', 'FAILED']}),
    TextDyField.data_source('Version', 'data.db_version'),
    TextDyField.data_source('Workload Type', 'data.db_workload'),
    TextDyField.data_source('Unique Name', 'data.db_unique_name'),
    TextDyField.data_source('PDB Name', 'data.pdb_name'),
    TextDyField.data_source('Database Software Image', 'data.database_software_image_id'),
    TextDyField.data_source('DB Home Id', 'data.db_home_id'),
    TextDyField.data_source('VM Cluster Id', 'data.vm_cluster_id'),
    TextDyField.data_source('Character Set', 'data.character_set'),
    TextDyField.data_source('National Character Set', 'data.ncharacter_set'),
    TextDyField.data_source('KMS key Id', 'data.kms_key_id'),
    DateTimeDyField.data_source('Created', 'data.time_created')
])

vm_db_connection_strings_default = ItemDynamicLayout.set_fields('Default',
                                                             root_path='data.connection_strings', fields=[
        TextDyField.data_source('CDB default', 'cdb_default'),
        TextDyField.data_source('CDB IP default', 'cdb_ip_default')
    ])

vm_db_connection_strings_all = TableDynamicLayout.set_fields('Connection Strings',
                                                          root_path='data.connection_strings.all_connection_strings', fields=[
        TextDyField.data_source('Name', 'key'),
        TextDyField.data_source('Connection String', 'value')
    ])
vm_db_connection_meta = ListDynamicLayout.set_layouts('Connection Strings', [vm_db_connection_strings_default,
                                                                             vm_db_connection_strings_all])

vm_db_tags = TableDynamicLayout.set_fields('Tags', 'data.freeform_tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

vm_db_metadata = CloudServiceMeta.set_layouts([vm_db_base, vm_db_connection_meta, vm_db_tags])

'''
DatabaseSoftwareImage
'''
vm_db_image_base = ItemDynamicLayout.set_fields('General Info', fields=[
    TextDyField.data_source('Name', 'data.display_name'),
    TextDyField.data_source('Id', 'data.id'),
    TextDyField.data_source('Compartment', 'data.compartment_name'),
    TextDyField.data_source('DB version', 'data.database_version'),
    EnumDyField.data_source('State', 'data.lifecycle_state', default_state={
        'safe': ['AVAILABLE'],
        'warning': ['PROVISIONING', 'DELETING', 'TERMINATING', 'UPDATING'],
        'alert': ['DELETED', 'FAILED', 'TERMINATED']
    }),
    EnumDyField.data_source('Image Type', 'data.image_type',
                            default_outline_badge=['GRID_IMAGE', 'DATABASE_IMAGE']),
    EnumDyField.data_source('Image Shape', 'data.image_shape_family',
                            default_outline_badge=['VM_BM_SHAPE', 'EXADATA_SHAPE']),
    TextDyField.data_source('PSU/BP/RU', 'data.patch_set'),
    ListDyField.data_source('One-Off Patches', 'data.database_software_image_one_off_patches', options={
        'delimiter': '<br>'
    }),
    EnumDyField.data_source('Upgrade Supported', 'data.is_upgrade_supported',
                            default_badge={'indigo.500': ['true'], 'coral.600': ['false']}),
    DateTimeDyField.data_source('Created', 'data.time_created')

])

vm_db_image_tags = TableDynamicLayout.set_fields('Tags', 'data.freeform_tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

vm_db_image_metadata = CloudServiceMeta.set_layouts([vm_db_image_base, vm_db_image_tags])

'''
Backup
'''
vm_db_backup_base = ItemDynamicLayout.set_fields('General Info', fields=[
    TextDyField.data_source('Id', 'data.id'),
    TextDyField.data_source('Compartment', 'data.compartment_name'),
    TextDyField.data_source('Source DB ID', 'data.database_id'),
    EnumDyField.data_source('Type', 'data.type',
                            default_outline_badge=['INCREMENTAL', 'FULL', 'VIRTUAL_FULL']),
    EnumDyField.data_source('Edition', 'data.database_edition',
                            default_outline_badge=['STANDARD_EDITION', 'ENTERPRISE_EDITION',
                                                   'ENTERPRISE_EDITION_HIGH_PERFORMANCE',
                                                   'ENTERPRISE_EDITION_EXTREME_PERFORMANCE']),
    TextDyField.data_source('Shape', 'data.shape'),
    TextDyField.data_source('Availability Domain', 'data.availability_domain'),
    TextDyField.data_source('Size(GB)', 'data.database_size_in_gbs'),
    DateTimeDyField.data_source('KMS key Id', 'data.kms_key_id'),
    DateTimeDyField.data_source('Time Started', 'data.time_started'),
    DateTimeDyField.data_source('Time Ended', 'data.time_ended')
])

vm_db_backup_tags = TableDynamicLayout.set_fields('Tags', 'data.freeform_tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

db_backup_metadata = CloudServiceMeta.set_layouts([vm_db_backup_base, vm_db_backup_tags])


class ExadataCloudResource(CloudServiceResource):
    cloud_service_group = StringType(default='ExadataCloudDatabase')


# ExadataInfrastructure
class ExadataInfrastructureResource(ExadataCloudResource):
    cloud_service_type = StringType(default='ExadataInfrastructure')
    data = ModelType(CloudExadataInfra)
    _metadata = ModelType(CloudServiceMeta, default=exadata_infra_meta, serialized_name='metadata')


class ExadataInfrastructureResponse(CloudServiceResponse):
    resource = PolyModelType(ExadataInfrastructureResource)


# ExadataVMCluster
class ExadataVMClusterResource(ExadataCloudResource):
    cloud_service_type = StringType(default='ExadataVMCluster')
    data = ModelType(CloudVMCluster)
    _metadata = ModelType(CloudServiceMeta, default=vm_cluster_meta, serialized_name='metadata')


class ExadataVMClusterResponse(CloudServiceResponse):
    resource = PolyModelType(ExadataVMClusterResource)


# Database
class ExadataDatabaseResource(ExadataCloudResource):
    cloud_service_group = StringType(default='Database')
    data = ModelType(Database)
    _metadata = ModelType(CloudServiceMeta, default=vm_db_metadata, serialized_name='metadata')


class ExadataDatabaseResponse(CloudServiceResponse):
    resource = PolyModelType(ExadataDatabaseResource)


# DatabaseSoftwareImage
class ExadataDatabaseSoftwareImageResource(ExadataCloudResource):
    cloud_service_type = StringType(default='DatabaseSoftwareImage')
    data = ModelType(DatabaseSoftwareImage)
    _metadata = ModelType(CloudServiceMeta, default=vm_db_image_metadata, serialized_name='metadata')


class ExadataDatabaseSoftwareImageResponse(CloudServiceResponse):
    resource = PolyModelType(ExadataDatabaseSoftwareImageResource)


# Backup
class ExadataBackupResource(ExadataCloudResource):
    cloud_service_group = StringType(default='Backup')
    data = ModelType(Backup)
    _metadata = ModelType(CloudServiceMeta, default=db_backup_metadata, serialized_name='metadata')


class ExadataBackupResponse(CloudServiceResponse):
    resource = PolyModelType(ExadataBackupResource)


