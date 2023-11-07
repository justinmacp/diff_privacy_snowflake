from flask import Blueprint, request, abort, make_response, jsonify
import datetime

# Make the Snowflake connection
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from snowflake.snowpark import Session
import snowflake.snowpark.functions as f
from config import creds

from snowpark_src import laplacian_mechanisms


def connect() -> Session:
    if 'private_key' in creds:
        if not isinstance(creds['private_key'], bytes):
            p_key = serialization.load_pem_private_key(
                creds['private_key'].encode('utf-8'),
                password=None,
                backend=default_backend()
            )
            pkb = p_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption())
            creds['private_key'] = pkb
    return Session.builder.configs(creds).create()


session = connect()

# Make the API endpoints
snowpark = Blueprint('snowpark', __name__)

# Top 10 customers in date range
dateformat = '%Y-%m-%d'


@snowpark.route('/dp_sum')
def dp_sum():
    # Validate arguments
    privacy_budget_str = request.args.get('privacy_budget')
    table_name_str = request.args.get('table_name')
    column_name_string = request.args.get('column_name')
    lower_bound_str = request.args.get('lower_bound')
    upper_bound_str = request.args.get('upper_bound')
    try:
        privacy_budget = float(privacy_budget_str)
        lower_bound = int(lower_bound_str)
        upper_bound = int(upper_bound_str)
    except:
        abort(400, "Invalid privacy budget, lower bound or upper bound. Please enter a number")
    try:
        df = session.table(table_name_str)
        res = laplacian_mechanisms.dp_sum(df, f.col(column_name_string), privacy_budget, lower_bound, upper_bound)
        return make_response(jsonify(res))
    except:
        abort(500, "Error reading from Snowflake. Check the logs for details.")


@snowpark.route('/dp_count')
def dp_count():
    # Validate arguments
    privacy_budget_str = request.args.get('privacy_budget')
    table_name_str = request.args.get('table_name')
    try:
        privacy_budget = float(privacy_budget_str)
    except:
        abort(400, "Invalid privacy budget. Please enter a number")
    try:
        df = session.table(table_name_str)
        res = laplacian_mechanisms.dp_count(df, privacy_budget)
        return make_response(jsonify(res))
    except:
        abort(500, "Error reading from Snowflake. Check the logs for details.")


@snowpark.route('/customers/top10')
def customers_top10():
    # Validate arguments
    sdt_str = request.args.get('start_range') or '1995-01-01'
    edt_str = request.args.get('end_range') or '1995-03-31'
    try:
        sdt = datetime.datetime.strptime(sdt_str, dateformat)
        edt = datetime.datetime.strptime(edt_str, dateformat)
    except:
        abort(400, "Invalid start and/or end dates.")
    try:
        df = session.table('snowflake_sample_data.tpch_sf10.orders') \
            .filter((f.col('O_ORDERDATE') >= sdt) & (f.col('O_ORDERDATE') <= edt)) \
            .group_by(f.col('O_CUSTKEY')) \
            .agg(f.sum(f.col('O_TOTALPRICE')).alias('SUM_TOTALPRICE')) \
            .sort(f.col('SUM_TOTALPRICE').desc()) \
            .limit(10)
        return make_response(jsonify([x.as_dict() for x in df.to_local_iterator()]))
    except:
        abort(500, "Error reading from Snowflake. Check the logs for details.")


# Monthly sales for a clerk in a year
@snowpark.route('/clerk/<clerkid>/yearly_sales/<year>')
def clerk_monthly_sales(clerkid, year):
    # Validate arguments
    try:
        year_int = int(year)
    except:
        abort(400, "Invalid year.")
    if not clerkid.isdigit():
        abort(400, "Clerk ID can only contain numbers.")
    clerkid_str = f"Clerk#{clerkid}"
    try:
        df = session.table('snowflake_sample_data.tpch_sf10.orders') \
            .filter(f.year(f.col('O_ORDERDATE')) == year_int) \
            .filter(f.col('O_CLERK') == clerkid_str) \
            .with_column('MONTH', f.month(f.col('O_ORDERDATE'))) \
            .groupBy(f.col('O_CLERK'), f.col('MONTH')) \
            .agg(f.sum(f.col('O_TOTALPRICE')).alias('SUM_TOTALPRICE')) \
            .sort(f.col('O_CLERK'), f.col('MONTH'))
        return make_response(jsonify([x.as_dict() for x in df.to_local_iterator()]))
    except:
        abort(500, "Error reading from Snowflake. Check the logs for details.")
