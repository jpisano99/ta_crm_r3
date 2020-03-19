import my_app.tool_box as tool


def delete_current_tables():
    tool.drop_tables("bookings")
    tool.drop_tables("bookings_deleted")

    tool.drop_tables("subscriptions")
    tool.drop_tables("subscriptions_deleted")

    tool.drop_tables("services")
    tool.drop_tables("telemetry")

    tool.drop_tables("subscription_ids")
    tool.drop_tables("web_orders")
    tool.drop_tables("sales_orders")

    tool.drop_tables("customer_aliases")
    tool.drop_tables("customer_ids")

    return


if __name__ == "__main__" and __package__ is None:
    delete_current_tables()
    exit()
