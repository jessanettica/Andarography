"""Andarography."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
import requests

from model import connect_to_db, db, User, Experience, Provider, Venue, Booked, Wanderlist, Category


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC123"


app.jinja_env.undefined = StrictUndefined
#raise error when variable is undefined in Jinja2


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get from variables
    user_firstname = request.form["user_firstname"]
    user_lastname = request.form["user_lastname"]
    user_email = request.form["user_email"]
    user_instagram = request.form["user_instagram"]
    user_city = request.form["user_city"]
    user_password = request.form["user_password"]

    new_user = User(user_firstname=user_firstname, user_lastname=user_lastname, user_email=user_email, user_instagram=user_instagram, user_city=user_city, user_password=user_password)

    db.session.add(new_user)
    db.session.commit()

    flash("Hi %s! Welcome to Andarography." % user_firstname)
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

    user = User.query.filter_by(user_email=email).first()
    #why first and not one? does not error out X)
    if not user:
        flash("No such user")
        return redirect("/login")

    if user.user_password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id
    session["user_firstname"] = user.user_firstname

    flash("Logged in")
    return redirect("/")
    #return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


# @app.route("/howitworks")
# def howitworks():
#     """Explain the path of the user through the web app"""

    #return render_template("howitworks.html")


@app.route("/experience_sf")
def experince_list():
    """Show list of experiences in San Francisco"""

    #this is a line continuation backslash
    #query the db session itself, grab Exp, Provider, and Venue, and then join.
    experiences_and_providers_and_venues = db.session.query(Experience, Provider, Venue)\
        .filter_by(exp_city="San Francisco")\
        .join(Provider)\
        .join(Venue)\
        .all()
    print experiences_and_providers_and_venues
    # venues = Venue.query.all()

    return render_template("experience_page_sf.html", experiences_and_providers_and_venues=experiences_and_providers_and_venues)


# @app.route("/user/<int:user_id>")
# def user_page(user_id):
#     """Show info about user."""

#     user = User.query.get(user_id)
#     return render_template("user.html", user=user)

# @app.route("/booked/<int:user_id>")
# def user_booking():
#     """Display the user's booking data"""

#     #requests for info go here

    #return render_template("user_booking.html")

# @app.route("/wanderlist/<int:user_id>")
# def user_wanderlist():
#     """Display the user's wishlist data"""

#     #requests for info go here

    #return render_template("user_wanderlist.html")

if __name__ == "__main__":
    app.debug = True
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()