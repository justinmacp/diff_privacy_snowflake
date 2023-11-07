Basic command:

>curl -X GET http://localhost:8001/snowpark/<your command>?arg1=value1&arg2=value2"

The allowed commands and their arguments:

1. dp_count: This gives a differentially private count of rows
    1. table_name
    2. privacy_budget
2. dp_sum: This gives a differentially private sum of a column
    1. table_name
   2. column_name
   3. lower_bound
   4. upper_bound
   5. privacy_budget