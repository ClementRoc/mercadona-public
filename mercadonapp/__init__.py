from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

from mercadonapp.views import home
from mercadonapp.views import catalog

app.register_blueprint(home.mod)
app.register_blueprint(catalog.mod)

# from mercadonapp.database import init_db
#
# init_db()
