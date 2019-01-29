import os,csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
choice = input("Choice: ")

while True:
    if choice =="0":
        break
    elif choice =="1":
        db.execute("CREATE TABLE books(id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INTEGER NOT NULL)")
        db.commit()
        break
    elif choice =="2":
        db.execute("CREATE TABLE profiles(id SERIAL PRIMARY KEY, login VARCHAR NOT NULL, password VARCHAR NOT NULL,email_add VARCHAR NOT NULL)")
        db.commit()
        break
    elif choice=="3":
        db.execute("CREATE TABLE reviews(id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, isbn VARCHAR NOT NULL, review VARCHAR NOT NULL )")
        db.commit()
        break
          

