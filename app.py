import os

from flask import Flask, session, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    '''login_page'''
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/login",methods=["POST"])
def login():
    return render_template("login.html")
@app.route("/search",methods=["POST"])
def book_browser():
    return render_template("search.html")
@app.route("/logout")
def logout():
    return render_template("logout.html")
@app.route("/error")
def error():
    return render_template("error.html")

