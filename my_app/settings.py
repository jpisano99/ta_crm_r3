from my_app.my_secrets import passwords
import os


# application predefined constants
app_cfg = dict(
    # RUNTIME_ENV='AWS',
    RUNTIME_ENV='LOCAL',
    # RUNTIME_ENV='PYTHONANYWHERE',

    VERSION=1.0,
    GITHUB="{url}",
    HOME=os.path.expanduser("~"),
    MOUNT_POINT='my_app_data',
    MY_APP_DIR='ta_adoption',
    WORKING_SUB_DIR='app_work',
    UPDATES_SUB_DIR='app_updates 02-03-20',
    ARCHIVES_SUB_DIR='app_archives',
    PROD_DATE='',
    UPDATE_DATE='',
    META_DATA_FILE='config_data.json',

    # Raw Data Files to ingest
    RAW_SUBSCRIPTIONS='TA Master Subscriptions as of',
    RAW_ENT_AGREEMENTS='TA Enterprise Subscriptions as of',
    RAW_PRODUCT_BOOKINGS='TA Product Bookings with SO as of',
    RAW_SERVICES_BOOKINGS='TA Services Bookings with SO as of',
    RAW_TA_AS_FIXED_SKU='TA AS Delivery Status as of',
    RAW_TELEMETRY_DR='TA SPOCK_sensor_sum as of',
    RAW_TELEMETRY_NON_DR='TA STROM_sensor_sum as of',
    RAW_SAAS_TRACKING='TA SaaS Customer Tracking as of',

    # Scrubbed Data Working Files
    XLS_SUBSCRIPTIONS='tmp_Master Subscriptions.xlsx',
    XLS_AS_DELIVERY_STATUS='tmp_AS Delivery.xlsx',
    XLS_BOOKINGS='tmp_TA Master Bookings.xlsx',
    XLS_AS_SKUS='tmp_TA AS SKUs.xlsx',
    XLS_CUSTOMER='tmp_TA Customer List.xlsx',
    XLS_DASHBOARD='tmp_TA Unified Adoption Dashboard.xlsx',
    XLS_TELEMETRY='tmp_TA_telemetry.xlsx',

    #
    # Testing
    #

    XLS_UNIQUE_CUSTOMERS='tmp_unique_customer_names.xlsx',
    XLS_EN_AGREEMENTS = 'TA Enterprise Agreements as of 02-03-20.xlsx',

    # SmartSheet Sheets and Names
    SS_SAAS='SaaS customer tracking',
    SS_CX='CX Tetration Customer Comments v3.0',
    SS_AS='Tetration Shipping Notification & Invoicing Status',
    SS_COVERAGE='Tetration Coverage Map',
    SS_SKU='Tetration SKUs',
    SS_CUSTOMERS='TA Customer List',
    SS_DASHBOARD='TA Unified Adoption Dashboard',
    SS_WORKSPACE='Tetration Customer Adoption Workspace',
)

# database configuration settings
# selected via the app_cfg['RUNTIME_ENV'] setting
if app_cfg['RUNTIME_ENV'] == 'AWS':
    # This is for a AWS based SQL db
    db_config = dict(
        DATABASE="test_db",
        USER="admin",
        PASSWORD=passwords["DB_PASSWORD"],
        HOST="database-1.cp1kaaiuayns.us-east-1.rds.amazonaws.com"
    )
elif app_cfg['RUNTIME_ENV'] == 'PYTHONANYWHERE':
    # This is for PythonAnywhere based SQL db
    db_config = dict(
        DATABASE="jpisano$test_db",
        USER="jpisano",
        PASSWORD=passwords["DB_PASSWORD"],
        HOST="jpisano.mysql.pythonanywhere-services.com"
    )
elif app_cfg['RUNTIME_ENV'] == 'LOCAL':
    # This is for a local based SQL db
    db_config = dict(
        DATABASE="ta_adoption_db",
        USER="root",
        PASSWORD=passwords["DB_PASSWORD"],
        HOST="localhost"
    )

# Smart sheet Config settings
ss_token = dict(
    SS_TOKEN=passwords["SS_TOKEN"]
)

