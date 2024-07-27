from base64 import b64encode
from random import randint
from typing import Any, Dict, Union

from flask import render_template, request
from requests import get, post, Response
from werkzeug.datastructures import MultiDict

from app.modules.base64 import BASE_64
from app.modules.colors import COLORS
from app.modules.environment_variables import ENV_VARS
from app.modules.parsed_arguments import ParsedArgs


class SpotifyAPI:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

    def get_token(self) -> str:
        """Get a new access token."""
        response: Response = post(
            url="https://accounts.spotify.com/api/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make a request to the specified Spotify endpoint."""
        token = self.get_token()
        response: Response = get(
            url=f"https://api.spotify.com/v1/{endpoint}",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        response.raise_for_status()
        return {} if response.status_code == 204 else response.json()


class ImageLoader:
    @staticmethod
    def load_base_64_image_from_url(image_url: str) -> str:
        """Get the Base64 encoded image from url."""
        response: Response = get(image_url)
        response.raise_for_status()
        return b64encode(response.content).decode("ascii")


class WidgetGenerator:
    @staticmethod
    def generate_eq_bars_html(bar_count: int, eq_color: str) -> str:
        """Build the HTML/CSS snippets for the equalizer bars to be injected."""
        css: str = ""
        if eq_color == "rainbow":
            css += ".bar-container { animation-duration: 2s; }"
        for i in range(bar_count):
            random_duration: int = randint(500, 750)
            background_color: str = (
                COLORS.SPECTRUM[i] if eq_color == "rainbow" else eq_color
            )
            css += f""".bar:nth-child({i + 1}) {{
                animation-duration: {random_duration}ms;
                background: #{background_color};
            }}"""
        bar_html: str = "<div class='bar'></div>"
        eq_bars_html: str = "".join([bar_html for _ in range(bar_count)])
        return f"""
            {eq_bars_html}
            <style>{css}</style>
        """


def parse_request_args(request_args: MultiDict) -> ParsedArgs:
    """Parse the request args into a ParsedArgs object."""
    parsed_request_args: Dict[str, Any] = ParsedArgs.parse_request_args(request_args)
    return ParsedArgs(**parsed_request_args)


def get_track(spotify_api: SpotifyAPI) -> Dict[str, Any]:
    """Get the currently playing track."""
    now_playing: Dict[str, Any] = spotify_api.make_request(
        "me/player/currently-playing"
    )
    recently_played: Dict[str, Any] = spotify_api.make_request(
        "me/player/recently-played?limit=1"
    )

    now_playing_track: Dict[str, Any] | None = now_playing.get("item")
    recently_played_track: Dict[str, Any] = recently_played.get("items", [{}])[0].get(
        "track"
    )

    return now_playing_track if now_playing_track else recently_played_track


def get_base_64_track_image(track: Dict[str, Any]) -> str:
    """Get the Base64 encoded image from a track."""
    images = track.get("album", {}).get("images", [])
    if images:
        album_image_url: str = images[1]["url"]
        return ImageLoader.load_base_64_image_from_url(album_image_url)
    return BASE_64.PLACEHOLDER_IMAGE


def get_base_64_scan_code(spotify_uri: str, background: str, foreground: str) -> str:
    """Get the track (scan) code for a song in Base64."""
    scan_code_url = f"https://scannables.scdn.co/uri/plain/png/{background}/{foreground}/500/{spotify_uri}"
    return (
        ImageLoader.load_base_64_image_from_url(scan_code_url)
        or BASE_64.PLACEHOLDER_SCAN_CODE
    )


def prepare_widget_template_variables(
    parsed_args: ParsedArgs, spotify_api: SpotifyAPI
) -> Dict[str, Union[str, bool]]:
    track = get_track(spotify_api)

    eq_bars_html = WidgetGenerator.generate_eq_bars_html(
        parsed_args.bar_count, parsed_args.eq_color
    )
    track_name = track.get("name", "Unknown Track")
    track_artist = track.get("artists", [{}])[0].get("name", "Unknown Artist")
    base_64_track_image = get_base_64_track_image(track)
    base_64_scan_code = (
        get_base_64_scan_code(
            track["uri"],
            parsed_args.scan_color_background,
            parsed_args.scan_color_foreground,
        )
        if parsed_args.scan
        else ""
    )
    spin = parsed_args.spin
    logo = BASE_64.SPOTIFY_LOGO
    title_color = f"#{parsed_args.title_color}"
    subtitle_color = f"#{parsed_args.subtitle_color}"
    background_color = f"#{parsed_args.main_background_color}"

    return {
        "eq_bars_html": eq_bars_html,
        "track_name": track_name,
        "track_artist": track_artist,
        "base_64_track_image": base_64_track_image,
        "base_64_scan_code": base_64_scan_code,
        "spin": spin,
        "logo": logo,
        "title_color": title_color,
        "subtitle_color": subtitle_color,
        "background_color": background_color,
    }


def make_svg_widget() -> str:
    """Returns the HTML of the widget to be rendered."""
    parsed_args = parse_request_args(request.args)
    spotify_api = SpotifyAPI(
        client_id=ENV_VARS.CLIENT_ID,
        client_secret=ENV_VARS.CLIENT_SECRET,
        refresh_token=ENV_VARS.REFRESH_TOKEN,
    )
    template_variables = prepare_widget_template_variables(parsed_args, spotify_api)
    return render_template("widget.html", **template_variables)


def make_link_page() -> str:
    """Returns the HTML of the link page to be rendered."""
    spotify_api = SpotifyAPI(
        client_id=ENV_VARS.CLIENT_ID,
        client_secret=ENV_VARS.CLIENT_SECRET,
        refresh_token=ENV_VARS.REFRESH_TOKEN,
    )
    track = get_track(spotify_api)
    track_id = track["id"]
    embed_link = f"https://open.spotify.com/embed/track/{track_id}"
    return render_template("link.html", embed_link=embed_link)
