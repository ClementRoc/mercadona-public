import json
import config

from mercadonapp import app
from contentful import Client


def get_articles_data():
    client = Client(config.CONTENTFUL_SPACE_ID, config.CONTENTFUL_ACCESS_TOKEN)
    articles = client.entries()

    articles_list = []

    for entry in articles:
        article = {
            'brand': entry.brand,
            'product': entry.product,
            'description': entry.description
        }
        articles_list.append(article)

    return articles_list
