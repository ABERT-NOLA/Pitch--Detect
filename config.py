class Config(object):
    """
    Default configuration
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://pitch:password@localhost:5432/pitch"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ""
    SENDER_MAIL_USERNAME = ""
    MAIL_PASSWORD = ""

    UPLOADED_PHOTOS_DEST = 'app/static/uploads/photos'
    UPLOADED_AUDIO_DEST = 'app/static/uploads/audio'


class ProdConfig(Config):
    """
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):
    """
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    """

    DEBUG = True
    DEVELOPMENT = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}
