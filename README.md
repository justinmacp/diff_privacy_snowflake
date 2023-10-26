# diff_privacy_snowflake
An SQL based differentially private interface

This is an SQL based differential privacy application.

It is intended to fit as an interface ontop of a Database and which will return differentially private responses to any queries.

To use the code in this repository, pull this repository into your Snowflake account

## Summary

A user that would like to gain insights from the data needs access to aggregations (sums, averages, medians, etc.) of the data as well as samples (top K rows) from the data.

The data owner would like to not expose private information to the user.

These two requirements seem to conflict, but they can be solved with privacy technologies like synthetic data for samples and differentially private mechanisms for aggregates.

The database must keep track of (and also cap) it's users' consumption of privacy (also known as the privacy budget).

To ensure, that the user gets what they need and the data owner can retain the privacy of their data, the data owner must also know what the user is querying so as to prevent attacks on the data.
