"""Andarography."""

from jinja2 import StrictUndefined

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
import requests

#from model import connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC123"


app.jinja_env.undefined = StrictUndefined
#raise error when variable is undefined in Jinja2


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get from variables
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % username)
    return redirect("/")

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get from variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()
    #why first and not one?

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

@app.route("/howitworks")
def howitworks():
    """Explain the path of the user through the web app"""

    return render_template("howitworks.html")

@app.route("/experience_sf")
def sf_experience():
    """Show experiences availabel in SF"""
    params = {'token': 'MEPMC6UJ5E5BE5L5DKIH', 'venue.city': 'San Francisco', 'categories': '110'}
    r = requests.get('https://www.eventbriteapi.com/v3/events/search/', params=params)
    print r
    print '*' * 20
    print r.url
    print '*' * 20
    events=r.json()['events']
    for event in events:
        # print event.get('description').get('text') 
        #     gets the description of the event in SF 
        # print event.get('name').get('text')
        #     gets the event title of the event in SF
        # print event.get('start').get('local').split("T")[0]
        #     gets the start date of the event in year-month-day format
        # print event.get('start').get('local').split("T")[1]
        #     gets the start time of the event
        # print event.get('end').get('local').split("T")[0]
        #     gets the end date of the event in year-month-day format
        # print event.get('end').get('local').split("T")[1]
        #     gets the end time of the event
        print event
    return 'success'

@app.route("/user/<int:user_id>")
def user_page():
    """Display the user's data"""

    #requests for info go here

    return render_template("user_page.html")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    #connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()