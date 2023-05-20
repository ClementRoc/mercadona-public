from flask import Flask, render_template

"""
Define the application and fetch the configuration settings
"""

app = Flask(__name__)
app.config.from_object('config')

"""
ErrorHandlers for 404 and 500.
"""


@app.errorhandler(404)
def not_found(e):
    return render_template(
        'errors/404.html',
        error=e,
        title='Oupsi, un truc cloche !'
    )


@app.errorhandler(500)
def internal_error(e):
    return render_template(
        'errors/500.html',
        error=e,
        title='Problème serveur'
    )


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
