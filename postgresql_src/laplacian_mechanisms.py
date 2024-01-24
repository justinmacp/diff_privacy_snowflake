from sqlalchemy import create_engine, insert, text


def main():
    engine = create_engine("postgresql+psycopg2://postgres@db:5432/DB")
    conn = engine.connect()
    query = text("SELECT * FROM passengers")

if __name__ == "__main__":
    main()
