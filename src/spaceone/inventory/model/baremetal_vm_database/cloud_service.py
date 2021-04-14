# Created By Seungho
from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.baremetal_vm_database.data import DbSystem, DatabaseSoftwareImage, Backup, Database
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField,\
                                                                  EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
DBSystems
'''
dbsystem_base = ItemDynamicLayout.set_fields('General Info', fields=[
    EnumDyField.data_source('Lifecycle State', 'data.lifecycle_state', default_state={
        'safe': ['ACTIVE'],
        'warning': ['UPDATING', 'TERMINATING', 'MAINTENANCE_IN_PROGRESS'],
        'alert': ['TERMINATED', 'FAILED', 'MIGRATED', 'NEEDS_ATTENTION']
    }),
    TextDyField.data_source('Availability Domain', 'data.availability_domain'),
    ListDyField.data_source('Fault Domains','data.fault_domains', options={
        'delimiter': '<br>'
    }),
    TextDyField.data_source('Cluster Name', 'data.cluster_name'),
    TextDyField.data_source('OCID', 'data.id'),
    TextDyField.data_source('Shape', 'data.shape'),
    TextDyField.data_source('Version', 'data.version'),
    DateTimeDyField.data_source('Created', 'data.time_created'),
    TextDyField.data_source('Time Zone', 'data.time_zone'),
    TextDyField.data_source('Compartment', 'data.compartment_name'),
    EnumDyField.data_source('Oracle Database Software Edition', 'data.database_edition',
                            default_outline_badge=['STANDARD_EDITION', 'ENTERPRISE_EDITION',
                                                   'ENTERPRISE_EDITION_HIGH_PERFORMANCE',
                                                   'ENTERPRISE_EDITION_EXTREME_PERFORMANCE']),
    TextDyField.data_source('Storage Management Software', 'data.db_system_options.storage_management'),
    SizeField.data_source('Storage Size', 'data.data_storage_size_in_gbs', options={
        'display_unit': 'GB',
        'source_unit': 'GB'
    }),
    TextDyField.data_source('Licence Type', 'data.license_model'),
    TextDyField.data_source('Maintenance Window', 'data.maintenance_window.display'),
    TextDyField.data_source('KMS key Id', 'data.kms_key_id'),
    ListDyField.data_source('SSH Public Key', 'data.ssh_public_keys', options={
        'delimiter': '<br>'
    })
])

dbsystem_network = ItemDynamicLayout.set_fields('Network', fields= [
    TextDyField.data_source('Subnet Id', 'data.subnet_id'),
    TextDyField.data_source('Backup Subnet Id', 'data.backup_subnet_id'),
    ListDyField.data_source('NSG Id', 'data.nsg_id', options={
        'delimiter': '<br>'
    }),
    ListDyField.data_source('Backup Network NSG Id', 'data.backup_network_nsg_ids', options={
        'delimiter': '<br>'
    }),
    TextDyField.data_source('Hostname', 'data.hostname'),
    TextDyField.data_source('Domain', 'data.domain'),
    TextDyField.data_source('Port', 'data.listener_port'),
    TextDyField.data_source('Scan DNS Name', 'data.scan_dns_name'),
    ListDyField.data_source('Vip Ids', 'data.vip_ids', options={
        'delimiter': '<br>'
    })
])

dbsystem_database = TableDynamicLayout.set_fields('Databses', root_path='data.list_database', fields=[
    TextDyField.data_source('Name', 'db_name'),
    EnumDyField.data_source('State', 'lifecycle_state', default_state={
        'safe': ['AVAILABLE'],
        'warning': ['PROVISIONING', 'UPDATING',
                    'BACKUP_IN_PROGRESS', 'UPGRADING', 'TERMINATING'],
        'alert': ['TERMINATED', 'RESTORE_FAILED', 'FAILED']
    }),
    TextDyField.data_source('Database Unique Name', 'db_unique_name'),
    TextDyField.data_source('Workload Type', 'db_workload'),
    DateTimeDyField.data_source('Created', 'time_created')
])

dbsystem_node = TableDynamicLayout.set_fields('Nodes', root_path='data.list_db_node', fields=[
    TextDyField.data_source('Name', 'hostname'),
    EnumDyField.data_source('State', 'lifecycle_state', default_state={
        'safe': ['AVAILABLE'],
        'warning': ['PROVISIONING', 'UPDATING', 'STOPPING', 'STARTING', 'TERMINATING'],
        'alert': ['STOPPED', 'TERMINATED', 'FAILED']
    }),
    TextDyField.data_source('Vnic Id', 'vnic_id'),
    TextDyField.data_source('Fault Domain', 'fault_domain'),
    TextDyField.data_source('Storage Size', 'software_storage_size_in_gb'),
    DateTimeDyField.data_source('Created', 'time_created')
])

dbsystem_patches = TableDynamicLayout.set_fields('Patches', root_path='data.list_patches', fields=[
    TextDyField.data_source('Patch description', 'description'),
    EnumDyField.data_source('State', 'lifecycle_state', default_state={
        'safe': ['AVAILABLE','SUCCESS'],
        'warning': ['IN_PROGRESS'],
        'alert': ['FAILED']
    }),
    TextDyField.data_source('Version', 'version'),
    DateTimeDyField.data_source('Released date', 'time_released')
])

dbsystem_patch_history = TableDynamicLayout.set_fields('Patch History', root_path='data.list_patch_history', fields=[
    TextDyField.data_source('ID', 'patch_id'),
    EnumDyField.data_source('State', 'lifecycle_state', default_state={
        'safe': ['SUCCEEDED'],
        'warning': ['IN_PROGRESS'],
        'alert': ['FAILED']
    }),
    EnumDyField.data_source('Operation Type', 'action', default_outline_badge=['APPLY', 'PRECHECK']),
    DateTimeDyField.data_source('Started', 'time_started'),
    DateTimeDyField.data_source('Ended', 'time_ended')
])

dbsystem_console_connection = \
    TableDynamicLayout.set_fields('Console Connections',
                                  root_path='data.console_connections',
                                  fields=[
                                      TextDyField.data_source('Node Id', 'db_node_id'),
                                      EnumDyField.data_source('State', 'lifecycle_state',
                                                              default_state={
                                                                  'safe': ['ACTIVE'],
                                                                  'warning': ['CREATING', 'DELETING'],
                                                                  'alert': ['DELETED', 'FAILED']}),
                                      TextDyField.data_source('Fingerprint', 'fingerprint'),
                                      TextDyField.data_source('Connection String', 'connection_string')
])

dbsystem_tags = TableDynamicLayout.set_fields('Tags', root_path='data.freeform_tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

dbsystem_metadata = CloudServiceMeta.set_layouts([dbsystem_base, dbsystem_network,
                                              dbsystem_database, dbsystem_node,
                                              dbsystem_patches, dbsystem_patch_history,
                                              dbsystem_console_connection, dbsystem_tags])

'''
Database
'''
db_base = ItemDynamicLayout.set_fields('General Info', fields=[
    TextDyField.data_source('DB Name', 'data.db_name'),
    TextDyField.data_source('Id', 'data.id'),
    TextDyField.data_source('Compartment Id', 'data.compartment_id'),
    EnumDyField.data_source('State', 'data.lifecycle_state',
                            default_state={
                                'safe': ['AVAILABLE'],
                                'warning': ['PROVISIONING', 'UPDATING',
                                            'BACKUP_IN_PROGRESS', 'UPGRADING', 'TERMINATING'],
                                'alert': ['TERMINATED', 'RESTORE_FAILED', 'FAILED']}),
    TextDyField.data_source('Workload Type', 'data.db_workload'),
    TextDyField.data_source('Unique Name', 'data.db_unique_name'),
    TextDyField.data_source('PDB Name', 'data.pdb_name'),
    TextDyField.data_source('Database Software Image', 'data.database_software_image_id'),
    TextDyField.data_source('DB Home Id', 'data.db_home_id'),
    TextDyField.data_source('Db System Id', 'data.db_system_id'),
    TextDyField.data_source('Character Set', 'data.character_set'),
    TextDyField.data_source('National Character Set', 'data.ncharacter_set'),
    TextDyField.data_source('KMS key Id', 'data.kms_key_id'),
    DateTimeDyField.data_source('Created', 'data.time_created')
])

db_update_history = TableDynamicLayout.set_fields('Update History', root_path='data.list_upgrade_history', fields=[
    TextDyField.data_source('Id', 'id'),
    EnumDyField.data_source('State', 'state',
                            default_state={
                                'safe': ['SUCCEEDED'],
                                'warning': ['IN_PROGRESS'],
                                'alert': ['FAILED']
                            }),
    EnumDyField.data_source('Type', 'type',
                            default_outline_badge=['DB_HOME', 'DB_VERSION', 'DB_SOFTWARE_IMAGE']),
    EnumDyField.data_source('Operation type', 'action',
                            default_outline_badge=['PRECHECK', 'UPGRADE', 'ROLLBACK']),
    DateTimeDyField.data_source('Started', 'time_started'),
    DateTimeDyField.data_source('Ended', 'time_ended')
])

db_dataguard_associations = TableDynamicLayout.set_fields('Data Guard Associations',
                                                         root_path='data.list_dataguard_association', fields=[
        TextDyField.data_source('Peer database', 'peer_database_id'),
        TextDyField.data_source('Peer DB system', 'peer_db_system_id'),
        EnumDyField.data_source('Peer role', 'peer_role',
                                default_outline_badge=['PRIMARY', 'STANDBY', 'DISABLED_STANDBY']),
        EnumDyField.data_source('Protection Mode', 'protection_mode',
                                default_outline_badge=['MAXIMUM_AVAILABILITY',
                                                       'MAXIMUM_PERFORMANCE', 'MAXIMUM_PROTECTION']),
        EnumDyField.data_source('Transport type', 'transport_type',
                                default_outline_badge=['SYNC', 'ASYNC', 'FASTSYNC']),
        TextDyField.data_source('Apply lag', 'apply_lag'),
        DateTimeDyField.data_source('Launched', 'time_created')
    ])

db_connection_strings_default = ItemDynamicLayout.set_fields('Default',
                                                             root_path='data.connection_strings', fields=[
        TextDyField.data_source('CDB default', 'cdb_default'),
        TextDyField.data_source('CDB IP default', 'cdb_ip_default')
    ])

db_connection_strings_all = TableDynamicLayout.set_fields('Connection Strings',
                                                          'data.connection_strings', fields=[
        TextDyField.data_source('Name', 'key'),
        TextDyField.data_source('Connection String', 'value')
    ])
db_connection_meta = ListDynamicLayout.set_layouts('Connection Strings', [db_connection_strings_default,
                                                                          db_connection_strings_all])

db_tags = TableDynamicLayout.set_fields('Tags', 'data.freeform_tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

db_metadata = CloudServiceMeta.set_layouts([db_base, db_update_history, db_dataguard_associations,
                                            db_connection_meta, db_tags])

'''
Database Software Images
'''
db_image_base = ItemDynamicLayout.set_fields('General Info', fields=[
    TextDyField.data_source('Name', 'data.display_name'),
    TextDyField.data_source('Id', 'data.id'),
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
    TextDyField.data_source('Patch Set', 'data.patch_set'),
    EnumDyField.data_source('Upgrade Supported', 'data.is_upgrade_supported',
                            default_badge={'indigo.500': ['true'], 'coral.600': ['false']}),
    DateTimeDyField.data_source('Created', 'data.time_created')

])

db_image_tags = TableDynamicLayout.set_fields('Tags', 'data.freeform_tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

db_image_metadata = CloudServiceMeta.set_layouts([db_image_base, db_image_tags])

'''
Backup
'''
db_backup_base = TableDynamicLayout.set_fields('General Info', fields=[
    TextDyField.data_source('Id', 'data.id'),
    TextDyField.data_source('Compartment Id', 'data.compartment_id'),
    EnumDyField.data_source('Type', 'data.type',
                            default_outline_badge=['INCREMENTAL', 'FULL', 'VIRTUAL_FULL']),
    TextDyField.data_source('Version', 'data.version'),
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

db_backup_tags = TableDynamicLayout.set_fields('Tags', 'data.freeform_tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

db_backup_metadata = CloudServiceMeta.set_layouts([db_backup_base, db_backup_tags])


class BaremetalVMResource(CloudServiceResource):
    cloud_service_group = StringType(default='BareMetal,VMDatabase')


# DbSystems
class DBSystemsResource(BaremetalVMResource):
    cloud_service_type = StringType(default='DBSystems')
    data = ModelType(DbSystem)
    _metadata = ModelType(CloudServiceMeta, default=dbsystem_metadata, serialized_name='metadata')


class DBSystemResponse(CloudServiceResponse):
    resource = PolyModelType(DBSystemsResource)


# Database
class DatabaseResource(BaremetalVMResource):
    cloud_service_type = StringType(default='Database')
    data = ModelType(Database)
    _metadata = ModelType(CloudServiceMeta, default=db_metadata, serialized_name='metadata')


class DatabaseResponse(CloudServiceResponse):
    resource = PolyModelType(DatabaseResource)


# DatabaseSoftwareImages
class DatabaseSoftwareImagesResource(BaremetalVMResource):
    cloud_service_type = StringType(default='DatabaseSoftwareImages')
    data = ModelType(DatabaseSoftwareImage)
    _metadata = ModelType(CloudServiceMeta, default=db_image_metadata, serialized_name='metadata')


class DatabaseResponse(CloudServiceResponse):
    resource = PolyModelType(DatabaseSoftwareImagesResource)


# Backup
class BackupResource(BaremetalVMResource):
    cloud_service_type = StringType(default='Backup')
    data = ModelType(Backup)
    _metadata = ModelType(CloudServiceMeta, default=db_backup_metadata, serialized_name='metadata')


class BackupResponse(CloudServiceResponse):
    resource = PolyModelType(BackupResource)