from app.services.app import app
from . import algorithm
from . import literaryMaps


def init_routes():
    app.add_url_rule(
        '/methodOne', view_func=algorithm.Algorithm.as_view('methodOne'))

    app.add_url_rule(
        '/literaryMaps', view_func=literaryMaps.LiteraryMaps.as_view('literaryMaps'))
