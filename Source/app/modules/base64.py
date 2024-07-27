from pathlib import Path

from app.modules.paths import PATHS


class BASE_64:
    BASE_64_FOLDER: Path = PATHS.ROOT_DIRECTORY / "app" / "static" / "base64"

    with open(BASE_64_FOLDER / "spotify_logo.txt") as f:
        SPOTIFY_LOGO: str = f.read()
    with open(BASE_64_FOLDER / "placeholder_image.txt") as f:
        PLACEHOLDER_IMAGE: str = f.read()
    with open(BASE_64_FOLDER / "placeholder_scan_code.txt") as f:
        PLACEHOLDER_SCAN_CODE: str = f.read()
