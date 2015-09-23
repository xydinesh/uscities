from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


from pyramid import events

def get_engine_name(event):
    request = event.request
    state = request.params.get('state', None)
    zip_code = request.params.get('zip', None)
    if state is not None:
        if state == 'TN':
            return 'east'
        else:
            return 'west'
    elif zip_code is not None:
        zip_code = int(zip_code)
        if zip_code > 50000:
            return 'west'
        else:
            return 'east'
    else:
        return 'east'


def on_new_request(event):
    # http://stackoverflow.com/a/13372001
    # handling multi-tenancy with schema
    # schema_name = _figire_out_schema_name_from_request(event.request)
    # DBSession.execute("SET search_path TO %s" % schema_name)
    engine_name = get_engine_name(event)
    DBSession.configure(bind=engine[engine_name])
    Base.metadata.bind = engine[engine_name]

engine = {}
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    global engine
    engine = {
        'east': engine_from_config(settings, 'sqlalchemy.east.', logging_name='east'),
        'west': engine_from_config(settings, 'sqlalchemy.west.', logging_name='west'),
    }
    DBSession.configure(bind=engine['east'])
    Base.metadata.bind = engine['east']
    config = Configurator(settings=settings)
    config.add_route('city', '/api/1/cities/{code}')
    config.add_route('cities', '/api/1/cities')
    config.scan()
    config.add_subscriber(on_new_request, events.NewRequest)
    return config.make_wsgi_app()
