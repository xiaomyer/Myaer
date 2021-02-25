from aiohttp import web
import json

with open("config.json") as config:
    config = json.load(config)
    CLIENT_ID = config["id"]
    CLIENT_SECRET = config["secret"]
ACCOUNTS = "https://accounts.spotify.com"
REDIRECT_URI = "https://myer.wtf/spotify"


async def process(request):
    query, state, success = get_query(request)
    if success:
        return web.Response(text=f"{query}")
    else:
        return web.Response(text="You shouldn't be here!")


def get_query(request) -> tuple:
    state = request.query.get("state", None)
    if code := request.query.get("code", None):
        return code, state, True  # success
    elif error := request.query.get("error", None):
        return error, state, False  # failure
    else:
        return None, None, False  # you fucked up!


async def spotify():
    app = web.Application()
    app.router.add_get('/spotify', process)
    return app
