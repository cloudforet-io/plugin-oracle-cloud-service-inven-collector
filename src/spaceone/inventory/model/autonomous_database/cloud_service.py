from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.autonomous_database.data import Database
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField,\
                                                                  EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Autonomous Database Information
'''
general_info_meta = ItemDynamicLayout.set_fields('General Information', fields=[
    TextDyField.data_source('Display Name', 'data.display_name'),
    TextDyField.data_source('Workload Type', 'data.db_workload_display'),
    EnumDyField.data_source('Is dedicated', 'data.is_dedicated',
                            default_badge={'indigo.500': ['true'],
                                           'coral.600': ['false'],
                                           }),
    TextDyField.data_source('Region', 'data.region'),
    TextDyField.data_source('Compartment', 'data.compartment_name'),
    TextDyField.data_source('OCID', 'data.id'),
    TextDyField.data_source('OCPU Count', 'data.cpu_core_count'),
    TextDyField.data_source('Storage in GB', 'data.data_storage_size_in_gbs'),
    TextDyField.data_source('License Type', 'data.license_model'),
    TextDyField.data_source('Database version', 'data.db_version'),
    EnumDyField.data_source('Auto Scaling', 'data.is_auto_scaling_enabled',
                            default_badge={'indigo.500': ['true'],
                                           'coral.600': ['false'],
                                           }),
    EnumDyField.data_source('Lifecycle State', 'data.lifecycle_state', default_state={
                                'safe': ['AVAILABLE','AVAILABLE_NEEDS_ATTENTION'],
                                'warning': ['PROVISIONING', 'STOPPING','STARTING','TERMINATING',
                                            'RESTORE_IN_PROGRESS','BACKUP_IN_PROGRESS','SCALE_IN_PROGRESS',
                                            'UPDATING', 'MAINTENANCE_IN_PROGRESS', 'RESTARTING','RECREATING',
                                            'ROLE_CHANGE_IN_PROGRESS', 'UPGRADING'],
                                'alert': ['STOPPED', 'TERMINATED', 'UNAVAILABLE','RESTORE_FAILED','UNKNOWN_ENUM_VALUE']
                            }),
    EnumDyField.data_source('Is Free Tier', 'data.is_free_tier', default_badge={
                                'indigo.500': ['true'],
                                'coral.600': ['false'],
                            }),
    TextDyField.data_source('Open Mode', 'data.open_mode'),
    EnumDyField.data_source('Data Guard Enable', 'data.is_data_guard_enable', default_badge={
                                'indigo.500': ['true'],
                                'coral.600': ['false']
                            }),
    TextDyField.data_source('Service Console URL', 'data.service_console_url'),
    EnumDyField.data_source('Data Safe Status', 'data.data_safe_status', default_state={
                                'safe': ['REGISTERED'],
                                'warning': ['REGISTERING', 'DEREGISTERING'],
                                'alert': ['NOT_REGISTERED', 'FAILED']
                            }),
    TextDyField.data_source('Key Store id', 'data.key_store_id'),
    TextDyField.data_source('Oracle Key Vault Wallet Name', 'data.key_store_wallet_name'),
    DateTimeDyField.data_source('Created', 'data.time_created')
])

network_meta = ItemDynamicLayout.set_fields('Network', fields=[
    TextDyField.data_source('Access Type', 'data.permission_level'),
    ListDyField.data_source('NSG ids', 'data.nsg_ids', options={'delimiter': '<br>'}),
    TextDyField.data_source('Subnet id', 'data.subnet_id'),
    TextDyField.data_source('Private Endpoint', 'data.private_endpoint'),
    TextDyField.data_source('Private Endpoint ip', 'data.private_endpoint_ip'),
    TextDyField.data_source('Private Endpoint Label', 'data.private_endpoint_label')
])

maintenance_meta = ItemDynamicLayout.set_fields('Maintenance', fields=[
    DateTimeDyField.data_source('Next Maintenance Begin', 'data.time_maintenance_begin'),
    DateTimeDyField.data_source('Next Maintenance End', 'data.time_maintenance_end')
])

database_meta = ListDynamicLayout.set_layouts('Autonomous Database Information',
                                              [general_info_meta, network_meta, maintenance_meta])

'''
Connection
'''
connection_string_meta = ItemDynamicLayout.set_fields('Service Console Connection Strings',
                                                      root_path='data.connection_string',
                                                      fields=[TextDyField.data_source('High', 'high'),
                                                              TextDyField.data_source('Medium', 'medium'),
                                                              TextDyField.data_source('Low', 'low')])

connection_url_meta = ItemDynamicLayout.set_fields('Developer Tools Connection URLs',
                                                   root_path='data.connection_urls',
                                                   fields=[TextDyField.data_source('Database Action', 'sql_dev_web_url'),
                                                           TextDyField.data_source('Oracle Application Express',
                                                                                   'apex_url'),
                                                           TextDyField.data_source('Oracle ML User Administration',
                                                                                   'machine_learning_user_management_url')
                                                           ])

connection_meta = ListDynamicLayout.set_layouts('Connection', [connection_string_meta,connection_url_meta])

'''
Backup
'''
backup_meta = TableDynamicLayout.set_fields('Backup',
                                            root_path='data.list_autonomous_backup'
                                            , fields=[TextDyField.data_source('Display Name', 'display_name'),
                                                      EnumDyField.data_source('State','lifecycle_state',
                                                                              default_state={
                                                                                  'safe': ['ACTIVE'],
                                                                                  'warning': ['CREATING','DELETING'],
                                                                                  'alert': ['DELETED', 'FAILED']
                                                                              }),
                                                      EnumDyField.data_source('Type', '_type'),
                                                      EnumDyField.data_source('Automatic', 'is_automatic',
                                                                              default_badge={
                                                                                    'indigo.500': ['true'],
                                                                                    'coral.600': ['false'],
                                                                              }),
                                                      EnumDyField.data_source('Restorable', 'is_restorable',
                                                                              default_badge={
                                                                                  'indigo.500': ['true'],
                                                                                  'coral.600': ['false'],
                                                                              }),
                                                      DateTimeDyField.data_source('Started', 'time_started'),
                                                      DateTimeDyField.data_source('Ended', 'time_ended')
                                                      ])

'''
Refeshable Clones
'''
refresh_clone_meta = \
    TableDynamicLayout.set_fields('Refreshable Clones', root_path='data.list_autonomous_database_clones',
                                  fields=[TextDyField.data_source('Display name', 'display_name'),
                                          TextDyField.data_source('Database name', 'db_name'),
                                          EnumDyField.data_source('Lifecycle State', 'lifecycle_state',
                                                                  default_state={
                                                                    'safe': ['AVAILABLE','AVAILABLE_NEEDS_ATTENTION'],
                                                                    'warning': ['PROVISIONING', 'STOPPING','STARTING',
                                                                                'TERMINATING', 'RESTORE_IN_PROGRESS',
                                                                                'BACKUP_IN_PROGRESS','SCALE_IN_PROGRESS',
                                                                                'UPDATING', 'MAINTENANCE_IN_PROGRESS',
                                                                                'RESTARTING','RECREATING',
                                                                                'ROLE_CHANGE_IN_PROGRESS', 'UPGRADING'],
                                                                    'alert': ['STOPPED', 'TERMINATED', 'UNAVAILABLE',
                                                                              'RESTORE_FAILED','UNKNOWN_ENUM_VALUE']}),
                                          DateTimeDyField.data_source('Last Refresh', 'last_refresh'),
                                          DateTimeDyField.data_source('Refresh Point', 'time_of_last_refresh_point')
                                          ])

# TAB - tags
database_tags = TableDynamicLayout.set_fields('Tags', 'data.freeform_tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

adb_meta = CloudServiceMeta.set_layouts([database_meta,
                                         connection_meta,
                                         backup_meta,
                                         refresh_clone_meta,
                                         database_tags])


class AutonomousDatabaseResource(CloudServiceResource):
    cloud_service_group = StringType(default='AutonomousDatabase')


class DatabaseResource(AutonomousDatabaseResource):
    cloud_service_type = StringType(default='Database')
    data = ModelType(Database)
    _metadata = ModelType(CloudServiceMeta, default=adb_meta, serialized_name='metadata')


class DatabaseResponse(CloudServiceResponse):
    resource = PolyModelType(DatabaseResource)
