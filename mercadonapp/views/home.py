from flask import Blueprint, render_template

mod = Blueprint('home', __name__)


@mod.route('/', methods=['GET'])
def home():
    return render_template(
        'home.html',
        title='Mercadona - Plus de 100 promotions'
    )
