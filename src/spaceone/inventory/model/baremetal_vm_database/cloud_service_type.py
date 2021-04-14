from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField,SearchField, DateTimeDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

'''
DBSystems
'''
cst_bmvm_dbsystems = CloudServiceTypeResource()
cst_bmvm_dbsystems.name = 'DBSystems'
cst_bmvm_dbsystems.provider = 'oracle_cloud'
cst_bmvm_dbsystems.group = 'BareMetal,VMDatabase'
cst_bmvm_dbsystems.labels = ['Database']
cst_bmvm_dbsystems.service_code = 'OracleEnterpriseDatabaseService'
cst_bmvm_dbsystems.is_primary = True
cst_bmvm_dbsystems.is_major = True
cst_bmvm_dbsystems.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/oci/OCI_icon_Database_Service.svg'
}

cst_bmvm_dbsystems._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Display Name', 'data.display_name'),
        EnumDyField.data_source('State', 'data.lifecycle_state', default_state={
            'safe': ['ACTIVE'],
            'warning': ['UPDATING', 'TERMINATING', 'MAINTENANCE_IN_PROGRESS'],
            'alert': ['TERMINATED', 'FAILED', 'MIGRATED', 'NEEDS_ATTENTION']
        }),
        TextDyField.data_source('Availability Domain', 'data.availability_domain'),
        TextDyField.data_source('Shape', 'data.shape'),
        TextDyField.data_source('CPU Core Count', 'data.cpu_core_count'),
        TextDyField.data_source('Version', 'data.version'),
        DateTimeDyField.data_source('Created', 'data.time_created'),
    ],
    search=[
        SearchField.set(name='Display Name', key='data.display_name'),
        SearchField.set(name='State', key='data.lifecycle_state'),
        SearchField.set(name='Availability Domain', key='data.availability_domain'),
        SearchField.set(name='Shape', key='data.shape'),
        SearchField.set(name='CPU Core Count', key='data.cpu_core_count'),
        SearchField.set(name='Version', key='data.version'),
        SearchField.set(name='Created', key='data.time_created', data_type='datetime'),
    ]
)

'''
Database
'''
cst_bmvm_db = CloudServiceTypeResource()
cst_bmvm_db.name = 'Database'
cst_bmvm_db.provider  = 'oracle_cloud'
cst_bmvm_db.group = 'Baremetal,VMDatabase'
cst_bmvm_db.labels = ['Database']
cst_bmvm_db.service_code = 'OracleEnterpriseDatabaseService'
cst_bmvm_db.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/oci/OCI_icon_Database_Service.svg'
}

cst_bmvm_db._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.db_name'),
        EnumDyField.data_source('State', 'data.lifecycle_state', default_state={
                                'safe': ['AVAILABLE'],
                                'warning': ['PROVISIONING', 'UPDATING',
                                            'BACKUP_IN_PROGRESS', 'UPGRADING', 'TERMINATING'],
                                'alert': ['TERMINATED', 'RESTORE_FAILED', 'FAILED']}),
        TextDyField.data_source('Database Unique Name', 'data.db_unique_name'),
        TextDyField.data_source('Workload Type', 'data.db_workload'),
        DateTimeDyField.data_source('Created', 'data.time_created')
    ],
    search=[
        SearchField.set(name='Name', key='data.db_name'),
        SearchField.set(name='State', key='data.lifecycle_state'),
        SearchField.set(name='Database Unique Name', key='data.db_unique_name'),
        SearchField.set(name='Workload Type', key='data.db_workload'),
        SearchField.set(name='Created', key='data.time_created', data_type='datetime')
    ]
)


'''
DatabaseSoftwareImages
'''
cst_bmvm_images = CloudServiceTypeResource()
cst_bmvm_images.name = 'DatabaseSoftwareImages'
cst_bmvm_images.provider = 'oracle_cloud'
cst_bmvm_images.group = 'Baremetal,VMDatabase'
cst_bmvm_images.labels = ['Database']
cst_bmvm_images.service_code = 'OracleEnterpriseDatabaseService'
cst_bmvm_images.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/oci/OCI_icon_Database_Service.svg'
}

cst_bmvm_images._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Display name', 'data.display_name'),
        EnumDyField.data_source('State', 'data.lifecycle_state', default_state={
            'safe': ['AVAILABLE'],
            'warning': ['PROVISIONING', 'DELETING', 'TERMINATING', 'UPDATING'],
            'alert': ['DELETED', 'FAILED', 'TERMINATED']
        }),
        TextDyField.data_source('Shape Family', 'data.image_shape_family'),
        TextDyField.data_source('Database Version', 'data.database_version'),
        DateTimeDyField.data_source('Created', 'data.time_created')
    ],
    search=[
        SearchField.set('Display name', key='data.display_name'),
        SearchField.set('State', 'data.lifecycle_state'),
        SearchField.set('Shape Family', 'data.image_shape_family'),
        SearchField.set('Database Version', 'data.database_version'),
        SearchField.set('Created', 'data.time_created')
    ]
)

'''
Backup
'''
cst_bmvm_backup = CloudServiceTypeResource()
cst_bmvm_backup.name = 'Backup'
cst_bmvm_backup.provider = 'oracle_cloud'
cst_bmvm_backup.group = 'Baremetal,VMDatabase'
cst_bmvm_backup.labels = ['Database']
cst_bmvm_backup.service_code = 'OracleEnterpriseDatabaseService'
cst_bmvm_backup.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/oci/OCI_icon_Database_Service.svg'
}

cst_bmvm_images._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Display Name', 'data.display_name'),
        EnumDyField.data_source('State', 'data.lifecycle_state', default_state={
            'safe': ['ACTIVE'],
            'warning': ['CREATING', 'DELETING', 'RESTORING'],
            'alert': ['DELETED', 'FAILED']
        }),
        TextDyField.data_source('Availability Domain', 'data.availability_domain'),
        DateTimeDyField.data_source('Started', 'data.time_started'),
        DateTimeDyField.data_source('Ended', 'data.time_ended')
    ],
    search=[
        SearchField.set(name='Display Name', key='data.display_name'),
        SearchField.set(name='State', key='data.lifecycle_state'),
        SearchField.set(name='Availability Domain', key='data.availability_domain'),
        SearchField.set(name='Stated', key='data.time_started', data_type='datetime'),
        SearchField.set(name='Ended', key='data.time_ended', data_type='datetime')
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_bmvm_dbsystems}),
    CloudServiceTypeResponse({'resource': cst_bmvm_db}),
    CloudServiceTypeResponse({'resource': cst_bmvm_images}),
    CloudServiceTypeResponse({'resource': cst_bmvm_backup})
]
