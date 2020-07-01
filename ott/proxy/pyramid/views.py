from pyramid.view import view_config
from ott.utils.dao import base

import logging
log = logging.getLogger(__file__)


cache_long = 500
system_err_msg = base.ServerError()

port = "55"
tiles_url = "http://localhost:{}".format(port)


def do_view_config(cfg):
    cfg.add_route('home',  '/')
    cfg.add_route('tiles', '/tiles')


@view_config(route_name='home', renderer='tilejson.mako', http_cache=cache_long)
def home(request):
    request.response.content_type = 'application/json'
    return {}


@view_config(route_name='tiles', renderer='string', http_cache=cache_long)
def tiles(request):
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
