"""Utility file to seed experience database from data in seed_data/"""

#LOOK OVER THIS WHOLE FILE




import datetime
import requests

from model import connect_to_db, db, Experience, User, Booked, Provider, Wanderlist #names of model classes
from server import app
import os

# def load_users():
#     """Load users from User class into database."""

#     print "Users"

#     for i, row in enumerate(open("seed_data/u.user")):
#         row = row.rstrip()
#         user_id, age, gender, occupation, zipcode = row.split("|")

#         user = User(user_id=user_id,
#                     age=age,
#                     zipcode=zipcode)

#         db.session.add(user)

#         # provide some sense of progress
#         if i % 100 == 0:
#             print i

#     db.session.commit()


def load_experiences():
    """Load movies from u.experiences into database."""

    print "Experiences"

    for i, row in enumerate(open("seed_data/u.experiences")):
        
        row = row.rstrip()

        exp_name, exp_category, exp_city, exp_startdate, exp_enddate, exp_starttime, exp_endtime, exp_description, exp_currency, exp_price, exp_address_line1, exp_address_line2, exp_address_city, exp_address_region, exp_address_country, exp_address_zipcode, exp_provider_name, exp_provider_contact = row.split("|")

        # The date is in the file as daynum-month_abbreviation-year;
        # we need to convert it to an actual datetime object.

        if exp_startdate:
            exp_startdate = datetime.datetime.strptime(exp_startdate_str, "%d-%b-%Y")
        else:
            exp_startdate = None

        experience = Experience(exp_name=exp_name, exp_category=exp_category,exp_city=exp_city, exp_startdate=exp_startdate, 
                                exp_enddate=exp_enddate, exp_starttime=exp_starttime,
                                exp_endtime=exp_endtime, exp_description=exp_description,
                                exp_currency=exp_currency, exp_price=exp_price, exp_address_line1=exp_address_line1,
                                exp_address_line2=exp_address_line2, exp_address_city=exp_address_city, exp_address_region=exp_address_region,
                                exp_address_country=exp_address_country, exp_address_zipcode=exp_address_zipcode, 
                                exp_provider_name=exp_provider_name, exp_provider_contact=exp_provider_contact)

        # We need to add to the session or it won't ever be stored
        db.session.add(experience)

        # provide some sense of progress
        if i % 100 == 0:
            print i


    db.session.commit()

def get_provider(provider_id):
    # This is where you'd add a provider to your db
    pass

def get_venue(venue_id):
    # This is where you'd add a venue to your db
    pass

def sf_experience(category):
    token = os.environ.get('EVENTBRITE_TOKEN')
    """Show Eventbrite experiences available in SF"""
    params = {'token': token, 'venue.city': 'San Francisco', 'categories': category}
    r = requests.get('https://www.eventbriteapi.com/v3/events/search/', params=params)
    events=r.json()['events']

    for event in events:
        # print "Currently working on event:", event

        event_name = event.get('name').get('text')
        event_description = event.get('description').get('text') 
        event_start_datetime = datetime.datetime.strptime(event.get('start').get('local'), "%Y-%m-%dT%H:%M:%S")
        # print event_start_datetime
        event_end_datetime = datetime.datetime.strptime(event.get('end').get('local'), "%Y-%m-%dT%H:%M:%S")
        # print event_end_datetime
        # event_start_date = event.get('start').get('local').split("T")[0] #gets the start date of the event in year-month-day format
        # print "Event Start Date", event_start_date
        # event_start_time = event.get('start').get('local').split("T")[1]
        # print "Event Start Time", event_start_time
        # event_end_date = event.get('end').get('local').split("T")[0]
        # print "Event End Date", event_end_date
        # event_end_time = event.get('end').get('local').split("T")[1]
        # print "Event End Time", event_end_time
        event_category = "Food & Drinks"
        event_city = "San Francisco"

        event_id_sf = event.get('id')
        venue_id_sf = event.get('venue_id')
        organizer_id_sf = event.get('organizer_id')



        params = {'token': token}
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

        # if venue_id in db:
        #     do nothing
        # else:
        #     get_venue(venue_id)
        # move this stuff to get_venue()
        params = {'token': token}
        request_url = "https://www.eventbriteapi.com/v3/venues/"+venue_id_sf
        venue_request = requests.get(request_url, params=params)

        venue=venue_request.json()['address']
        print "Venue", venue

        # for venue in venues:
        #     address_line1 = venues['address_1']
        #     address_line2 = venues['address_2']
        #     address_city = venues['city']
        #     address_region = venues['region']
        #     address_country = venues['country']
        #     address_zipcode = venues['postal_code']

        # there might be some venues that are missing some of these fields, which will
        # cause a KeyError. Maybe use .get()?
        # address_line1 = venue.get('address_1', None)

        address_line1 = venue['address_1']
        print "Address Line 1", address_line1
        address_line2 = venue['address_2']
        address_city = venue['city']
        address_region = venue['region']
        address_country = venue['country']
        address_zipcode = venue['postal_code']

        # TODO Build more structure around this to minimized API queries. Check db
        # for existing organizer ids
        params = {'token': token}
        request_url = "https://www.eventbriteapi.com/v3/organizers/"+organizer_id_sf
        organizer_request = requests.get(request_url, params=params)

        organizer_info=organizer_request.json()
        organizer_name=organizer_info['name']
        organizer_url=organizer_info['url']


        new_experience = Experience(exp_name=event_name, exp_category=event_category, exp_city = event_city, 
                                exp_start_datetime=event_start_datetime, 
                                exp_end_datetime=event_end_datetime, exp_description=event_description,
                                exp_currency=ticket_currency, exp_price=ticket_price, exp_address_line1=address_line1,
                                exp_address_line2=address_line2, exp_address_city=address_city, exp_address_region=address_region,
                                exp_address_country=address_country, exp_address_zipcode=address_zipcode)

        db.session.add(new_experience)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # load_users()
    # load_movies()
    # load_ratings()
    sf_experience(110)
    # sf_experience(108)
