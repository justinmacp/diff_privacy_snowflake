import snowflake.snowpark as snowpark
import snowflake.snowpark.functions as f
import numpy as np


def dp_count(df: snowpark.DataFrame, epsilon: float) -> float:
    """Returns a differentially private row count.

    Parameters
    ----------
    df : The table on which the count is performed
    epsilon : The privacy budget for the query

    Returns
    -------
    float : The row count of the dataframe with laplacian added nose according to the privacy budget

    """
    sensitivity = 1  # The sensitivity of a count is 1
    return np.random.laplace(df.count(), sensitivity / epsilon)


def dp_sum(
        df: snowpark.DataFrame,
        col: snowpark.Column,
        epsilon: float,
        lower_bound: int,
        upper_bound: int
) -> float:
    """Returns a differentially private sum

    Parameters
    ----------
    df : The table which contains the numerical column upon which the sum is to be computed
    col : The numerical column in the data frame upon which the sum is to be computed
    epsilon : The privacy budget
    lower_bound : In order to guarantee that the sum operation has a limited sensitivity all data points must be clipped
        with a lower bound
    upper_bound : The upper bound of the clipping to ensure limited sensitivity of the sum

    Returns
    -------
    float : The sum of the numerical column with laplacian added nose according to the privacy budget
    """
    sensitivity = upper_bound - lower_bound  # Sensitivity for a sum operation is the range of possibilities
    df = df.withColumn(
        col.getName(),
        f.when(col > upper_bound, upper_bound).otherwise(col)
        .when(col < lower_bound, lower_bound).otherwise(col)
    )
    df = df.agg(f.sum(col))
    return np.random.laplace(df.collect()[0][0], sensitivity / epsilon)
