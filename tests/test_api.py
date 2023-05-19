from contentful import Client

import config
client = Client(config.CONTENTFUL_SPACE_ID, config.CONTENTFUL_ACCESS_TOKEN)


def test_api_config():
    assert client.environment == "master"
    assert client.api_url == "cdn.contentful.com"

