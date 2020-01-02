from my_app import app
from my_app.main import get_customer
from my_app.pre_run_file_checks import pre_run_file_checks
from my_app.import_updates_to_sql import import_updates_to_sql
from my_app.settings import app_cfg
from flask import render_template, url_for, request, jsonify

from my_app.models import Bookings, BookingsSchema


@app.route('/', methods=['GET', 'POST'])
def index():
    # Go run this script when this route is called
    cust_name, test_list = get_customer()

    if request.method == 'POST':
        some_json = request.get_json()
        print('type', type(some_json))
        print('json:', some_json)
        type_of_url = 'POSTED Version 2.0'
    else:
        type_of_url = 'GET Version 1.0 ' + cust_name
    # return jsonify({'about': type_of_url}), 201
    # return render_template('login.html', cust_name=cust_name)
    return render_template('index_old.html', type_of_url=type_of_url, cust_name=cust_name)


@app.route('/scrub_data', methods=['GET', 'POST'])
def scrub_data():
    msg = pre_run_file_checks()
    print(msg)
    # return render_template('basic_list.html', type_of_url=type_of_url, cust_name=cust_name, sku_list=sku_list)
    return (msg)

@app.route('/load_data', methods=['GET', 'POST'])
def load_data():
    msg = import_updates_to_sql()
    print(msg)
    # return render_template('basic_list.html', type_of_url=type_of_url, cust_name=cust_name, sku_list=sku_list)
    return (msg)


@app.route('/dash_board', methods=['GET', 'POST'])
@app.route('/dash', methods=['GET', 'POST'])
def dash_board():
    if request.method == 'POST':
        srch_val = request.form.get('srch_val')
        print('looking for', srch_val)
        rslt = Bookings.query.filter(Bookings.erp_end_customer_name == srch_val).all()
        bookings_schema = BookingsSchema(many=True)
        output = bookings_schema.dump(rslt)
        return render_template('tables.html', title='Tables', my_rows=output)
    return render_template('index.html', title='Index')


@app.route('/tables')
def tables():
    rslt = Bookings.query.filter(Bookings.end_customer_global_ultimate_id == "46372").all()
        # filter(Bookings.erp_end_customer_name != "UNKNOWN").all()
    bookings_schema = BookingsSchema(many=True)
    output = bookings_schema.dump(rslt)
    for row in output:
        row['erp_end_customer_name'] = row['erp_end_customer_name'][0:10]
    return render_template('tables.html', title='Tables', my_rows=output)


@app.route('/jsoned')
def jsoned():
    rslt = Bookings.query.filter(Bookings.end_customer_global_ultimate_id == "46372").all()
        # filter(Bookings.erp_end_customer_name != "UNKNOWN").all()
    bookings_schema = BookingsSchema(many=True)
    output = bookings_schema.dump(rslt)
    return jsonify({'booking': output})


@app.route('/register')
def register():
    return render_template('register.html', title='Register')


@app.route('/login')
def login():
    return render_template('login.html', title='Login')


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot-password.html', title='Forgot Password')


@app.route('/about')
def about():
    return render_template('about.html', title='About')