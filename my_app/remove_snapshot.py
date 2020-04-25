from my_app import db


def remove_snapshot(snap_shot_date):
    sql = "DELETE FROM ta_adoption_db.archive_bookings_repo WHERE date_added = '" + snap_shot_date + "' ;"
    sql_results = db.engine.execute(sql)
    print("Bookings removed", sql_results.rowcount)

    sql = "DELETE FROM ta_adoption_db.archive_telemetry_repo WHERE date_added = '" + snap_shot_date + "' ;"
    sql_results = db.engine.execute(sql)
    print("Telemetry removed", sql_results.rowcount)

    sql = "DELETE FROM ta_adoption_db.archive_subscriptions_repo WHERE date_added = '" + snap_shot_date + "' ;"
    sql_results = db.engine.execute(sql)
    print("Subscriptions removed", sql_results.rowcount)

    sql = "DELETE FROM ta_adoption_db.archive_services_repo WHERE date_added = '" + snap_shot_date + "' ;"
    sql_results = db.engine.execute(sql)
    print("Services removed", sql_results.rowcount)
    return


if __name__ == "__main__" and __package__ is None:
    remove_snapshot('2020-03-30')
    exit()
