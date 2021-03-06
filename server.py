"""Andarography."""

import os
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
import requests
from cStringIO import StringIO
import csv
from datetime import datetime
from collections import Counter
import random


from model import connect_to_db, db, User, Experience, Provider, Venue, Booked, Wanderlist, Category, Listed


app = Flask(__name__)

app.secret_key = "ABC123"


app.jinja_env.undefined = StrictUndefined


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

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(user_email=email).first()
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


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route("/experience_sf")
def experince_list():
    """Show list of experiences in San Francisco"""

    experiences_and_providers_and_venues = db.session.query(Experience, Provider, Venue)\
        .filter(Experience.exp_city == "San Francisco", Experience.private == False)\
        .outerjoin(Provider)\
        .outerjoin(Venue)\
        .all()
    print "OUTPUT", experiences_and_providers_and_venues

    favorited_experiences = db.session.query(Wanderlist.exp_id).filter_by(user_id=session.get('user_id')).all()
    favorited_experiences = [favorited_experience.exp_id for favorited_experience in favorited_experiences]

    booked_experiences = db.session.query(Booked.exp_id).filter_by(user_id=session.get('user_id')).all()
    booked_experiences = [booked_experience.exp_id for booked_experience in booked_experiences]

    return render_template("experience_page_sf.html", favorited_experiences=favorited_experiences,
                           booked_experiences=booked_experiences,
                           experiences_and_providers_and_venues=experiences_and_providers_and_venues)


@app.route("/experiment")
def experiment():

    experiences_and_providers_and_venues = db.session.query(Experience, Provider, Venue)\
        .filter_by(exp_city="San Francisco", private="0")\
        .join(Provider)\
        .join(Venue)\
        .all()
    print experiences_and_providers_and_venues

    favorited_experiences = db.session.query(Wanderlist.exp_id).filter_by(user_id=session.get('user_id')).all()
    favorited_experiences = [favorited_experience.exp_id for favorited_experience in favorited_experiences]

    booked_experiences = db.session.query(Booked.exp_id).filter_by(user_id=session.get('user_id')).all()
    booked_experiences = [booked_experience.exp_id for booked_experience in booked_experiences]

    pics = ["balloon.jpeg", "beer.jpeg", "biker.jpeg", "bridge2.jpeg", "camping.jpeg", "colorrun.jpeg",
            "dance.jpeg", "DeathtoStock_Medium4.jpg", "DeathtoStock_Medium7.jpg", "DeathtoStock_Medium9.jpg"
            "food.jpeg", "guitar.jpeg", "hill.jpeg", "sfbridge.jpeg", "skyline.jpeg", "smoothie.jpeg"]


    return render_template("experiment.html", favorited_experiences=favorited_experiences, booked_experiences=booked_experiences, 
                           experiences_and_providers_and_venues=experiences_and_providers_and_venues, pics=pics)

@app.route('/add_booked', methods=["POST"])
def add_booked():
    """
    I talk to AJAX. I update the Booked table when users click on Booked button.
    I get the experience ID from AJAX and the user ID from session.
    """

    this_user_id = session.get('user_id')

    if this_user_id:

        experience_id = request.form.get('experience_id')

        print "experience_id = ", experience_id

        experience_had = Booked.query.filter(Booked.exp_id == experience_id,
                                                 Booked.user_id == this_user_id).first()

        print experience_had

        if not experience_had:
            print "adding new experience!"
            print "user id and experience id", this_user_id, experience_id
            new_exp = Booked(user_id=this_user_id,
                             exp_id=experience_id)
            db.session.add(new_exp)
            db.session.commit()
    return "success"


@app.route('/add_wanderlist', methods=["POST"])
def add_wanderlist():
    """
    I talk to AJAX. I update the Wanderlist table when users click on Wanderlist button.
    I get the experience ID from AJAX and the user ID from session.
    """

    this_user_id = session.get('user_id')

    if this_user_id:

        experience_id = request.form.get('experience_id')

        print experience_id

        experience_saved = Wanderlist.query.filter(Wanderlist.exp_id == experience_id,
                                                   Wanderlist.user_id == this_user_id).first()

        if not experience_saved:
            print "adding new experience!"
            print "user id and experience id", this_user_id, experience_id
            new_exp = Wanderlist(user_id=this_user_id,
                                 exp_id=experience_id)
            db.session.add(new_exp)
            db.session.commit()
    return "success"


@app.route('/add_form', methods=["POST"])
def add_form():
    """
    Update the Experience table when users click on Submit button. Then
    I update the Booked table. I get the experience ID from AJAX and the user ID from session.
    """
    name = request.form.get("experience-name")
    city = request.form.get("city")
    date = request.form.get("date")
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
    description = request.form.get("description")
    category = request.form.get("category")

    new_exp = Experience(exp_name=name,
                         exp_city=city,
                         exp_start_datetime=date,
                         exp_description=description,
                         exp_category=category,
                         private=True)
    db.session.add(new_exp)
    db.session.commit()

    this_user_id = int(session.get('user_id'))
    exp_id = db.session.query(Experience.exp_id).filter(name == Experience.exp_name).one()[0]

    new_exp = Booked(user_id=this_user_id,
                     exp_id=exp_id)
    db.session.add(new_exp)
    db.session.commit()

    return redirect(url_for('user_page'))


@app.route('/list_form', methods=["POST"])
def list_form():
    """
    Update the Experience table when users click on Submit button. Then
    I update the Listed table. I get the experience ID from AJAX and the user ID from session.
    """
    name = request.form.get("experience-name")
    city = request.form.get("city")
    date = request.form.get("date")
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
    description = request.form.get("description")
    price = request.form.get("price")
    category = request.form.get("category")

    new_exp = Experience(exp_name=name,
                         exp_city=city,
                         exp_start_datetime=date,
                         exp_description=description,
                         exp_price=price,
                         exp_category=category,
                         private=False)
    db.session.add(new_exp)
    db.session.commit()

    this_user_id = int(session.get('user_id'))
    exp_id = db.session.query(Experience.exp_id).filter(name == Experience.exp_name).one()[0]

    new_exp = Listed(user_id=this_user_id,
                     exp_id=exp_id)
    db.session.add(new_exp)
    db.session.commit()

    return redirect(url_for('user_page'))


@app.route("/user")
def user_page():
    """Show info about user."""
    user_id = session['user_id']
    user = User.query.filter_by(user_id=user_id).first()

    exp_booked = db.session.query(Booked,Experience).filter(Booked.user_id==user_id).join(Experience).all()

    exp_wanderlisted = db.session.query(Wanderlist, Experience).filter(Wanderlist.user_id==user_id).join(Experience).all()

    exp_listed = db.session.query(Listed,Experience).filter(Listed.user_id==user_id).join(Experience).all()

    return render_template("user_page.html", user=user, exp_booked=exp_booked, exp_wanderlisted=exp_wanderlisted, exp_listed=exp_listed)


@app.route("/visualize")
def count_exp_in_category():
    """For user in session, count the number of booked experiences in each category"""

    this_user_id = session.get('user_id')

    if this_user_id:

        experience_booked = Booked.query.filter(Booked.user_id == this_user_id).all()
        print experience_booked
    category_ids = []
    for activity in experience_booked:

        category_ids.append(activity.experience.category.category_name)

    category_counter = Counter(category_ids)

    categories_to_count = category_counter.items()

    if request.args.get("data"):

        my_list = []

        for category in categories_to_count:
            my_list.append({"category": category[0], "cat_count": category[1]})
        return jsonify({"data": my_list})

    return render_template("donut.html")


if __name__ == "__main__":
    app.debug = False
    PORT = int(os.environ.get("PORT", 5000))

    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=PORT, host="0.0.0.0")