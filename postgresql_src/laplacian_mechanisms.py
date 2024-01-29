from sqlalchemy import create_engine, insert, text
import time
import pandas as pd


def main():
    connection_url = "postgresql+psycopg2://postgres:postgres@db:5432/DB"
    engine = create_engine(connection_url)
    connection = engine.connect()
    query = text("SELECT * FROM passengers")
    connection.execute(query)
    connection.commit()
    print("done")


if __name__ == "__main__":
    time.sleep(5)
    main()
