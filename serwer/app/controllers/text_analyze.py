from flask.views import MethodView
from app.services.text_analyse import analyze_text
from flask import request, abort
from app.services.db import db
from app.models.literary_map import LiteraryMap
import json

class TextAnalyze(MethodView):
    def post(self):
        dataFromJson = request.get_json()
        n = dataFromJson['name']
        lm = LiteraryMap(ready=0, nodesData="", name=n,
                         settings="")
        db.session.add(lm)
        db.session.commit()

        analyze_text(dataFromJson['text'], lm.id)
        return str(lm.id)

    def get(self):
        lm_id = request.args.get('id')
        lm = LiteraryMap.query.filter_by(id=lm_id).first()

        if lm is not None:
                return lm.toJSON()
        else:
            return abort(404)
