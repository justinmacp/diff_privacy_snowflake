from flask import Blueprint, request, abort, make_response, jsonify, Flask

# Make the postgres connection
from sqlalchemy import create_engine, Connection, URL
from api.src.config import postgres_creds
from postgresql_src import laplacian_mechanisms


def connect() -> Connection:
    url_object = URL.create(
        drivername=postgres_creds['sql_dialect'] + "+" + postgres_creds['adapter'],
        username=postgres_creds['username'],
        password=postgres_creds['password'],
        host=postgres_creds['host'],
        port=postgres_creds['port'],
        database=postgres_creds['database']
    )
    engine = create_engine(url_object)
    return engine.connect()


session = connect()

postgres = Blueprint('postgres', __name__)

user_privacy_budgets_table_str = "usage_tracking.users.privacy_budgets"
privacy_budget_col = "privacy_budget"
api_service_col = "api_service"
write_mode = "overwrite"


class BudgetError:
    pass


@postgres.route('passengers/dp_count')
def dp_count():
    # Validate arguments
    privacy_budget_str = request.args.get('privacy_budget')
    try:
        privacy_budget = float(privacy_budget_str)
        budgets_df = session.table(user_privacy_budgets_table_str)
        total_budget = (
            budgets_df
            .where(f.col(api_service_col) == postgres_creds['user'])
            .select(privacy_budget_col)
        )
        total_budget = total_budget.collect()[0][0]
        if privacy_budget <= 0 or total_budget - privacy_budget < 0:
            privacy_budget_error = ValueError(
                "The privacy budget should be greater 0 and smaller than your overall budget"
            )
            raise privacy_budget_error
    except BudgetError:
        abort(400, "Invalid privacy budget.")
    try:
        df = session.table(table_name_str)
        res = laplacian_mechanisms.dp_count(df, privacy_budget)
        (
            budgets_df
            .withColumn(
                privacy_budget_col,
                f.when(f.col(api_service_col) == postgres_creds['user'], total_budget - privacy_budget)
                .otherwise(f.col(api_service_col)))
            .write
            .saveAsTable(user_privacy_budgets_table_str, mode=write_mode)
        )
        print("Your remaining budget is ", total_budget - privacy_budget)
        return make_response(jsonify(res))
    except :
        abort(500, "Error reading from Snowflake. Check the logs for details.")
