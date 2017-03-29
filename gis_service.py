import json


class ZipCodeService:

    class __ZipCodeService:

        _coords = {}

        def __init__(self):
            f = open('gis_service_db.json', 'r')
            self._coords = json.load(f)
            f.close()

        def get_coords(self, zip_code):
            return self._coords[zip_code]

    # singleton pattern to load the zip code file only once
    instance = __ZipCodeService()

    # returns {'lat': 33.2009, 'lon': -117.2856}
    def get_coords(self, zip_code):
        return self.instance.get_coords(zip_code)
