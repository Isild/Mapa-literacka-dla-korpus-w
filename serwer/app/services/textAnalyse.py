import requests
import json
import xml.etree.ElementTree as ET
from geopy.geocoders import Nominatim

clarinpl_url = "http://ws.clarin-pl.eu/nlprest2/base"
url = clarinpl_url + "/process"
user_mail = "testo@.test.pl"
# Tag and recognize localizations (coarse-grained categories)
lpmn = 'wcrft2|liner2({"model":"top9"})'

text = "Paweł robi zadanie z Przemek w Polska.\
Przemek współpracuje z Pawłem już nie w Polsce.\
Wojtek pisze jutro Kolokwium z angielskiego we Wrocławiu.\
Przemek pisze kolokwium z Wojtkiem w Chałupach.\
Bartosz zrobił już coś, żartowałem nie ma go na ziemii.\
Np. Bartosz zna się tylko z Pawłem w Karkonoszach.\
Reszta grupy jest nieznana.\
Mariusz jedzie autem Mariuszem do Mariuszowa.\
Z Wołowa do Wrocławia jednym pociągiem, polecam Paweł, kolekcja klasyki z Polski."


def main(text):
    # Get analyzed XML
    info = getTextInf(text)
    json = get_location(info)

    return json


def getTextInf(textToSend):
    payload = {'text': textToSend, 'lpmn': lpmn, 'user': user_mail}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    ccl = r.content.decode('utf-8')
    id_num = 0

    loc_ann = []
    tree = ET.fromstring(ccl)
    previousStr = ''
    sentenceIt = 1
    for tok in tree.iter("tok"):
        location_dict = {}
        annot = tok.findall('ann')
        for ann in annot:
            if (ann is not None):
                lexBase = tok.find('./lex/base')
                if (previousStr != '.' and lexBase.text == '.'):
                    sentenceIt = sentenceIt + 1
                ann_attr = ann.attrib
                if (ann_attr["chan"] == "nam_loc" and "head" in ann_attr):
                    location_dict["id"] = id_num
                    location_dict["name"] = lexBase.text
                    location_dict["time"] = sentenceIt
                    loc_ann.append(location_dict)
                    id_num += 1

                if (lexBase.text != '.'):
                    previousStr = 'c'
                else:
                    previousStr = lexBase.text
    return loc_ann


def get_location(info):
    geolocator = Nominatim(user_agent="map")

    for line in info:
        loc = line["name"]

        location = geolocator.geocode(loc)
        line["coords"] = {
            "lat": location.latitude,
            "lng": location.longitude
        }

    loc_json = json.dumps(info)

    return loc_json


if __name__ == "__main__":
    main(text)
