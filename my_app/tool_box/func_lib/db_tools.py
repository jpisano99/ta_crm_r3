from my_app.models import *
from my_app.settings import db_config
import hashlib


def create_tables(tbl_name='all'):
    created = False
    if tbl_name == 'all':
        db.create_all()
        print('ALL Tables created')
        created = True
    elif table_exist(tbl_name) is False:
        try:
            eval(tbl_name)
        except NameError:
            print(tbl_name, "Model Not Found - Nothing Created")
            created = False
        else:
            print(tbl_name, "Not Found")
            db_cmd = tbl_name + ".__table__.create(db.session.bind)"
            exec(db_cmd)
            print('CREATED Table:', tbl_name)
            created = True
    elif table_exist(tbl_name) is True:
        print(tbl_name, 'Already Exists')
        created = False
    return created


def drop_tables(tbl_name='all'):
    dropped = False
    if tbl_name == 'all':
        db.drop_all()
        print('ALL Tables deleted')
        dropped = True
    elif table_exist(tbl_name) is True:
        sql = "DROP TABLE "+tbl_name+";"
        db.engine.execute(sql)
        print('DELETED Table:', tbl_name)
        dropped = True
    elif table_exist(tbl_name) is False:
        print(tbl_name, " does NOT exist")
        dropped = False
    return dropped


def table_exist(tbl_name):
    tbl_name = tbl_name.lower()
    sql = "SHOW TABLES;"
    existing_tbls = db.engine.execute(sql)
    tbl_exists = False

    for t_name in existing_tbls:
        if tbl_name == t_name[0]:
            tbl_exists = True
            break
    return tbl_exists


def get_db():
    sql = "SELECT DATABASE();"
    result = db.engine.execute(sql)
    for x in result:
        print('Currently Selected DB:', x[0])
    return x[0]


def switch_db(select_db):
    sql = "SELECT DATABASE();"
    result = db.engine.execute(sql)
    for x in result:
        print('Currently Selected DB:', x[0])

    sql = "USE " + select_db + ";"

    db.engine.execute(sql)
    for x in result:
        print(x[0])

    sql = "SELECT DATABASE();"
    result = db.engine.execute(sql)
    for x in result:
        print(x[0])
    print('Now Selected DB:', x[0])
    return


def create_db(db_name):
    db.engine.execute("CREATE SCHEMA IF NOT EXISTS " + db_name + ";")  # create db
    db.engine.execute("USE " + db_name + ";")  # select new db
    return


def drop_db(db_name):
    # Drop db_name and connect to the default DB
    db.engine.execute("DROP SCHEMA IF EXISTS " + db_name + ";")  # create db
    # db.engine.execute("USE " + db_config['DATABASE'] + ";")  # select new db
    return


def create_row_hash(table_to_hash):
    # Collect the column names we are going to hash
    col_names = []
    print("Hashing ....", table_to_hash)
    for x in eval(table_to_hash).__table__.columns:
        # Don't include these two columns for hashing purposes
        if x.name == 'id' or x.name == 'hash_value' or x.name == 'date_added':
            continue
        else:
            col_names.append(x.name)

    # Loop over the table, create the hash, update the table
    my_table_rows = eval(table_to_hash).query.all()
    for r in my_table_rows:
        row_as_string = ''
        for x in col_names:
            my_cmd = "r." + x
            row_as_string = row_as_string + str(eval(my_cmd))

        hash_val = hashlib.md5(row_as_string.encode('utf-8')).hexdigest()
        r.hash_value = hash_val

    db.session.commit()
    return


# def createdb():
#     #create_database('mysql+pymysql://root:YOUR_PASSWORD@aay9qgi0q2ps45.cp1kaaiuayns.us-east-1.rds.amazonaws.com/cust_ref_db')
#     print('Database created')
