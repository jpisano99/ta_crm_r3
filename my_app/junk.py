from my_app.settings import db_config
from sqlalchemy import desc, asc
import my_app.tool_box as tool
from my_app import db
from my_app.models import Bookings, Customer_Ids, Customer_Aliases, Sales_Orders, BookingsSchema
import time
from flask import jsonify

jim = {}
id = 123
id2 = 345

cust_data = {}
erp_name_list = {}

cust_data['global_names'] = [1,2,3]
cust_data['erp_names'] = [10,20,30]
cust_data['so_nums'] = ['AA','BB','CC']
cust_data['web_ids'] = ['ZZ','XX','YY']

jim[id] = cust_data
jim[id2] = cust_data

print (jim)
exit()


jim = 'BUNDESRECHENZENTRUM GESELLSCHAFT MIT BESCHRÃƒÃ—NKTER HAFTUNG'
print(len(jim))
jim = ['a','g','h']
if 'w' in jim:
    print('hello')

exit()


# tool.create_tables("Customer_Ids")
tool.drop_tables("Sales_Orders")
tool.create_tables("Sales_Orders")
# tool.create_tables("Bookings_New")


# tool.drop_tables("Bookings")

# tool.drop_tables("Customer_Ids")


exit()

#
# table_name = "bookings"
#
# tool.drop_tables("Customers")
# tool.create_tables("Customers")
#
# tool.drop_tables("Customer_Names")
# tool.create_tables("Customer_Names")
#
# tool.drop_tables("Orders")
# tool.create_tables("Orders")

#
# Scrub Raw Bookings Table of Invalid Data
#

# kwargs = {'end_customer_global_ultimate_id': '-999',
#           'erp_sales_order_number': '-7777',
#           'erp_end_customer_name' : 'UNKNOWN'}
# my_bookings = Bookings.query.filter_by(**kwargs).delete()
# print(my_bookings)
# db.session.commit()

my_bookings = Bookings.query.filter(Bookings.end_customer_global_ultimate_id == "-999").\
                filter(Bookings.erp_end_customer_name != "-UNKNOWN").all()

# jim = Bookings.query.first()
# # print(jsonify(jim))
# bookings_schema = BookingsSchema()
# output = bookings_schema.dump(jim)
# print(output)
#
#
# # print(jsonify(output))
# exit()


stan = db.engine.execute("SHOW COLUMNS FROM `bookings`;")
for i in stan:
    print(i[0])

print(len(my_bookings))
names_with_no_id = {}
for x in my_bookings:
    # print(x.erp_end_customer_name, x.end_customer_global_ultimate_id)
    names_with_no_id[x.erp_end_customer_name] = x.end_customer_global_ultimate_id
    print(x.sales_agent_name)

print(len(names_with_no_id))
print(names_with_no_id)
time.sleep(.5)
exit()



# db.session.delete(my_bookings)

# my_bookings = Bookings.query.filter_by(end_customer_global_ultimate_id="-999").all()

# my_bookings = Bookings.query.filter_by(end_customer_global_ultimate_id="-999").\
#             filter_by(erp_sales_order_number="-7777").\
#             filter_by(erp_end_customer_name='UNKNOWN').all()

# print(len(my_bookings))
exit()

#
# Create Customer ID Table
#
# table_name = 'bookings'
sql = "INSERT INTO `customers` (`end_customer_global_ultimate_id`) " + \
      "SELECT DISTINCT `end_customer_global_ultimate_id` FROM " +\
      "`" + db_config['DATABASE'] + "`.`" + table_name + "`"
sql_results = db.engine.execute(sql)
# print(dir(sql_results))
# print(sql_results.fetchone())
# print(sql_results.lastrowid)
print("Loaded Customers:", sql_results.rowcount, ' rows')



#
# Create Customer Names Table
#
table_name = 'bookings'
sql = "INSERT INTO `customer_names` (`erp_end_customer_name`, `end_customer_global_ultimate_id`) " + \
      "SELECT DISTINCT `erp_end_customer_name`, `end_customer_global_ultimate_id` FROM " +\
      "`" + db_config['DATABASE'] + "`.`" + table_name + "`"
sql_results = db.engine.execute(sql)
print("Loaded Customer_Names:", sql_results.rowcount, ' rows')


# Customer Orders
table_name = 'bookings'
sql = "INSERT INTO `orders` (`erp_sales_order_number`, `end_customer_global_ultimate_id`) " + \
      "SELECT DISTINCT `erp_sales_order_number`, `end_customer_global_ultimate_id` FROM " +\
      "`" + db_config['DATABASE'] + "`.`" + table_name + "`"

sql_results = db.engine.execute(sql)
print("Loaded Customer Unique Order Numbers:", sql_results.rowcount)

#
# Build Customer View (ID, Aliases, Orders, Items)
#
cust_id_recs = Customers.query.order_by(asc(Customers.end_customer_global_ultimate_id)).all()

for cust_id_rec in cust_id_recs:
    cust_id = cust_id_rec.end_customer_global_ultimate_id
    if cust_id == '-999':
        continue

    cust_names = Customer_Names.query.\
        filter_by(end_customer_global_ultimate_id=cust_id).all()

    orders = Orders.query.\
        filter_by(end_customer_global_ultimate_id=cust_id).all()

    print(cust_id)

    for cust_name in cust_names:
        print("\t", cust_name.erp_end_customer_name)

    for order in orders:
        order_id = order.erp_sales_order_number
        print("\t\t", order_id)
        items = Bookings.query. \
            filter_by(erp_sales_order_number=order_id).all()

        for item in items:
            print("\t\t\t", item.bundle_product_id)

    time.sleep(.25)


