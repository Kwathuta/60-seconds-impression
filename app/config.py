import os


class Config:
    """
    General parent configuration class
    """

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://moringa:aljokela7247@localhost/impression"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """
    Production configuration child class
    Args:
        Config: The parent configuration class with Generl configuration settings
    """


class DevConfig(Config):
    """
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    """

    DEBUG = True


config_options = {"development": DevConfig, "production": ProdConfig}
