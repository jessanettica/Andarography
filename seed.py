"""Utility file to seed experience database from data in seed_data/"""

#LOOK OVER THIS WHOLE FILE

import datetime
import requests

from model import connect_to_db, db, Experience, User, Booked, Provider, Wanderlist, Category, Venue
#names of model classes
from server import app
import os


def load_categories():
    """Load categories from u.categories into database"""

    print "Categories"

    for i, row in enumerate(open("seed_data/u.categories")):
        row = row.rstrip()

        category_id, category_name = row.split("|")

        category = Category(category_id=category_id, category_name=category_name)

        db.session.add(category)

        if i % 100 == 0:
            print i

    db.session.commit()


def load_experiences():
    """Load movies from u.experiences into database."""

    print "Experiences"

    for i, row in enumerate(open("seed_data/u.experiences")):
        row = row.rstrip()

        exp_name, exp_category, exp_city, exp_startdate, exp_enddate, exp_starttime, exp_endtime, exp_description, exp_currency, exp_price, exp_address_line1, exp_address_line2, exp_address_city, exp_address_region, exp_address_country, exp_address_zipcode, exp_provider_name, exp_provider_contact = row.split("|")

        if exp_startdate:
            exp_startdate = datetime.datetime.strptime(exp_startdate, "%d-%m-%Y")
        else:
            exp_startdate = None

        experience = Experience(exp_name=exp_name, exp_category=exp_category, exp_city=exp_city, exp_startdate=exp_startdate,
                                exp_enddate=exp_enddate, exp_starttime=exp_starttime,
                                exp_endtime=exp_endtime, exp_description=exp_description,
                                exp_currency=exp_currency, exp_price=exp_price, exp_address_line1=exp_address_line1,
                                exp_address_line2=exp_address_line2, exp_address_city=exp_address_city, exp_address_region=exp_address_region,
                                exp_address_country=exp_address_country, exp_address_zipcode=exp_address_zipcode,
                                exp_provider_name=exp_provider_name, exp_provider_contact=exp_provider_contact)

        db.session.add(experience)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    db.session.commit()


def get_provider(organizer_id_sf):
    token = os.environ.get('EVENTBRITE_TOKEN')
    """Add an Eventbrite provider to  db """
    # TODO: Check db for existing organizer ids
    params = {'token': token}
    request_url = "https://www.eventbriteapi.com/v3/organizers/"+organizer_id_sf

    if organizer_id_sf in db:
        pass
    else:
        organizer_request = requests.get(request_url, params=params)

        organizer_info = organizer_request.json()
        organizer_name = organizer_info['name']
        organizer_url = organizer_info['url']

        provider = Provider(exp_provider_name=organizer_name, exp_provider_url=organizer_url)

        db.session.add(provider)

        db.session.commit()

    return "YAY"


def get_venue(venue_id_sf):
    token = os.environ.get('EVENTBRITE_TOKEN')
    """Add an Eventbrite venue to db"""

    params = {'token': token}
    request_url = "https://www.eventbriteapi.com/v3/venues/"+venue_id_sf

    if venue_id_sf in db:
        pass
    else:
        venue_request = requests.get(request_url, params=params)

        venue = venue_request.json()['address']
        print "Venue", venue
        address_line1 = venue.get('address_1', None)
        print "Address Line 1", address_line1
        address_line2 = venue.get('address_2', None)
        address_city = venue.get('city', None)
        address_region = venue.get('region', None)
        address_country = venue.get('country', None)
        address_zipcode = venue.get('postal_code', None)

        venue = Venue(exp_address_line1=address_line1, exp_address_line2=address_line2, exp_address_city=address_city, exp_address_region=address_region, exp_address_country=address_country, exp_address_zipcode=address_zipcode)

        db.session.add(venue)

        db.session.commit()


def sf_experience(category):
    token = os.environ.get('EVENTBRITE_TOKEN')
    """Show Eventbrite experiences available in SF"""
    params = {'token': token, 'venue.city': 'San Francisco', 'categories': category}
    r = requests.get('https://www.eventbriteapi.com/v3/events/search/', params=params)
    events = r.json()['events']

    for event in events:

        print "Currently working on event:", event

        event_name = event.get('name').get('text')
        event_description = event.get('description').get('text')
        event_start_datetime = datetime.datetime.strptime(event.get('start').get('local'), "%Y-%m-%dT%H:%M:%S")
        event_end_datetime = datetime.datetime.strptime(event.get('end').get('local'), "%Y-%m-%dT%H:%M:%S")
        event_category = category
        event_city = "San Francisco"

        event_id_sf = event.get('id')
        venue_id_sf = event.get('venue_id')
        organizer_id_sf = event.get('organizer_id')

        params = {'token': token}
        request_url = "https://www.eventbriteapi.com/v3/events/"+event_id_sf+"/ticket_classes"
        ticket_class_request = requests.get(request_url, params=params)
        tickets = ticket_class_request.json()['ticket_classes']

        for ticket in tickets:
            if ticket is None:
                continue
            if ticket.get('fee') is None:
                continue
            ticket_price = ticket.get('fee').get('display')
            ticket_currency = ticket.get('fee').get('currency')

        new_experience = Experience(exp_name=event_name,
                                    exp_category=event_category,
                                    exp_city=event_city,
                                    exp_start_datetime=event_start_datetime,
                                    exp_end_datetime=event_end_datetime,
                                    exp_description=event_description,
                                    exp_currency=ticket_currency,
                                    exp_price=ticket_price,
                                    exp_venue_id=venue_id_sf,
                                    exp_provider_id=organizer_id_sf)

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
