import os
import re
import json
import googlemaps
from dotenv import load_dotenv
from tqdm import tqdm
from filometro import update_data


env = load_dotenv()
API_KEY = os.environ['API_KEY']


def preprocess_address(add):
    return re.sub(' FONE:.*', '', add)


def get_geodata():

    gmaps = googlemaps.Client(key=API_KEY)
    geodata = []
    data = update_data()
    for id, item in tqdm(enumerate(data, start=1), total=len(data)):
        item_dict = {}
        address = item.get('endereco')
        name = item.get('equipamento')
        clean_address = preprocess_address(address)
        full_address = name + ', ' + clean_address + ' São Paulo-SP'
        item_geo = gmaps.geocode(full_address)

        item_dict['name'] = item['equipamento']
        item_dict['geometry'] = item_geo[0]['geometry'] 

        geodata.append(item_dict)

    place_geo = {i['name']: i['geometry'] for i in geodata}
    with open('../data/geodata.json', 'w+') as f:
        json.dump(place_geo, f, indent=4)


if __name__ == '__main__':
    get_geodata()