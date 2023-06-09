import config

from mercadonapp import app, internal_error
from contentful import Client
from flask_sqlalchemy import SQLAlchemy

# from flask_migrate import Migrate


"""
Configuration's variables
"""

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
# migrate = Migrate(app, db)
client = Client(config.CONTENTFUL_SPACE_ID, config.CONTENTFUL_ACCESS_TOKEN)

"""
Initialize the database
"""


def init_db():
    with app.app_context():
        db.create_all()
        fetch_articles()
        # migrate.init_app(app, db)


"""
Article class to define the table in SQL
"""


class Article(db.Model):
    __tablename__ = "article"

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    product = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String, nullable=False)
    filters = db.relationship('Filter', backref='article')
    tags = db.relationship('Tag', backref='article')
    categories = db.Column(db.String, nullable=False)
    subcategories = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    promotion_percentage = db.Column(db.Integer, nullable=True)
    promoted_price = db.Column(db.Float, nullable=True)
    promotion_start = db.Column(db.String, nullable=True)
    promotion_end = db.Column(db.String, nullable=True)

    def __init__(self, image, brand, product, description, filters, tags, categories, subcategories, price,
                 promotion_percentage, promoted_price, promotion_start, promotion_end):
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


"""
Filter class to define the table in SQL
"""


class Filter(db.Model):
    __tablename__ = "filter"

    id = db.Column(db.Integer, primary_key=True)
    classe = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __init__(self, classe, name):
        self.classe = classe
        self.name = name


"""
Tag class to define the table in SQL
"""


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __init__(self, name):
        self.name = name


"""
Fetch the articles on Contentful and put them all in an Array
Hydrate the database with the tables below and return the articles.
"""


def fetch_articles():
    try:
        articles = client.entries(
            query={
                'content_type': 'article'
            }
        )
    except (KeyError, TypeError) as e:
        return internal_error(e)

    articles_list = []

    for entry in articles:
        article = {
            'image': entry.image.url(),
            'brand': entry.brand.upper(),
            'product': entry.product,
            'description': entry.description,
            'categories': entry.categories.name,
            'subcategories': entry.subcategories.name,
            'filters': [],
            'tags': [],
            'price': entry.price,
        }

        if hasattr(entry, 'filters'):
            for filter_name in entry.filters:
                if filter_name == 'Frais':
                    f = Filter('cold', 'FRAIS')
                    article['filters'].append(f)
                elif filter_name == 'Surgelé':
                    f = Filter('frozen', 'GEL')
                    article['filters'].append(f)
                elif filter_name == 'Bio':
                    f = Filter('bio', 'BIO')
                    article['filters'].append(f)
        else:
            article['filters'] = []

        if hasattr(entry, 'tags'):
            for tag in entry.tags:
                t = Tag(tag)
                article['tags'].append(t)
        else:
            article['tags'] = []

        if hasattr(entry, 'promotion'):
            article['promotion_percentage'] = entry.promotion.percentage
            article['promoted_price'] = round(
                article['price'] - round((article['price'] / 100 * entry.promotion.percentage),
                                         2), 2)
            article['promotion_start'] = str(entry.promotion.start.day) + '/' + str(
                '{:02d}'.format(entry.promotion.start.month))
            article['promotion_end'] = str(entry.promotion.end.day) + '/' + str(
                '{:02d}'.format(entry.promotion.start.month))
            f = Filter('promotion', '-' + str(entry.promotion.percentage) + '%')
            article['filters'].append(f)
        else:
            article['promotion_percentage'] = None
            article['promoted_price'] = None
            article['promotion_start'] = None
            article['promotion_end'] = None

        articles_list.append(article)

    hydrate_articles(articles_list)

    return Article.query.all()


"""
Hydrate the articles, turn the Array into an Article class
"""


def hydrate_articles(articles):
    for article in articles:
        article_database = Article.query.filter_by(product=article['product']).first()

        if not article_database:
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

        elif article_database in Article.query.all():
            article_database.image = article['image']
            article_database.brand = article['brand']
            article_database.product = article['product']
            article_database.description = article['description']
            article_database.filters = article['filters']
            article_database.tags = article['tags']
            article_database.categories = article['categories']
            article_database.subcategories = article['subcategories']
            article_database.price = article['price']
            article_database.promotion_percentage = article['promotion_percentage']
            article_database.promoted_price = article['promoted_price']
            article_database.promotion_start = article['promotion_start']
            article_database.promotion_end = article['promotion_end']

    return db.session.commit()


"""
Get all the categories on Contentful
Return an Array
"""


def get_categories():
    try:
        categories = client.entries(
            query={
                'content_type': 'categories'
            }
        )
    except (KeyError, TypeError) as e:
        return internal_error(e)

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
