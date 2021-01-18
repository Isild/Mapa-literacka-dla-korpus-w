import requests
import json
import xml.etree.ElementTree as Et
from geopy.geocoders import Nominatim
from app.models.literary_map import LiteraryMap
from app.services.db import db


clarinpl_url = "http://ws.clarin-pl.eu/nlprest2/base"
url = clarinpl_url + "/process"
user_mail = "testo@.test.pl"
# Tag and recognize localizations (coarse-grained categories)
lpmn = 'wcrft2|liner2({"model":"n82"})'

text = "Paweł robi zadanie z Przemek w Polska.\
Przemek współpracuje z Pawłem już nie w Polsce.\
Wojtek pisze jutro Kolokwium z angielskiego we Wrocławiu.\
Przemek pisze kolokwium z Wojtkiem w Chałupach.\
Bartosz zrobił już coś, żartowałem nie ma go na ziemii.\
Np. Bartosz zna się tylko z Pawłem w Karkonoszach.\
Reszta grupy jest nieznana.\
Mariusz jedzie autem Mariuszem do Mariuszowa.\
Z Wołowa do Wrocławia jednym pociągiem, polecam Paweł, kolekcja klasyki z Polski."


def analyze_text(text_to_analyze, lm_id):
    # Get analyzed XML
    info = getTextInf(text_to_analyze, lm_id)
    return_json = get_location(info)

    lm_obj = LiteraryMap.query.filter(LiteraryMap.id == lm_id).first()
    lm_obj.ready = 1
    lm_obj.nodesData = json.loads(return_json)
    db.session.commit()

    return return_json


def getTextInf(text_to_send, lm_id):
    payload = {'text': text_to_send, 'lpmn': lpmn, 'user': user_mail}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    ccl = r.content.decode('utf-8')
    id_num = 0

    loc_ann = []
    tree = Et.fromstring(ccl)
    previousStr = ''
    sentenceIt = 1
    prev_city = 0
    location_dict = {}
    city_word_cnt = 0
    for tok in tree.iter("tok"):
        annot = tok.findall('ann')
        for ann in annot:
            if (ann is not None):
                lexBase = tok.find('./lex/base')
                if (previousStr != '.' and lexBase.text == '.'):
                    sentenceIt = sentenceIt + 1
                ann_attr = ann.attrib
                if (ann_attr["chan"] == 'nam_loc_gpe_city'):
                    is_city = int(ann.text)
                    if (is_city):
                        if (prev_city == is_city):
                            location_dict["name"] += " " + lexBase.text
                            location_dict["orth"] += " " + tok.find("orth").text
                            location_dict["ctag"] += " " + tok.find("./lex/ctag").text
                            city_word_cnt += 1
                        else:
                            if (location_dict):
                                location_dict["word_cnt"] = city_word_cnt
                                city_word_cnt = 0
                                loc_ann.append(location_dict)
                            id_num += 1
                            location_dict = {}
                            location_dict["id"] = id_num
                            location_dict["time"] = sentenceIt
                            location_dict["name"] = lexBase.text
                            location_dict["orth"] = tok.find("orth").text
                            location_dict["ctag"] = tok.find("./lex/ctag").text
                            city_word_cnt += 1
                            prev_city = is_city

                if (lexBase.text != '.'):
                    previousStr = 'c'
                else:
                    previousStr = lexBase.text

    location_dict["word_cnt"] = city_word_cnt
    loc_ann.append(location_dict)
    return loc_ann


def get_location(info):
    geolocator = Nominatim(user_agent="map")

    for line in info:
        try:
            base = line["name"]
            orth = line["orth"]
            ctag = line["ctag"]
            flags = "True True"
            ann = "nam_loc_gpe_city"

            phrases = []
            phrases.append([orth, base, ctag, flags, ann])

            payload = {'lexeme_polem': phrases, 'tool': 'polem', 'options': [], 'lexeme':'', 'task':'all'}
            headers = {'content-type': 'application/json'}
            url = 'http://ws.clarin-pl.eu/lexrest/lex'

            response = requests.post(url, data=json.dumps(payload), headers=headers).text
            response_json = json.loads(response)
            loc = response_json["results"][0]

            line["name"] = loc
            location = geolocator.geocode(loc)
            line["coords"] = {
                "lat": location.latitude,
                "lng": location.longitude
            }
        except:
            print(line)

    loc_json = json.dumps(info)

    return loc_json


if __name__ == "__main__":
    main(text)
