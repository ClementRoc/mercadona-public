from flask import Blueprint, render_template
from mercadonapp import internal_error
from mercadonapp.database import get_categories

mod = Blueprint('home', __name__)


"""
Homepage routing and variables
"""

@mod.route('/', methods=['GET'])
def home():
    try:
        return render_template(
            'home.html',
            title='Mercadona - Plus de 100 promotions',
            categories=get_categories()
        )
    except RuntimeError as e:
        return internal_error(e)
