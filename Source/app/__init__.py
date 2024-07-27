from flask import Flask, Response

from app.modules.functions import make_link_page, make_svg_widget


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    @app.route("/link")
    def link() -> Response:
        """Display setup instructions as well as the current song."""
        resp: Response = Response(
            response=make_link_page(),
            mimetype="text/html",
        )
        resp.headers["Cache-Control"] = "s-maxage=1"  # Cache for 1 second
        resp.headers["Access-Control-Allow-Origin"] = "*"  # Allow all origins
        return resp

    @app.route(rule="/", defaults={"path": ""})
    @app.route(rule="/<path:path>")
    def catch_all(path: str) -> Response:
        """Catch all requests and return the rendered SVG."""
        resp: Response = Response(
            response=make_svg_widget(),
            mimetype="image/svg+xml",
        )
        resp.headers["Cache-Control"] = "s-maxage=1"  # Cache for 1 second
        resp.headers["Access-Control-Allow-Origin"] = "*"  # Allow all origins
        return resp

    return app
