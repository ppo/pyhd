"""
Swiss Ephemeris wrapper for planetary position calculations.

`calc_ut()` returns `(xx, ret)` – where `xx` is:
- 0: Ecliptic longitude in tropical zodiac
- 1: Ecliptic latitude in tropical zodiac
- 2: Distance
- 3: Longitude speed in degrees per day
- 4: Latitude speed in degrees per day
- 5: Speed distance

🔴 `swe_utc_to_jd()` is more precise because it handles leap seconds properly.
UTC has had 27 leap seconds added between 1972 and 2017 (and counting). These are one-second
adjustments to keep UTC synchronized with Earth's rotation.
For example: 2016-12-31 23:59:60 UTC existed

    `swe_julday(year, month, day, hour)`
        - Simple calendar → Julian Day conversion
        - Assumes smooth, continuous time
        - No leap second corrections
        - Good enough for most purposes (precision ~1 second)

    `swe_utc_to_jd(year, month, day, hour, min, sec, gregflag)`
        - Accounts for leap seconds inserted into UTC since 1972
        - Returns two Julian Day values:
            - JD in TT (Terrestrial Time / Ephemeris Time)
            - JD in UT1 (Universal Time)
        - Precision to the second level
        - Handles the discontinuities in the UTC time scale

Requirements: https://github.com/astrorigin/pyswisseph
Doc:
- https://www.astro.com/swisseph/swephprg.htm
- https://github.com/aloistr/swisseph/
"""

from datetime import UTC, datetime

import swisseph as swe

from ..constants import DESIGN_IMPRINT_DEGREES, Planets

# Configure Swiss Ephemeris.
# Use Moshier (built-in, no external files needed). Precision: ~0.001° for inner planets.
# Note: Pre-computed tables are slightly more accurate (~0.0001°). Not necessary here.
#   Files are needed for research-grade astrological work or asteroid calculations.
swe.set_ephe_path(None)

# Flags for regular calculations.
EPHEMERIS_FLAGS = swe.FLG_MOSEPH

# Special flags for 88° solar arc calculation.
# `swe.FLG_SPEED` returns also the planet's velocity (degrees per day).
# This can potentially be helpful for 88° solar arc iteration – but not required.
SOLAR_ARC_EPHEMERIS_FLAGS = EPHEMERIS_FLAGS | swe.FLG_SPEED


class Position:
    """TODO.

    Or Emphemeris, Astro? Containing all utils?

    Props:
        - sign  # zodiac_sign
        - symbol  # zodiac_sign_symbol
        - dms
        - lon
        - ❓ gate
        - ❓ line, color, tone, base
    Class Methods:
        - degrees_to_dms(cls, degrees: float) -> str
        - dms_to_degrees(cls, dms: str) -> float
    """

    def __init__(self, position: float | str) -> None:
        # Store lon|dms => keep precision? + lazy conversion
        self.lon = (position if isinstance(position, float)
                    else self.dms_to_degrees(position))


def get_planet_longitude(planet: Planets, dt: datetime) -> float | dict[str, float]:
    """Get planet's tropical ecliptic longitude in absolute degrees (0-360).

    Remarks:
    - In `PLANETS`, `EARTH` = `swe.SUN` and `NORTH_NODE` & `SOUTH_NODE` = `swe.TRUE_NODE`.
    - `Earth` must be calculated as `Sun + 180°`.
    - True Node is the actual lunar node position – the precise, real-time point where the Moon’s
      orbit intersects the ecliptic (the Sun’s apparent path). Do NOT use Mean Node.
    - `North Node` and `South Node` are always exactly opposite each other on a celestial chart.
    - `North Node` is the `True Node`.
    - `South Node` must be calculated as `True Node + 180°`.

    Args:
        planet: Planet enum
        dt: Datetime (UTC, timezone-aware)

    Returns:
        Longitude in degrees (0-360)
    """
    jd = datetime_to_julian(dt)
    longitude = swe.calc_ut(jd, planet.swe_id, EPHEMERIS_FLAGS)[0][0]

    # Special cases: Earth and South Node are 180° opposite of Sun and North Node.
    if planet in (Planets.EARTH, Planets.SOUTH_NODE):
        longitude += 180

    return normalize_degrees(longitude)


def datetime_to_julian(dt: datetime) -> float:
    """Convert datetime (UTC) to Julian Day."""
    # Require a timezone-aware datetime to be sure.
    # We could assume it's an UTC time but it's not really safe.
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware.")

    # Convert to UTC.
    dt_utc = dt.astimezone(UTC)

    # 🔴
    # hour_decimal = (dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600
    #                 + dt_utc.microsecond / 3_600_000_000)  # For extreme precision! ;-)
    #
    # return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour_decimal)
    # ^^^^^^^^^^^^^^^^^^^^^

    second_decimal = dt_utc.second + (dt_utc.microsecond / 1_000_000)

    # `swe_utc_to_jd()` returns `(jd_et, jd_ut1)`.
    result = swe.utc_to_jd(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour, dt_utc.minute,
                           second_decimal, swe.GREG_CAL)

    # `result[0]` is JD in ET/TT (for theoretical calculations).
    # `result[1]` is JD in UT1 (what we want for apparent positions).
    return result[1]  # UT1 for astronomical positions

def julian_to_datetime(jd: float) -> datetime:
    """Convert Julian Day to datetime (UTC).

    Note: Microsecond precision may vary due to floating-point limitations.
    """
    # 🔴
    # year, month, day, hour_decimal = swe.revjul(jd, swe.GREG_CAL)
    #
    # # Convert decimal hours to time components.
    # total_seconds = hour_decimal * 3600
    # hour, remainder = divmod(total_seconds, 3600)
    # minute, remainder = divmod(remainder, 60)
    # second, remainder = divmod(remainder, 1)
    # microsecond = round((remainder % 1) * 1_000_000)
    # # Remark: `round()` minimizes the rounding error compared to `int()`.
    #
    # hour, minute, second = int(hour), int(minute), int(second)
    # ^^^^^^^^^^^^^^^^^^^^^

    # `swe_jdut1_to_utc()` returns `(year, month, day, hour, min, sec)`.
    result = swe.jdut1_to_utc(jd, swe.GREG_CAL)

    year, month, day, hour, minute, second_decimal = result

    # Split seconds into integer and fractional parts.
    second = int(second_decimal)
    microsecond = round((second_decimal - second) * 1_000_000)

    return datetime(year, month, day, hour, minute, second, microsecond, tzinfo=UTC)


def get_design_datetime(birth_dt: datetime) -> tuple[datetime, float]:
    """Calculate the Design time (when Sun is at 88° before birth).

    Uses Newton-Raphson iteration to find the moment when the Sun's longitude was exactly 88°
    before its position at birth.

    The algorithm:
    1. Starts with an initial estimate (~88.5 days before birth)
    2. Calculates the angular error (target - current position)
    3. Uses the Sun's velocity to estimate the time correction needed
    4. Iterates until the error is below tolerance (typically 3-4 iterations)

    The angular difference is normalized to [-180°, +180°] to handle the circular nature of angles,
    ensuring we always move in the shortest direction (critical when crossing the 0°/360° boundary).

    Args:
        birth_dt: Birth datetime in UTC.

    Returns:
        Tuple(design datetime, longitude).
    """
    # Average Sun speed estimated based on its known min and max speeds.
    AVG_SUN_SPEED = (0.95 + 1.02) / 2
    # Average days required for the Sun to move `DESIGN_IMPRINT_DEGREES`°.
    AVG_DIFF_DAYS = DESIGN_IMPRINT_DEGREES / AVG_SUN_SPEED
    # Max iterations for Newton-Raphson algorithm. It typically takes 3-4 iterations.
    MAX_ITERATIONS = 10
    # Precision we tolerate for the Design Imprint shift.
    # Note: 0.1 arcsecond (1/36_000_000) is the max achievable with double-precision.
    TOLERANCE_DEGREES = 1 / (60 * 60 * 10_000)

    # Calculate the target longitude for the Design Imprint.
    birth_jd = datetime_to_julian(birth_dt)
    birth_lon = swe.calc_ut(birth_jd, swe.SUN, EPHEMERIS_FLAGS)[0][0]
    design_lon = normalize_degrees(birth_lon - DESIGN_IMPRINT_DEGREES)

    # Start with birth time - average days calculated above.
    current_jd = birth_jd - AVG_DIFF_DAYS

    # Iterate to located the desired position of the Sun.
    for _ in range(MAX_ITERATIONS):
        # Get current position and velocity of the Sun.
        data, _ = swe.calc_ut(current_jd, Planets.SUN.swe_id, SOLAR_ARC_EPHEMERIS_FLAGS)
        longitude = data[0]  # Longitude in degrees
        current_speed = data[3]  # Velocity in degrees/day

        # Calculate angular difference, normalized to [-180°, +180°] range.
        # This ensures we always take the shortest path on the circle (ex: 2 - 358 = -356° => +4°).
        diff = (design_lon - longitude + 180) % 360 - 180

        # Check if we've reached target precision.
        if abs(diff) < TOLERANCE_DEGREES:
            break

        # Newton-Raphson step: adjust time by (angular error / angular velocity).
        current_jd += diff / current_speed

    else:
        # Should never reach here, but log if we do.
        print(f"Warning: get_design_datetime() didn't converge after {MAX_ITERATIONS} iterations."
              f"Final diff: {abs(diff):.6f}° ({abs(diff) * 3600:.2f} arcsec)")

    return julian_to_datetime(current_jd), longitude


def normalize_degrees(degrees: float) -> float:
    """Normalize degrees to 0-360 range.

    See https://github.com/aloistr/swisseph/blob/0a869a82130ebf2c4a47c1dfc32ace619412915e/swephlib.c#L104
    """
    return swe.degnorm(degrees)
