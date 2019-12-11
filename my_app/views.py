from my_app import app
from my_app.main import get_customer
from my_app.pre_run_file_checks import pre_run_file_checks
from my_app.import_updates_to_sql import import_updates_to_sql
from my_app.settings import app_cfg
from flask import render_template, url_for, request, jsonify


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
    return render_template('index.html', type_of_url=type_of_url, cust_name=cust_name)


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