import os

class Config(object):
    #This is the parent configuration class
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    ENV = 'development'
    TESTING = False


class DevelopmentConfig(Config):
    #create configurations for development
    DEBUG = True
    url = "dbname='store_manager_v2' host='127.0.0.1' port='5432' user='catherine_store' password='admin'"
    os.environ['ENV'] = 'development' #exposes this DevelopmentConfig to the entire application


class TestingConfig(Config):
    #configurations for testing
    DEBUG = True
    url = "dbname='store_tests' host='127.0.0.1' port='5432' user='catherine_store' password='admin'"
    os.environ['ENV'] = 'testing' #exposes this TestingConfig to the entire application

class StagingConfig(Config):
    #configurations for staging
    DEBUG = True


class ProductionConfig(Config):
    #configurations for production
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}


secret_key = Config.SECRET_KEY
