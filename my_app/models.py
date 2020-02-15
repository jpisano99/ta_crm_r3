from my_app import db
from my_app import ma


class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer(), primary_key=True)
    bill_to_customer = db.Column(db.String(50))
    reseller = db.Column(db.String(50))
    end_customer = db.Column(db.String(50))
    offer_name = db.Column(db.String(50))
    subscription_id = db.Column(db.String(50))
    status = db.Column(db.String(50))
    start_date = db.Column(db.DateTime)
    initial_term = db.Column(db.String(50))
    renewal_date = db.Column(db.DateTime)
    currency = db.Column(db.String(50))
    monthly_charge = db.Column(db.String(50))
    auto_renewal_term = db.Column(db.String(50))
    billing_model = db.Column(db.String(50))
    purchase_order_number = db.Column(db.String(50))
    weborderid = db.Column(db.String(50))
    site_url = db.Column(db.String(50))
    customer_success_manager = db.Column(db.String(50))
    partner_success_manager = db.Column(db.String(50))
    sales_owner = db.Column(db.String(50))
    customer_success_manager_email = db.Column(db.String(50))
    partner_success_manager_email = db.Column(db.String(50))
    sales_owner_email = db.Column(db.String(50))
    account_type = db.Column(db.String(50))
    days_until_renewal = db.Column(db.String(50))


class Services(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer(), primary_key=True)
    pid = db.Column(db.String(50))
    delivery_manager = db.Column(db.String(50))
    end_customer = db.Column(db.String(50))
    project_department_name = db.Column(db.String(50))
    op_pm = db.Column(db.String(50))
    color_indicator = db.Column(db.String(50))
    delivery_pm = db.Column(db.String(50))
    tracking_status = db.Column(db.String(50))
    tracking_sub_status = db.Column(db.String(50))
    comments = db.Column(db.String(50))
    dmc_updates = db.Column(db.String(50))
    dmc_act_fcst_end = db.Column(db.String(50))
    op_forecast = db.Column(db.String(50))
    cost_index = db.Column(db.String(50))
    sku = db.Column(db.String(50))
    project_name = db.Column(db.String(50))
    unit = db.Column(db.String(50))
    region = db.Column(db.String(50))
    wm_in_op = db.Column(db.String(50))
    so = db.Column(db.String(50))
    as_approved_cost_budget = db.Column(db.String(50))
    as_approved_revenue_budget = db.Column(db.String(50))
    actual_total_costs = db.Column(db.String(50))
    actual_revenue = db.Column(db.String(50))
    status = db.Column(db.String(50))
    project_class = db.Column(db.String(50))
    project_scheduled_start_date = db.Column(db.DateTime)
    scheduled_end_date = db.Column(db.DateTime)
    project_creation_date = db.Column(db.DateTime)
    project_closed_date = db.Column(db.DateTime)
    traffic_lights_account_team = db.Column(db.String(50))
    tracking_responsible = db.Column(db.String(50))
    column30 = db.Column(db.String(50))

    def __repr__(self):
        return f"Services for ('{self.pid}' , '{self.end_customer}')"


class Bookings(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer(), primary_key=True)
    fiscal_year = db.Column(db.String(50))
    fiscal_quarter_id = db.Column(db.String(50))
    fiscal_period_id = db.Column(db.String(50))
    sales_level_1 = db.Column(db.String(50))
    sales_level_2 = db.Column(db.String(50))
    sales_level_3 = db.Column(db.String(50))
    sales_level_4 = db.Column(db.String(50))
    sales_level_5 = db.Column(db.String(50))
    sales_level_6 = db.Column(db.String(50))
    sales_agent_name = db.Column(db.String(50))
    email_id = db.Column(db.String(50))
    erp_sales_order_number = db.Column(db.String(50))
    # erp_sales_order_number = db.Column(db.String(50), db.ForeignKey('sales_orders.so_number'), nullable=True)
    web_order_id = db.Column(db.String(50))
    erp_end_customer_name= db.Column(db.String(100))
    end_customer_global_ultimate_name = db.Column(db.String(100))
    end_customer_global_ultimate_id = db.Column(db.String(50))
    tms_level_2_sales_allocated = db.Column(db.String(50))
    product_family = db.Column(db.String(50))
    bundle_product_id = db.Column(db.String(50))
    product_id = db.Column(db.String(50))
    tms_sales_allocated_product_bookings_net = db.Column(db.Float)
    tms_sales_allocated_service_bookings_net = db.Column(db.Float)
    hash_value = db.Column(db.String(100))
    date_added = db.Column(db.DateTime)


# class Bookings_New(db.Model):
#     __tablename__ = 'bookings_new'
#
#     id = db.Column(db.Integer(), primary_key=True)
#     fiscal_year = db.Column(db.String(50))
#     fiscal_quarter_id = db.Column(db.String(50))
#     fiscal_period_id = db.Column(db.String(50))
#     sales_level_1 = db.Column(db.String(50))
#     sales_level_2 = db.Column(db.String(50))
#     sales_level_3 = db.Column(db.String(50))
#     sales_level_4 = db.Column(db.String(50))
#     sales_level_5 = db.Column(db.String(50))
#     sales_level_6 = db.Column(db.String(50))
#     sales_agent_name = db.Column(db.String(50))
#     email_id = db.Column(db.String(50))
#     # erp_sales_order_number = db.Column(db.String(50))
#     erp_sales_order_number = db.Column(db.String(50), db.ForeignKey('sales_orders.so_number'), nullable=True)
#     web_order_id = db.Column(db.String(50))
#     erp_end_customer_name= db.Column(db.String(50))
#     end_customer_global_ultimate_name = db.Column(db.String(50))
#     end_customer_global_ultimate_id = db.Column(db.String(50))
#     tms_level_2_sales_allocated = db.Column(db.String(50))
#     product_family = db.Column(db.String(50))
#     bundle_product_id = db.Column(db.String(50))
#     product_id = db.Column(db.String(50))
#     tms_sales_allocated_product_bookings_net = db.Column(db.Float)
#     tms_sales_allocated_service_bookings_net = db.Column(db.Float)
#     hash_value = db.Column(db.String(50))
#     date_added = db.Column(db.DateTime)


class BookingsSchema(ma.ModelSchema):
    class Meta:
        model = Bookings


class Customer_Ids(db.Model):
    __tablename__ = 'customer_ids'

    customer_id = db.Column(db.String(50), primary_key=True)
    customer_aliases = db.relationship('Customer_Aliases', backref='my_customer_id', lazy=True)
    customer_so_numbers = db.relationship('Sales_Orders', backref='my_customer_id', lazy=True)
    customer_web_order_ids = db.relationship('Web_Orders', backref='my_customer_id', lazy=True)


class Customer_Aliases(db.Model):
    __tablename__ = 'customer_aliases'

    id = db.Column(db.Integer(), primary_key=True)
    customer_alias = db.Column(db.String(50))
    customer_id = db.Column(db.String(50), db.ForeignKey('customer_ids.customer_id'))


class Sales_Orders(db.Model):
    __tablename__ = 'sales_orders'

    id = db.Column(db.Integer(), primary_key=True)
    so_number = db.Column(db.String(50))
    customer_id = db.Column(db.String(50), db.ForeignKey('customer_ids.customer_id'))
    # order_detail = db.relationship('Bookings', backref='my_so_number', lazy=True)


class Web_Orders(db.Model):
    __tablename__ = 'web_orders'

    id = db.Column(db.Integer(), primary_key=True)
    web_order_id = db.Column(db.String(50))
    customer_id = db.Column(db.String(50), db.ForeignKey('customer_ids.customer_id'))

class Telemetry(db.Model):
    __tablename__ = 'telemetry'

    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(25))
    type = db.Column(db.String(10))
    vrf = db.Column(db.Integer)
    licensed = db.Column(db.Integer)
    installed = db.Column(db.Integer)
    inactive = db.Column(db.Integer)
    autoupg = db.Column(db.Integer)
    windows = db.Column(db.Integer)
    linux = db.Column(db.Integer)
    aix = db.Column(db.Integer)
    lightwt = db.Column(db.Integer)
    legacy = db.Column(db.Integer)
    deepvis = db.Column(db.Integer)
    enforce = db.Column(db.Integer)
    enforce_enabled = db.Column(db.Integer)
    pid_enabled = db.Column(db.Integer)
    forensics_enabled = db.Column(db.Integer)
    inventory = db.Column(db.Integer)
    anyconnect = db.Column(db.Integer)
    anyproxy = db.Column(db.Integer)
    erspan = db.Column(db.Integer)
    f5 = db.Column(db.Integer)
    netflow = db.Column(db.Integer)
    netscaler = db.Column(db.Integer)
    others = db.Column(db.Integer)


class Test_Table(db.Model):
    __tablename__ = 'test_table'

    # Use this to specify a default schema/db for this table
    # __table_args__ = {'schema': 'dev'}

    # Us this to specify a different bind/sql server for this table
    # __bind_key__ = 'dev'

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    qty_on_hand = db.Column(db.Integer)
    cost = db.Column(db.Float)
    date_added = db.Column(db.DateTime)
    password_hash = db.Column(db.String(128))

    @staticmethod
    def newest():
        return Test_Table.query.all()

    def newest_name(num):
        return Test_Table.query.order_by(Test_Table.first_name).limit(num)

    def __repr__(self):
       return "<name {}: '{} , {}'>".format(self.id, self.pss_name,self.tsa_name)
