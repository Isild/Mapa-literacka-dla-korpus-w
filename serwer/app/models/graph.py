from app.services.db import db


class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    ready = db.Column(db.Integer)
    nodesData = db.Column(db.String(1000000000))
    name = db.Column(db.String(255))
    settings = db.Column(db.String(255))

    def __repr__(self):
        return '{"id":"' + str(self.id) + '", "name":"' + self.name + \
            '", "ready": "' + str(self.ready) + '", "nodesData": "' + \
            self.nodesData + '", "settings": "' + self.settings + '"}'

    def toJSON(self):
        json = '{"id": "' + str(self.id) + '", "nodesData": ' + \
            self.nodesData + ', "name": "' + self.name + \
            '", "settings": "' + self.settings + '"}'
        return json
