import os,requests, uuid, hashlib

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

def hash_password(password):
    salt=uuid.uuid4().hex
    return hashlib.sha256(salt.encode()+password.encode()).hexdigest()+" : " + salt
def check_password(hashed_pass,user_pass):
    password,salt = hashed_pass.split(' : ')
    return password == hashlib.sha256(salt.encode() + user_pass.encode()).hexdigest()

@app.route("/")
def index():
    if not session.get ('logged_in'):
        return render_template('login.html')
    else:
        return render_template("index.html", message="Welcome to the World of Bookworming")

@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/add_user", methods=["POST"])
def add_user_to_database():
    login=request.form.get("login")
    email_add=request.form.get("email_add")
    password=request.form.get("password")
    password2=request.form.get("password2")
    if db.execute("SELECT * FROM profiles WHERE login=:login OR email_add=:email_add", {"login":login, "email_add":email_add}).rowcount==0:
        if password==password2:
            db.execute("INSERT INTO profiles(login,password,email_add) VALUES (:login, :password, :email_add)",{"login":login,"password":hash_password(password),"email_add":email_add})
        else:
            return render_template("error.html", message="Passwords HAVE TO be exactly the same")
    else:
        return render_template("error_html", message="Login or e-mail already in the database. Please try again")
@app.route("/log_me_in", methods=["POST"])
def log_user():
    login=request.form.get("login")
    entered_password=request.form.get("password")
    if db.execute("SELECT * FROM profiles WHERE login=:login", {"login":login}).rowcount==0:
        return render_template("login.html", failure = "No such username in the database. Try again")
    else:
        user_id, db_password=db.execute("SELECT id, password FROM profiles WHERE login=:login",{"login":login})
        if check_password(db_password,entered_password):
            session[user_id] = True
            session['logged in'] = True
            return render_template("login.html", success="Logged in successfully !")


@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/search",methods=["POST"])
def book_browser():
    return render_template("search.html")
@app.route("/logout")
def logout():
    user = session["user_id"]
    session[user] = False
    session['logged in']=False
    return render_template("index.html")
@app.route("/error")
def error():
    return render_template("error.html")

