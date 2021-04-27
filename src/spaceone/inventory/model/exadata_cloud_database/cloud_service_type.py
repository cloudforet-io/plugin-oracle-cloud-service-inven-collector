from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField,SearchField, DateTimeDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

'''
ExadataInfrastructure
'''
cst_exadata_infrastructure = CloudServiceTypeResource()
cst_exadata_infrastructure.name = 'ExadataInfrastructure'
cst_exadata_infrastructure.provider = 'oracle_cloud'
cst_exadata_infrastructure.group = 'ExadataCloudDatabase'
cst_exadata_infrastructure.labels = ['Database']
cst_exadata_infrastructure.service_code = 'OracleExadataCloudService'
cst_exadata_infrastructure.is_primary = True
cst_exadata_infrastructure.is_major = True
cst_exadata_infrastructure.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/oci/OCI_icon_Database_Service.svg'
}

cst_exadata_infrastructure._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Display Name', 'data.display_name'),
        EnumDyField.data_source('Lifecycle State', 'data.lifecycle_state', default_state={
            'safe': ['AVAILABLE'],
            'warning': ['UPDATING', 'TERMINATING', 'MAINTENANCE_IN_PROGRESS'],
            'alert': ['TERMINATED', 'FAILED']
        }),
        TextDyField.data_source('Availability Domain', 'data.availability_domain'),
        TextDyField.data_source('Compartment', 'data.compartment_name'),
        TextDyField.data_source('Shape', 'data.shape'),
        TextDyField.data_source('Version', 'data.version'),
        SizeField.data_source('Available Storage Size', 'data.available_storage_size_in_gbs', options={
            'display_unit': 'GB',
            'source_unit': 'GB'
        }),
        DateTimeDyField.data_source('Created', 'data.time_created')
    ],
    search=[
        SearchField.set(name='Display Name', key='data.display_name'),
        SearchField.set(name='Lifecycle State', key='data.lifecycle_state'),
        SearchField.set(name='Availability Domain', key='data.availability_domain'),
        SearchField.set(name='Compartment', key='data.compartment_name'),
        SearchField.set(name='Shape', key='data.shape'),
        SearchField.set(name='Version', key='data.version'),
        SearchField.set(name='Available Storage Size', key='data.available_storage_size_in_gbs'),
        SearchField.set(name='Created', key='data.time_created', data_type='datetime')
    ]
)

'''
ExadataVMCluster
'''
cst_exadata_vm_cluster = CloudServiceTypeResource()
cst_exadata_vm_cluster.name = 'ExadataVMCluster'
cst_exadata_vm_cluster.provider = 'oracle_cloud'
cst_exadata_vm_cluster.group = 'ExadataCloudDatabase'
cst_exadata_vm_cluster.labels = ['Database']
cst_exadata_vm_cluster.service_code = 'OracleExadataCloudService'
cst_exadata_vm_cluster.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/oci/OCI_icon_Database_Service.svg'
}

cst_exadata_vm_cluster._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Display Name', 'data.display_name'),
        TextDyField.data_source('Cluster Name', 'data.cluster_name'),
        EnumDyField.data_source('State', 'lifecycle_state', default_state={
            'safe': ['AVAILABLE'],
            'warning': ['PROVISIONING', 'UPDATING',
                        'TERMINATING','MAINTENANCE_IN_PROGRESS'],
            'alert': ['TERMINATED', 'FAILED']
        }),
        TextDyField.data_source('Availability Domain', 'data.availability_domain'),
        TextDyField.data_source('Compartment', 'data.compartment_name'),
        TextDyField.data_source('Shape', 'data.shape'),
        TextDyField.data_source('CPU Core Count', 'data.cpu_core_count'),
        SizeField.data_source('Storage Size','data.storage_size_in_gbs', options={
            'display_unit': 'GB',
            'source_unit': 'GB'
        }),
        TextDyField.data_source('System Version', 'data.system_version'),
        DateTimeDyField.data_source('Created', 'data.time_created')
    ],
    search=[
        SearchField.set(name='Display Name', key='data.display_name'),
        SearchField.set(name='Cluster Name', key='data.cluster_name'),
        SearchField.set(name='State', key='lifecycle_state'),
        SearchField.set(name='Availability Domain', key='data.availability_domain'),
        SearchField.set(name='Compartment', key='data.compartment_name'),
        SearchField.set(name='Shape', key='data.shape'),
        SearchField.set(name='CPU Core Count', key='data.cpu_core_count'),
        SearchField.set(name='System Version', key='data.system_version'),
        SearchField.set(name='Created', key='data.time_created', data_type='datetime'),
    ]
)

'''
Database
'''
cst_vm_database = CloudServiceTypeResource()
cst_vm_database.name = 'Database'
cst_vm_database.provider = 'oracle_cloud'
cst_vm_database.group = 'ExadataCloudDatabase'
cst_vm_database.labels = ['Database']
cst_vm_database.service_code = 'OracleExadataCloudService'
cst_vm_database.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/oci/OCI_icon_Database_Service.svg'
}

cst_vm_database._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.db_name'),
        EnumDyField.data_source('State', 'data.lifecycle_state', default_state={
                                'safe': ['AVAILABLE'],
                                'warning': ['PROVISIONING', 'UPDATING',
                                            'BACKUP_IN_PROGRESS', 'UPGRADING', 'TERMINATING'],
                                'alert': ['TERMINATED', 'RESTORE_FAILED', 'FAILED']}),
        TextDyField.data_source('Database Unique Name', 'data.db_unique_name'),
        TextDyField.data_source('Version', 'data.db_version'),
        TextDyField.data_source('Workload Type', 'data.db_workload'),
        DateTimeDyField.data_source('Created', 'data.time_created')
    ],
    search=[
        SearchField.set(name='Name', key='data.db_name'),
        SearchField.set(name='State', key='data.lifecycle_state'),
        SearchField.set(name='Database Unique Name', key='data.db_unique_name'),
        SearchField.set(name='Version', key='data.db_version'),
        SearchField.set(name='Workload Type', key='data.db_workload'),
        SearchField.set(name='Created', key='data.time_created', data_type='datetime')
    ]
)

'''
DatabaseSoftwareImage
'''
cst_exadata_image = CloudServiceTypeResource()
cst_exadata_image.name = 'DatabaseSoftwareImage'
cst_exadata_image.provider = 'oracle_cloud'
cst_exadata_image.group = 'ExadataCloudDatabase'
cst_exadata_image.labels = ['Database']
cst_exadata_image.service_code = 'OracleExadataCloudService'
cst_exadata_image.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/oci/OCI_icon_Database_Service.svg'
}

cst_vm_database._metadata = CloudServiceTypeMeta.set_meta(
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
cst_exadata_backup = CloudServiceTypeResource()
cst_exadata_backup.name = 'Backup'
cst_exadata_backup.provider = 'oracle_cloud'
cst_exadata_backup.group = 'ExadataCloudDatabase'
cst_exadata_backup.labels = ['Database']
cst_exadata_backup.service_code = 'OracleExadataCloudService'
cst_exadata_image.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/oci/OCI_icon_Database_Service.svg'
}

cst_exadata_backup._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Display Name', 'data.display_name'),
        EnumDyField.data_source('State', 'data.lifecycle_state', default_state={
            'safe': ['ACTIVE'],
            'warning': ['CREATING', 'DELETING', 'RESTORING'],
            'alert': ['DELETED', 'FAILED']
        }),
        TextDyField.data_source('Compartment', 'data.compartment_name'),
        TextDyField.data_source('Availability Domain', 'data.availability_domain'),
        DateTimeDyField.data_source('Started', 'data.time_started'),
        DateTimeDyField.data_source('Ended', 'data.time_ended')
    ],
    search=[
        SearchField.set(name='Display Name', key='data.display_name'),
        SearchField.set(name='State', key='data.lifecycle_state'),
        SearchField.set(name='Source DB ID', key='data.database_id'),
        SearchField.set(name='Availability Domain', key='data.availability_domain'),
        SearchField.set(name='Stated', key='data.time_started', data_type='datetime'),
        SearchField.set(name='Ended', key='data.time_ended', data_type='datetime')
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_exadata_infrastructure}),
    CloudServiceTypeResponse({'resource': cst_exadata_vm_cluster}),
    CloudServiceTypeResponse({'resource': cst_vm_database}),
    CloudServiceTypeResponse({'resource': cst_exadata_image}),
    CloudServiceTypeResponse({'resource': cst_exadata_backup})
]






