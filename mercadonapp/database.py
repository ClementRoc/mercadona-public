import config

from mercadonapp import app
from contentful import Client
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy(app)

client = Client(config.CONTENTFUL_SPACE_ID, config.CONTENTFUL_ACCESS_TOKEN)


# def init_db():
#     with app.app_context():
#         db.drop_all()
#         db.create_all()
#         db.session.commit()


# class Article(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     image = db.Column(db.String, nullable=False)
#     brand = db.Column(db.String(50), nullable=False)
#     product = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.String, nullable=False)
#     filters = db.Column(db.String, nullable=False)
#     tags = db.Column(db.String, nullable=True)
#     categories = db.Column(db.String, nullable=False)
#     subcategories = db.Column(db.String, nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     promotion_percentage = db.Column(db.Integer, nullable=False)
#     promotion_start = db.Column(db.Date, nullable=False)
#     promotion_end = db.Column(db.Date, nullable=False)
#
#     def __init__(self, image, brand, product, description, filters, tags, categories, subcategories, price,
#                  promotion_percentage, promotion_start, promotion_end):
#         self.image = image
#         self.brand = brand
#         self.product = product
#         self.description = description
#         self.filters = filters
#         self.tags = tags
#         self.categories = categories
#         self.subcategories = subcategories
#         self.price = price
#         self.promotion_percentage = promotion_percentage
#         self.promotion_start = promotion_start
#         self.promotion_end = promotion_end


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

        for filter_name in entry.filters:
            if filter_name == 'Frais':
                f = {'class': 'cold', 'name': 'FRAIS'}
                article['filters'].append(f)
            elif filter_name == 'Surgelé':
                f = {'class': 'cold', 'name': 'GEL'}
                article['filters'].append(f)
            elif filter_name == 'Bio':
                f = {'class': 'cold', 'name': 'BIO'}
                article['filters'].append(f)

        for category in entry.categories:
            article['categories'].append(category.name)

        for subcategory in entry.subcategories:
            article['subcategories'].append(subcategory.name)

        if hasattr(entry, 'tags'):
            article['tags'] = entry.tags

        if hasattr(entry, 'promotion'):
            article['promotion_percentage'] = entry.promotion.percentage
            article['promoted_price'] = article['price'] - round((article['price']/100 * entry.promotion.percentage), 2)
            article['promotion_start'] = str(entry.promotion.start.day) + '/' + str('{:02d}'.format(entry.promotion.start.month))
            article['promotion_end'] = str(entry.promotion.end.day) + '/' + str('{:02d}'.format(entry.promotion.start.month))
            f = {'class': 'promotion', 'name': '-' + str(entry.promotion.percentage) + '%'}
            article['filters'].append(f)

        articles_list.append(article)

    return articles_list


# def get_articles():
#     articles = fetch_articles()
#
#     for article in articles:
#         a = Article(
#             article['image'],
#             article['brand'],
#             article['product'],
#             article['description'],
#             article['filters'],
#             article['tags'],
#             article['categories'],
#             article['subcategories'],
#             article['price'],
#             article['promotion-percentage'],
#             article['promotion-start'],
#             article['promotion-end'],
#         )
#
#         db.session.add(a)
#         db.session.commit()
#
#     return Article.query.all()


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
            category['sub-categories'].append(subcategory.name)

        categories_list.append(category)

    return categories_list


def get_subcategories():
    subcategories = client.entries(
        query={
            'content_type': 'subcategories'
        }
    )

    subcategories_list = []

    for entry in subcategories:
        subcategory = {
            'name': entry.name
        }

        subcategories_list.append(subcategory)

    return subcategories_list
