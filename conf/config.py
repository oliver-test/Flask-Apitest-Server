import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
   #本地环境
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret'
    # DB_HOST = '127.0.0.1'
    # DB_USER = 'root'
    # DB_PASSWD = '11111111'
    # DB_DATABASE = 'education'
    # ITEMS_PER_PAGE = 10

    #线上环境  
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret'
    DB_HOST = '39.107.92.144'
    DB_USER = 'root'
    DB_PASSWD = 'qweqwe123'
    DB_DATABASE = 'education'
    ITEMS_PER_PAGE = 10
    
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
