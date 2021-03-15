# plugin-oracle-cloud-services

![OCI](https://user-images.githubusercontent.com/44199159/111094011-a4f72a80-857d-11eb-929f-b55433eddcae.png)

**Plugin for OCI (Oracle Cloud Infrastructure)**
> SpaceONE's [plugin-oracle-cloud-services](https://github.com/spaceone-dev/plugin-oracle-cloud-services)
> is a convenient tool to get cloud services data from Oracle Cloud Infrastructure. 

Find us also at [Dockerhub]()
> Latest stable version : 1.0

Please contact us if you need any further information. <support@spaceone.dev>




## Authentication Overview

--- 


Registered service account on SpaceONE must have certain permissions to collect cloud service data Please, set authentication privilege for followings:



### Contents
- Table of Contents
  - [Database](#Database)
    - [AutonomousDatabase](#AutonomousDatabase)
    
--- 

#### [Database](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/database/client/oci.database.DatabaseClient.html#oci.database.DatabaseClient.list_autonomous_databases)

 - ##### AutonomousDatabase

    - Scopes
       *  https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm
       *  https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/identity/client/oci.identity.IdentityClient.html#oci.identity.IdentityClient.list_compartments
       *  https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/identity/client/oci.identity.IdentityClient.html#oci.identity.IdentityClient.list_region_subscriptions   
       *  https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/database/client/oci.database.DatabaseClient.html#oci.database.DatabaseClient.list_autonomous_databases
       *  https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/database/client/oci.database.DatabaseClient.html#oci.database.DatabaseClient.list_autonomous_database_backups
       *  https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/database/client/oci.database.DatabaseClient.html#oci.database.DatabaseClient.list_autonomous_database_clones
    
    - IAM 
        * Allow group ListDBSystemGroup to inspect compartments in tenancy
        * Allow group ListDBSystemGroup to inspect tenancies in tenancy
        * Allow group ListDBSystemGroup to inspect db-systems in tenancy


    
    

