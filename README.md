# diff_privacy_snowflake
An SQL based differentially private interface

This is an SQL based differential privacy application.

It is intended to fit as an interface on top of a Database and which will return differentially private responses to any queries.

The DP theory is based upon the following textbook: https://programming-dp.com/book.pdf

## Summary

A user that would like to gain insights from the data needs access to aggregations (sums, averages, medians, etc.) of the data as well as samples (top K rows) from the data.

The data owner would like to not expose private information to the user.

These two requirements seem to conflict, but they can be solved with privacy technologies like synthetic data for samples and differentially private mechanisms for aggregates.

The database must keep track of (and also cap) it's users' consumption of privacy (also known as the privacy budget).

To ensure, that the user gets what they need and the data owner can retain the privacy of their data, the data owner must also know what the user is querying to prevent attacks on the data.

## Usage

1. Sign up for a Snowflake account and set up your data (you can sign up for a free trial account)
   1. The data being used here is the titanic training data from: https://www.kaggle.com/c/titanic/data
2. Follow the setup from https://quickstarts.snowflake.com/guide/build_a_custom_api_in_python/index.html?index=..%2F..index#10
   1. Run the following to start the REST API service:
    >python api/src/app.py 
4. Check the API doc for the possible commands that can be run
