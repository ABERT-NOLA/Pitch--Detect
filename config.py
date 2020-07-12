class Config(object):
    DEBUG = True
    DEVELOPMENT = True 
    SQLALCHEMY_DATABASE_URI = "postgresql://pitch:password@localhost:5432/pitch"
    SQLALCHEMY_TRACK_MODIFICATIONS = False