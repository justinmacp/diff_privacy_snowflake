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

COPY passengers(PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked)
FROM '/app/train.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE users (
    UserId INT PRIMARY KEY,
    PrivacyBudget FLOAT,
    APIService VARCHAR(255)
);