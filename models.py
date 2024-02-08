from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Feedback(db.Model):
    """User feedback"""
    
    __tablename__ = "feedbacks"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))
    

class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), nullable=False,  unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name =  db.Column(db.String(30), nullable=False)
    
    feedback = db.relationship('Feedback', backref="users", cascade="all,delete")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user with hashed password & return user."""
        
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(username=username, 
                   password=hashed_utf8,
                   email=email, 
                   first_name=first_name, 
                   last_name=last_name
        )
        
        return user
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists and password is correct.
           return user if valid, else return False."""
        
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        
        

    
    