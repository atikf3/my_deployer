import os


__author__ = 'talamo_a'


class Config:
    FLASK_ENV = os.getenv('API_ENV')
    FLASK_APP = os.getenv("API_NAME")
    FLASK_DEBUG = os.getenv("API_DBG")
