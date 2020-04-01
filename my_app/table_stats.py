from my_app import db


def table_stats(table_names):
    snap_shots = []
    for table_name, sql_name in table_names.items():
        sql = "SELECT DISTINCT  `date_added` " \
              "FROM " + sql_name + ";"
        sql_results = db.engine.execute(sql)
        print('Repo ' + table_name + ' has ', sql_results.rowcount, 'snapshots')

        for r in sql_results:
            date_added_str = r.date_added.strftime('%Y-%m-%d')
            sql = "SELECT count(*) FROM " + sql_name + " WHERE date_added = '" + date_added_str + "';"
            sql_results_1 = db.engine.execute(sql)
            x = 0
            for x in sql_results_1:
                snap_shots.append((r.date_added, x[0], table_name, sql_name))
            print('\t', date_added_str, x[0])

    # Create a sorted index list of date_added dates
    snap_shots.sort(key=lambda x: x[0], reverse=True)

    return snap_shots


if __name__ == "__main__" and __package__ is None:
    # jim = table_stats({'bookings': 'archive_bookings_repo'})
    # print(jim[0])
    # print()
    table_names = {'telemetry': 'archive_telemetry_repo',
                   'bookings': 'archive_bookings_repo',
                   'subscriptions': 'archive_subscriptions_repo',
                   'services': 'archive_services_repo'}
    jim = table_stats(table_names)

