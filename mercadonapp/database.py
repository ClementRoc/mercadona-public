import json
import config

from mercadonapp import app
from contentful import Client
from flask_sqlalchemy import SQLAlchemy
from psycopg2.extensions import register_adapter, AsIs


def adapt_dict(dict_var):
    return AsIs("'" + json.dumps(dict_var) + "'")


register_adapter(dict, adapt_dict)

db = SQLAlchemy(app)


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()


client = Client(config.CONTENTFUL_SPACE_ID, config.CONTENTFUL_ACCESS_TOKEN)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    product = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String, nullable=False)
    filters = db.relationship('filter', backref='article')
    tags = db.relationship('tag', backref='article')
    categories = db.Column(db.String, nullable=False)
    subcategories = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    promotion_percentage = db.Column(db.Integer, nullable=True)
    promoted_price = db.Column(db.Float, nullable=True)
    promotion_start = db.Column(db.String, nullable=True)
    promotion_end = db.Column(db.String, nullable=True)

    def __init__(self, image, brand, product, description, filters, tags, categories, subcategories, price, promotion_percentage, promoted_price, promotion_start, promotion_end):
        self.image = image
        self.brand = brand
        self.product = product
        self.description = description
        self.filters = filters
        self.tags = tags
        self.categories = categories
        self.subcategories = subcategories
        self.price = price
        self.promotion_percentage = promotion_percentage
        self.promoted_price = promoted_price
        self.promotion_start = promotion_start
        self.promotion_end = promotion_end


class Filter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classe = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __init__(self, classe, name):
        self.classe = classe
        self.name = name


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __init__(self, name):
        self.name = name


def fetch_articles():
    articles = client.entries(
        query={
            'content_type': 'article'
        }
    )

    articles_list = []

    for entry in articles:
        article = {
            'image': entry.image.url(),
            'brand': entry.brand.upper(),
            'product': entry.product,
            'description': entry.description,
            'categories': [],
            'subcategories': [],
            'filters': [],
            'price': entry.price,
        }

        if hasattr(entry, 'filters'):
            for filter_name in entry.filters:
                if filter_name == 'Frais':
                    f = {'class': 'cold', 'name': 'FRAIS'}
                    article['filters'].append(f)
                elif filter_name == 'Surgelé':
                    f = {'class': 'frozen', 'name': 'GEL'}
                    article['filters'].append(f)
                elif filter_name == 'Bio':
                    f = {'class': 'bio', 'name': 'BIO'}
                    article['filters'].append(f)
        else:
            article['filters'] = []

        for category in entry.categories:
            article['categories'].append(category.name)

        for subcategory in entry.subcategories:
            article['subcategories'].append(subcategory.name)

        if hasattr(entry, 'tags'):
            article['tags'] = entry.tags
        else:
            article['tags'] = None

        if hasattr(entry, 'promotion'):
            article['promotion_percentage'] = entry.promotion.percentage
            article['promoted_price'] = article['price'] - round((article['price'] / 100 * entry.promotion.percentage),
                                                                 2)
            article['promotion_start'] = str(entry.promotion.start.day) + '/' + str(
                '{:02d}'.format(entry.promotion.start.month))
            article['promotion_end'] = str(entry.promotion.end.day) + '/' + str(
                '{:02d}'.format(entry.promotion.start.month))
            f = {'class': 'promotion', 'name': '-' + str(entry.promotion.percentage) + '%'}
            article['filters'].append(f)
        else:
            article['promotion_percentage'] = None
            article['promoted_price'] = None
            article['promotion_start'] = None
            article['promotion_end'] = None

        articles_list.append(article)

    return articles_list


def get_articles():
    articles = fetch_articles()

    for article in articles:
        a = Article(
            article['image'],
            article['brand'],
            article['product'],
            article['description'],
            article['filters'],
            article['tags'],
            article['categories'],
            article['subcategories'],
            article['price'],
            article['promotion_percentage'],
            article['promoted_price'],
            article['promotion_start'],
            article['promotion_end']
        )

        db.session.add(a)
        db.session.commit()

    return Article.query.all()


def get_categories():
    categories = client.entries(
        query={
            'content_type': 'categories'
        }
    )

    categories_list = []

    for entry in categories:
        category = {
            'name': entry.name,
            'subcategories': []
        }

        for subcategory in entry.subcategories:
            category['subcategories'].append(subcategory.name)

        categories_list.append(category)

    return categories_list
