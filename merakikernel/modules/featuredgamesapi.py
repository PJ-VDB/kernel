import bottle

import merakikernel.riotapi.featuredgamesapi
import merakikernel.common

# Special note - since the featured games endpoint doesn't take region as an argument and is served
# per server, kernel takes the region as a GET parameter. You can safely send this parameter to the
# Riot servers as well without any effect on the response you'd normally get.


@bottle.route("/observer-mode/rest/featured", method=["GET", "OPTIONS"])
@merakikernel.common.riot_endpoint
def featured_games():
    params = dict(bottle.request.query)
    try:
        region = params["region"].lower()
        return merakikernel.riotapi.featuredgamesapi.featured_games(region, params)
    except KeyError:
        bottle.abort(400, "No region parameter specified!")
