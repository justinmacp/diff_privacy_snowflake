from flask import Blueprint, request, abort, make_response, jsonify

# Make the postgres connection
from api.src.config import postgres_creds
from postgresql_src import laplacian_mechanisms
from postgresql_src.api.models.passengers import Passengers
from postgresql_src.api.models.users import Users

postgres = Blueprint('postgres', __name__)

user_privacy_budgets_table_str = "usage_tracking.users.privacy_budgets"
privacy_budget_col = "privacy_budget"
api_service_col = "api_service"
write_mode = "overwrite"


class SnowflakeError(Exception):
    status_code = 400

    def __init__(self):
        super().__init__()


@postgres.route('passengers/dp_count')
def dp_count():
    # Validate arguments
    privacy_budget_str = request.args.get('privacy_budget')
    try:
        privacy_budget = float(privacy_budget_str)
        total_budget = Users.query.filter(Users.username == postgres_creds['user']).privacy_budget
        total_budget = 100
        if privacy_budget <= 0 or total_budget - privacy_budget < 0:
            privacy_budget_error = ValueError(
                "The privacy budget should be greater 0 and smaller than your overall budget"
            )
            raise privacy_budget_error
    except ValueError:
        abort(400, "Invalid privacy budget.")
    try:
        res = laplacian_mechanisms.dp_count(Passengers.query, privacy_budget)
        (
            Users.query
            .filter(Users.username == postgres_creds['user'])
            .update({Users.privacy_budget: Users.privacy_budget - total_budget}, syncronize_session='fetch')
        )
        print("Your remaining budget is ", total_budget - privacy_budget)
        return make_response(jsonify(res))
    except SnowflakeError:
        abort(500, "Error reading from Snowflake. Check the logs for details.")
