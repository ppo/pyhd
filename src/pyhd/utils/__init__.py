"""
Helpers.
"""

# Table of Contents
#
# === astro.py =====================================================================================
# RE_ECLIPTIC_PARSE   – TODO.
# ZODIAC_SIGN_SEGMENT – TODO.
# ZODIAC_SIGN_SYMBOLS – TODO.
# ZODIAC_SIGN_NAMES   – TODO.
# degrees_to_dms      – Convert the ecliptic longitude from absolute degrees to DMS with zodiac sign.
# dms_to_degrees      – Convert the ecliptic longitude from DMS with zodiac sign to absolute degrees.
#
# === data.py ======================================================================================
# to_dict() – TODO.
#
# === superenum.py =================================================================================
# SuperEnum – Enhanced `Enum` base class.
#
# === swissephemeris.py ============================================================================
# EPHEMERIS_FLAGS           – Flags for regular calculations.
# SOLAR_ARC_EPHEMERIS_FLAGS – Special flags for 88° solar arc calculation.
# Position                  – TODO.
# get_planet_longitude      – Get planet's tropical ecliptic longitude in absolute degrees (0-360).
# datetime_to_julian        – Convert datetime (UTC) to Julian Day.
# julian_to_datetime        – Convert Julian Day to datetime (UTC).
# get_design_datetime       – Calculate the Design time (when Sun is at 88° before birth).
# normalize_degrees         – Normalize degrees to 0-360 range.

from .astro import (
    RE_ECLIPTIC_PARSE,
    ZODIAC_SIGN_NAMES,
    ZODIAC_SIGN_SEGMENT,
    ZODIAC_SIGN_SYMBOLS,
    degrees_to_dms,
    dms_to_degrees,
)
from .data import filter_list, to_dict
from .display import (
    C,
    cprint,
    format_datetime,
    get_indent,
    print_csv_list,
    print_dim,
    print_h1,
    print_h2,
    print_key,
    print_kv,
    print_num_list,
    print_table,
    print_value,
)

# from .superenum import SuperEnum
from .swissephemeris import (
    EPHEMERIS_FLAGS,
    SOLAR_ARC_EPHEMERIS_FLAGS,
    Position,
    datetime_to_julian,
    get_design_datetime,
    get_planet_longitude,
    julian_to_datetime,
    normalize_degrees,
)

__all__ = [
    # From `.astro`.
    "RE_ECLIPTIC_PARSE",
    "ZODIAC_SIGN_NAMES",
    "ZODIAC_SIGN_SEGMENT",
    "ZODIAC_SIGN_SYMBOLS",
    "degrees_to_dms",
    "dms_to_degrees",

    # From `.data`.
    "filter_list",
    "to_dict",

    # From `.display`.
    "C",
    "cprint",
    "format_datetime",
    "get_indent",
    "print_csv_list",
    "print_dim",
    "print_h1",
    "print_h2",
    "print_key",
    "print_kv",
    "print_num_list",
    "print_table",
    "print_value",

    # # From `.superenum`.
    # "SuperEnum",

    # From `.swissephemeris`.
    "EPHEMERIS_FLAGS",
    "SOLAR_ARC_EPHEMERIS_FLAGS",
    "Position",
    "datetime_to_julian",
    "get_design_datetime",
    "get_planet_longitude",
    "julian_to_datetime",
    "normalize_degrees",
]
