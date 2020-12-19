from flask.views import MethodView
from app.services.text_analyse import main
from flask import request
from app.services.db import db
from app.models.literary_map import LiteraryMap


class TextAnalyze(MethodView):
    def post(self):
        dataFromJson = request.get_json()
        n = dataFromJson['name']
        lm = LiteraryMap(ready=0, nodesData="", name=n,
                         settings="")
        db.session.add(lm)
        db.session.commit()

        main(dataFromJson['text'])
        return str(lm.id)

    def get(self):
        lmID = request.args.get('id')
        lm = LiteraryMap.query.filter_by(id=lmID).first()

        if lm.ready:
            json = lm.toJSON()
            return '{"status":"ready", "literaryMap":' + str(json) + '}'
        else:
            return '{"status":"analyzing"}'
