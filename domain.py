import re

'''
url regex from:
http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
'''
url_regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

class URLShortner(object):
    def __init__(self):
        self.seed = 37483299
        self.urls = {}
        self.count = 10000000000000000

    def _create_url(self, uid):
        '''
            from: https://github.com/mrigor/url-shortener/blob/master/url_shortener.py
        '''
        HASH_BASE = 'lahcx9yV6OsuefCEvJAbd0SZIGWYFQtUB8KX5jqR4NMzH1PTg37npwrLimD2ko'
        s = []
        mod = len(HASH_BASE)
        while uid:
            uid, c = divmod(uid, mod)
            s.append(HASH_BASE[c])
        return ''.join(s)

    def add_url(self, url, shortned=None):
        if url_regex.match(url) == None:
            raise Exception("Invalid URL")

        if not shortned or shortned == "":
            self.count += self.seed
            shortned = self._create_url(self.count)

        self.urls[shortned] = {'resolved': 0, 'url': url}
        return dict(shortned=shortned, url=url)


    def resolve(self, _id):
        try:
            self.urls[_id]['resolved'] += 1
            return self.urls[_id]['url']
        except KeyError as ke:
            raise ke
