from . import db

class UserProfile(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=False)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    biography = db.Column(db.Text)
    image = db.Column(db.String(255))
    created_on = db.Column(db.String(80))
    
    def __init__(self, userid, fname, lname, username, age, gender, biography, imagename, created):
        self.userid = userid
        self.fname = fname
        self.lname = lname
        self.username = username
        self.age = age
        self.gender = gender
        self.biography = biography
        self.image = imagename
        self.created_on = created
    
    

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)