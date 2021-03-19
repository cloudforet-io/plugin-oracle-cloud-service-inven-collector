from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField,SearchField, DateTimeDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_adb = CloudServiceTypeResource()
cst_adb.name = 'Database'
cst_adb.provider = 'oracle_cloud'
cst_adb.group = 'AutonomousDatabase'
cst_adb.labels = ['database']
cst_adb.service_code = 'OracleAutonomousDatabase'
cst_adb.is_primary = True
cst_adb.is_major = True
cst_adb.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/oci/OCI_icon_Autonomous.svg'
}

cst_adb._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Display Name', 'data.display_name'),
        EnumDyField.data_source('State', 'data.lifecycle_state',
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
        EnumDyField.data_source('Dedicated', 'data.is_dedicated', default_badge={
                                                                    'indigo.500': ['true'],
                                                                    'coral.600': ['false'], }),
        TextDyField.data_source('OCPUs', 'data.cpu_core_count'),
        SizeField.data_source('Storage', 'data.size'),
        TextDyField.data_source('Workload Type', 'data.db_workload_display'),
        EnumDyField.data_source('Autonomous Data Guard', 'data.is_data_guard_enable',
                                default_badge={
                                    'indigo.500': ['true'],
                                    'coral.600': ['false']
                                }),
        DateTimeDyField.data_source('Created', 'data.time_created'),
    ],
    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Display Name', key='data.display_name'),
        SearchField.set(name='Compartment', key='data.compartment_name'),
        SearchField.set(name='Region', key='data.region'),
        SearchField.set(name='State', key='data.lifecycle_state'),
        SearchField.set(name='Workload Type', key='data.db_workload_display'),
        SearchField.set(name='Creation time', key='data.time_created', data_type='datetime')
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_adb})
]
