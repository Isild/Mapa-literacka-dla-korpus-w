from app.services.app import app
from . import text_analyze
from . import literary_maps


def init_routes():
    app.add_url_rule(
        '/processText', view_func=text_analyze.TextAnalyze.as_view('processText'))

    app.add_url_rule(
        '/literaryMaps', view_func=literary_maps.LiteraryMaps.as_view('literaryMaps'))
