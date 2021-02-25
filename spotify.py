from aiohttp import web
import aiohttp
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
        async with aiohttp.request("POST", f"{ACCOUNTS}/api/token", data={
            "grant_type": "authorization_code",
            "code": query,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }) as response:
            response = await response.json()
            print(response)
        return web.Response(text=str(response))
    else:
        return web.Response(text="You shouldn't be here!")


def get_query(request) -> tuple:
    state = request.query.get("state", None)
    if code := request.query.get("code", None):
        return code, state, True  # success
    elif error := request.query.get("code", None):
        return error, state, False  # failure
    else:
        return "myer", "stupid", False


async def spotify():
    app = web.Application()
    app.router.add_get('/spotify', process)
    return app
