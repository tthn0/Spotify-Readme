import requests
from base64 import b64encode
from dotenv import find_dotenv, load_dotenv
from flask import Flask, Response, render_template, request
from os import getenv
from random import randint

# Load environment variables
load_dotenv(find_dotenv())

# Define base-64 encoded images
with open("api/base64/placeholder_scan_code.txt") as f:
    B64_PLACEHOLDER_SCAN_CODE = f.read()
with open("api/base64/placeholder_image.txt") as f:
    B64_PLACEHOLDER_IMAGE = f.read()
with open("api/base64/spotify_logo.txt") as f:
    B64_SPOTIFY_LOGO = f.read()


def get_token():
    """Get a new access token"""
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": getenv("REFRESH_TOKEN"),
            "client_id": getenv("CLIENT_ID"),
            "client_secret": getenv("CLIENT_SECRET"),
        },
    )
    try:
        return r.json()["access_token"]
    except BaseException:
        raise Exception(r.json())


def spotify_request(endpoint):
    """Make a request to the specified endpoint"""
    r = requests.get(
        f"https://api.spotify.com/v1/{endpoint}",
        headers={"Authorization": f"Bearer {get_token()}"},
    )
    return {} if r.status_code == 204 else r.json()


def generate_bars(bar_count, rainbow):
    """Build the HTML/CSS for the bars to be injected"""
    bars = "".join(["<div class='bar'></div>" for _ in range(bar_count)])
    css = "<style>"
    if rainbow and rainbow != "false" and rainbow != "0":
        css += ".bar-container { animation-duration: 2s; }"
    spectrum = [
        "#ff0000",
        "#ff4000",
        "#ff8000",
        "#ffbf00",
        "#ffff00",
        "#bfff00",
        "#80ff00",
        "#40ff00",
        "#00ff00",
        "#00ff40",
        "#00ff80",
        "#00ffbf",
        "#00ffff",
        "#00bfff",
        "#0080ff",
        "#0040ff",
        "#0000ff",
        "#4000ff",
        "#8000ff",
        "#bf00ff",
        "#ff00ff",
    ]
    for i in range(bar_count):
        css += f""".bar:nth-child({i + 1}) {{
                animation-duration: {randint(500, 750)}ms;
                background: {spectrum[i] if rainbow and rainbow != 'false' and rainbow != '0' else '#24D255'};
            }}"""
    return f"{bars}{css}</style>"


def load_image_base64(url):
    """Get the base-64 encoded image from url"""
    resposne = requests.get(url)
    return b64encode(resposne.content).decode("ascii")


def get_scan_code(spotify_uri):
    """Get the track code for a song"""
    return load_image_base64(
        f"https://scannables.scdn.co/uri/plain/png/000000/white/640/{spotify_uri}"
    )


def make_svg(spin, scan, theme, rainbow):
    """Render the HTML template with variables"""
    data = spotify_request("me/player/currently-playing")
    if data:
        item = data["item"]
    else:
        item = spotify_request("me/player/recently-played?limit=1")["items"][0]["track"]

    if item["album"]["images"] == []:
        image = B64_PLACEHOLDER_IMAGE
    else:
        image = load_image_base64(item["album"]["images"][1]["url"])

    if scan and scan != "false" and scan != "0":
        bar_count = 10
        scan_code = get_scan_code(item["uri"])
    else:
        bar_count = 12
        scan_code = None

    return render_template(
        "index.html",
        **{
            "bars": generate_bars(bar_count, rainbow),
            "artist": item["artists"][0]["name"].replace("&", "&amp;"),
            "song": item["name"].replace("&", "&amp;"),
            "image": image,
            "scan_code": scan_code if scan_code != "" else B64_PLACEHOLDER_SCAN_CODE,
            "theme": theme,
            "spin": spin,
            "logo": B64_SPOTIFY_LOGO,
        },
    )


app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    resp = Response(
        make_svg(
            request.args.get("spin"),
            request.args.get("scan"),
            request.args.get("theme"),
            request.args.get("rainbow"),
        ),
        mimetype="image/svg+xml",
    )
    resp.headers["Cache-Control"] = "s-maxage=1"
    return resp


if __name__ == "__main__":
    app.run(debug=True)
