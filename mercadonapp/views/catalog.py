from flask import Blueprint, render_template

mod = Blueprint('catalog', __name__)


@mod.route('/catalog', methods=['GET'])
def catalog():
    return render_template(
        'catalog.html',
        title='Catalogue'
    )
