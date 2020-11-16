import requests
import json
import xml.etree.ElementTree as ET

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
Mariusz jedzie autem Mariuszem do Mariuszowa."


def main():
    # Get analyzed XML
    info = getTextInf(text)

def getTextInf(textToSend):
    payload = {'text': textToSend, 'lpmn': lpmn, 'user': user_mail}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    ccl = r.content.decode('utf-8')

    loc_ann = []
    tree = ET.fromstring(ccl)
    for tok in tree.iter("tok"):
        annot = tok.findall('ann')
        for ann in annot:
            if (ann is not None):
                ann_attr = ann.attrib
                if (ann_attr["chan"] == "nam_loc" and "head" in ann_attr):
                    location_dict = ann_attr.copy()
                    location_dict["location"] = tok.find('./lex/base').text
                    loc_ann.append(location_dict)
                    print(location_dict)

    return loc_ann


if __name__ == "__main__":
    main()
