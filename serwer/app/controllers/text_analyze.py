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
        # obszar testowy
        x1 = -102
        y1 = 52
        x2 = 54
        y2 = 30
        ################
        lmJson = lm.toJSON()
        if request.args.get('x1') and request.args.get('y1') and request.args.get('x2') and request.args.get('y2'):
            wH = 10
            wW = 20
            d = x2 - x1
            h = y1 - y2
            maxPointAmount = 10

            # print(lm.toJSON()['nodesData'])
            print("\n")
            print("\n")

            
            locations = lm.toJSON()['nodesData']
            maxTime = 0
            for loc in locations:
                # print(loc)
                if (maxTime < int(loc['time'])):
                    maxTime = int(loc['time'])

            # myMap = [[20], [10]]
            # myMap = [[[]]*20]*10
            myMap = []
            for i in range(0, 20):
                row = []
                for j in range(0, 10):
                    row.append([])
                myMap.append(row)

            print(myMap)
            print("\n")
            p = 0
            for loc in locations:
                xP = loc['coords']['lng']
                yP =loc['coords']['lat']
                # if p < 3:
                # print("? ", x2, " ", xP, " ",
                #       x1, " ; ", y1, " ", yP, " ", y2)
                # print(x2 >= xP,
                #       " ", xP >= x1, " ", y1 >= yP, " ", yP >= y2)
                if x2 >= xP and xP >= x1 and y1 >= yP and yP >= y2:
                    xMyMap =getColumnNumber((
                        loc['coords']['lng']), x1, wW, d)
                    yMyMap =getRowNumber((loc['coords']['lat']), y2, wH, h)
                    myMap[xMyMap][yMyMap].append(loc)
                    p = p + 1
                    # print("## ", xMyMap, " ", yMyMap, " ", loc['name'])
                    # print(loc['name'], " : ", loc['coords'], " ", loc['coords']
                        #   ['lat'], " ", loc['coords']['lng'], ", time in book: ", int(int(loc['time'])/maxTime*100))
            print("max time: ", maxTime)

            newPointsList =  []
            for row in myMap:
                for places in row:
                    # print(places, ", len: ", len(places))
                    it = 0
                    for p in places:
                        if it < maxPointAmount: 
                            newPointsList.append(p)
                            print("_",p)
                            it = it+1
                # print("#\n")

            print(newPointsList, "\n")

            # print(myMap[0][0][1]) #tutaj jeszcze znać size, żeby sprawdzić ile gdzie jest punktów
            # print("\n", myMap)
            print(lm.toJSON(), "\n")
            newReturnList = {}
            newReturnList["id"] = lmJson['id']
            newReturnList["nodesData"] = newPointsList
            newReturnList["name"] = lmJson['name']
            newReturnList["settings"] = lmJson['settings']
            newReturnList["status"] = lmJson['status']
            newReturnList["maxTime"] = maxTime

            print(newReturnList)

            if lm is not None:
                return lm.toJSON()
            else:
                return abort(404)
        elif request.args.get('timeStart') and request.args.get('timeEnd'):
            timeStart = 20#request.args.get('timeStart')
            timeEnd = 80#request.args.get('timeEnd')
            locations = lm.toJSON()['nodesData']
            maxTime = 0
            for loc in locations:
                # print(loc)
                if (maxTime <= (loc['time'])):
                    maxTime = (loc['time'])

            print("max time: ", maxTime)
            pointsFromTimeWindow = []
            for loc in locations:
                loc['time'] = (loc['time']/maxTime)*100
                # print((loc['time']/maxTime)*100)
                # print("loc: ", loc)
                if loc['time'] >= timeStart and timeEnd >= loc['time']:
                    pointsFromTimeWindow.append(loc)

            print(pointsFromTimeWindow)
            newReturnList = {}
            newReturnList["id"] = lmJson['id']
            newReturnList["nodesData"] = pointsFromTimeWindow
            newReturnList["name"] = lmJson['name']
            newReturnList["settings"] = lmJson['settings']
            newReturnList["status"] = lmJson['status']
            newReturnList["maxTime"] = maxTime
            newReturnList["timeStart"] = timeStart
            newReturnList["timeEnd"] = timeEnd

            print(newReturnList)
            if lm is not None:
                return lm.toJSON()
            else:
                return abort(404)
        else:
            if lm is not None:
                return lm.toJSON()
            else:
                return abort(404)
        return abort(404)
        

        

def getColumnNumber(xP, x1, wW, d):
    k = (wW / d) * (xP - x1)

    return int(k)


def getRowNumber(yP, y2, wH, h):
    l = (wH / h)*(yP - y2)

    return int(l)
