from my_app.settings import db_config
from my_app import db

table_name = "bookings"

sql = "SELECT DISTINCT `end_customer_global_ultimate_id` FROM " + \
      "`" + db_config['DATABASE'] + "`.`" + table_name + "`"
sql_results = db.engine.execute(sql)

for x in sql_results:
    print(x[0])

sql = "SELECT DISTINCT `erp_end_customer_name` FROM " + \
      "`" + db_config['DATABASE'] + "`.`" + table_name + "`"
sql_results = db.engine.execute(sql)
for x in sql_results:
    print(x[0])

# print(len(sql_results))
