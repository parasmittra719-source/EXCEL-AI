from db import engine
from sqlalchemy import text

def create_tables():
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS organizations (id SERIAL PRIMARY KEY, name TEXT)"))
        conn.execute(text("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, org_id INTEGER REFERENCES organizations(id), username TEXT UNIQUE, password TEXT, role TEXT)"))
        conn.commit()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
