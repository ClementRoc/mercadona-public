from flask import Blueprint, render_template
from mercadonapp.database import fetch_articles, get_categories


mod = Blueprint('catalog', __name__)


@mod.route('/catalog', methods=['GET'])
def catalog():
    return render_template(
        'catalog.html',
        title='Catalogue',
        categories=get_categories(),
        articles=fetch_articles()
    )
