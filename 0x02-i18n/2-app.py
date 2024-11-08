#!/usr/bin/env python3
"""Module: 2-app

Route:
    - / - welcome page

Function:
    - get_locale - get locale from request

Class:
    - Config - Configuration class
"""
from flask import Flask, render_template, request
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
    return render_template('2-index.html')


@babel.localeselector
def get_locale():
    """Get locale from request"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == '__main__':
    app.config.from_object(Config)
    app.run()
