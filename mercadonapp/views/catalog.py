from flask import Blueprint, render_template
from mercadonapp import internal_error
from mercadonapp.database import get_categories, fetch_articles


mod = Blueprint('catalog', __name__)

"""
Catalog page routing and variables
"""

@mod.route('/catalogue', methods=['GET'])
def catalog():
    try:
        return render_template(
            'catalog.html',
            title='Catalogue',
            categories=get_categories(),
            articles=fetch_articles()
        )
    except RuntimeError as e:
        return internal_error(e)
