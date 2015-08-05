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
    email = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    user_instagram_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s>" % (self.user_id, self.username)


class Experience(db.Model):
    """Movie on ratings website."""

    __tablename__ = "experiences"

    experience_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    experience_name = db.Column(db.String(64))
    experience_date = db.Column(db.DateTime)
    

    #could i use this to link to other websites?:imdb_url = db.Column(db.String(200))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Movie movie_id=%s title=%s>" % (self.movie_id, self.title)


class Rating(db.Model):
    """Rating of a movie by a user."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    score = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
            self.rating_id, self.movie_id, self.user_id, self.score)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."