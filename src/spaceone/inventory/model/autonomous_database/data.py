from schematics import Model
from schematics.types import ModelType, ListType, StringType,\
                             FloatType, DateTimeType, IntType, \
                             BooleanType


class Tags(Model):
    key = StringType()
    value = StringType()


class ApexDetails(Model):
    apex_version = StringType(deserialize_from='_apex_version')
    ords_version = StringType(deserialize_from='_ords_version')


class BackupConfig(Model):
    manual_backup_bucket_name = StringType(deserialize_from='_manual_backup_bucket_name', serialize_when_none=False)
    manual_backup_type = StringType(deserialize_from='_manual_backup_type', serialize_when_none=False)


class ConnectionString(Model):
    dedicated = StringType(deserialize_from='_dedicated', serialize_when_none=False)
    high = StringType(deserialize_from='_high')
    low = StringType(deserialize_from='_low')
    medium = StringType(deserialize_from='_medium')


class ConnectionUrls(Model):
    apex_url = StringType(deserialize_from='_apex_url')
    machine_learning_user_management_url = StringType(deserialize_from='_machine_learning_user_management_url')
    sql_dev_web_url = StringType(deserialize_from='_sql_dev_web_url')


class Define_tags(Model):
    define_tags = ModelType(Tags)
    pass


class Autonomous_Backup(Model):
    autonomous_id = StringType(deserialize_from='_autonomous_id')
    compartment_id = StringType(deserialize_from='_compartment_id', serialize_when_none=False)
    database_size_in_tbs = FloatType(deserialize_from='_database_size_in_tbs')
    display_name = StringType(deserialize_from='_display_name')
    id = StringType(deserialize_from='_id')
    is_automatic = BooleanType(deserialize_from='_is_automatic')
    is_restorable = BooleanType(deserialize_from='_is_restorable', serialize_when_none=False)
    key_store_id = StringType(deserialize_from='_key_store_id', serialize_when_none=False)
    key_store_wallet_name = StringType(deserialize_from='_key_store_wallet_name', serialize_when_none=False)
    lifecycle_details = StringType(deserialize_from='_lifecycle_details')
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                 choices=('CREATING', 'ACTIVE', 'DELETING',
                                          'DELETED', 'FAILED', 'UNKNOWN_ENUM_VALUE'))
    time_ended = DateTimeType(deserialize_from='_time_ended')
    time_started = DateTimeType(deserialize_from='_time_started')
    _type = StringType(deserialize_from='_type')


class Autonomous_database_clones(Model):
    display_name = StringType(deserialize_from='_display_name')
    db_name = StringType(deserialize_from='_db_name')
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                   choices=('PROVISIONING', 'AVAILABLE', 'STOPPING', 'STOPPED', 'STARTING',
                                            'TERMINATING', 'TERMINATED', 'UNAVAILABLE', 'RESTORE_IN_PROGRESS',
                                            'RESTORE_FAILED', 'BACKUP_IN_PROGRESS', 'SCALE_IN_PROGRESS',
                                            'AVAILABLE_NEEDS_ATTENTION', 'UPDATING', 'MAINTENANCE_IN_PROGRESS',
                                            'RESTARTING', 'RECREATING', 'ROLE_CHANGE_IN_PROGRESS', 'UPGRADING',
                                            'UNKNOWN_ENUM_VALUE'))
    last_refresh = DateTimeType(deserialize_from='_time_of_last_refresh')
    time_of_last_refresh_point = DateTimeType(deserialize_from='_time_of_last_refresh_point')


class Database(Model):
    compartment_name = StringType(deserialize_from='compartment_name')
    region = StringType(deserialize_from='region')
    compartment_id = StringType(deserialize_from='_compartment_id')
    id = StringType(deserialize_from='_id')
    apex_details = ModelType(ApexDetails, deserialize_from='_apex_details')
    are_primary_whitelisted_ips_used = StringType(deserialize_from='_are_primary_whitelisted_ips_used',
                                                  serialize_when_none=False)
    autonomous_container_database_id = StringType(deserialize_from='_autonomous_container_database_id',
                                                  serialize_when_none=False)
    available_upgrade_version = ListType(StringType(), deserialize_from='_available_upgrade_versions', default=[])
    backup_config = ModelType(BackupConfig, deserialize_from='_backup_config')
    connection_string = ModelType(ConnectionString, deserialize_from='_connection_strings')
    connection_urls = ModelType(ConnectionUrls, deserialize_from='_connection_urls')
    cpu_core_count = IntType(deserialize_from='_cpu_core_count')
    data_safe_status = StringType(deserialize_from='_data_safe_status',
                                  choices=( 'REGISTERING', 'REGISTERED',
                                            'DEREGISTERING', 'NOT_REGISTERED',
                                            'FAILED', 'UNKNOWN_ENUM_VALUE'))
    data_storage_size_in_gbs = IntType(deserialize_from='_data_storage_size_in_gbs')
    data_storage_size_in_tbs = FloatType(deserialize_from='_data_storage_size_in_tbs')
    size = IntType(deserialize_from='size')
    db_name = StringType(deserialize_from='_db_name')
    db_version = StringType(deserialize_from='_db_version')
    db_workload = StringType(deserialize_from='_db_workload')
    db_workload_display = StringType(serialize_when_none=False)
    #define_tags = ListType(ModelType(Define_tags), deserialize_from='_defined_tags', default=[])
    display_name = StringType(deserialize_from='_display_name')
    failed_data_recovery_in_seconds = IntType(deserialize_from='_failed_data_recovery_in_seconds',
                                              serialize_when_none=False)
    freeform_tags = ListType(ModelType(Tags), deserialize_from='_freeform_tags', default=[])
    infrastructure_type = StringType(deserialize_from='_infrastructure_type',
                                     choices=('CLOUD', 'CLOUD_AT_CUSTOMER', 'UNKNOWN_ENUM_VALUE'))
    is_access_control_enabled = BooleanType(deserialize_from='_is_access_control_enabled')
    is_auto_scaling_enabled = BooleanType(deserialize_from='_is_auto_scaling_enabled')
    is_data_guard_enable = BooleanType(deserialize_from='_is_data_guard_enabled')
    is_dedicated = BooleanType(deserialize_from='_is_dedicated')
    is_free_tier = BooleanType(deserialize_from='_is_free_tier')
    is_preview = BooleanType(deserialize_from='_is_preview')
    is_refreshable_clone = BooleanType(deserialize_from='_is_refreshable_clone', serialize_when_none=False)
    key_store_id = StringType(deserialize_from='_key_store_id', serialize_when_none=False)
    key_store_wallet_name = StringType(deserialize_from='_key_store_wallet_name', serialize_when_none=False)
    license_model = StringType(deserialize_from='_license_model')
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                   choices=('PROVISIONING', 'AVAILABLE', 'STOPPING', 'STOPPED', 'STARTING',
                                            'TERMINATING', 'TERMINATED', 'UNAVAILABLE', 'RESTORE_IN_PROGRESS',
                                            'RESTORE_FAILED', 'BACKUP_IN_PROGRESS', 'SCALE_IN_PROGRESS',
                                            'AVAILABLE_NEEDS_ATTENTION', 'UPDATING', 'MAINTENANCE_IN_PROGRESS',
                                            'RESTARTING', 'RECREATING', 'ROLE_CHANGE_IN_PROGRESS', 'UPGRADING',
                                            'UNKNOWN_ENUM_VALUE'))
    lifecycle_details = StringType(deserialize_from='_lifecycle_details', serialize_when_none=False)
    nsg_ids = ListType(StringType(), deserialize_from='_nsg_ids', serialize_when_none=False)
    open_mode = StringType(deserialize_from='_open_mode', choices=('READ_ONLY', 'READ_WRITE', 'UNKNOWN_ENUM_VALUE'))
    operations_insights_status = StringType(deserialize_from='_operations_insights_status',
                                            choices=('ENABLING', 'ENABLED', 'DISABLING', 'NOT_ENABLED',
                                                     'FAILED_ENABLING', 'FAILED_DISABLING', 'UNKNOWN_ENUM_VALUE'))
    permission_level = StringType(deserialize_from='_permission_level')
    private_endpoint = StringType(deserialize_from='_private_endpoint', serialize_when_none=False)
    private_endpoint_ip = StringType(deserialize_from='_private_endpoint_ip', serialize_when_none=False)
    private_endpoint_label = StringType(deserialize_from='_private_endpoint_label', serialize_when_none=False)
    refreshable_mode = StringType(deserialize_from='_refreshable_mode', choices=('AUTOMATIC', 'MANUAL',
                                                                                 'UNKNOWN_ENUM_VALUE'))
    refreshable_status = StringType(deserialize_from='_refreshable_status', choices=('REFRESHING', 'NOT_REFRESHING'))
    role = StringType(deserialize_from='_role', choices=('PRIMARY', 'STANDBY', 'DISABLED_STANDBY',
                                                         'UNKNOWN_ENUM_VALUE'), serialize_when_none=False)
    service_console_url = StringType(deserialize_from='_service_console_url')
    source_id = StringType(deserialize_from='_source_id', serialize_when_none=False)
    standby_whitelisted_ips = ListType(StringType(), deserialize_from='_standby_whitelisted_ips',
                                       serialize_when_none=False)
    subnet_id = StringType(deserialize_from='_subnet_id', serialize_when_none=False)
    #system_tags = ModelType(Define_tags, deserialize_from='_system_tags')
    time_created = DateTimeType(deserialize_from='_time_created')
    time_deletion_of_free_autonomous_database = DateTimeType(deserialize_from=
                                                             'time_deletion_of_free_autonomous_database')
    time_maintenance_begin = DateTimeType(deserialize_from='_time_maintenance_begin')
    time_maintenance_end = DateTimeType(deserialize_from='_time_maintenance_end')
    time_of_last_failover = DateTimeType(deserialize_from='_time_of_last_failover', serialize_when_none=False)
    time_of_last_refresh = DateTimeType(deserialize_from='_time_of_last_refresh', serialize_when_none=False)
    time_of_last_refresh_point = DateTimeType(deserialize_from='_time_of_last_refresh_point', serialize_when_none=False)
    time_of_last_switchover = DateTimeType(deserialize_from='_time_of_last_switchover', serialize_when_none=False)
    time_of_next_refresh = DateTimeType(deserialize_from='_time_of_next_refresh', serialize_when_none=False)
    time_reclamation_of_free_autonomous_database = DateTimeType(deserialize_from=
                                                                '_time_reclamation_of_free_autonomous_database')
    used_data_storage_size_in_tbs = IntType(deserialize_from='_used_data_storage_size_in_tbs')
    whitelisted_ips = ListType(StringType(),deserialize_from='_whitelisted_ips', serialize_when_none=False)
    list_autonomous_backup = ListType(ModelType(Autonomous_Backup), default=[])
    list_autonomous_database_clones = ListType(ModelType(Autonomous_database_clones), default=[])

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://cloud.oracle.com/db/adb/{self.id}?region={self.region}",
        }
