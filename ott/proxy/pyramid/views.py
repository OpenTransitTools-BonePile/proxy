from pyramid.view import view_config
from ott.utils.dao import base

import logging
log = logging.getLogger(__file__)


cache_long = 500
system_err_msg = base.ServerError()

port = "55"
tiles_url = "http://localhost:{}".format(port)


def do_view_config(cfg):
    cfg.add_route('p', '/')


@view_config(route_name='p', renderer='string', http_cache=cache_long)
def p(request):
    # import pdb; pdb.set_trace()
    ret_val = tiles_url
    return ret_val
