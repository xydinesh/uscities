from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    City,
    )


@view_defaults(renderer='json')
class CityView(object):
    """Class for handling city requests"""
    def __init__(self, request):
        self.request = request

    @view_config(
        route_name='cities',
        request_method='GET'
    )
    def cities_get(self):
        request = self.request
        state = request.params.get('state', None)
        zip_code = request.params.get('zip', None)
        cities_list = []
        if state is None and zip_code is None:
            return None
        elif state is not None:
            cities = DBSession.query(City).filter_by(state=state)
        else:
            zip_code = int(zip_code)
            cities = DBSession.query(City).filter_by(zip=zip_code)
        
        for city in cities.all():
            cities_list.append(city.get_json())
        return cities_list


    @view_config(
        route_name='city',
        request_method='GET'
    )
    def city_get(self):
        request = self.request
        zip_code = int(request.matchdict.get('code'))
        return City.get_city(zip_code)
