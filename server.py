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

    #return render_template("homepage.html")

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
    #return redirect("/")

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    #return render_template("login_form.html")

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
    #return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    #return redirect("/")

@app.route("/howitworks")
def howitworks():
    """Explain the path of the user through the web app"""

    #return render_template("howitworks.html")

@app.route("/experience_sf")
def sf_experience():
    """Show Eventbrite experiences available in SF"""
    params = {'token': 'MEPMC6UJ5E5BE5L5DKIH', 'venue.city': 'San Francisco', 'categories': '110'}
    r = requests.get('https://www.eventbriteapi.com/v3/events/search/', params=params)
    events=r.json()['events']

    for event in events:
        event_name = event.get('name').get('text')
        event_description = event.get('description').get('text') 
        event_start_date = event.get('start').get('local').split("T")[0] #gets the start date of the event in year-month-day format
        event_start_time = event.get('start').get('local').split("T")[1]
        event_end_date = event.get('end').get('local').split("T")[0]
        event_end_time = event.get('end').get('local').split("T")[1]
        event_category = "Food & Drinks"
        event_city = "San Francisco"

        event_id_sf = event.get('id')
        venue_id_sf = event.get('venue_id')
        organizer_id_sf= = event.get('organizer_id')



        params = {'token': 'MEPMC6UJ5E5BE5L5DKIH'}
        request_url = "https://www.eventbriteapi.com/v3/events/"+event_id_sf+"/ticket_classes"
        ticket_class_request= requests.get(request_url, params=params)
            
        tickets=ticket_class_request.json()['ticket_classes']
            
        for ticket in tickets:
            if ticket == None:
                continue
            if ticket.get('fee')==None:
                continue
            ticket_price = ticket.get('fee').get('display')
            ticket_currency = ticket.get('fee').get('currency')



        params = {'token': 'MEPMC6UJ5E5BE5L5DKIH'}
        request_url = "https://www.eventbriteapi.com/v3/venues/"+venue_id_sf
        venue_request = requests.get(request_url, params=params)

        venues=venue_request.json()['address']

        for venue in venues:
            address_line1 = venues['address_1']
            address_line2 = venues['address_2']
            address_city = venues['city']
            address_region = venues['region']
            address_country = venues['country']
            address_zipcode = venues['postal_code']

        params = {'token': 'MEPMC6UJ5E5BE5L5DKIH'}
        request_url = "https://www.eventbriteapi.com/v3/organizers/"+organizer_id_sf
        organizer_request = requests.get(request_url, params=params)

        # organizers=venue_request.json()['name']
        # organizers=venue_request.json()['url']

        # for venue in venues:
        #     address_line1 = venues['address_1']
        #     address_line2 = venues['address_2']
        #     address_city = venues['city']
        #     address_region = venues['region']
        #     address_country = venues['country']
        #     address_zipcode = venues['postal_code']



    print "The last event details: "
    print event_name

        new_experience = Experience(exp_name=event_name, exp_category=event_category, exp_city = event_city, exp_startdate=event_start_date, 
                                exp_enddate=event_end_date, exp_starttime=event_start_time,
                                exp_endtime=event_end_time, exp_description=event_description,
                                exp_currency=ticket_currency, exp_price=ticket_price, exp_address_line1=address_line1,
                                exp_address_line2=address_line2, exp_address_city=address_city, exp_address_region=address_region,
                                exp_address_country=address_country, exp_address_zipcode=address_zipcode, 
                                exp_provider_name=event_provider_name, exp_provider_contact=event_provider_contact)


#     new_experience= Experience( tables name = above variable name, for all of them
#     )

    db.session.add(new_experience)
db.session.commit()


# python -i model.py
# >>>db.create_all()
# exit
# run server.py



    return 'success'




@app.route("/user/<int:user_id>")
def user_page():
    """Display the user's data"""

    #requests for info go here

    #return render_template("user_page.html")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    #connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()