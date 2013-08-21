import logging
import re

from decouple import Config
from coopy.base import init_persistent_system
from flask import Flask, abort, request, render_template, redirect, jsonify

from domain import URLShortner

log = logging.getLogger(__name__)

config = Config('settings.ini')
app = Flask(__name__)
app.secret_key = config('SECRET_KEY').encode('utf-8')
app.logger.addHandler(logging.StreamHandler())
system = init_persistent_system(URLShortner())
MAIN_SITE = "http://loogi.ca"

@app.route('/')
def main_site():
    return render_template('loogica.html')

@app.route('/urls/')
def urls():
    return jsonify(system.urls)

@app.route('/add_url/', methods=['POST'])
def add_url():
    url = request.json['url']
    try:
        return jsonify(system.add_url(url))
    except Exception as e:
        return jsonify(dict(error=str(e)))

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
