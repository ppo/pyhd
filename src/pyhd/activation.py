"""
Activation: Provides Gate, Line, Color, Tone, Base for a planet body at a given time.

Variables Online Calculators:
- [Genetic Matrix](https://www.geneticmatrix.com/) (via variable values, not numbers)
- 🤔 Leann Wolff: [Power of Self](https://www.powerofself.ca/humandesginvariablecalculator)
- 🤔 [Vaness Henry](https://www.vanesshenry.com/variable-calculator)
"""

from datetime import datetime
from typing import Iterable

from .constants import (
    BASE_SEGMENT,
    COLOR_SEGMENT,
    GATE_SEGMENT,
    GATE_WHEEL_START_DEGREES,
    LINE_SEGMENT,
    TONE_SEGMENT,
    Bases,
    Colors,
    Gates,
    Lines,
    Planets,
    Tones,
)
from .models import ActivationLightModel, ActivationModel
from .utils import filter_list, get_planet_longitude, normalize_degrees


class Activation:
    """A planetary activation.

    Provides Gate, Line, Color, Tone, Base for a planet body at a given time.
    """

    PROPS = (
        "planet", "dt",
        "longitude", "angle", "gate", "line", "color", "tone", "base",
        "color_percentage", "tone_percentage", "base_percentage",
    )

    def __init__(self, planet: Planets, dt: datetime) -> None:
        self.planet = planet
        self.dt = dt

        self._compute_position()
        self._compute_data()

    def __str__(self) -> str:
        return f"{self.gate.num}.{self.line}.{self.color}.{self.tone}"  # TODO: .{self.base}

    def __repr__(self) -> str:
        return f"Activation({self.planet}: {self})"

    # TODO: Better as lazy computation? Gate…Base are not.
    # @cached_property
    # def longitude(self) -> float:
    #     """Calculate the position (ecliptic longitude in absolute degrees)."""
    #     return get_planet_longitude(self.planet, self.dt)
    #
    # @cached_property
    # def angle(self) -> float:
    #     """Calculate the angular distance from first Gate's start to the planet's position.
    #
    #     Note: Counterclockwise around the Wheel.
    #     """
    #     return normalize_degrees(self.longitude - GATE_WHEEL_START_DEGREES)

    def _compute_position(self) -> None:
        """Compute longitude and angle."""
        # Calculate the position (ecliptic longitude in absolute degrees).
        self.longitude = get_planet_longitude(self.planet, self.dt)

        # Calculate the angular distance from first Gate's start to the planet's position.
        # Note: Mathematical convention: Angles are conventionally measured counterclockwise from 0°.
        self.angle = normalize_degrees(self.longitude - GATE_WHEEL_START_DEGREES)

    def _compute_data(self) -> None:
        """Compute Gate, Line, Color, Base, Tone, Base."""
        gate_index,  position_in_gate  = divmod(self.angle,        GATE_SEGMENT)
        line_index,  position_in_line  = divmod(position_in_gate,  LINE_SEGMENT)
        color_index, position_in_color = divmod(position_in_line,  COLOR_SEGMENT)
        tone_index,  position_in_tone  = divmod(position_in_color, TONE_SEGMENT)
        base_index,  position_in_base  = divmod(position_in_tone,  BASE_SEGMENT)

        self.gate  = Gates.get_by_wheel_index(int(gate_index))
        self.line  = Lines(int(line_index + 1))
        self.color = Colors(int(color_index + 1))
        self.tone  = Tones(int(tone_index + 1))
        self.base  = Bases(int(base_index + 1))

        # TODO: Calculate relative position within segment.
        self.color_percentage = position_in_color / COLOR_SEGMENT * 100.0
        self.tone_percentage  = position_in_tone / TONE_SEGMENT * 100.0
        self.base_percentage  = position_in_base / BASE_SEGMENT * 100.0

        # TODO: ?
        # Option 1: Distance to nearest edge (0-50%, where 50% = maximum certainty)
        #   self.color_certainty = min(position_in_color / COLOR_SEGMENT, 1 - position_in_color / COLOR_SEGMENT) * 100.0
        # Option 2: Normalized certainty (0 = on edge, 100 = dead center)
        #   self.color_certainty = (1 - 2 * abs(0.5 - (position_in_color / COLOR_SEGMENT))) * 100.0

        # self.is_retrograde = ???  TODO: Useful? How to find that?

    def _compute_proximity(self):
        """Calculate the proximity of data to the closest edge of the segment.

        🟠 This allows to estimate the truth probability (as the birth time is often approximative).
        """
        pass

    # EXPORT ---------------------------------------------------------------------------------------

    def to_dict(self, include: Iterable[str] = None, exclude: Iterable[str] = None) -> dict:
        """Return a dict representation of this Activation."""
        keys = filter_list(self.PROPS, include=include, exclude=exclude)
        return {k: getattr(self, k) for k in keys}

    def to_light_model(self) -> ActivationLightModel:
        """Capture current computed state as an immutable model."""
        props = (p for p in self.PROPS if p not in ("planet", "dt"))
        return ActivationLightModel(**{p: getattr(self, p) for p in props})

    def to_model(self) -> ActivationModel:
        """Capture current computed state as an immutable model."""
        return ActivationModel(**{p: getattr(self, p) for p in self.PROPS})
