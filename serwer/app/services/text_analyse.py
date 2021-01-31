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
    sentenceIt = 1
    city_location_dict = {}
    country_location_dict = {}
    goe_location_dict = {}
    city_word_cnt = 0
    country_word_cnt = 0
    goe_word_cnt = 0

    for sentence in tree.iter("sentence"):
        prev_city = 0
        prev_country = 0
        prev_goe = 0
        for tok in sentence.iter("tok"):
            annot = tok.findall('ann')
            for ann in annot:
                if (ann is not None):
                    ann_attr = ann.attrib
                    if (ann_attr["chan"] == 'nam_loc_gpe_city'):
                        is_city = int(ann.text)
                        if (is_city):
                            if (prev_city == is_city):
                                city_location_dict["name"] += " " + tok.find('./lex/base').text
                                city_location_dict["orth"] += " " + tok.find("orth").text
                                city_location_dict["ctag"] += " " + tok.find("./lex/ctag").text
                                city_word_cnt += 1
                            else:
                                if (city_location_dict):
                                    city_location_dict["word_cnt"] = city_word_cnt
                                    city_word_cnt = 0
                                    loc_ann.append(city_location_dict)
                                    # print(city_location_dict)
                                id_num += 1
                                city_location_dict = {}
                                city_location_dict["id"] = id_num
                                city_location_dict["time"] = sentenceIt
                                city_location_dict["name"] = tok.find('./lex/base').text
                                city_location_dict["orth"] = tok.find("orth").text
                                city_location_dict["ctag"] = tok.find("./lex/ctag").text
                                city_location_dict["ann"] = 'nam_loc_gpe_city'
                                city_word_cnt += 1
                                prev_city = is_city
                        else:
                            if (city_location_dict):
                                city_location_dict["word_cnt"] = city_word_cnt
                                city_word_cnt = 0
                                loc_ann.append(city_location_dict)
                                # print(city_location_dict)
                            city_location_dict = {}
                    if (ann_attr["chan"] == 'nam_loc_gpe_country'):
                        is_country = int(ann.text)
                        if (is_country):
                            if (prev_country == is_country):
                                country_location_dict["name"] += " " + tok.find('./lex/base').text
                                country_location_dict["orth"] += " " + tok.find("orth").text
                                country_location_dict["ctag"] += " " + tok.find("./lex/ctag").text
                                country_word_cnt += 1
                            else:
                                if (country_location_dict):
                                    country_location_dict["word_cnt"] = country_word_cnt
                                    country_word_cnt = 0
                                    loc_ann.append(country_location_dict)
                                    # print(country_location_dict)
                                id_num += 1
                                country_location_dict = {}
                                country_location_dict["id"] = id_num
                                country_location_dict["time"] = sentenceIt
                                country_location_dict["name"] = tok.find('./lex/base').text
                                country_location_dict["orth"] = tok.find("orth").text
                                country_location_dict["ctag"] = tok.find("./lex/ctag").text
                                country_location_dict["ann"] = 'nam_loc_gpe_country'
                                country_word_cnt += 1
                                prev_country = is_country
                        else:
                            if (country_location_dict):
                                country_location_dict["word_cnt"] = country_word_cnt
                                country_word_cnt = 0
                                loc_ann.append(country_location_dict)
                                # print(country_location_dict)
                            country_location_dict = {}
                    if (ann_attr["chan"] == 'nam_fac_goe'):
                        is_goe = int(ann.text)
                        if (is_goe):
                            if (prev_goe == is_goe):
                                goe_location_dict["name"] += " " + tok.find('./lex/base').text
                                goe_location_dict["orth"] += " " + tok.find("orth").text
                                goe_location_dict["ctag"] += " " + tok.find("./lex/ctag").text
                                goe_word_cnt += 1
                            else:
                                if (goe_location_dict):
                                    goe_location_dict["word_cnt"] = goe_word_cnt
                                    goe_word_cnt = 0
                                    loc_ann.append(goe_location_dict)
                                    # print(goe_location_dict)
                                id_num += 1
                                goe_location_dict = {}
                                goe_location_dict["id"] = id_num
                                goe_location_dict["time"] = sentenceIt
                                goe_location_dict["name"] = tok.find('./lex/base').text
                                goe_location_dict["orth"] = tok.find("orth").text
                                goe_location_dict["ctag"] = tok.find("./lex/ctag").text
                                goe_location_dict["ann"] = 'nam_fac_goe'
                                goe_word_cnt += 1
                                prev_goe = is_goe
                        else:
                            if (goe_location_dict):
                                goe_location_dict["word_cnt"] = goe_word_cnt
                                goe_word_cnt = 0
                                loc_ann.append(goe_location_dict)
                                # print(goe_location_dict)
                            goe_location_dict = {}
        sentenceIt = sentenceIt + 1

    return loc_ann

def get_location(info):
    geolocator = Nominatim(user_agent="map")
    phrases = []

    for line in info:
        try:
            base = line["name"]
            orth = line["orth"]
            ctag = line["ctag"]
            word_cnt = line["word_cnt"]
            flags = ""
            for i in range(word_cnt - 1):
                flags += "True "
            flags += "False"
            ann = line["ann"]

            phrases.append([orth, base, ctag, flags, ann])

            payload = {'lexeme_polem': phrases, 'tool': 'polem', 'options': [], 'lexeme':'', 'task':'all'}
            headers = {'content-type': 'application/json'}
            url = 'http://ws.clarin-pl.eu/lexrest/lex'

        except:
            print(line)
    response = requests.post(url, data=json.dumps(payload), headers=headers).text
    response_json = json.loads(response)

    res = 0
    for line in info:
        loc = response_json["results"][res]
        location = geolocator.geocode(loc)
        line["name"] = location.address.split(", ")[0]
        line["coords"] = {
            "lat": location.latitude,
            "lng": location.longitude
        }
        res += 1

    loc_json = json.dumps(info, indent=2)

    return loc_json


if __name__ == "__main__":
    main(text)
