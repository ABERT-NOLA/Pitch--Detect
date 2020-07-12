from  app import db
from werkzeug.security import generate_password_hash,check_password_hash
#...

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'owner',lazy="dynamic")
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    pass_secure = db.Column(db.String(255))
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

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

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'Role {self.name}'
