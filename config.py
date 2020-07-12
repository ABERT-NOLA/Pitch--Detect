class Config(object):
    """
    Default configuration
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://admin:admin@localhost:5432/pitch"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

    UPLOADED_PHOTOS_DEST = 'app/static/photos'


class ProdConfig(Config):
    """
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    """
    pass


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
