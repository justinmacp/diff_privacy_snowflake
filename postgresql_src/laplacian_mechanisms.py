import numpy as np
from sqlalchemy.orm import Query


def dp_count(table_query: Query, epsilon: float) -> float:
    """Returns a differentially private row count.

    Parameters
    ----------
    table_query : The table on which the count is performed
    epsilon : The privacy budget for the query

    Returns
    -------
    float : The row count of the dataframe with laplacian added nose according to the privacy budget
    """
    sensitivity = 1
    return np.random.laplace(table_query.count(), sensitivity / epsilon)
