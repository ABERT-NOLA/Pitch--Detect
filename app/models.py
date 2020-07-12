from  app import db

#...

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'owner',lazy="dynamic")
    def __repr__(self):
        return f'User {self.username}'

class Pitch(db.Model):
    __tablename__ = 'pitch'
    id = db.Column(db.Integer,primary_key = True)
    filepath = db.Column(db.String(255))
    name = db.Column(db.String(50))
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # pitch = Pitch()
    # you have access to pitch.owner


    def __repr__(self):
        return f'Pitch {self.name}'
