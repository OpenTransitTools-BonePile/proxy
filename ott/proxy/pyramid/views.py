from pyramid.response import Response
from pyramid.view import view_config

from ott.map_server.model import stop_data
from ott.map_server.model import stop_popup

from ott.utils.parse.url.geo_param_parser import StopGeoParamParser
from ott.utils.dao import base
from ott.utils import web_utils
from ott.utils import json_utils
from ott.utils import pyramid_utils

import logging
log = logging.getLogger(__file__)


cache_long = 500
system_err_msg = base.ServerError()
session = None
stop_map_url = "https://maps.trimet.org/ride_ws/stop?stop_id={}"


def do_view_config(cfg):
    cfg.add_route('map_url_via_stopid', '/map_url_via_stopid')
    cfg.add_route('map_via_stopid', '/map_via_stopid')
    cfg.add_route('map_stop_popup', '/map_stop_popup')


@view_config(route_name='map_stop_popup', renderer='json', http_cache=cache_long)
def map_stop_popup(request):
    """
    https://maps.trimet.org/ride_ws/stop?id=2&agency=TRIMET
    """
    params = StopGeoParamParser(request)
    stop = stop_data.get_stop(params.stop_id)
    json = {}
    if stop:
        if stop.get('has_errors') is not True:
            json = stop_popup.make_legacy_stop_popup_json(stop)
        else:
            json = stop
    return json


@view_config(route_name='map_url_via_stopid', renderer='string', http_cache=cache_long)
def map_url_via_stopid(request):
    """
    https://maps.trimet.org/ride_ws/stop?id=2&agency=TRIMET

    # https://ride.trimet.org/eapi/ws/V1/    mapimage || stopimage
    #   format/png/width/350/height/350/zoom/6/extraparams/format_options=layout:scale/id/2
    #   format/png/width/800/height/600/zoom/9/coord/-122.675671,45.420609/extraparams/format_options=layout:place

    # /geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=hybridOSM&styles=&bbox=-13656617,5703496,-13655897,5703976&srs=EPSG:900913&format=application/openlayers&width=600&height=400

    """
    params = StopGeoParamParser(request)
    stop = stop_data.get_stop(params.stop_id)
    map_url = stop
    return map_url


@view_config(route_name='map_via_stopid', renderer='string', http_cache=cache_long)
def map_via_stopid(request):
    # import pdb; pdb.set_trace()
    map_url = map_url_via_stopid(request)
    ret_val = map_url # grab img
    return ret_val
