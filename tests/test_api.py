import config

from contentful import Client

client = Client(config.CONTENTFUL_SPACE_ID, config.CONTENTFUL_ACCESS_TOKEN)


def test_api_config():
    assert client.space_id == config.CONTENTFUL_SPACE_ID
    assert client.access_token == config.CONTENTFUL_ACCESS_TOKEN
    assert client.environment == "master"
    assert client.api_url == "cdn.contentful.com"


def test_api_entries_status():
    entries = client.entries()

    for entry in entries:
        assert entry.sys['type'] == "Entry"
        assert entry.sys['environment'].sys['id'] == "master"
        assert entry.sys['content_type'].sys['id'] == "article" or "categories" or "subCategories" or "promotion"
