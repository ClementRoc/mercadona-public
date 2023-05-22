import os

_basedir = os.path.abspath(os.path.dirname(__file__))


# DEV ENV
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'username')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'password')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'host')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'name')

SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

CONTENTFUL_SPACE_ID = 'Space ID here'
CONTENTFUL_ACCESS_TOKEN = 'Access Token here'

del os
