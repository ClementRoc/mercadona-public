from contentful import Client

import config


def test_api_config():
    client = Client(config.CONTENTFUL_SPACE_ID, config.CONTENTFUL_ACCESS_TOKEN)

    assert client.environment == "master"
    assert client.api_url == "cdn.contentful.com"
