#!/usr/bin/env python3
"""Module: 1-app
route:
    - / - welcome page
"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Configuration class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)


@app.route('/')
def home():
    """Render a welcome page"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.config.from_object(Config)
    app.run()
