from mercadonapp.database import Article, Filter, Tag


def test_adding_data_to_database():
    f = Filter('promo', '-40%')
    t = Tag('1sachet')
    t2 = Tag('500G')
    a = Article(
        'path/to/img',
        'LUSTUCRU',
        'gnocchi',
        'coucou je test les gnocchis',
        [f],
        [t, t2],
        'Frais',
        'Pâtes',
        8.9,
        30,
        3.5,
        '14/05',
        '28/05'
    )
    assert a.image == 'path/to/img'
    assert a.brand == 'LUSTUCRU'
    assert a.product == 'gnocchi'
    assert a.description == 'coucou je test les gnocchis'
    assert a.filters == [f]
    assert a.tags == [t, t2]
    assert a.categories == 'Frais'
    assert a.subcategories == 'Pâtes'
    assert a.price == 8.9
    assert a.promotion_percentage == 30
    assert a.promoted_price == 3.5
    assert a.promotion_start == '14/05'
    assert a.promotion_end == '28/05'
