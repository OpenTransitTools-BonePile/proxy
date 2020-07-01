from pyramid.view import view_config
from ott.utils.dao import base

import logging
log = logging.getLogger(__file__)


cache_long = 500
system_err_msg = base.ServerError()


def do_view_config(cfg):
    cfg.add_route('tilejson',  '/tilejson')
    cfg.add_route('tiles', '/tiles/{z}/{x}/{y}')
    cfg.add_route('all',   '/*')


@view_config(route_name='tilejson', renderer='tilejson.mako', http_cache=cache_long)
def tilejson(request):
    log.info("tilejson")
    request.response.content_type = 'application/json'
    # TODO: build the "http://localhost:51915" from the request object
    tiles = "http://localhost:51915/tiles/{z}/{x}/{y}.pbf"
    tiles = "http://localhost:8090/tiles/{z}/{x}/{y}.pbf"
    #tiles = "https://api.maptiler.com/tiles/v3/{z}/{x}/{y}.pbf?key=iPpYk5aa9BhaiVdDqgek"
    return {"TILES_URL": tiles}


@view_config(route_name='tiles', renderer='string', http_cache=cache_long)
def tiles(request):
    ret_val = request.__dict__
    log.info(ret_val)
    return ret_val


@view_config(route_name='all', renderer='string', http_cache=cache_long)
def all(request):
    ret_val = request.__dict__
    log.info(ret_val)
    return ret_val


def planner_geocode(request):
    """ for the ambiguous geocode page
    """
    try:
        geo_place = None
        geo_type = html_utils.get_first_param(request, 'geo_type', 'place')
        if 'from' in geo_type:
            geo_place = html_utils.get_first_param(request, 'from')
        elif 'to' in geo_type:
            geo_place = html_utils.get_first_param(request, 'to')

        ret_val = geocode_utils.call_geocoder(request, geo_place, geo_type)
    except Exception as e:
        log.warning('{0} exception:{1}'.format(request.path, e))
        ret_val = make_subrequest(request, '/exception.html')
    return ret_val
