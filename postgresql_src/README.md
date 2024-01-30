This source code 

setup

https://www.commandprompt.com/education/how-to-create-a-postgresql-database-in-docker/
https://annaz4.medium.com/how-to-load-a-csv-file-into-a-remote-docker-mysql-container-fba89cf42880
https://medium.com/@romanbessouat/deploy-and-access-a-postgres-dabatase-using-docker-and-sqlalchemy-d06de37079f8
https://medium.com/@pooya.oladazimi/dockerizing-flask-app-with-postgres-a-step-by-step-guide-e9fc9939deff

docker pull postgres

docker run -d --name postgresCont -p 5432:5432 -e POSTGRES_PASSWORD=pass123 --mount type=bind,source=C:\Users\jumacp\Desktop\SnowflakeProject\diff_privacy_snowflake\Data,target=/app postgres

docker ps

docker exec -it db bash

psql -h localhost -U postgres

CREATE DATABASE titanic;

\l

\c titanic_passengers

CREATE TABLE passengers (
    PassengerId INT PRIMARY KEY,
    Survived INT,
    Pclass INT,
    Name VARCHAR(255),
    Sex VARCHAR(10),
    Age FLOAT,
    SibSp INT,
    Parch INT,
    Ticket VARCHAR(50),
    Fare FLOAT,
    Cabin VARCHAR(15),
    Embarked CHAR(1)
);

copy passengers(PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked) from '/app/train.csv' delimiter ',' csv header;


