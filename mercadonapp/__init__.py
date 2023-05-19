from flask import Flask

"""
Define the application and fetch the configuration settings
"""

app = Flask(__name__)
app.config.from_object('config')

"""
Get the routing
"""

from mercadonapp.views import home
from mercadonapp.views import catalog

app.register_blueprint(home.mod)
app.register_blueprint(catalog.mod)

"""
Initialize the database
"""

from mercadonapp.database import init_db

init_db()
