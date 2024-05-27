from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

import psycopg2
# import just the values of the columns without name
from psycopg2.extras import RealDictCursor
import time

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True :
#     try:
#         #conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name, user=settings.database_username, password=settings.database_password, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was succesfull !!!')
#         break
#     except Exception as e:
#         print('connection to DB failed')
#         print('Error', f'e')
#         time.sleep(2)