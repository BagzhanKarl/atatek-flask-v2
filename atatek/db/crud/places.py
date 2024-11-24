from atatek.db import db, Places
from sqlalchemy.exc import IntegrityError

def get_place_by_osm(osm):
    place = Places.query.filter_by(osm=osm).first()
    return place