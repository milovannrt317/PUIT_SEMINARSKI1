import json

class Automobil:
    def __init__(self, id, naziv, cena):
        self.id = id
        self.naziv = naziv
        self.cena = cena

    def __str__(self):
        return "ID: {:<4} Naziv: {:<20} Cena: {:<5}".format(str(self.id),self.naziv,str(self.cena))

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)