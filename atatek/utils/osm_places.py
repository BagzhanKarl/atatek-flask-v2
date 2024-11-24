import requests
from atatek.db import db, Places

def get_data(query: str, country: str):
    url = 'https://nominatim.openstreetmap.org/search.php?format=jsonv2&q='
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MyApp/1.0; +https://alash.atatek.kz)'
    }
    response = requests.get(url + query + "+" + country, headers=headers)
    data = response.json()

    for item in data:
        exists_place = db.session.query(Places).filter_by(osm=item['osm_id']).first()
        if not exists_place:
            place = Places(
                osm=item['osm_id'],
                lat=item['lat'],
                lon=item['lon'],
                type=item['type'],
                name=item['name'],
                display_name=item['display_name'],
            )
            db.session.add(place)
    db.session.commit()

    filtered_data = [
        {
            'display_name': item['display_name'],
            'category': item['category'],
            'addresstype': item['addresstype'],
            'place_id': item['place_id'],
            'osm_id': item['osm_id']
        }
        for item in data
    ]

    return filtered_data
