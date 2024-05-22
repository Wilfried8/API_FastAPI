from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
# import just the values of the columns without name
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True :
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was succesfull !!!')
        break
    except Exception as e:
        print('connection to DB failed')
        print('Error', f'e')
        time.sleep(2)