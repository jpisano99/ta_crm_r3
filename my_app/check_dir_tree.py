import os
from my_app.settings import app_cfg


def check_dir_tree():
    print()
    print('Directory Tree Structure')
    print('\tHOME DIRECTORY:', app_cfg['HOME'])
    print('\tMOUNT POINT:', app_cfg['MOUNT_POINT'])
    print('\tAPPLICATION DIRECTORY:', app_cfg['MY_APP_DIR'])
    print('\tWORKING SUB DIRECTORY:', app_cfg['WORKING_SUB_DIR'])
    print('\tUPDATES SUB DIRECTORY:', app_cfg['UPDATES_SUB_DIR'])
    print('\tARCHIVES SUB DIRECTORY:', app_cfg['ARCHIVES_SUB_DIR'])
    print()
    print('\tDirectories in my HOME Dir', os.listdir(app_cfg["HOME"]))
    print()

    # Check the mount point and path to app main directory
    path_to_main_app = os.path.join(app_cfg['HOME'], app_cfg['MOUNT_POINT'])
    do_it(path_to_main_app)
    path_to_main_app = os.path.join(path_to_main_app, app_cfg['MY_APP_DIR'])
    do_it(path_to_main_app)

    # Now check the sub directories for this app
    path_to_check = os.path.join(path_to_main_app, app_cfg['WORKING_SUB_DIR'])
    do_it(path_to_check)
    path_to_check = os.path.join(path_to_main_app, app_cfg['UPDATES_SUB_DIR'])
    do_it(path_to_check)
    path_to_check = os.path.join(path_to_main_app, app_cfg['ARCHIVES_SUB_DIR'])
    do_it(path_to_check)
    return


def do_it(tmp_path):
    if os.path.exists(tmp_path) is False:
        os.mkdir(tmp_path)
        print('\tCREATED:', tmp_path)
    else:
        print('\tDirectory already exists:', tmp_path)
    return
