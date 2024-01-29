from flask import Blueprint, request, abort, make_response, jsonify

# Make the postgres connection
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from sqlalchemy import create_engine, Connection
from config import postgres_creds


def connect() -> Connection:
    engine = create_engine(postgres_creds.database_uri)
    return engine.connect()


session = connect()

postgres = Blueprint('postgres', __name__)

user_privacy_budgets_table_str = "usage_tracking.users.privacy_budgets"
privacy_budget_col = "privacy_budget"
api_service_col = "api_service"
write_mode = "overwrite"


@postgres.route('/dp_sum')
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
        budgets_df = session.table(user_privacy_budgets_table_str)
        total_budget = (
            budgets_df
            .select(privacy_budget_col)
            .where(f.col(api_service_col) == creds['user'])
            .collect()[0][0]
        )
        if privacy_budget <= 0 or total_budget - privacy_budget < 0:
            privacy_budget_error = ValueError(
                "The privacy budget should be greater 0 and smaller than your overall budget."
            )
            raise privacy_budget_error
    except:
        abort(400, "Invalid privacy budget, lower bound or upper bound.")
    try:
        df = session.table(table_name_str)
        res = laplacian_mechanisms.dp_sum(df, f.col(column_name_string), privacy_budget, lower_bound, upper_bound)
        (
            budgets_df
            .withColumn(
                privacy_budget_col,
                f.when(f.col(api_service_col) == creds['user'], total_budget - privacy_budget)
                .otherwise(f.col(api_service_col)))
            .write
            .saveAsTable(user_privacy_budgets_table_str, mode=write_mode)
        )
        print("Your remaining budget is ", total_budget - privacy_budget)
        return make_response(jsonify(res))
    except:
        abort(500, "Error reading from Snowflake. Check the logs for details.")
