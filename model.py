"""Models and database functions for Andar"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_firstname = db.Column(db.String(64))
    user_lastname = db.Column(db.String(64), nullable=True)
    user_email = db.Column(db.String(64))
    user_instagram = db.Column(db.String(64), nullable=True)
    user_city = db.Column(db.String(64), nullable=True)
    user_password = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s>" % (self.user_id, self.user_email)


class Experience(db.Model):
    """Experiences and activities offered."""

    __tablename__ = "experiences"

    exp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    eventbrite_event_id = db.Column(db.Integer)
    exp_name = db.Column(db.String(64))
    exp_city = db.Column(db.String(64))
    exp_start_datetime = db.Column(db.DateTime)
    exp_end_datetime = db.Column(db.DateTime)
    exp_description = db.Column(db.String(400), nullable=True)
    exp_currency = db.Column(db.String(4))
    exp_price = db.Column(db.Integer, nullable=True)
    exp_category = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    exp_venue_id = db.Column(db.Integer, db.ForeignKey('venues.exp_venue_id'))
    exp_provider_id = db.Column(db.Integer, db.ForeignKey('providers.exp_provider_id'))

    category = db.relationship("Category", backref=db.backref("experiences", order_by=exp_id))

    provider = db.relationship("Provider", backref=db.backref("experiences", order_by=exp_id))

    venue = db.relationship("Venue", backref=db.backref("experiences", order_by=exp_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        #repr no longer includes names, because some names have special unicode characters
        return "<Experience exp_id=%s exp_category=%s>" % (self.exp_id, self.exp_category)


class Provider(db.Model):
    """Information about experience and activity providers."""

    __tablename__ = "providers"

    exp_provider_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    eventbrite_provider_id = db.Column(db.Integer)
    exp_provider_name = db.Column(db.String(50))
    exp_provider_url = db.Column(db.String(200), nullable=True)
    exp_provider_contact = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        #repr no longer includes names, because some names have special unicode characters
        return "<Provider provider_id=%s>" % (
            self.exp_provider_id)


class Venue(db.Model):
    """Information about venues where the experiences and activities are located."""

    __tablename__ = "venues"

    exp_venue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    eventbrite_venue_id = db.Column(db.Integer)
    exp_address_line1 = db.Column(db.String(250))
    exp_address_line2 = db.Column(db.String(250), nullable=True)
    exp_address_city = db.Column(db.String(200))
    exp_address_region = db.Column(db.String(50), nullable=True)
    exp_address_country = db.Column(db.String(250))
    exp_address_zipcode = db.Column(db.String(10))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Venue venue_id=%s venue_address_line1=%s" % (
            self.exp_venue_id, self.exp_address_line1)


class Booked(db.Model):
    """Experiences booked by a user."""

    __tablename__ = "booked"

    booked_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    exp_id = db.Column(db.Integer, db.ForeignKey('experiences.exp_id'))

    user = db.relationship("User", backref=db.backref("booked", order_by=booked_id))

    experience = db.relationship("Experience", backref=db.backref("booked", order_by=booked_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Booked booked_id=%s user_id=%s exp_id=%s " % (
            self.booked_id, self.user_id, self.exp_id)


class Wanderlist(db.Model):
    """Experiences bookmarked by a user."""

    __tablename__ = "wanderlist"

    wander_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    exp_id = db.Column(db.Integer, db.ForeignKey('experiences.exp_id'))

    user = db.relationship("User",
                           backref=db.backref("wanderlist", order_by=wander_id))

    experience = db.relationship("Experience", backref=db.backref("wanderlist", order_by=wander_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Wanderlist wander_id=%s user_id=%s exp_id=%s " % (
            self.wander_id, self.user_id, self.exp_id)


class Category(db.Model):
    """Categories for experiences and activities."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s category_name " % (
            self.category_id, self.category_name)


# class City(db.Model):
#     """Cities available to search."""

#     __tablename__ = "cities"

#     city_id = db.Column(db.Integer, primary_key=True)
#     city_name = db.Column(db.String(64), nullable=True)
#     country_name = db.Column(db.String(64), nullable=True)

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<City city_id=%s city_name " % (
#             self.city_id, self.city_name

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///andar.db'
    db.app = app
    #connecting my model and my database
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."