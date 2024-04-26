import encodings
import json


def test():
    return None


json_path = "./config.json"
json_data = '{"nimi":"Aleksander Milishenko", "vanus":16, "prillid":true}'
data = json.loads(json_data)

data2 = {
    "nimi":"Anna",
    "vanus":16,
    "prillid":False,
    "lapsed":("Inna", "Mati"),
    "koduloomad":None,
    "autod":[{"muudel":"BMW", "värv":"punane", "number":"451 JBF", "jõud":500}, {"muudel":"Ford", "värv":"must", "number":"360 GOM", "jõud":300}]
    }

with open(file = json_path, mode="r", encoding = "utf-8") as f:
    print(type(f))
   
    print(json.load(f))
   