from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from werkzeug.datastructures import MultiDict

from app.modules.colors import COLORS


class THEME(Enum):
    LIGHT = "light"
    DARK = "dark"


class CONSTANTS:
    HEX_CODE_LENGTH: int = 6
    MIN_WIDGET_WIDTH: int = 400  # Unused for now but will be used in the future
    MAX_WIDGET_WIDTH: int = 800  # Unused for now but will be used in the future


@dataclass(frozen=True)
class ParsedArgs:
    spin: bool = False
    scan: bool = False
    theme: THEME = THEME.LIGHT
    eq_color: str = COLORS.SPOTIFY_GREEN
    width: int = 500  # Unused for now but will be used in the future

    @property
    def main_background_color(self) -> str:
        if self.theme == THEME.LIGHT:
            return COLORS.GITHUB_LIGHT
        else:
            return COLORS.GITHUB_DARK

    @property
    def scan_color_background(self) -> str:
        if self.theme == THEME.LIGHT:
            return COLORS.BLACK
        else:
            return COLORS.WHITE

    @property
    def scan_color_foreground(self) -> str:
        # The scannables.scdn.co API requires a text color
        if self.theme == THEME.LIGHT:
            return "white"
        else:
            return "black"

    @property
    def title_color(self) -> str:
        if self.theme == THEME.LIGHT:
            return COLORS.BLACK
        else:
            return COLORS.WHITE

    @property
    def subtitle_color(self) -> str:
        return COLORS.GREY

    @property
    def bar_count(self) -> int:
        return 10 if self.scan else 12

    @staticmethod
    def is_truhty(value: str) -> bool:
        return value.lower() in {
            "true",
            "1",
            "yes",
            "on",
        }

    @staticmethod
    def parse_request_args(request_args: MultiDict) -> dict[str, Any]:
        get_param: Callable = request_args.get
        return {
            "spin": ParsedArgs.is_truhty(get_param("spin", "false", type=str)),
            "scan": ParsedArgs.is_truhty(get_param("scan", "false", type=str)),
            "theme": THEME(get_param("theme", THEME.LIGHT.value, type=str)),
            "eq_color": get_param("eq_color", COLORS.SPOTIFY_GREEN, type=str),
            "width": get_param("width", CONSTANTS.MAX_WIDGET_WIDTH, type=int),
        }

    def __post_init__(self) -> None:
        self._validate_spin()
        self._validate_scan()
        self._validate_theme()
        self._validate_eq_color()
        self._validate_width()

    def _validate_spin(self) -> None:
        if not isinstance(self.spin, bool):
            raise ValueError("`spin` must be of type `bool`.")

    def _validate_scan(self) -> None:
        if not isinstance(self.scan, bool):
            raise ValueError("`scan` must be of type `bool`.")

    def _validate_theme(self) -> None:
        if self.theme not in THEME:
            raise ValueError("`theme` must be an instance of `THEME`.")

    def _validate_eq_color(self) -> None:
        if not isinstance(self.eq_color, str):
            raise ValueError("`eq_color` must be of type `str`.")
        if (
            self.eq_color != "rainbow"
            and len(self.eq_color) != CONSTANTS.HEX_CODE_LENGTH
        ):
            raise ValueError(
                "`eq_color` must be a valid hex color code of length 6 without a leading `#`."
            )

    def _validate_width(self) -> None:
        if not isinstance(self.width, int):
            raise ValueError("`width`must be of type `int`.")
        if not (CONSTANTS.MIN_WIDGET_WIDTH <= self.width <= CONSTANTS.MAX_WIDGET_WIDTH):
            raise ValueError(
                f"Width must be ∈ [{CONSTANTS.MIN_WIDGET_WIDTH}, {CONSTANTS.MAX_WIDGET_WIDTH}]."
            )
