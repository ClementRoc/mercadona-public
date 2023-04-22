from flask import Blueprint, render_template
from mercadonapp.database import get_articles_data

mod = Blueprint('catalog', __name__)


@mod.route('/catalog', methods=['GET'])
def catalog():
    return render_template(
        'catalog.html',
        title='Catalogue',
        articles=get_articles_data()
    )
