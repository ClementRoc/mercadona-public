import os

_basedir = os.path.abspath(os.path.dirname(__file__))

APP_ENV = os.getenv('APP_ENV', 'development')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'postgres')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'Panribou1')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'postgres')

SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

CONTENTFUL_SPACE_ID = 'ivu7p66elrjd'
CONTENTFUL_ACCESS_TOKEN = 'DQPKTv3cLkLLYkiZdubD4vrLAQgy0q1tVpepW3mbSKM'
# CONTENTFUL_MANAGEMENT_ACCESS_TOKEN = 'CFPAT-0txYVnkTk_rekQy1_bdHjFJDaFWQ8KtiqpKM4g0WpdI'

del os
