import domain

def test_urlshortner_init():
    shortner = domain.URLShortner()
    assert {} == shortner.urls
    assert 37483299 == shortner.seed
    assert 10000000000000000 == shortner.count

def test_urlshortner_add_url():
    shortner = domain.URLShortner()
    data = shortner.add_url('http://loogi.ca')
    assert 'url' in data
    assert 'http://loogi.ca' in data['url']
    assert 'shortned' in data

def test_urlshortner_resolve():
    shortner = domain.URLShortner()
    data = shortner.add_url('http://loogi.ca')
    shortner.resolve(data['shortned'])

    assert 1 == shortner.urls[data['shortned']]['resolved']
