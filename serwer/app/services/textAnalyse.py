from flask import json
import requests
import xml.etree.ElementTree as ET
from app.services.db import db
from app.models.literaryMap import LiteraryMap

text = "Paweł robi zadanie z Przemek.\
Przemek współpracuje z Pawłem.\
Wojtek pisze jutro Kolokwium z angielskiego.\
Przemek pisze kolokwium z Wojtkiem.\
Bartosz zrobił już coś.\
Np. Bartosz zna się tylko z Pawłem.\
Reszta grupy jest nieznana.\
Mariusz jedzie autem Mariuszem."


def main(text, id):
    return "{}"


if __name__ == "__main__":
    main(text)
