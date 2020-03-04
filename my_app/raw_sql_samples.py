from my_app import db


sql = 'SELECT id, web_order_id from ta_adoption_db.archive_bookings_repo;'
my_tbl = "ta_adoption_db.archive_bookings_repo"
my_recs = db.engine.execute(sql)

for row in my_recs:
    d = dict(row.items())
    row_id = d['id']
    web_order_id = d['web_order_id']

    if web_order_id.find('.') != -1:
        new_web_order_id = web_order_id[0:(web_order_id.find('.'))]
        print(web_order_id, new_web_order_id)
        sql = "UPDATE " + my_tbl + " SET web_order_id = " + new_web_order_id + " WHERE id = " + str(row_id)
        db.engine.execute(sql)
