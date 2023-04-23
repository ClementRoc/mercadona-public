from flask import Blueprint, render_template
from mercadonapp.database import fetch_articles

mod = Blueprint('catalog', __name__)


@mod.route('/catalog', methods=['GET'])
def catalog():
    return render_template(
        'catalog.html',
        title='Catalogue',
        articles=fetch_articles()
    )
