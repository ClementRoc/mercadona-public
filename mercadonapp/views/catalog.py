from flask import Blueprint, render_template
from mercadonapp.database import get_categories, get_articles


mod = Blueprint('catalog', __name__)


@mod.route('/catalog', methods=['GET'])
def catalog():
    return render_template(
        'catalog.html',
        title='Catalogue',
        categories=get_categories(),
        articles=get_articles()
    )
