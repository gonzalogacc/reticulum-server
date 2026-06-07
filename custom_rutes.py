import random

import RNS

from router import Router

routes = Router()


@routes.route_decorator(path="/random/text")
def random_text_generator(
    path, data, request_id, link_id, remote_identity, requested_at
):
    RNS.log(
        f"Generating response to request \
        {RNS.prettyhexrep(request_id)=} \
            on link {RNS.prettyhexrep(link_id)=}"
    )
    return data


@routes.route_decorator(path="/random/number")
def random_int_generator(
    path, data, request_id, link_id, remote_identity, requested_at
):
    RNS.log(
        f"Generating response to request \
        {RNS.prettyhexrep(request_id)} \
            on link "
        + RNS.prettyhexrep(link_id)
    )
    return str(random.randint(0, 100))
