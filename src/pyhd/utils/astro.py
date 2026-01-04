"""
Astronomy/astrology helpers.

Terminology:
- Ecliptic longitude (or just "longitude") is the angular position along the ecliptic. {TODO: define ecliptic}
  It's the absolute degrees (0-360) – measured from 0°00'00" Aries. Ex: `223.25°`.
- Ecliptic position in DMS is the ecliptic longitude expressed in degrees-minutes-seconds within
  a zodiac sign. Ex: `13°15'00" ♏︎` or `13°15'00" Scorpio`.
"""

import re

from .swissephemeris import normalize_degrees

RE_ECLIPTIC_PARSE = re.compile(r"""^(\d+)°(\d+)'(\d+)" (.+)$""")

ZODIAC_SIGN_SEGMENT = 30.0

ZODIAC_SIGN_SYMBOLS = ("♈︎", "♉︎", "♊︎", "♋︎", "♌︎", "♍︎", "♎︎", "♏︎", "♐︎", "♑︎", "♒︎", "♓︎")
ZODIAC_SIGN_NAMES = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio",
                     "Sagittarius", "Capricorn", "Aquarius", "Pisces")


def degrees_to_dms(degrees: float, use_symbol: bool = True) -> str:
    """Convert the ecliptic longitude from absolute degrees to DMS with zodiac sign.

    Args:
        degrees: Ecliptic longitude in absolute degrees (0-360). Ex: `223.25`.
        use_symbol: If True, use symbol (`♏︎`), otherwise name (`Scorpio`).

    Returns:
        Ecliptic longitude in DMS with zodiac sign (ex: `13°15'00" ♏︎` or `13°15'00" Scorpio`).
    """
    # Normalize to 0-360.
    degrees = normalize_degrees(degrees)

    # Find astrological sign (each sign is 30°).
    sign_index, position_in_sign = divmod(degrees, ZODIAC_SIGN_SEGMENT)
    sign_index = int(sign_index)
    sign = (ZODIAC_SIGN_SYMBOLS[sign_index] if use_symbol
            else ZODIAC_SIGN_NAMES[sign_index])

    # Calculate position within sign.
    degrees, remainder = divmod(position_in_sign, 1)
    minutes, remainder = divmod(remainder * 60, 1)
    seconds = round(remainder * 60)  # Use `round()` for better floating-point handling.
    degrees, minutes = int(degrees), int(minutes)

    return f"""{degrees}°{minutes:02d}'{seconds:02d}" {sign}"""


def dms_to_degrees(dms: str) -> float:
    """Convert the ecliptic longitude from DMS with zodiac sign to absolute degrees.

    Args:
        dms: Ecliptic longitude in DMS with zodiac sign (ex: `13°15'00" ♏︎` or `13°15'00" Scorpio`).

    Returns:
        Ecliptic longitude in absolute degrees (0-360). Ex: `223.25`.
    """
    # Parse degrees, minutes, seconds, sign.
    match = RE_ECLIPTIC_PARSE.match(dms)
    if not match:
        raise ValueError(f"Invalid position format: {dms}")

    degrees = int(match.group(1))
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    sign = match.group(4).strip()
    use_symbols = len(sign) == 1

    # Find the index of `sign` to calculate offset.
    try:
        sign_index = (ZODIAC_SIGN_SYMBOLS.index(sign) if use_symbols
                      else ZODIAC_SIGN_NAMES.index(sign))
        sign_offset = sign_index * ZODIAC_SIGN_SEGMENT
    except ValueError:
        sign_type = "symbol" if use_symbols else "name"
        raise ValueError(f"Invalid zodiac sign {sign_type}: {sign}")

    # Calculate absolute degrees
    position_degrees = degrees + minutes / 60 + seconds / 3600
    return normalize_degrees(sign_offset + position_degrees)
