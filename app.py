
import os,requests, uuid, hashlib

from flask import Flask, session, render_template,request
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
app.config["DATABASE_URL"]="postgres://vatyzmoocsncfa:2d77ab6ee89190035f8bfeb8e9a65a0956c5003489bb2959560de66043807282@ec2-54-228-212-134.eu-west-1.compute.amazonaws.com:5432/dflt9fobvro5sm"

Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def hash_password(password):
    
    return hashlib.sha256(password.encode()).hexdigest()
def check_password(hashed_pass,user_pass):
    if  hashed_pass == hashed_pass:
        return True


@app.route("/")
def index():
    return render_template("index.html", message="Welcome to the World of Bookworming")

@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/add_user", methods=["POST","GET"])
def add_user_to_database():
    login=request.form.get("login")
    email_add=request.form.get("email_add")
    password=request.form.get("password")
    password2=request.form.get("password2")
    if db.execute("SELECT * FROM profiles WHERE login=:login OR email_add=:email_add", {"login":login, "email_add":email_add}).rowcount==0:
        if password==password2:
            db.execute("INSERT INTO profiles(login,password,email_add) VALUES (:login, :password, :email_add)",{"login":login,"password":hash_password(password),"email_add":email_add})
            db.commit()
            return render_template("register.html", message="Success")
        else:
            return render_template("register.html", message="Passwords HAVE TO be exactly the same")
    else:
        return render_template("register.html", message="Login or e-mail already in the database. Please try again")
@app.route("/log_me_in", methods=["POST"])

def log_user():
    login=request.form.get("login")
    entered_password=request.form.get("password")
    if db.execute("SELECT * FROM profiles WHERE login=:login", {"login":login}).rowcount==0:
        return render_template("login.html", failure = "No such username in the database. Try again")
    else:
        db_password=db.execute("SELECT password FROM profiles WHERE login=:login",{"login":login})
        if check_password(db_password,entered_password):
            
            session['logged_in'] = True
            return render_template("login.html", success="Logged in successfully !")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/search",methods=["POST","GET"])
def search():
    return render_template("search.html")

@app.route("/search_book", methods=["POST","GET"])
def search_book():
    command = "SELECT * FROM books WHERE"
    title = request.form.get("title")
    command+=" title "
    if title=="":
            command+="=COALESCE(title)"
    else:
        command+="LIKE '%"+title+"%'"
    author = request.form.get("author")
    command+=" AND author "
    if author =="":
        command+="=COALESCE(author)"
    else:
        command+="LIKE '%"+author+"%'"
    isbn = request.form.get("isbn")
    command+=" AND isbn"
    if isbn=="":
        command+="=COALESCE(isbn)"
    else:
        command+="LIKE '%"+isbn+"%'"
    year = request.form.get("year")
    command+=" AND year"
    if year=="":
        command+="=COALESCE(year)"
    else:
        command+="LIKE '%"+year+"%'"
    command+=" ORDER BY year DESC"
    result=db.execute(command)
    #result = db.execute("SELECT * FROM books WHERE title=:title AND author=:author AND isbn=:isbn AND year=:year",{"title":title,"author":author,"isbn":isbn,"year":year}).fetchall()
    return render_template("search.html", result=result)
@app.route("/quick_search", methods=["POST","GET"])
def quick_search():
    quick=request.form.get("quick")
    if quick.isnumeric():
        result = db.execute("SELECT * FROM books WHERE title=:title OR year=:year",{"title":quick,"year":quick}).fetchall()
    else:
        result = db.execute("SELECT * FROM books WHERE title=:title OR author=:author OR isbn=:isbn" ,{"title":quick,"author":quick,"isbn":quick}).fetchall()
    
    return render_template("search.html", result=result)
@app.route("/books/<int:book_id>")
def book(book_id):
    book = db.execute("SELECT * from books WHERE id=:id", {"id":book_id}).fetchone()
    isbn=db.execute("SELECT isbn FROM books WHERE id=:id",{"id":book_id})
    more=requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "XPTyzNNRxunppqVTmqTw", "isbns":isbn})
    more = more.json()
    rating = more["books"][0]['average_rating']
    rating_count = more["books"][0]['work_ratings_count']
    isbn = str(isbn)
    res = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+isbn)
    formatted = res.json()
    if formatted['totalItems']>0:
        cover=formatted['items'][0]['volumeInfo']['imageLinks']['thumbnail']
        desc=formatted['items'][0]['volumeInfo']['description']
    else:
        cover=False
        desc=False
    return render_template("book.html",book=book, rating=rating, rating_count=rating_count, cover=cover, desc=desc)

@app.route("/books")
def books():
    books = db.execute("SELECT * from books").fetchall()
    return render_template("books.html",books=books)
@app.route("/logout")
def logout():
    session['logged_in']= False
    return render_template("index.html",message = 'Logged out successfully')
@app.route("/error")
def error():
    return render_template("error.html")

