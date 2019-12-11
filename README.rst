This is a template for a basic Flask based app
It supports LOCAL execution, AWS and PythonAnywhere deployments
It supports a local MySQL db, PythonAnywhere db or RDS (AWS) db

Simply change the settings.py file:
    # application predefined constants
    app_cfg = dict(
        RUNTIME_ENV='AWS',
        # RUNTIME_ENV='LOCAL',
        # RUNTIME_ENV='PYTHONANYWHERE',

