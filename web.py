import re

from coopy.base import init_persistent_system
from flask import Flask, abort, request, render_template, redirect, jsonify

app = Flask(__name__)

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

    def add_url(self, url):
        if url_regex.match(url) == None:
            raise Exception("Invalid URL")
        self.count += self.seed
        shortened = self._create_url(self.count)
        self.urls[shortened] = url
        return dict(shortened=shortened,
                    url=url)

    def resolve(self, _id):
        return self.urls[_id]

system = init_persistent_system(URLShortner())
MAIN_SITE = "http://loogica.net"

@app.route('/')
def main_site():
    return redirect(MAIN_SITE)

@app.route('/main/')
def main():
    return render_template('index.html')

@app.route('/urls/')
def urls():
    return jsonify(system.urls)

@app.route('/add_url/', methods=['POST'])
def add_url():
    url = request.json['url']
    try:
        return jsonify(system.add_url(url))
    except Exception as e:
        return jsonify(dict(error=e))

@app.route('/<shortened>')
def resolve(shortened):
    try:
        return redirect(system.resolve(shortened))
    except Exception as e:
        abort(404)

@app.errorhandler(404)
def handle_404(error):
    return render_template('404.html'), 404

application = app

if __name__ == "__main__":
    app.run(debug=True)
