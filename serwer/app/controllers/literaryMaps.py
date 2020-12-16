from flask.views import MethodView
from flask import json
from app.models.literaryMap import LiteraryMap


class LiteraryMaps(MethodView):
    def get(self):
        try:
            literaryMap = LiteraryMap.query.with_entities(
                LiteraryMap.id, LiteraryMap.name, LiteraryMap.ready).all()
            return '{"literaryMaps":' + json.dumps(literaryMap) + '}'
        except Exception as e:
            print("Failed get literary maps data: ", e)
            return str(500)
