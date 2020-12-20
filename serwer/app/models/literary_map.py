from app.services.db import db


class LiteraryMap(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    ready = db.Column(db.Integer())
    nodesData = db.Column(db.JSON())
    name = db.Column(db.String(255))
    settings = db.Column(db.JSON())

    def __repr__(self):
        return '{"id":"' + str(self.id) + '", "name":"' + self.name + \
            '", "ready": "' + str(self.ready) + '", "nodesData": "' + \
            self.nodesData + '", "settings": "' + self.settings + '"}'

    def toJSON(self):
        if self.ready == 1:
            status = "ready"
        else:
            status = "analyzing"

        json_data = {
            "id": self.id,
            "nodesData": self.nodesData,
            "name": self.name,
            "settings": self.settings,
            "status": status
        }
        return json_data
