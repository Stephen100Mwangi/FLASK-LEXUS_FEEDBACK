# Import dependencies
from flask import Flask, request, render_template
# Dependency for SQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Import sendmail
from send_mail import send_mail

# Initialize app
app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/lexus_car'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''


# To avoid warnings on the console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Define a base class for declarative models
class Base(DeclarativeBase):
    pass

# Create a db object
db = SQLAlchemy(app)
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer,primary_key=True)
    customer = db.Column(db.String(200),unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())


    # Initializer
    # self is more like this keyword
    def __init__(self,customer,dealer,rating,comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit",methods=["POST"])
def submit():
    if request.method == "POST":
        # Grab data from form
        customer = request.form["customer"]
        dealer = request.form["dealer"]
        rating = request.form["rating"]
        comments = request.form["comments"]

        if customer == '' or dealer == '' or rating == '' or comments == '':
            return render_template("index.html", message="All fields are required")

        # Check if customer exists
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer,dealer,rating,comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer,dealer,rating,comments)
            return render_template("success.html")
        return render_template("index.html",message="You have already submitted feedback")

@app.cli.command("init-db")
def init_db():
    # Initialize the database
    db.create_all()   
    print("Initialized the database")     


if __name__ == "__main__":
    app.run()