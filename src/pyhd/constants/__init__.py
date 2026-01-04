"""
Constants.

Conventions:
- `name` is the default string representation.
- `title` is used for the name of elements that are usually referred by a number.
  Ex: "Investigator" for Line 1.
- `full_name` provides the fully detailed name.
  Ex: "1: Investigator", "4/1: Opportunist/Investigator", "☉ Sun".
    - The default `full_name` returns "<name>: <title>" if `title` exists; otherwise simply `name`.

Design Decisions:
- The Enums are used everywhere as return values. So they are "all-included" for a better DX – at
  the cost of some redundancy in definition.
- 🔴 This library is meant to be as precise as it can. So an Enum contains all possible values – i.e.
  overarching types and all subtypes. Ex: "Projector" and "Mental Projector", "Energy Projector",
  "Classic Projector".
  - As convenience for list manipulations, there's an `<overarching>_<enum>S` constant listing all
    subtypes.
  - As convenience for quick testing from the return value, there's an `is_<overarching>` property
    for each overarching type.

Requirements:
- [Python extension to Swiss Ephemeris](https://github.com/astrorigin/pyswisseph)

References:
- "[The Definitive Book of Human Design](https://www.ihdschool.com/products/definitive-book)"
  by Ra Uru Hu, Lynda Bunnell (ISBN: 978-0615552149)
"""

# ruff: noqa
# Note: Formatted for readability and multi-cursor manipulations.

# Table of Contents:
#
# === ASTRONOMY & I CHING ==========================================================================
# DESIGN_IMPRINT_DEGREES    | float        | Design Imprint time (= when the Sun is at 88° before birth).
# GATE_WHEEL_START_DEGREES  | float        | Position of the beginning of the first Gate in the I Ching Wheel.
# NUM_GATES                 | int          | Number of Gates in the I Ching Wheel.
# NUM_LINES                 | int          | Number of Lines per Gate.
# NUM_COLORS                | int          | Number of Colors per Line.
# NUM_TONES                 | int          | Number of Tones per Color.
# NUM_BASES                 | int          | Number of Bases per Tone.
# GATE_SEGMENT              | float        | Subdivision segment for a Gate.
# LINE_SEGMENT              | float        | Subdivision segment for a Line.
# COLOR_SEGMENT             | float        | Subdivision segment for a Color.
# TONE_SEGMENT              | float        | Subdivision segment for a Tone.
# BASE_SEGMENT              | float        | Subdivision segment for a Base.
#
# Planets                   | SuperEnum    | The 13 planets (celestial bodies).
# Imprints                  | SuperEnum    | The 2 Imprints.
#
# === CENTERS ======================================================================================
# Centers                   | SuperEnum    | The 9 Centers.
#
# MANIFESTATION_CENTERS     | tuple        | List of manifestation Centers.
# PRESSURE_CENTERS          | tuple        | List of pressure Centers.
# AWARENESS_CENTERS         | tuple        | List of awareness Centers.
# MOTOR_CENTERS             | tuple        | List of motor Centers.
# NON_MOTOR_CENTERS         | tuple        | List of non-motor Centers.
# IDENTITY_CENTERS          | tuple        | List of identity Centers.
# NON_SACRAL_MOTOR_CENTERS  | tuple        | List of non-Sacral motor Centers.
# CLASSIC_PROJECTOR_CENTERS | tuple        | List of Centers to identify Classic Projectors.
# MENTAL_PROJECTOR_CENTERS  | tuple        | List of Centers to identify Mental Projectors.
#
# DefinitionTypes           | SuperEnum    | The 4-6 Definition Types.
#
# SPLIT_DEFINITION_TYPES    | tuple        | Sub-types of the overarching Split Type.
#
# === GATES ========================================================================================
# Quarters                  | SuperEnum    | The 4 Quarters.
# Gates                     | SuperEnum    | The 64 Gates.
# TODO: ? `EmotionalWaveTypes`: Ratchet, Spike, Crash
# TODO: ? `EmotionalWaveVariations` (& Gates): Tribal/Need (6, 37, 49), Individual/Passion (22, 55), Collective/Desire (30, 36)
#
# === CHANNELS =====================================================================================
# Circuits                  | SuperEnum    | The 6 Circuits.
# CircuitGroups             | SuperEnum    | The 3 Circuit Groups.
# ChannelTypes              | SuperEnum    | The 4 Channel Types.
# Channels                  | SuperEnum    | The 36 Channels.
#
# INTEGRATION_CHANNEL       | tuple        | List of Channels forming the Integration Channel.
#
# === TYPES ========================================================================================
# Strategies                | SuperEnum    | The 4 Strategies.
# Signatures                | SuperEnum    | The 4 Signatures.
# NotSelfThemes             | SuperEnum    | The 4 Not-Self Themes.
# Types                     | SuperEnum    | The 4+1 Types.
#
# GENERATOR_TYPES           | tuple        | Sub-types of the overarching Generator Type.
# PROJECTOR_TYPES           | tuple        | Sub-types of the overarching Projector Type.
# ENERGY_TYPES              | tuple        | List of energy Types.
# NON_ENERGY_TYPES          | tuple        | List of non-energy Types.
#
# === CROSSES ======================================================================================
# Destinies                 | SuperEnum    | The 3 Destinies.
# Geometries                | SuperEnum    | The 3 Geometries.
# Crosses                   | SuperEnum    | The 192 Incarnation Crosses.
#
# === PROFILES =====================================================================================
# Lines                     | SuperEnum    | The 6 (Profile) Lines.
# Profiles                  | SuperEnum    | The 12 Profiles.
#
# === AUTHORITIES ==================================================================================
# Authorities               | SuperEnum    | The 8 (Inner Personal) Authorities.
#
# === STATES =======================================================================================
# StateEnum                 | Base Class   | Base `SuperEnum` for the states.
#
# CenterStates              | SuperEnum    | The 3 possible states for Centers.
# ChannelStates             | SuperEnum    | The 2 possible states for Channels.
# GateStates                | SuperEnum    | The 6 possible states for Gates.
#
# === VARIABLES ====================================================================================
# Colors                    | SuperEnum    | The 6 Colors.
# Tones                     | SuperEnum    | The 6 Tones.
# Bases                     | SuperEnum    | The 5 Bases.
#
# Orientations              | SuperEnum    | The 2 Orientations for Variables.
# VariableOrientations      | SuperEnum    | The 16 Variable Orientations.
#
# VariableEnum              | Base Class   | Base `SuperEnum` for the concrete Variables.
#
# Determinations            | VariableEnum | The 6 Determinations (Design Sun Color, top-left Variable).
# Cognitions                | VariableEnum | The 6 Cognitions (Design Sun Tone, top-left Variable).
# Environments              | VariableEnum | The 6 Environments (Design North Node Color, bottom-left Variable).
# Perspectives              | VariableEnum | The 6 Perspectives (Personality North Node Color, bottom-right Variable).
# Motivations               | VariableEnum | The 6 Motivations (Personality Sun Color, top-right Variable).
# Senses                    | VariableEnum | The 6 Senses (Personality Sun Tone, top-right Variable).

from functools import cached_property

import swisseph as swe

from .superenum import SuperEnum


# ==================================================================================================
# ASTRONOMY & I CHING
# ==================================================================================================

# Design Imprint time (= when the Sun is at 88° before birth).
DESIGN_IMPRINT_DEGREES = 88.0

# Position of the start of the first Gate in the I Ching Wheel (angle, in degrees).
# Gates are listed counterclockwise starting from Gate 41 beginning at 02°00'00" Aquarius (= 302°).
# Note: Mathematical convention: Angles are conventionally measured counterclockwise from 0°.
# TODO: Why does SharpAstrology use `3.875`? https://github.com/CReizner/SharpAstrology.HumanDesign/blob/v1.1.2/Utility/HumanDesignUtility.cs#L12
GATE_WHEEL_START_DEGREES = 302.0

# Number of subdivisions of the I Ching Wheel.
NUM_GATES  = 64  # Total in the Wheel:     64
NUM_LINES  = 6   # Total in the Wheel:    384
NUM_COLORS = 6   # Total in the Wheel:  2.304
NUM_TONES  = 6   # Total in the Wheel: 13.824
NUM_BASES  = 5   # Total in the Wheel: 69.120

# Degrees of each subdivision segment.
# Note: Tone and base are not hardcoded as they require extra precision.
GATE_SEGMENT  = 5.625            # 360° ÷ 64 gates
LINE_SEGMENT  = 0.9375           # ÷ 6 lines
COLOR_SEGMENT = 0.15625          # ÷ 6 colors
TONE_SEGMENT  = 0.15625 / 6      # ÷ 6 tones (~0.026041667)
BASE_SEGMENT  = 0.15625 / 6 / 5  # ÷ 5 bases (~0.005208333)


# PLANETS ------------------------------------------------------------------------------------------

class Planets(SuperEnum):
    """The 13 planets (celestial bodies).

    These are all the celestial bodies that can activate Gates.

    Fields:
    - `name`: Name of the planet.
    - `symbol`: Symbol of the planet.
    - `swe_id`: Swiss Ephemeris ID.

    Remarks related to Swiss Ephemeris:
    - `swe.EARTH` (14) is the heliocentric Earth position (Earth's position as seen from the Sun).
    - `Earth` must be calculated as `Sun + 180°`.
    - `True Node` is the precise, real-time point where the Moon's orbit intersects the ecliptic
      (the Sun's apparent path).
    - `North Node` and `South Node` are always exactly opposite each other on a celestial chart.
    - `North Node` is the `True Node`.
    - `South Node` must be calculated as `True Node + 180°`.

    References: "The Definitive Book of Human Design" p36-38.
    """
    # Sorting: Book order.
    __FIELDS__ = "name",        "symbol",  "swe_id"
    SUN        = "Sun",         "☉",       swe.SUN
    EARTH      = "Earth",       "⊕",       swe.SUN
    MOON       = "Moon",        "☽",       swe.MOON
    NORTH_NODE = "North Node",  "☊",       swe.TRUE_NODE
    SOUTH_NODE = "South Node",  "☋",       swe.TRUE_NODE
    MERCURY    = "Mercury",     "☿",       swe.MERCURY
    VENUS      = "Venus",       "♀",       swe.VENUS
    MARS       = "Mars",        "♂",       swe.MARS
    JUPITER    = "Jupiter",     "♃",       swe.JUPITER
    SATURN     = "Saturn",      "♄",       swe.SATURN
    URANUS     = "Uranus",      "⛢",       swe.URANUS
    NEPTUNE    = "Neptune",     "♆",       swe.NEPTUNE
    PLUTO      = "Pluto",       "♇",       swe.PLUTO

    @property
    def full_name(self) -> str:
        """Return the symbol and name."""
        return f"{self.symbol} {self.name}"

    @classmethod
    def get_by_swe_id(cls, swe_id: int) -> "Planets":
        """Return the Planet associated with the given Swiss Ephemeris ID."""
        # TODO: How to handle Earth and South Node?!
        for planet in cls:
            if planet.swe_id == swe_id:
                return planet

        raise ValueError(f"No Planet found with Swiss Ephemeris ID {swe_id}.")


# IMPRINTS -----------------------------------------------------------------------------------------

class Imprints(SuperEnum):
    """The 2 Imprints.

    - The Personality Imprint is at the time of birth (when the baby has left the womb, not when the
        umbilical cord is cut).
    - The Design Imprint is when the Personality Crystal is brought into the body (88° of the Sun
        before birth).

    References: "The Definitive Book of Human Design" p31.
    """
    DESIGN      = "Design"
    PERSONALITY = "Personality"


# ==================================================================================================
# CENTERS
# ==================================================================================================

# CENTERS ------------------------------------------------------------------------------------------

class Centers(SuperEnum):
    """The 9 Centers.

    References: "The Definitive Book of Human Design" p44-103. Glossary: p423.
    """
    # Sorting: From bottom to top.
    ROOT         = "Root"          # [Ref. p61-65]
    SPLENIC      = "Splenic"       # [Ref. p71-76]
    SACRAL       = "Sacral"        # [Ref. p91-96]
    SOLAR_PLEXUS = "Solar Plexus"  # [Ref. p77-85]
    HEART        = "Heart"         # [Ref. p86-90]
    G            = "G"             # [Ref. p97-103]
    THROAT       = "Throat"        # [Ref. p52-56]
    AJNA         = "Ajna"          # [Ref. p66-70]
    HEAD         = "Head"          # [Ref. p57-60]

    @property
    def channels(self) -> tuple["Channels"]:
        """Return the list of Channels related to this Center."""
        return tuple(channel for channel in Channels if self in channel.centers)

    @property
    def gates(self) -> tuple["Gates"]:
        """Return the list of Gates included in this Center."""
        return tuple(gate for gate in Gates if gate.center == self)

    @property
    def is_motor(self) -> bool:
        """Return whether this is a Motor Center."""
        return self in MOTOR_CENTERS


# LISTS FOR CENTERS --------------------------------------------------------------------------------

# Different categories of Centers. [Ref. p45]
# Sorting: Centers from bottom to top.
MANIFESTATION_CENTERS = (Centers.THROAT,)
PRESSURE_CENTERS      = (Centers.ROOT, Centers.HEAD)
AWARENESS_CENTERS     = (Centers.SPLENIC, Centers.SOLAR_PLEXUS, Centers.AJNA)
MOTOR_CENTERS         = (Centers.ROOT, Centers.SACRAL,  Centers.SOLAR_PLEXUS,  Centers.HEART)
NON_MOTOR_CENTERS     = (Centers.SPLENIC, Centers.G,  Centers.THROAT,  Centers.AJNA,  Centers.HEAD)
IDENTITY_CENTERS      = (Centers.G,)

# Non-Sacral Motor Centers (for Type identification).
NON_SACRAL_MOTOR_CENTERS = (Centers.ROOT, Centers.SOLAR_PLEXUS, Centers.HEART)

# Lists for Projector Categories identification.
CLASSIC_PROJECTOR_CENTERS = (Centers.SPLENIC, Centers.G)  # Non-Motor Centers below the Throat.
MENTAL_PROJECTOR_CENTERS = (Centers.THROAT, Centers.AJNA, Centers.HEAD)


# DEFINITION TYPES ---------------------------------------------------------------------------------

class DefinitionTypes(SuperEnum):
    """The 4-6 Definition Types.

    Represent how energy flows, or is interrupted by gaps in circuitry, between defined areas in a
    BodyGraph.

    A Definition is all the Channels and Centers that are defined and connected together.
    The Definition Type is related to how all the defined Channels and Centers are connected in 1+
    continuous flow.

    1. No Definition: A Reflector with no centers defined.
    2. Single Definition: All defined Channels and defined Centers are connected in 1 continuous
        flow.
    3. Split Definition: 2 separate areas of definition that are not connected to each other.
        1. Simple-Split Definition: When the 2 areas are separated by a single Gate.
        2. Wide-Split Definition: When the 2 areas are separated by multiple Gates or a Channel
            through the Throat.
    4. Triple-Split Definition: 3 separate areas of definition that are not connected to each other.
    5. Quadruple-Split Definition: 4 separate areas of definition not connected to each other.

    References: "The Definitive Book of Human Design" p426, 150-155.
    """
    NO              = "No"
    SINGLE          = "Single"
    SIMPLE_SPLIT    = "Simple-Split"
    WIDE_SPLIT      = "Wide-Split"
    TRIPLE_SPLIT    = "Triple-Split"
    QUADRUPLE_SPLIT = "Quadruple-Split"

    @property
    def is_split(self) -> bool:
        """Return whether this is an overarching Split Definition Type."""
        return self in SPLIT_DEFINITION_TYPES


# LISTS FOR DEFINITION TYPES -----------------------------------------------------------------------

# Overarching Types with their sub-values.
SPLIT_DEFINITION_TYPES = (DefinitionTypes.SIMPLE_SPLIT, DefinitionTypes.WIDE_SPLIT)


# ==================================================================================================
# GATES
# ==================================================================================================

# QUARTERS -----------------------------------------------------------------------------------------

class Quarters(SuperEnum):
    """The 4 Quarters.

    The Quarters formed when the Mandala is divided by the four Gates of the Right Angle Cross
    of the Sphinx.

    References: "The Definitive Book of Human Design" p288-309.
    """
    # TODO: `Purpose fulfilled through <theme>`
    __FIELDS__   = "num",  "name",          "realm",    "theme",           "mystical_theme"
    INITIATION   = 1,      "Initiation",    "Alcyone",  "Mind",            "The Witness Returns"  # [Ref. p290, 294-297]
    CIVILIZATION = 2,      "Civilization",  "Duhbe",    "Form",            "Womb to Room"         # [Ref. p291, 293-301]
    DUALITY      = 3,      "Duality",       "Jupiter",  "Bonding",         "Measure for Measure"  # [Ref. p292, 302-305]
    MUTATION     = 4,      "Mutation",      "Sirius",   "Transformation",  "Accepting Death"      # [Ref. p293, 306-309]

    @property
    def crosses(self) -> tuple["Crosses"]:
        """Return the list of Crosses related in this Quarter."""
        return tuple(cross for cross in Crosses if cross.quarter == self)

    @property
    def full_name(self) -> str:
        """Return `<title> – Realm of <realm>`."""
        return f"{self.title} – Realm of {self.realm}"

    @property
    def gates(self) -> tuple["Gates"]:
        """Return the list of Gates included in this Quarter."""
        return tuple(gate for gate in Gates if gate.quarter == self)

    @property
    def title(self) -> str:
        """Return `The Quarter of <name>`."""
        return f"The Quarter of {self.name}"


# GATES --------------------------------------------------------------------------------------------

class Gates(SuperEnum):
    """The 64 Gates.

    The `wheel index` is the order in the I Ching Wheel – counterclockwise starting from Gate 41
    at 02°00'00" Aquarius = 302° (from 0° Aries). See `GATE_WHEEL_START_DEGREES` in `base.py`.

    References: "The Definitive Book of Human Design" p27-30, 163-251, 294-309. Index table: p416-419.
    """
    __NUMBERED__ = True  # Adds auto-`num` (= `name`). Allows `ENUM(<num>)`.

    # Sorting: Numerically.
    __FIELDS__ = "gate_of",                        "center",              "quarter",              "title",                           "wheel_index"
    _01        = "Self-Expression",                Centers.G,             Quarters.MUTATION,      "The Creative",                    50,            # [Ref. p179, 306]
    _02        = "The Direction of the Self",      Centers.G,             Quarters.CIVILIZATION,  "The Receptive",                   18,            # [Ref. p177, 298]
    _03        = "Ordering",                       Centers.SACRAL,        Quarters.INITIATION,    "Difficulty at the Beginning",     15,            # [Ref. p175, 297]
    _04        = "Formulization",                  Centers.AJNA,          Quarters.DUALITY,       "Youthful Folly",                  35,            # [Ref. p213, 302]
    _05        = "Fixed Patterns",                 Centers.SACRAL,        Quarters.MUTATION,      "Waiting",                         55,            # [Ref. p205, 307]
    _06        = "Friction",                       Centers.SOLAR_PLEXUS,  Quarters.DUALITY,       "Conflict",                        41,            # [Ref. p237, 303]
    _07        = "The Self in Interaction",        Centers.G,             Quarters.DUALITY,       "The Army",                        34,            # [Ref. p207, 302]
    _08        = "Contribution",                   Centers.THROAT,        Quarters.CIVILIZATION,  "Holding Together",                20,            # [Ref. p179, 298]
    _09        = "Focus",                          Centers.SACRAL,        Quarters.MUTATION,      "The Taming Power of the Small",   54,            # [Ref. p203, 307]
    _10        = "The Behavior of the Self",       Centers.G,             Quarters.MUTATION,      "Treading",                        58,            # [Ref. p167, 169, 195, 308]
    _11        = "Ideas",                          Centers.AJNA,          Quarters.MUTATION,      "Peace",                           57,            # [Ref. p231, 307]
    _12        = "Caution",                        Centers.THROAT,        Quarters.CIVILIZATION,  "Standstill",                      25,            # [Ref. p191, 299]
    _13        = "The Listener",                   Centers.G,             Quarters.INITIATION,    "The Fellowship of Man",            2,            # [Ref. p223, 294]
    _14        = "Power Skills",                   Centers.SACRAL,        Quarters.MUTATION,      "Possession in Great Measure",     52,            # [Ref. p177, 306]
    _15        = "Extremes",                       Centers.G,             Quarters.CIVILIZATION,  "Modesty",                         26,            # [Ref. p205, 300]
    _16        = "Skills",                         Centers.THROAT,        Quarters.CIVILIZATION,  "Enthusiasm",                      22,            # [Ref. p211, 299]
    _17        = "Opinion",                        Centers.AJNA,          Quarters.INITIATION,    "Following",                       11,            # [Ref. p215, 296]
    _18        = "Correction",                     Centers.SPLENIC,       Quarters.DUALITY,       "Work on What Has Been Spoilt",    43,            # [Ref. p209, 304]
    _19        = "Wanting",                        Centers.ROOT,          Quarters.MUTATION,      "Approach",                         1,            # [Ref. p247, 309]
    _20        = "The Now",                        Centers.THROAT,        Quarters.CIVILIZATION,  "Contemplation",                   21,            # [Ref. p165, 169, 187, 298]
    _21        = "The Hunter/Huntress",            Centers.HEART,         Quarters.INITIATION,    "Biting Through",                  12,            # [Ref. p251, 296]
    _22        = "Openness",                       Centers.SOLAR_PLEXUS,  Quarters.INITIATION,    "Grace",                            8,            # [Ref. p191, 295]
    _23        = "Assimilation",                   Centers.THROAT,        Quarters.CIVILIZATION,  "Splitting Apart",                 19,            # [Ref. p183, 298]
    _24        = "Rationalization",                Centers.AJNA,          Quarters.INITIATION,    "The Return",                      17,            # [Ref. p181, 297]
    _25        = "The Spirit of the Self",         Centers.G,             Quarters.INITIATION,    "Innocence",                       10,            # [Ref. p197, 296]
    _26        = "The Egoist",                     Centers.HEART,         Quarters.MUTATION,      "The Taming Power of the Great",   56,            # [Ref. p245, 307]
    _27        = "Caring",                         Centers.SACRAL,        Quarters.INITIATION,    "Nourishment",                     16,            # [Ref. p239, 297]
    _28        = "The Game Player",                Centers.SPLENIC,       Quarters.DUALITY,       "Preponderance of the Great",      48,            # [Ref. p185, 305]
    _29        = "Perseverance",                   Centers.SACRAL,        Quarters.DUALITY,       "The Abysmal",                     36,            # [Ref. p221, 302]
    _30        = "Feelings",                       Centers.SOLAR_PLEXUS,  Quarters.INITIATION,    "The Cliging Fire",                 4,            # [Ref. p225, 294]
    _31        = "Influence",                      Centers.THROAT,        Quarters.CIVILIZATION,  "Influence",                       32,            # [Ref. p207, 301]
    _32        = "Continuity",                     Centers.SPLENIC,       Quarters.DUALITY,       "Duration",                        46,            # [Ref. p243, 305]
    _33        = "Privacy",                        Centers.THROAT,        Quarters.CIVILIZATION,  "Retreat",                         33,            # [Ref. p223, 301]
    _34        = "Power",                          Centers.SACRAL,        Quarters.MUTATION,      "The Power of the Great",          53,            # [Ref. p163, 165, 195, 306]
    _35        = "Change",                         Centers.THROAT,        Quarters.CIVILIZATION,  "Progress",                        23,            # [Ref. p227, 299]
    _36        = "Crisis",                         Centers.SOLAR_PLEXUS,  Quarters.INITIATION,    "The Darkening of the Light",       9,            # [Ref. p227, 295]
    _37        = "Friendship",                     Centers.SOLAR_PLEXUS,  Quarters.INITIATION,    "The Family",                       6,            # [Ref. p249, 295]
    _38        = "The Fighter",                    Centers.ROOT,          Quarters.MUTATION,      "Opposition",                      60,            # [Ref. p185, 308]
    _39        = "Provocation",                    Centers.ROOT,          Quarters.CIVILIZATION,  "Obstruction",                     28,            # [Ref. p189, 300]
    _40        = "Aloneness",                      Centers.HEART,         Quarters.DUALITY,       "Deliverance",                     38,            # [Ref. p249, 303]
    _41        = "Contraction",                    Centers.ROOT,          Quarters.MUTATION,      "Decrease",                         0,            # [Ref. p225, 309]
    _42        = "Growth",                         Centers.SACRAL,        Quarters.INITIATION,    "Increase",                        14,            # [Ref. p219, 297]
    _43        = "Insight",                        Centers.AJNA,          Quarters.MUTATION,      "Breakthrough",                    51,            # [Ref. p183, 306]
    _44        = "Alertness",                      Centers.SPLENIC,       Quarters.DUALITY,       "Coming to Meet",                  49,            # [Ref. p245, 305]
    _45        = "Gatherer",                       Centers.THROAT,        Quarters.CIVILIZATION,  "Gathering Together",              24,            # [Ref. p251, 299]
    _46        = "The Determination of the Self",  Centers.G,             Quarters.DUALITY,       "Pushing Upward",                  42,            # [Ref. p221, 304]
    _47        = "Realization",                    Centers.AJNA,          Quarters.DUALITY,       "Oppression",                      40,            # [Ref. p229, 303]
    _48        = "Depth",                          Centers.SPLENIC,       Quarters.DUALITY,       "The Well",                        44,            # [Ref. p211, 304]
    _49        = "Principles",                     Centers.SOLAR_PLEXUS,  Quarters.INITIATION,    "Revolution",                       3,            # [Ref. p247, 294]
    _50        = "Values",                         Centers.SPLENIC,       Quarters.DUALITY,       "The Cauldron",                    47,            # [Ref. p239, 305]
    _51        = "Shock",                          Centers.HEART,         Quarters.INITIATION,    "The Arousing",                    13,            # [Ref. p197, 296]
    _52        = "Stillness",                      Centers.ROOT,          Quarters.CIVILIZATION,  "Keeping Still (Mountain)",        27,            # [Ref. p203, 300]
    _53        = "Beginnings",                     Centers.ROOT,          Quarters.CIVILIZATION,  "Development",                     29,            # [Ref. p219, 300]
    _54        = "Drive",                          Centers.ROOT,          Quarters.MUTATION,      "The Marrying Maiden",             61,            # [Ref. p243, 308]
    _55        = "Spirit",                         Centers.SOLAR_PLEXUS,  Quarters.INITIATION,    "Abundance",                        5,            # [Ref. p189, 294]
    _56        = "Stimulation",                    Centers.THROAT,        Quarters.CIVILIZATION,  "The Wanderer",                    31,            # [Ref. p231, 301]
    _57        = "Intuitive Insight",              Centers.SPLENIC,       Quarters.DUALITY,       "The Gentle",                      45,            # [Ref. p163, 167, 187, 304]
    _58        = "Vitality",                       Centers.ROOT,          Quarters.MUTATION,      "The Joyous",                      59,            # [Ref. p209, 308]
    _59        = "Sexuality",                      Centers.SACRAL,        Quarters.DUALITY,       "Dispersion",                      37,            # [Ref. p237, 302]
    _60        = "Acceptance",                     Centers.ROOT,          Quarters.MUTATION,      "Limitation",                      63,            # [Ref. p175, 309]
    _61        = "Mystery",                        Centers.HEAD,          Quarters.MUTATION,      "Inner Truth",                     62,            # [Ref. p181, 309]
    _62        = "Details",                        Centers.THROAT,        Quarters.CIVILIZATION,  "The Preponderance of the Small",  30,            # [Ref. p215, 301]
    _63        = "Doubt",                          Centers.HEAD,          Quarters.INITIATION,    "After Completion",                 7,            # [Ref. p213, 295]
    _64        = "Confusion",                      Centers.HEAD,          Quarters.DUALITY,       "Before Completion",               39,            # [Ref. p229, 303]

    @property
    def channels(self) -> tuple["Channels"]:
        """Return the list of Channels including this Gate.

        The majority of Gates are in a single Channel, except four Gates (10, 20, 34, 57) that are
        in three Channels.
        """
        return tuple(channel for channel in Channels if self in channel.gates)

    @property
    def crosses(self) -> tuple["Crosses"]:
        """Return the list of Crosses including this Gate."""
        return tuple(cross for cross in Crosses if self in cross.gates)

    @property
    def start_angle(self) -> float:
        """Return the start angle of the Gate in the I Ching Wheel."""
        return (GATE_WHEEL_START_DEGREES + (self.wheel_index * GATE_SEGMENT)) % 360

    @property
    def end_angle(self) -> float:
        """Return the end angle of the Gate in the I Ching Wheel."""
        return (self.start_angle + GATE_SEGMENT) % 360

    @classmethod
    def get_by_wheel_index(cls, index: int) -> "Gates":
        """Return the Gate at the given index in the I Ching Wheel."""
        if index < 0 or index > 63:
            raise ValueError(f"Invalid wheel index ({index}). It must be between 0 and 63.")

        for gate in cls:
            if gate.wheel_index == index:
                return gate

        raise ValueError(f"No Gate found at wheel index {index}.")

    @classmethod
    def get_wheel_order(cls) -> tuple["Gates"]:
        """Return the list of Gates sorted by their index in the I Ching Wheel.

        Wheel order (counterclockwise):
          41, 19, 13, 49, 30, 55, 37, 63, 22, 36, 25, 17, 21, 51, 42, 3, 27, 24, 2, 23, 8, 20, 16,
          35, 45, 12, 15, 52, 39, 53, 62, 56, 31, 33, 7, 4, 29, 59, 40, 64, 47, 6, 46, 18, 48, 57,
          32, 50, 28, 44, 1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 38, 54, 61, 60
        """
        return tuple(sorted(cls, key=lambda gate: gate.wheel_index))


# ==================================================================================================
# CHANNELS
# ==================================================================================================

# CIRCUITS -----------------------------------------------------------------------------------------

class Circuits(SuperEnum):
    """The 6 Circuits.

    Channels and their Gates are bundled together forming six basic Circuits.

    Gates per Circuit:
    - Centering: 10, 25, 34, 51.
    - Defense: 6, 27, 50, 59.
    - Ego: 19, 21, 26, 32, 37, 40, 44, 45, 49, 54.
    - Integration: 10, 10, 20, 20, 34, 34, 57, 57.
    - Knowing: 1, 2, 3, 8, 12, 14, 20, 22, 23, 24, 28, 38, 39, 43, 55, 57, 60, 61.
    - Sensing: 11, 13, 29, 30, 33, 35, 36, 41, 42, 46, 47, 53, 56, 64.
    - Understanding: 4, 5, 7, 9, 15, 16, 17, 18, 31, 48, 52, 58, 62, 63.

    References: "The Definitive Book of Human Design" p158-251.
    """
    CENTERING     = "Centering"      # [Ref. p192-197]
    DEFENSE       = "Defense"        # [Ref. p234-239]
    EGO           = "Ego"            # [Ref. p240-251]
    INTEGRATION   = "Integration"    # [Ref. p160-169]
    KNOWING       = "Knowing"        # [Ref. p172-191]
    SENSING       = "Sensing"        # [Ref. p216-231]
    UNDERSTANDING = "Understanding"  # [Ref. p200-215]

    @property
    def channels(self) -> tuple["Channels"]:
        """Return the list of Channels included in this Circuit."""
        return tuple(channel for channel in Channels if channel.circuit == self)

    @property
    def gates(self) -> tuple["Gates"]:
        """Return the list of Gates included in the Channels included in this Circuit."""
        return tuple(sorted([gate for channel in self.channels for gate in channel.gates]))


# CIRCUIT GROUPS -----------------------------------------------------------------------------------

class CircuitGroups(SuperEnum):
    """The 3 Circuit Groups.

    See also `INTEGRATION_CHANNEL` below.

    References: "The Definitive Book of Human Design" p158-251.
    """
    COLLECTIVE = "Collective"  # [Ref. p198-231]
    INDIVIDUAL = "Individual"  # [Ref. p170-197]
    TRIBAL     = "Tribal"      # [Ref. p232-251]

    @property
    def channels(self) -> tuple["Channels"]:
        """Return the list of Channels included in this Circuit Group."""
        return tuple(channel for channel in Channels if channel.circuit_group == self)


# CHANNEL TYPES ------------------------------------------------------------------------------------

class ChannelTypes(SuperEnum):
    """The 4 Channel Types.

    TODO: References: "The Definitive Book of Human Design" p.
    """
    GENERATED             = "Generated"
    MANIFESTING_GENERATED = "Manifesting Generated"
    MANIFESTED            = "Manifested"
    PROJECTED             = "Projected"

    @property
    def channels(self) -> tuple["Channels"]:
        """Return the list of Channels of this Channel Type."""
        return tuple(channel for channel in Channels if channel.channel_type == self)


# CHANNELS -----------------------------------------------------------------------------------------

class Channels(SuperEnum):
    """The 36 Channels.

    A Channel is the fixed structural pathway connecting two specific Gates between two Centers.
    The majority of Gates are in a single Channel, except four Gates (10, 20, 34, 57) that are
    in three Channels.

    References: "The Definitive Book of Human Design" p30, 34-35. Glossary: p424. Index table: p416-419.
    """
    # Sorting: Numerically. Gates = numerically, Centers = Gates order.
    __FIELDS__ = "title",           "gates",                 "channel_type",                      "circuit",               "is_creative",  "circuit_group",           "centers"
    _01_08     = "Inspiration",     (Gates._01, Gates._08),  ChannelTypes.PROJECTED,              Circuits.KNOWING,        True,           CircuitGroups.INDIVIDUAL,  (Centers.G,            Centers.THROAT)        # [Ref. p178]
    _02_14     = "Beat",            (Gates._02, Gates._14),  ChannelTypes.GENERATED,              Circuits.KNOWING,        False,          CircuitGroups.INDIVIDUAL,  (Centers.G,            Centers.SACRAL)        # [Ref. p176]
    _03_60     = "Mutation",        (Gates._03, Gates._60),  ChannelTypes.GENERATED,              Circuits.KNOWING,        False,          CircuitGroups.INDIVIDUAL,  (Centers.SACRAL,       Centers.ROOT)          # [Ref. p174]
    _04_63     = "Logic",           (Gates._04, Gates._63),  ChannelTypes.PROJECTED,              Circuits.UNDERSTANDING,  False,          CircuitGroups.COLLECTIVE,  (Centers.AJNA,         Centers.HEAD)          # [Ref. p212]
    _05_15     = "Rhythm",          (Gates._05, Gates._15),  ChannelTypes.GENERATED,              Circuits.UNDERSTANDING,  False,          CircuitGroups.COLLECTIVE,  (Centers.SACRAL,       Centers.G)             # [Ref. p204]
    _06_59     = "Intimacy",        (Gates._06, Gates._59),  ChannelTypes.GENERATED,              Circuits.DEFENSE,        True,           CircuitGroups.TRIBAL,      (Centers.SOLAR_PLEXUS, Centers.SACRAL)        # [Ref. p236]
    _07_31     = "The Alpha",       (Gates._07, Gates._31),  ChannelTypes.PROJECTED,              Circuits.UNDERSTANDING,  False,          CircuitGroups.COLLECTIVE,  (Centers.G,            Centers.THROAT)        # [Ref. p206]
    _09_52     = "Concentration",   (Gates._09, Gates._52),  ChannelTypes.GENERATED,              Circuits.UNDERSTANDING,  False,          CircuitGroups.COLLECTIVE,  (Centers.SACRAL,       Centers.ROOT)          # [Ref. p202]
    _10_20     = "Awakening",       (Gates._10, Gates._20),  ChannelTypes.PROJECTED,              Circuits.INTEGRATION,    False,          CircuitGroups.INDIVIDUAL,  (Centers.G,            Centers.THROAT)        # [Ref. p168]
    _10_34     = "Exploration",     (Gates._10, Gates._34),  ChannelTypes.GENERATED,              Circuits.CENTERING,      True,           CircuitGroups.INDIVIDUAL,  (Centers.G,            Centers.SACRAL)        # [Ref. p194]
    _10_57     = "Perfected Form",  (Gates._10, Gates._57),  ChannelTypes.PROJECTED,              Circuits.INTEGRATION,    True,           CircuitGroups.INDIVIDUAL,  (Centers.G,            Centers.SPLENIC)       # [Ref. p166]
    _11_56     = "Curiosity",       (Gates._11, Gates._56),  ChannelTypes.PROJECTED,              Circuits.SENSING,        False,          CircuitGroups.COLLECTIVE,  (Centers.AJNA,         Centers.THROAT)        # [Ref. p230]
    _12_22     = "Openness",        (Gates._12, Gates._22),  ChannelTypes.MANIFESTED,             Circuits.KNOWING,        False,          CircuitGroups.INDIVIDUAL,  (Centers.THROAT,       Centers.SOLAR_PLEXUS)  # [Ref. p190]
    _13_33     = "The Prodigal",    (Gates._13, Gates._33),  ChannelTypes.PROJECTED,              Circuits.SENSING,        False,          CircuitGroups.COLLECTIVE,  (Centers.G,            Centers.THROAT)        # [Ref. p222]
    _16_48     = "The Wavelength",  (Gates._16, Gates._48),  ChannelTypes.PROJECTED,              Circuits.UNDERSTANDING,  True,           CircuitGroups.COLLECTIVE,  (Centers.THROAT,       Centers.SPLENIC)       # [Ref. p210]
    _17_62     = "Acceptance",      (Gates._17, Gates._62),  ChannelTypes.PROJECTED,              Circuits.UNDERSTANDING,  False,          CircuitGroups.COLLECTIVE,  (Centers.AJNA,         Centers.THROAT)        # [Ref. p214]
    _18_58     = "Judgement",       (Gates._18, Gates._58),  ChannelTypes.PROJECTED,              Circuits.UNDERSTANDING,  False,          CircuitGroups.COLLECTIVE,  (Centers.SPLENIC,      Centers.ROOT)          # [Ref. p208]
    _19_49     = "Synthesis",       (Gates._19, Gates._49),  ChannelTypes.PROJECTED,              Circuits.EGO,            False,          CircuitGroups.TRIBAL,      (Centers.ROOT,         Centers.SOLAR_PLEXUS)  # [Ref. p246]
    _20_34     = "Charisma",        (Gates._20, Gates._34),  ChannelTypes.MANIFESTING_GENERATED,  Circuits.INTEGRATION,    False,          CircuitGroups.INDIVIDUAL,  (Centers.THROAT,       Centers.SACRAL)        # [Ref. p164]
    _20_57     = "The Brainwave",   (Gates._20, Gates._57),  ChannelTypes.PROJECTED,              Circuits.KNOWING,        False,          CircuitGroups.INDIVIDUAL,  (Centers.THROAT,       Centers.SPLENIC)       # [Ref. p186]
    _21_45     = "The Money Line",  (Gates._21, Gates._45),  ChannelTypes.MANIFESTED,             Circuits.EGO,            False,          CircuitGroups.TRIBAL,      (Centers.HEART,        Centers.THROAT)        # [Ref. p250]
    _23_43     = "Structuring",     (Gates._23, Gates._43),  ChannelTypes.PROJECTED,              Circuits.KNOWING,        False,          CircuitGroups.INDIVIDUAL,  (Centers.THROAT,       Centers.AJNA)          # [Ref. p182]
    _24_61     = "Awareness",       (Gates._24, Gates._61),  ChannelTypes.PROJECTED,              Circuits.KNOWING,        False,          CircuitGroups.INDIVIDUAL,  (Centers.AJNA,         Centers.HEAD)          # [Ref. p180]
    _25_51     = "Initiation",      (Gates._25, Gates._51),  ChannelTypes.PROJECTED,              Circuits.CENTERING,      False,          CircuitGroups.INDIVIDUAL,  (Centers.G,            Centers.HEART)         # [Ref. p196]
    _26_44     = "Surrender",       (Gates._26, Gates._44),  ChannelTypes.PROJECTED,              Circuits.EGO,            True,           CircuitGroups.TRIBAL,      (Centers.HEART,        Centers.SPLENIC)       # [Ref. p244]
    _27_50     = "Preservation",    (Gates._27, Gates._50),  ChannelTypes.GENERATED,              Circuits.DEFENSE,        False,          CircuitGroups.TRIBAL,      (Centers.SACRAL,       Centers.SPLENIC)       # [Ref. p238]
    _28_38     = "Struggle",        (Gates._28, Gates._38),  ChannelTypes.PROJECTED,              Circuits.KNOWING,        False,          CircuitGroups.INDIVIDUAL,  (Centers.SPLENIC,      Centers.ROOT)          # [Ref. p184]
    _29_46     = "Discovery",       (Gates._29, Gates._46),  ChannelTypes.GENERATED,              Circuits.SENSING,        False,          CircuitGroups.COLLECTIVE,  (Centers.SACRAL,       Centers.G)             # [Ref. p220]
    _30_41     = "Recognition",     (Gates._30, Gates._41),  ChannelTypes.PROJECTED,              Circuits.SENSING,        False,          CircuitGroups.COLLECTIVE,  (Centers.SOLAR_PLEXUS, Centers.ROOT)          # [Ref. p224]
    _32_54     = "Transformation",  (Gates._32, Gates._54),  ChannelTypes.PROJECTED,              Circuits.EGO,            False,          CircuitGroups.TRIBAL,      (Centers.SPLENIC,      Centers.ROOT)          # [Ref. p242]
    _34_57     = "Power",           (Gates._34, Gates._57),  ChannelTypes.GENERATED,              Circuits.INTEGRATION,    False,          CircuitGroups.INDIVIDUAL,  (Centers.SACRAL,       Centers.SPLENIC)       # [Ref. p162]
    _35_36     = "Transitoriness",  (Gates._35, Gates._36),  ChannelTypes.PROJECTED,              Circuits.SENSING,        True,           CircuitGroups.COLLECTIVE,  (Centers.THROAT,       Centers.SOLAR_PLEXUS)  # [Ref. p226]
    _37_40     = "Community",       (Gates._37, Gates._40),  ChannelTypes.PROJECTED,              Circuits.EGO,            False,          CircuitGroups.TRIBAL,      (Centers.SOLAR_PLEXUS, Centers.HEART)         # [Ref. p248]
    _39_55     = "Emoting",         (Gates._39, Gates._55),  ChannelTypes.PROJECTED,              Circuits.KNOWING,        False,          CircuitGroups.INDIVIDUAL,  (Centers.ROOT,         Centers.SOLAR_PLEXUS)  # [Ref. p188]
    _42_53     = "Maturation",      (Gates._42, Gates._53),  ChannelTypes.GENERATED,              Circuits.SENSING,        False,          CircuitGroups.COLLECTIVE,  (Centers.SACRAL,       Centers.ROOT)          # [Ref. p218]
    _47_64     = "Abstraction",     (Gates._47, Gates._64),  ChannelTypes.PROJECTED,              Circuits.SENSING,        False,          CircuitGroups.COLLECTIVE,  (Centers.AJNA,         Centers.HEAD)          # [Ref. p228]

    @property
    def name(self) -> str:
        """Return the name as `xx-xx`."""
        return "-".join([f"{num:02d}" for num in self.num])

    # TODO: Better?
    # @property
    # def full_name(self) -> str:
    #     """Return ."""
    #     creative = (" (creative)" if self.is_creative
    #                 else "")
    #     return f"{self.name}{creative}"

    @property
    def num(self) -> tuple[int]:
        """Return the number of the Gates composing this Channel."""
        return tuple(gate.num for gate in self.gates)

    def harmonic_center(self, center: Centers) -> "Centers":
        """Return the Center at the other end of the Channel, based on the given Center."""
        if center not in self.centers:
            valid = "-".join([str(c) for c in self.centers])
            raise ValueError(f"Center {center} is not connected to this Channel {self}"
                             f" (valid: {valid}).")

        return (self.centers[0] if self.centers[1] == center
                else self.centers[1])

    def harmonic_gate(self, gate: Gates) -> "Gates":
        """Return the Gate at the other end of the Channel, based on the given Gate."""
        if gate not in self.gates:
            raise ValueError(f"Gate {gate} is not connected to this Channel {self}.")

        return (self.gates[0] if self.gates[1] == gate
                else self.gates[1])

    @classmethod
    def connecting_centers(cls, center1: Centers, center2: Centers) -> tuple["Channels"]:
        """Return the list of Channels connecting the two given Centers."""
        target = {center1, center2}  # For matching unordered pairs.
        return tuple(channel for channel in cls if set(channel.centers) == target)


# LISTS FOR CHANNELS -------------------------------------------------------------------------------

# List of Channels forming the Integration Channel.
# It stands on its own alongside the 3 main Circuit Groups in the infrastructure of the BodyGraph.
# References: "The Definitive Book of Human Design" p160-169.
INTEGRATION_CHANNEL = (Channels._10_20, Channels._10_57, Channels._20_34, Channels._34_57)


# ==================================================================================================
# TYPES
# ==================================================================================================

# STRATEGIES ---------------------------------------------------------------------------------------

class Strategies(SuperEnum):
    """The 4 Strategies.

    There's a 1-1 relationship with `Types`. `Manifesting Generator` is a variation of pure
    `Generator`, so they share the same `Strategy`.

    References: "The Definitive Book of Human Design" p115, 117, 125, 133, 140. Glossary: p436.
    """
    INFORM      = "To Inform"                # Manifestor [Ref. p430, 117]
    RESPOND     = "To Respond"               # Generator  [Ref. p435, 125]
    INVITATION  = "Wait for the Invitation"  # Projector  [Ref. p430, 133]
    LUNAR_CYCLE = "Wait a Lunar Cycle"       # Reflector  [Ref. p431, 140]

    @property
    def types(self) -> tuple["Types"]:
        """Return the list of associated `Type`."""
        # Note: `_type_map` is built after the definition of `Types`.
        return self._type_map[self]


# SIGNATURES ---------------------------------------------------------------------------------------

class Signatures(SuperEnum):  # TODO
    """The 4 Signatures.

    There's a 1-1 relationship with `Types`. `Manifesting Generator` is a variation of pure
    `Generator`, so they share the same `Signature`.

    References: "The Definitive Book of Human Design" p115, 122, 128, 136, 142. Glossary: p435.
    """
    PEACE        = "Peace"         # Manifestor [Ref. p122]
    SATISFACTION = "Satisfaction"  # Generator  [Ref. p128]
    SUCCESS      = "Success"       # Projector  [Ref. p136]
    SURPRISE     = "Surprise"      # Reflector  [Ref. p142]

    @property
    def types(self) -> tuple["Types"]:
        """Return the list of associated `Type`."""
        # Note: `_type_map` is built after the definition of `Types`.
        return Signatures._type_map[self]


# NOT-SELF THEMES ----------------------------------------------------------------------------------

class NotSelfThemes(SuperEnum):  # TODO
    """The 4 Not-Self Themes.

    There's a 1-1 relationship with `Types`. `Manifesting Generator` is a variation of pure
    `Generator`, so they share the same `Not-Self Theme`.

    References: "The Definitive Book of Human Design" p116, 123, 129, 137. Glossary: p432.
    """
    ANGER          = "Anger"           # Manifestor [Ref. p422, 116, 121]
    FRUSTRATION    = "Frustration"     # Generator  [Ref. p428, 123, 127]
    BITTERNESS     = "Bitterness"      # Projector  [Ref. p423, 129, 135]
    DISAPPOINTMENT = "Disappointment"  # Reflector  [Ref. p427, 137, 141]

    @property
    def types(self) -> tuple["Types"]:
        """Return the list of associated `Type`."""
        # Note: `_type_map` is built after the definition of `Types`.
        return NotSelfThemes._type_map[self]


# TYPES --------------------------------------------------------------------------------------------

class Types(SuperEnum):
    """The 4+1 Types, and subtypes.

    `Manifesting Generator` is a variation of pure `Generator`.

    References: "The Definitive Book of Human Design" p114-142. Glossary: p437.
    """
    # Sorting: According to reference book.
    __FIELDS__            = "name",                   "parent",     "strategy",              "signature",              "not_self_theme"
    MANIFESTOR            = "Manifestor",             None,         Strategies.INFORM,       Signatures.PEACE,         NotSelfThemes.ANGER           # [Ref. p432, 116-122]
    GENERATOR             = "Generator",              None,         Strategies.RESPOND,      Signatures.SATISFACTION,  NotSelfThemes.FRUSTRATION     # [Ref. p429, 123-128]
    PURE_GENERATOR        = "Pure Generator",         "GENERATOR",  Strategies.RESPOND,      Signatures.SATISFACTION,  NotSelfThemes.FRUSTRATION     # [Ref. p429, 123-128]
    MANIFESTING_GENERATOR = "Manifesting Generator",  "GENERATOR",  Strategies.RESPOND,      Signatures.SATISFACTION,  NotSelfThemes.FRUSTRATION     # [Ref. p432, see Generator]
    PROJECTOR             = "Projector",              None,         Strategies.INVITATION,   Signatures.SUCCESS,       NotSelfThemes.BITTERNESS      # [Ref. p131]
    MENTAL_PROJECTOR      = "Mental Projector",       "PROJECTOR",  Strategies.INVITATION,   Signatures.SUCCESS,       NotSelfThemes.BITTERNESS      # [Ref. p131]
    ENERGY_PROJECTOR      = "Energy Projector",       "PROJECTOR",  Strategies.INVITATION,   Signatures.SUCCESS,       NotSelfThemes.BITTERNESS      # [Ref. p131]
    CLASSIC_PROJECTOR     = "Classic Projector",      "PROJECTOR",  Strategies.INVITATION,   Signatures.SUCCESS,       NotSelfThemes.BITTERNESS      # [Ref. p131]
    REFLECTOR             = "Reflector",              None,         Strategies.LUNAR_CYCLE,  Signatures.SURPRISE,      NotSelfThemes.DISAPPOINTMENT  # [Ref. p435, 137-142]

    @cached_property
    def generators(self) -> tuple["Types"]:
        """Return the overarching Generator Type."""
        return tuple(t for t in self.__class__ if t.parent == "GENERATOR")

    @cached_property
    def projectors(self) -> tuple["Types"]:
        """Return the overarching Projector Type."""
        return tuple(t for t in self.__class__ if t.parent == "PROJECTOR")

    @property
    def is_generator(self) -> bool:
        """Return whether this is an overarching Generator Type."""
        return self in self.generators

    @property
    def is_projector(self) -> bool:
        """Return whether this is an overarching Projector Type."""
        return self in self.projectors

    def is_type(self, type_: "Types") -> bool:
        """Return whether this Type is of the given Type."""
        # Testing an overarching type.
        if self.parent is None:
            return self is type_
        # Testing a precise type.
        return self is type_ or self.parent == type_._key

    @classmethod
    def all_items(cls) -> tuple["SuperEnum"]:
        """Return a list of all members."""
        return super().items()

    @classmethod
    def items(cls) -> tuple["SuperEnum"]:
        """Return a list of all overarching members."""
        return tuple(i for i in cls if i.parent is None)


# LISTS FOR TYPES ----------------------------------------------------------------------------------

# Overarching Types with their sub-values.
GENERATOR_TYPES = (Types.MANIFESTING_GENERATOR,)
PROJECTOR_TYPES = (Types.MENTAL_PROJECTOR, Types.ENERGY_PROJECTOR, Types.CLASSIC_PROJECTOR)

# Grouping of Types by energy/non-energy. [Ref. p428]
ENERGY_TYPES = (Types.MANIFESTOR, Types.PURE_GENERATOR, Types.MANIFESTING_GENERATOR)
NON_ENERGY_TYPES = (Types.MENTAL_PROJECTOR, Types.ENERGY_PROJECTOR, Types.CLASSIC_PROJECTOR, Types.REFLECTOR)

# TRICK: Mapping to retrieve the Type associated with Strategy, Signature, and Not-Self Theme.
Strategies._type_map    = {strategy:       tuple(type for type in Types if type.strategy == strategy)             for strategy in Strategies}
Signatures._type_map    = {signature:      tuple(type for type in Types if type.signature == signature)           for signature in Signatures}
NotSelfThemes._type_map = {not_self_theme: tuple(type for type in Types if type.not_self_theme == not_self_theme) for not_self_theme in NotSelfThemes}


# ==================================================================================================
# CROSSES
# ==================================================================================================

# DESTINIES ----------------------------------------------------------------------------------------

class Destinies(SuperEnum):
    """The 3 Destinies.

    Destinies are the qualitative nature of how a Geometry fulfills its purpose – the "flavor" of
    interaction with the world and others.

    Remark: There's almost a 1-1 relationship with Geometries – except for Profile 4/6 (Right Angle
        but Transpersonal).

    TODO: References: "The Definitive Book of Human Design" p.
    """
    TRANSPERSONAL = "Transpersonal/Karmic"
    FIXED_FATE    = "Fixed Fate"
    PERSONAL      = "Personal"

    @property
    def profiles(self) -> tuple["Profiles"]:
        """Return the list of Profiles related to this Destiny."""
        return tuple(profile for profile in Profiles if profile.destiny == self)


# GEOMETRIES ---------------------------------------------------------------------------------------

class Geometries(SuperEnum):
    """The 3 Geometries.

    Geometries are the three mechanical frameworks that determine how we interact with and impact
    others to fulfill our life purpose. Created by the Sun/Earth progression through the Mandala,
    they set the trajectory or direction of movement through life.

    Remark: There's almost a 1-1 relationship with Destinies – except for Profile 4/6 (Right Angle
        but Transpersonal).

    References: "The Definitive Book of Human Design" p429, 260-261.
    """
    LEFT_ANGLE    = "Left Angle"
    JUXTAPOSITION = "Juxtaposition"
    RIGHT_ANGLE   = "Right Angle"

    @property
    def crosses(self) -> tuple["Crosses"]:
        """Return the list of Crosses of this Geometry."""
        return tuple(cross for cross in Crosses if cross.geometry == self)

    @property
    def profiles(self) -> tuple["Profiles"]:
        """Return the list of Profiles related in this Geometry."""
        return tuple(profile for profile in Profiles if profile.geometry == self)

    @property
    def letter(self) -> str:
        return self.name[0].upper()


# CROSSES ------------------------------------------------------------------------------------------

class Crosses(SuperEnum):
    """The 192 Incarnation Crosses.

    The Quarter of a Cross is determined by the Personality Sun Gate.

    Fields:
    - `title`
    - `ps`: Personality Sun.
    - `pe`: Personality Earth.
    - `ds`: Design Sun.
    - `de`: Design Earth.
    - `geometry`

    References: "The Definitive Book of Human Design" p288-309.
    """
    # Sorting: Numerically.
    __FIELDS__     = "title",                   "ps",       "pe",       "ds",       "de",       "geometry"
    _01_02_04_49_L = "Defiance 2",              Gates._01,  Gates._02,  Gates._04,  Gates._49,  Geometries.LEFT_ANGLE
    _01_02_04_49_J = "Self Expression",         Gates._01,  Gates._02,  Gates._04,  Gates._49,  Geometries.JUXTAPOSITION
    _01_02_07_13_R = "The Sphinx 4",            Gates._01,  Gates._02,  Gates._07,  Gates._13,  Geometries.RIGHT_ANGLE
    _02_01_13_07_R = "The Sphinx 2",            Gates._02,  Gates._01,  Gates._13,  Gates._07,  Geometries.RIGHT_ANGLE
    _02_01_49_04_L = "Defiance 1",              Gates._02,  Gates._01,  Gates._49,  Gates._04,  Geometries.LEFT_ANGLE
    _02_01_49_04_J = "The Driver",              Gates._02,  Gates._01,  Gates._49,  Gates._04,  Geometries.JUXTAPOSITION
    _03_50_41_31_L = "Wishes 1",                Gates._03,  Gates._50,  Gates._41,  Gates._31,  Geometries.LEFT_ANGLE
    _03_50_41_31_J = "Mutation",                Gates._03,  Gates._50,  Gates._41,  Gates._31,  Geometries.JUXTAPOSITION
    _03_50_60_56_R = "Laws 1",                  Gates._03,  Gates._50,  Gates._60,  Gates._56,  Geometries.RIGHT_ANGLE
    _04_49_08_14_L = "Revolution 2",            Gates._04,  Gates._49,  Gates._08,  Gates._14,  Geometries.LEFT_ANGLE
    _04_49_08_14_J = "Formulization",           Gates._04,  Gates._49,  Gates._08,  Gates._14,  Geometries.JUXTAPOSITION
    _04_49_23_43_R = "Explanation 3",           Gates._04,  Gates._49,  Gates._23,  Gates._43,  Geometries.RIGHT_ANGLE
    _05_35_47_22_L = "Separation 2",            Gates._05,  Gates._35,  Gates._47,  Gates._22,  Geometries.LEFT_ANGLE
    _05_35_47_22_J = "Habits",                  Gates._05,  Gates._35,  Gates._47,  Gates._22,  Geometries.JUXTAPOSITION
    _05_35_64_63_R = "Consciousness 4",         Gates._05,  Gates._35,  Gates._64,  Gates._63,  Geometries.RIGHT_ANGLE
    _06_36_12_11_R = "Eden 3",                  Gates._06,  Gates._36,  Gates._12,  Gates._11,  Geometries.RIGHT_ANGLE
    _06_36_15_10_L = "The Plane 2",             Gates._06,  Gates._36,  Gates._15,  Gates._10,  Geometries.LEFT_ANGLE
    _06_36_15_10_J = "Conflict",                Gates._06,  Gates._36,  Gates._15,  Gates._10,  Geometries.JUXTAPOSITION
    _07_13_02_01_R = "The Sphinx 3",            Gates._07,  Gates._13,  Gates._02,  Gates._01,  Geometries.RIGHT_ANGLE
    _07_13_23_43_L = "Masks 2",                 Gates._07,  Gates._13,  Gates._23,  Gates._43,  Geometries.LEFT_ANGLE
    _07_13_23_43_J = "Interaction",             Gates._07,  Gates._13,  Gates._23,  Gates._43,  Geometries.JUXTAPOSITION
    _08_14_30_29_R = "Contagion 2",             Gates._08,  Gates._14,  Gates._30,  Gates._29,  Geometries.RIGHT_ANGLE
    _08_14_55_59_L = "Uncertainty 1",           Gates._08,  Gates._14,  Gates._55,  Gates._59,  Geometries.LEFT_ANGLE
    _08_14_55_59_J = "Contribution",            Gates._08,  Gates._14,  Gates._55,  Gates._59,  Geometries.JUXTAPOSITION
    _09_16_40_37_R = "Planning 4",              Gates._09,  Gates._16,  Gates._40,  Gates._37,  Geometries.RIGHT_ANGLE
    _09_16_64_63_L = "Identification 2",        Gates._09,  Gates._16,  Gates._64,  Gates._63,  Geometries.LEFT_ANGLE
    _09_16_64_63_J = "Focus",                   Gates._09,  Gates._16,  Gates._64,  Gates._63,  Geometries.JUXTAPOSITION
    _10_15_18_17_L = "Prevention 2",            Gates._10,  Gates._15,  Gates._18,  Gates._17,  Geometries.LEFT_ANGLE
    _10_15_18_17_J = "Behavior",                Gates._10,  Gates._15,  Gates._18,  Gates._17,  Geometries.JUXTAPOSITION
    _10_15_46_25_R = "The Vessel of Love 4",    Gates._10,  Gates._15,  Gates._46,  Gates._25,  Geometries.RIGHT_ANGLE
    _11_12_06_36_R = "Eden 4",                  Gates._11,  Gates._12,  Gates._06,  Gates._36,  Geometries.RIGHT_ANGLE
    _11_12_46_25_L = "Education 2",             Gates._11,  Gates._12,  Gates._46,  Gates._25,  Geometries.LEFT_ANGLE
    _11_12_46_25_J = "Ideas",                   Gates._11,  Gates._12,  Gates._46,  Gates._25,  Geometries.JUXTAPOSITION
    _12_11_25_46_L = "Education 1",             Gates._12,  Gates._11,  Gates._25,  Gates._46,  Geometries.LEFT_ANGLE
    _12_11_25_46_J = "Articulation",            Gates._12,  Gates._11,  Gates._25,  Gates._46,  Geometries.JUXTAPOSITION
    _12_11_36_06_R = "Eden 2",                  Gates._12,  Gates._11,  Gates._36,  Gates._06,  Geometries.RIGHT_ANGLE
    _13_07_01_02_R = "The Sphinx 1",            Gates._13,  Gates._07,  Gates._01,  Gates._02,  Geometries.RIGHT_ANGLE
    _13_07_43_23_L = "Masks 1",                 Gates._13,  Gates._07,  Gates._43,  Gates._23,  Geometries.LEFT_ANGLE
    _13_07_43_23_J = "Listening",               Gates._13,  Gates._07,  Gates._43,  Gates._23,  Geometries.JUXTAPOSITION
    _14_08_29_30_R = "Contagion 4",             Gates._14,  Gates._08,  Gates._29,  Gates._30,  Geometries.RIGHT_ANGLE
    _14_08_59_55_L = "Uncertainty 2",           Gates._14,  Gates._08,  Gates._59,  Gates._55,  Geometries.LEFT_ANGLE
    _14_08_59_55_J = "Empowering",              Gates._14,  Gates._08,  Gates._59,  Gates._55,  Geometries.JUXTAPOSITION
    _15_10_17_18_L = "Prevention 1",            Gates._15,  Gates._10,  Gates._17,  Gates._18,  Geometries.LEFT_ANGLE
    _15_10_17_18_J = "Extremes",                Gates._15,  Gates._10,  Gates._17,  Gates._18,  Geometries.JUXTAPOSITION
    _15_10_25_46_R = "The Vessel of Love 2",    Gates._15,  Gates._10,  Gates._25,  Gates._46,  Geometries.RIGHT_ANGLE
    _16_09_37_40_R = "Planning 2",              Gates._16,  Gates._09,  Gates._37,  Gates._40,  Geometries.RIGHT_ANGLE
    _16_09_63_64_L = "Identification 1",        Gates._16,  Gates._09,  Gates._63,  Gates._64,  Geometries.LEFT_ANGLE
    _16_09_63_64_J = "Experimentation",         Gates._16,  Gates._09,  Gates._63,  Gates._64,  Geometries.JUXTAPOSITION
    _17_18_38_39_L = "Upheaval 1",              Gates._17,  Gates._18,  Gates._38,  Gates._39,  Geometries.LEFT_ANGLE
    _17_18_38_39_J = "Opinions",                Gates._17,  Gates._18,  Gates._38,  Gates._39,  Geometries.JUXTAPOSITION
    _17_18_58_52_R = "Service 1",               Gates._17,  Gates._18,  Gates._58,  Gates._52,  Geometries.RIGHT_ANGLE
    _18_17_39_38_L = "Upheaval 2",              Gates._18,  Gates._17,  Gates._39,  Gates._38,  Geometries.LEFT_ANGLE
    _18_17_39_38_J = "Correction",              Gates._18,  Gates._17,  Gates._39,  Gates._38,  Geometries.JUXTAPOSITION
    _18_17_52_58_R = "Service 3",               Gates._18,  Gates._17,  Gates._52,  Gates._58,  Geometries.RIGHT_ANGLE
    _19_33_01_02_L = "Refinement 2",            Gates._19,  Gates._33,  Gates._01,  Gates._02,  Geometries.LEFT_ANGLE
    _19_33_01_02_J = "Need",                    Gates._19,  Gates._33,  Gates._01,  Gates._02,  Geometries.JUXTAPOSITION
    _19_33_44_24_R = "The Four Ways 4",         Gates._19,  Gates._33,  Gates._44,  Gates._24,  Geometries.RIGHT_ANGLE
    _20_34_37_40_L = "Duality 1",               Gates._20,  Gates._34,  Gates._37,  Gates._40,  Geometries.LEFT_ANGLE
    _20_34_37_40_J = "The Now",                 Gates._20,  Gates._34,  Gates._37,  Gates._40,  Geometries.JUXTAPOSITION
    _20_34_55_59_R = "The Sleeping Phoenix 2",  Gates._20,  Gates._34,  Gates._55,  Gates._59,  Geometries.RIGHT_ANGLE
    _21_48_38_39_R = "Tension 1",               Gates._21,  Gates._48,  Gates._38,  Gates._39,  Geometries.RIGHT_ANGLE
    _21_48_54_53_L = "Endeavor 1",              Gates._21,  Gates._48,  Gates._54,  Gates._53,  Geometries.LEFT_ANGLE
    _21_48_54_53_J = "Control",                 Gates._21,  Gates._48,  Gates._54,  Gates._53,  Geometries.JUXTAPOSITION
    _22_47_11_12_L = "Informing 1",             Gates._22,  Gates._47,  Gates._11,  Gates._12,  Geometries.LEFT_ANGLE
    _22_47_11_12_J = "Grace",                   Gates._22,  Gates._47,  Gates._11,  Gates._12,  Geometries.JUXTAPOSITION
    _22_47_26_45_R = "Rulership 1",             Gates._22,  Gates._47,  Gates._26,  Gates._45,  Geometries.RIGHT_ANGLE
    _23_43_30_29_L = "Dedication 1",            Gates._23,  Gates._43,  Gates._30,  Gates._29,  Geometries.LEFT_ANGLE
    _23_43_30_29_J = "Assimilation",            Gates._23,  Gates._43,  Gates._30,  Gates._29,  Geometries.JUXTAPOSITION
    _23_43_49_04_R = "Explanation 2",           Gates._23,  Gates._43,  Gates._49,  Gates._04,  Geometries.RIGHT_ANGLE
    _24_44_13_07_L = "Incarnation 1",           Gates._24,  Gates._44,  Gates._13,  Gates._07,  Geometries.LEFT_ANGLE
    _24_44_13_07_J = "Rationalization",         Gates._24,  Gates._44,  Gates._13,  Gates._07,  Geometries.JUXTAPOSITION
    _24_44_19_33_R = "The Four Ways 1",         Gates._24,  Gates._44,  Gates._19,  Gates._33,  Geometries.RIGHT_ANGLE
    _25_46_10_15_R = "The Vessel of Love 1",    Gates._25,  Gates._46,  Gates._10,  Gates._15,  Geometries.RIGHT_ANGLE
    _25_46_58_52_L = "Healing 1",               Gates._25,  Gates._46,  Gates._58,  Gates._52,  Geometries.LEFT_ANGLE
    _25_46_58_52_J = "Innocence",               Gates._25,  Gates._46,  Gates._58,  Gates._52,  Geometries.JUXTAPOSITION
    _26_45_06_36_L = "Confrontation 2",         Gates._26,  Gates._45,  Gates._06,  Gates._36,  Geometries.LEFT_ANGLE
    _26_45_06_36_J = "The Trickster",           Gates._26,  Gates._45,  Gates._06,  Gates._36,  Geometries.JUXTAPOSITION
    _26_45_47_22_R = "Rulership 4",             Gates._26,  Gates._45,  Gates._47,  Gates._22,  Geometries.RIGHT_ANGLE
    _27_28_19_33_L = "Alignment 1",             Gates._27,  Gates._28,  Gates._19,  Gates._33,  Geometries.LEFT_ANGLE
    _27_28_19_33_J = "Caring",                  Gates._27,  Gates._28,  Gates._19,  Gates._33,  Geometries.JUXTAPOSITION
    _27_28_41_31_R = "The Unexpected 1",        Gates._27,  Gates._28,  Gates._41,  Gates._31,  Geometries.RIGHT_ANGLE
    _28_27_31_41_R = "The Unexpected 3",        Gates._28,  Gates._27,  Gates._31,  Gates._41,  Geometries.RIGHT_ANGLE
    _28_27_33_19_L = "Alignment 2",             Gates._28,  Gates._27,  Gates._33,  Gates._19,  Geometries.LEFT_ANGLE
    _28_27_33_19_J = "Risks",                   Gates._28,  Gates._27,  Gates._33,  Gates._19,  Geometries.JUXTAPOSITION
    _29_30_08_14_R = "Contagion 3",             Gates._29,  Gates._30,  Gates._08,  Gates._14,  Geometries.RIGHT_ANGLE
    _29_30_20_34_L = "Industry 2",              Gates._29,  Gates._30,  Gates._20,  Gates._34,  Geometries.LEFT_ANGLE
    _29_30_20_34_J = "Commitment",              Gates._29,  Gates._30,  Gates._20,  Gates._34,  Geometries.JUXTAPOSITION
    _30_29_14_08_R = "Contagion 1",             Gates._30,  Gates._29,  Gates._14,  Gates._08,  Geometries.RIGHT_ANGLE
    _30_29_34_20_L = "Industry 1",              Gates._30,  Gates._29,  Gates._34,  Gates._20,  Geometries.LEFT_ANGLE
    _30_29_34_20_J = "Fates",                   Gates._30,  Gates._29,  Gates._34,  Gates._20,  Geometries.JUXTAPOSITION
    _31_41_24_44_L = "The Alpha 1",             Gates._31,  Gates._41,  Gates._24,  Gates._44,  Geometries.LEFT_ANGLE
    _31_41_24_44_J = "Influence",               Gates._31,  Gates._41,  Gates._24,  Gates._44,  Geometries.JUXTAPOSITION
    _31_41_27_28_R = "The Unexpected 2",        Gates._31,  Gates._41,  Gates._27,  Gates._28,  Geometries.RIGHT_ANGLE
    _32_42_56_60_L = "Limitation 2",            Gates._32,  Gates._42,  Gates._56,  Gates._60,  Geometries.LEFT_ANGLE
    _32_42_56_60_J = "Conservation",            Gates._32,  Gates._42,  Gates._56,  Gates._60,  Geometries.JUXTAPOSITION
    _32_42_62_61_R = "Maya 3",                  Gates._32,  Gates._42,  Gates._62,  Gates._61,  Geometries.RIGHT_ANGLE
    _33_19_02_01_L = "Refinement 1",            Gates._33,  Gates._19,  Gates._02,  Gates._01,  Geometries.LEFT_ANGLE
    _33_19_02_01_J = "Retreat",                 Gates._33,  Gates._19,  Gates._02,  Gates._01,  Geometries.JUXTAPOSITION
    _33_19_24_44_R = "The Four Ways 2",         Gates._33,  Gates._19,  Gates._24,  Gates._44,  Geometries.RIGHT_ANGLE
    _34_20_40_37_L = "Duality 2",               Gates._34,  Gates._20,  Gates._40,  Gates._37,  Geometries.LEFT_ANGLE
    _34_20_40_37_J = "Power",                   Gates._34,  Gates._20,  Gates._40,  Gates._37,  Geometries.JUXTAPOSITION
    _34_20_59_55_R = "The Sleeping Phoenix 4",  Gates._34,  Gates._20,  Gates._59,  Gates._55,  Geometries.RIGHT_ANGLE
    _35_05_22_47_L = "Separation 1",            Gates._35,  Gates._05,  Gates._22,  Gates._47,  Geometries.LEFT_ANGLE
    _35_05_22_47_J = "Experience",              Gates._35,  Gates._05,  Gates._22,  Gates._47,  Geometries.JUXTAPOSITION
    _35_05_63_64_R = "Consciousness 2",         Gates._35,  Gates._05,  Gates._63,  Gates._64,  Geometries.RIGHT_ANGLE
    _36_06_10_15_L = "The Plane 1",             Gates._36,  Gates._06,  Gates._10,  Gates._15,  Geometries.LEFT_ANGLE
    _36_06_10_15_J = "Crisis",                  Gates._36,  Gates._06,  Gates._10,  Gates._15,  Geometries.JUXTAPOSITION
    _36_06_11_12_R = "Eden 1",                  Gates._36,  Gates._06,  Gates._11,  Gates._12,  Geometries.RIGHT_ANGLE
    _37_40_05_35_L = "Migration 1",             Gates._37,  Gates._40,  Gates._05,  Gates._35,  Geometries.LEFT_ANGLE
    _37_40_05_35_J = "Bargains",                Gates._37,  Gates._40,  Gates._05,  Gates._35,  Geometries.JUXTAPOSITION
    _37_40_09_16_R = "Planning 1",              Gates._37,  Gates._40,  Gates._09,  Gates._16,  Geometries.RIGHT_ANGLE
    _38_39_48_21_R = "Tension 4",               Gates._38,  Gates._39,  Gates._48,  Gates._21,  Geometries.RIGHT_ANGLE
    _38_39_57_51_L = "Individualism 2",         Gates._38,  Gates._39,  Gates._57,  Gates._51,  Geometries.LEFT_ANGLE
    _38_39_57_51_J = "Opposition",              Gates._38,  Gates._39,  Gates._57,  Gates._51,  Geometries.JUXTAPOSITION
    _39_38_21_48_R = "Tension 2",               Gates._39,  Gates._38,  Gates._21,  Gates._48,  Geometries.RIGHT_ANGLE
    _39_38_51_57_L = "Individualism 1",         Gates._39,  Gates._38,  Gates._51,  Gates._57,  Geometries.LEFT_ANGLE
    _39_38_51_57_J = "Provocation",             Gates._39,  Gates._38,  Gates._51,  Gates._57,  Geometries.JUXTAPOSITION
    _40_37_16_09_R = "Planning 3",              Gates._40,  Gates._37,  Gates._16,  Gates._09,  Geometries.RIGHT_ANGLE
    _40_37_35_05_L = "Migration 2",             Gates._40,  Gates._37,  Gates._35,  Gates._05,  Geometries.LEFT_ANGLE
    _40_37_35_05_J = "Denial",                  Gates._40,  Gates._37,  Gates._35,  Gates._05,  Geometries.JUXTAPOSITION
    _41_31_28_27_R = "The Unexpected 4",        Gates._41,  Gates._31,  Gates._28,  Gates._27,  Geometries.RIGHT_ANGLE
    _41_31_44_24_L = "The Alpha 2",             Gates._41,  Gates._31,  Gates._44,  Gates._24,  Geometries.LEFT_ANGLE
    _41_31_44_24_J = "Fantasy",                 Gates._41,  Gates._31,  Gates._44,  Gates._24,  Geometries.JUXTAPOSITION
    _42_32_60_56_L = "Limitation 1",            Gates._42,  Gates._32,  Gates._60,  Gates._56,  Geometries.LEFT_ANGLE
    _42_32_60_56_J = "Completion",              Gates._42,  Gates._32,  Gates._60,  Gates._56,  Geometries.JUXTAPOSITION
    _42_32_61_62_R = "Maya 1",                  Gates._42,  Gates._32,  Gates._61,  Gates._62,  Geometries.RIGHT_ANGLE
    _43_23_04_49_R = "Explanation 4",           Gates._43,  Gates._23,  Gates._04,  Gates._49,  Geometries.RIGHT_ANGLE
    _43_23_29_30_L = "Dedication 2",            Gates._43,  Gates._23,  Gates._29,  Gates._30,  Geometries.LEFT_ANGLE
    _43_23_29_30_J = "Insight",                 Gates._43,  Gates._23,  Gates._29,  Gates._30,  Geometries.JUXTAPOSITION
    _44_24_07_13_L = "Incarnation 2",           Gates._44,  Gates._24,  Gates._07,  Gates._13,  Geometries.LEFT_ANGLE
    _44_24_07_13_J = "Alertness",               Gates._44,  Gates._24,  Gates._07,  Gates._13,  Geometries.JUXTAPOSITION
    _44_24_33_19_R = "The Four Ways 3",         Gates._44,  Gates._24,  Gates._33,  Gates._19,  Geometries.RIGHT_ANGLE
    _45_26_22_47_R = "Rulership 2",             Gates._45,  Gates._26,  Gates._22,  Gates._47,  Geometries.RIGHT_ANGLE
    _45_26_36_06_L = "Confrontation 1",         Gates._45,  Gates._26,  Gates._36,  Gates._06,  Geometries.LEFT_ANGLE
    _45_26_36_06_J = "Possession",              Gates._45,  Gates._26,  Gates._36,  Gates._06,  Geometries.JUXTAPOSITION
    _46_25_15_10_R = "The Vessel of Love 3",    Gates._46,  Gates._25,  Gates._15,  Gates._10,  Geometries.RIGHT_ANGLE
    _46_25_52_58_L = "Healing 2",               Gates._46,  Gates._25,  Gates._52,  Gates._58,  Geometries.LEFT_ANGLE
    _46_25_52_58_J = "Serendipity",             Gates._46,  Gates._25,  Gates._52,  Gates._58,  Geometries.JUXTAPOSITION
    _47_22_12_11_L = "Informing 2",             Gates._47,  Gates._22,  Gates._12,  Gates._11,  Geometries.LEFT_ANGLE
    _47_22_12_11_J = "Oppression",              Gates._47,  Gates._22,  Gates._12,  Gates._11,  Geometries.JUXTAPOSITION
    _47_22_45_26_R = "Rulership 3",             Gates._47,  Gates._22,  Gates._45,  Gates._26,  Geometries.RIGHT_ANGLE
    _48_21_39_38_R = "Tension 3",               Gates._48,  Gates._21,  Gates._39,  Gates._38,  Geometries.RIGHT_ANGLE
    _48_21_53_54_L = "Endeavor 2",              Gates._48,  Gates._21,  Gates._53,  Gates._54,  Geometries.LEFT_ANGLE
    _48_21_53_54_J = "Depth",                   Gates._48,  Gates._21,  Gates._53,  Gates._54,  Geometries.JUXTAPOSITION
    _49_04_14_08_L = "Revolution 1",            Gates._49,  Gates._04,  Gates._14,  Gates._08,  Geometries.LEFT_ANGLE
    _49_04_14_08_J = "Principles",              Gates._49,  Gates._04,  Gates._14,  Gates._08,  Geometries.JUXTAPOSITION
    _49_04_43_23_R = "Explanation 1",           Gates._49,  Gates._04,  Gates._43,  Gates._23,  Geometries.RIGHT_ANGLE
    _50_03_31_41_L = "Wishes 2",                Gates._50,  Gates._03,  Gates._31,  Gates._41,  Geometries.LEFT_ANGLE
    _50_03_31_41_J = "Values",                  Gates._50,  Gates._03,  Gates._31,  Gates._41,  Geometries.JUXTAPOSITION
    _50_03_56_60_R = "Laws 3",                  Gates._50,  Gates._03,  Gates._56,  Gates._60,  Geometries.RIGHT_ANGLE
    _51_57_54_53_R = "Penetration 1",           Gates._51,  Gates._57,  Gates._54,  Gates._53,  Geometries.RIGHT_ANGLE
    _51_57_61_62_L = "The Clarion 1",           Gates._51,  Gates._57,  Gates._61,  Gates._62,  Geometries.LEFT_ANGLE
    _51_57_61_62_J = "Shock",                   Gates._51,  Gates._57,  Gates._61,  Gates._62,  Geometries.JUXTAPOSITION
    _52_58_17_18_R = "Service 2",               Gates._52,  Gates._58,  Gates._17,  Gates._18,  Geometries.RIGHT_ANGLE
    _52_58_21_48_L = "Demands 1",               Gates._52,  Gates._58,  Gates._21,  Gates._48,  Geometries.LEFT_ANGLE
    _52_58_21_48_J = "Stillness",               Gates._52,  Gates._58,  Gates._21,  Gates._48,  Geometries.JUXTAPOSITION
    _53_54_42_32_L = "Cycles 1",                Gates._53,  Gates._54,  Gates._42,  Gates._32,  Geometries.LEFT_ANGLE
    _53_54_42_32_J = "Beginnings",              Gates._53,  Gates._54,  Gates._42,  Gates._32,  Geometries.JUXTAPOSITION
    _53_54_51_57_R = "Penetration 2",           Gates._53,  Gates._54,  Gates._51,  Gates._57,  Geometries.RIGHT_ANGLE
    _54_53_32_42_L = "Cycles 2",                Gates._54,  Gates._53,  Gates._32,  Gates._42,  Geometries.LEFT_ANGLE
    _54_53_32_42_J = "Ambition",                Gates._54,  Gates._53,  Gates._32,  Gates._42,  Geometries.JUXTAPOSITION
    _54_53_57_51_R = "Penetration 4",           Gates._54,  Gates._53,  Gates._57,  Gates._51,  Geometries.RIGHT_ANGLE
    _55_59_09_16_L = "Spirit 1",                Gates._55,  Gates._59,  Gates._09,  Gates._16,  Geometries.LEFT_ANGLE
    _55_59_09_16_J = "Moods",                   Gates._55,  Gates._59,  Gates._09,  Gates._16,  Geometries.JUXTAPOSITION
    _55_59_34_20_R = "The Sleeping Phoenix 1",  Gates._55,  Gates._59,  Gates._34,  Gates._20,  Geometries.RIGHT_ANGLE
    _56_60_03_50_R = "Laws 2",                  Gates._56,  Gates._60,  Gates._03,  Gates._50,  Geometries.RIGHT_ANGLE
    _56_60_27_28_L = "Distraction 1",           Gates._56,  Gates._60,  Gates._27,  Gates._28,  Geometries.LEFT_ANGLE
    _56_60_27_28_J = "Stimulation",             Gates._56,  Gates._60,  Gates._27,  Gates._28,  Geometries.JUXTAPOSITION
    _57_51_53_54_R = "Penetration 3",           Gates._57,  Gates._51,  Gates._53,  Gates._54,  Geometries.RIGHT_ANGLE
    _57_51_62_61_L = "The Clarion 2",           Gates._57,  Gates._51,  Gates._62,  Gates._61,  Geometries.LEFT_ANGLE
    _57_51_62_61_J = "Intuition",               Gates._57,  Gates._51,  Gates._62,  Gates._61,  Geometries.JUXTAPOSITION
    _58_52_18_17_R = "Service 4",               Gates._58,  Gates._52,  Gates._18,  Gates._17,  Geometries.RIGHT_ANGLE
    _58_52_48_21_L = "Demands 2",               Gates._58,  Gates._52,  Gates._48,  Gates._21,  Geometries.LEFT_ANGLE
    _58_52_48_21_J = "Vitality",                Gates._58,  Gates._52,  Gates._48,  Gates._21,  Geometries.JUXTAPOSITION
    _59_55_16_09_L = "Spirit 2",                Gates._59,  Gates._55,  Gates._16,  Gates._09,  Geometries.LEFT_ANGLE
    _59_55_16_09_J = "Strategy",                Gates._59,  Gates._55,  Gates._16,  Gates._09,  Geometries.JUXTAPOSITION
    _59_55_20_34_R = "The Sleeping Phoenix 3",  Gates._59,  Gates._55,  Gates._20,  Gates._34,  Geometries.RIGHT_ANGLE
    _60_56_28_27_L = "Distraction 2",           Gates._60,  Gates._56,  Gates._28,  Gates._27,  Geometries.LEFT_ANGLE
    _60_56_28_27_J = "Limitation",              Gates._60,  Gates._56,  Gates._28,  Gates._27,  Geometries.JUXTAPOSITION
    _60_56_50_03_R = "Laws 4",                  Gates._60,  Gates._56,  Gates._50,  Gates._03,  Geometries.RIGHT_ANGLE
    _61_62_32_42_R = "Maya 4",                  Gates._61,  Gates._62,  Gates._32,  Gates._42,  Geometries.RIGHT_ANGLE
    _61_62_50_03_L = "Obscuration 2",           Gates._61,  Gates._62,  Gates._50,  Gates._03,  Geometries.LEFT_ANGLE
    _61_62_50_03_J = "Thinking",                Gates._61,  Gates._62,  Gates._50,  Gates._03,  Geometries.JUXTAPOSITION
    _62_61_03_50_L = "Obscuration 1",           Gates._62,  Gates._61,  Gates._03,  Gates._50,  Geometries.LEFT_ANGLE
    _62_61_03_50_J = "Detail",                  Gates._62,  Gates._61,  Gates._03,  Gates._50,  Geometries.JUXTAPOSITION
    _62_61_42_32_R = "Maya 2",                  Gates._62,  Gates._61,  Gates._42,  Gates._32,  Geometries.RIGHT_ANGLE
    _63_64_05_35_R = "Consciousness 1",         Gates._63,  Gates._64,  Gates._05,  Gates._35,  Geometries.RIGHT_ANGLE
    _63_64_26_45_L = "Dominion 1",              Gates._63,  Gates._64,  Gates._26,  Gates._45,  Geometries.LEFT_ANGLE
    _63_64_26_45_J = "Doubts",                  Gates._63,  Gates._64,  Gates._26,  Gates._45,  Geometries.JUXTAPOSITION
    _64_63_35_05_R = "Consciousness 3",         Gates._64,  Gates._63,  Gates._35,  Gates._05,  Geometries.RIGHT_ANGLE
    _64_63_45_26_L = "Dominion 2",              Gates._64,  Gates._63,  Gates._45,  Gates._26,  Geometries.LEFT_ANGLE
    _64_63_45_26_J = "Confusion",               Gates._64,  Gates._63,  Gates._45,  Gates._26,  Geometries.JUXTAPOSITION

    @property
    def _name(self) -> str:
        """Return the name as `ps-pe-ds-de`."""
        return self.format_cross_gates(*self.gates)

    @property
    def full_name(self) -> str:
        """Return the name as `<geometry> Cross of <title> (<name>)`"""
        return f"{self.geometry} Cross of {self.title} ({self.name})"

    @property
    def gates(self) -> tuple[Gates]:
        """Return the Personality Sun/Earth & Design Sun/Earth Gates of this Cross."""
        return (self.ps, self.pe, self.ds, self.de)

    @property
    def quarter(self) -> Quarters:
        """Return the Quarter in which the Personality Sun Gate of this Cross is."""
        return self.gates[0].quarter

    @property
    def personality_sun_gate(self) -> Gates:
        return self.ps

    @property
    def personality_earth_gate(self) -> Gates:
        return self.pe

    @property
    def design_sun_gate(self) -> Gates:
        return self.ds

    @property
    def design_earth_gate(self) -> Gates:
        return self.de

    @classmethod
    def format_cross_gates(cls, ps: Gates, pe: Gates, ds: Gates, de: Gates) -> str:
        """Format the Gates of this Cross as `Personality Sun/Earth | Design Sun/Earth`."""
        return f"{ps.num}/{pe.num} | {ds.num}/{de.num}"

    @classmethod
    def get(cls, ps: Gates, pe: Gates, ds: Gates, de: Gates, geometry: Geometries) -> "Crosses":
        """Retrieve a Cross based on its Gates: Personality Sun & Earth, Design Sun & Earth."""
        key = f"_{ps.num:02d}_{pe.num:02d}_{ds.num:02d}_{de.num:02d}_{geometry.letter}"

        try:
            return cls[key]
        except KeyError:
            gates = cls.format_cross_gates(ps, pe, ds, de)
            raise ValueError(f"No Cross found for the ({gates}) Gates, {geometry}.")


# ==================================================================================================
# PROFILES
# ==================================================================================================

# LINES --------------------------------------------------------------------------------------------

class Lines(SuperEnum):
    """The 6 (Profile) Lines.

    References: "The Definitive Book of Human Design" p255-260.
    """
    __NUMBERED__ = True  # Adds auto-`num` (= `name`). Allows `ENUM(<num>)`.

    __FIELDS__ = "title",  # Trick to keep `name` = `num` & `full_name`.
    _1         = "Investigator"  # [Ref. p256]
    _2         = "Hermit"        # [Ref. p257]
    _3         = "Martyr"        # [Ref. p257-258]
    _4         = "Opportunist"   # [Ref. p258]
    _5         = "Heretic"       # [Ref. p258-259]
    _6         = "Role Model"    # [Ref. p259-260]

    @property
    def profiles(self) -> tuple["Profiles"]:
        """Return the list of Profiles including this Line."""
        return tuple(profile for profile in Profiles if self in profile.lines)


# PROFILES -----------------------------------------------------------------------------------------

class Profiles(SuperEnum):
    """The 12 Profiles.

    References: "The Definitive Book of Human Design" p254-285.
    """
    # Sorting: By lines.
    __FIELDS__ = "personality_line",  "design_line",  "geometry",               "destiny"
    _1_3       = Lines._1,            Lines._3,       Geometries.RIGHT_ANGLE,    Destinies.PERSONAL       # [Ref. p262-263]
    _1_4       = Lines._1,            Lines._4,       Geometries.RIGHT_ANGLE,    Destinies.PERSONAL       # [Ref. p264-265]
    _2_4       = Lines._2,            Lines._4,       Geometries.RIGHT_ANGLE,    Destinies.PERSONAL       # [Ref. p266-267]
    _2_5       = Lines._2,            Lines._5,       Geometries.RIGHT_ANGLE,    Destinies.PERSONAL       # [Ref. p268-269]
    _3_5       = Lines._3,            Lines._5,       Geometries.RIGHT_ANGLE,    Destinies.PERSONAL       # [Ref. p270-271]
    _3_6       = Lines._3,            Lines._6,       Geometries.RIGHT_ANGLE,    Destinies.PERSONAL       # [Ref. p272-273]
    _4_1       = Lines._4,            Lines._1,       Geometries.JUXTAPOSITION,  Destinies.FIXED_FATE     # [Ref. p276-277]
    _4_6       = Lines._4,            Lines._6,       Geometries.RIGHT_ANGLE,    Destinies.TRANSPERSONAL  # [Ref. p274-275]
    _5_1       = Lines._5,            Lines._1,       Geometries.LEFT_ANGLE,     Destinies.TRANSPERSONAL  # [Ref. p278-279]
    _5_2       = Lines._5,            Lines._2,       Geometries.LEFT_ANGLE,     Destinies.TRANSPERSONAL  # [Ref. p280-281]
    _6_2       = Lines._6,            Lines._2,       Geometries.LEFT_ANGLE,     Destinies.TRANSPERSONAL  # [Ref. p282-283]
    _6_3       = Lines._6,            Lines._3,       Geometries.LEFT_ANGLE,     Destinies.TRANSPERSONAL  # [Ref. p284-285]

    @property
    def lines(self) -> tuple[Lines]:
        """Return the list of Profile Lines."""
        return (self.personality_line, self.design_line)

    @property
    def name(self) -> str:
        """Return `<Personality Line number>/<Design Line number>`."""
        return "/".join([str(num) for num in self.num])

    @property
    def num(self) -> tuple[int]:
        """Return the number of the Lines composing this Profile."""
        return tuple(line.num for line in self.lines)

    @property
    def title(self) -> str:
        """Return `<Personality Line name>/<Design Line name>`."""
        return "/".join([line.title for line in self.lines])

    @classmethod
    def get(cls, personality: Lines, design: Lines) -> "Profiles":
        """Retrieve a Profile based on its Personality and Design Lines."""
        try:
            return cls[f"_{personality.num}_{design.num}"]
        except KeyError:
            raise ValueError(f"No Profile found for {personality}/{design} Lines.")


# ==================================================================================================
# AUTHORITIES
# ==================================================================================================

# AUTHORITIES --------------------------------------------------------------------------------------

class Authorities(SuperEnum):
    """The 8 (Inner Personal) Authorities.

    It's the source of inner guidance for making decisions as oneself.

    References: "The Definitive Book of Human Design" p106-111.
    """
    # Sorting: According to reference book.
    SOLAR_PLEXUS    = "Solar Plexus"     # Emotional Authority
    SACRAL          = "Sacral"           # Sacral Authority
    SPLENIC         = "Splenic"          # Splenic Authority
    EGO_MANIFESTED  = "Ego Manifested"   # Ego Authority
    EGO_PROJECTED   = "Ego Projected"    # Ego Authority
    SELF_PROJECTED  = "Self Projected"   # Self Authority (G Center)
    OUTER_AUTHORITY = "Outer Authority"  # No Inner Authority (Mental Projectors)
    LUNAR           = "Lunar"            # Lunar Cycle


# ==================================================================================================
# STATES
# ==================================================================================================

# SUPERENUM FOR STATES -----------------------------------------------------------------------------

class StateEnum(SuperEnum):
    """Base `SuperEnum` for the states."""

    @property
    def is_on(self) -> bool:
        """Return whether this State means ON."""
        return NotImplemented

    @property
    def is_off(self) -> bool:
        """Return whether this State means OFF/not ON."""
        return not self.is_on


# CENTER STATES ------------------------------------------------------------------------------------

class CenterStates(StateEnum):
    """The 3 possible states for Centers.

    - Defined: Each Channel activates the Centers it connects (via its 2 Gates).
        - Synonym: colored, colored-in, fixed, consistent.
    - Undefined: An has one or more Gates activations (dormant Gates).
        - Synonym: white (with gates), uncolored. ⚠️ NOT: open.
    - (Completely) Open: No Gates activations.
        - Synonym: white (without gates), totally open.

    ⚠️ Warning: When Ra uses "open", he means "completely open". But within the HD community, "open"
    is often incorrectly used as a synonym for "undefined".

    References: "The Definitive Book of Human Design" p46, 51
    """
    DEFINED   = "Defined"
    UNDEFINED = "Undefined"
    OPEN      = "Completely Open"

    @property
    def is_on(self) -> bool:
        """Return whether this Center State means Defined."""
        return self is self.__class__.DEFINED


# CHANNEL STATES -----------------------------------------------------------------------------------

class ChannelStates(StateEnum):
    """The 2 possible states for Channels.

    - Defined: Both Gates are activated.
        - Synonyms: complete, activated, colored, colored-in.
    - Undefined: One or both Gates are unactivated.
        - Synonyms: incomplete, unactivated, potential, white.

    References: "The Definitive Book of Human Design" p158
    """
    DEFINED   = "Defined"
    UNDEFINED = "Undefined"
    # TODO: Is there a term for those having only one Activated Gate?

    @property
    def is_on(self) -> bool:
        """Return whether this Channel State means Defined."""
        return self is not self.__class__.DEFINED


# GATE STATES --------------------------------------------------------------------------------------

class GateStates(StateEnum):
    """The 6 possible states for Gates.

    Primary States:
    - Activated: With a planetary activation.
        - Synonyms: colored, colored-in, active. Problematic: defined.
    - Unactivated: No planetary activation.
        - Synonyms: white, uncolored. Problematic: inactive, undefined.

    | SUBSTATES OVERVIEW | Gate | H.Gate | Center | Extra                 |
    | ------------------ | ---- | ------ | ------ | --------------------- |
    | Channeled          | Yes  | Yes    | -      |                       |
    | TODO?              | Yes  | No     | -      |                       |
    | TODO?              | No   | Yes    | -      |                       |
    | TODO?              | No   | No     | -      |                       |
    | Hanging            | Yes  | No     | Yes    |                       |
    | Dormant            | Yes  | No     | No     |                       |
    | Bridging           | No   | Yes    | -      | Merging 2 Definitions |
    | Harmonic Hanging   | No   | Yes    | Yes    |                       |
    | Harmonic Dormant   | No   | Yes    | No     |                       |

    Activated Gate Substates:
    - Channeled: Activated Gate with an Activated Harmonic Gate (so in a Defined Channel).
    - Hanging: Activated Gate with an Unactivated Harmonic Gate (so in an Undefined Channel),
      in a Defined Center (so the Center has an other Channel Defined). [Ref. p51, 429]
    - Dormant: Activated Gate with an Unactivated Harmonic Gate (so in an Undefined Channel),
      in an Undefined Center. [Ref. p51, 427]

    Unactivated Gate Substates:
    - Bridging: Unactivated Gate with an Activated Harmonic Gate (so in an Undefined Channel),
      in a Channel that would merge two Split Definitions if Activated. [Ref. p152, 423]
    - Harmonic Hanging: Unactivated Gate with a Hanging Harmonic Gate (so in an Undefined Channel),
      in a Defined Center.
    - Harmonic Dormant: Unactivated Gate with a Dormant Harmonic Gate (so in an Undefined Channel),
      in an Undefined Center.

    References: "The Definitive Book of Human Design" p51, 152, 423, 427, 429.
    """
    # TODO: Update items based on docstring.
    ACTIVATED   = "Activated"
    UNACTIVATED = "Unactivated"
    CHANNELED   = "Channeled"
    HANGING     = "Hanging"
    DORMANT     = "Dormant"
    BRIDGING    = "Bridging"

    @property
    def is_on(self) -> bool:
        """Return whether this Gate State means Activated taking into account its substates."""
        return self is not self.__class__.UNACTIVATED


# ==================================================================================================
# VARIABLES
# ==================================================================================================

# COLORS -------------------------------------------------------------------------------------------

class Colors(SuperEnum):
    """The 6 Colors.

    TODO:
    In order to get to color, you're going to have to be at least within two to three minutes to be safe. [Ref. "Colors" (Ra Uru Hu), p6]
    Color represents the way we're designed to respond to being. [Ref. "Colors" (Ra Uru Hu), p7]
    Response is the way that the vehicle is designed to respond to all things in life. Existence is a response. Color represents the underlying theme of how we respond to anything. [Ref. "Colors" (Ra Uru Hu), p7]
    Modes are modes that influence the way in which the lines operate. [Ref. "Colors" (Ra Uru Hu), p8]
    There are special relationships that exist between 1 and 2, 3 and 4, 5 and 6. [Ref. "Colors" (Ra Uru Hu), p8]
    /TODO
    """
    __NUMBERED__ = True

    __FIELDS__ = "response",   "modes",                         "binary"
    _1         = "Fear",       ("Communalist", "Separatist"),   Centers.SPLENIC
    _2         = "Hope",       ("Theist",      "Anti-Theist"),  Centers.SPLENIC
    _3         = "Desire",     ("Leader",      "Follower"),     Centers.AJNA
    _4         = "Need",       ("Master",      "Novice"),       Centers.AJNA
    _5         = "Guilt",      ("Conditioner", "Conditioned"),  Centers.SOLAR_PLEXUS
    _6         = "Innocence",  ("Observer",    "Observed"),     Centers.SOLAR_PLEXUS


# TONES --------------------------------------------------------------------------------------------

class Tones(SuperEnum):
    """The 6 Tones."""
    __NUMBERED__ = True

    __FIELDS__ = "theme",        "department",    "binary"
    _1         = "Security",     "Smell",         Centers.SPLENIC
    _2         = "Uncertainty",  "Taste",         Centers.SPLENIC
    _3         = "Action",       "Outer Vision",  Centers.AJNA
    _4         = "Meditation",   "Inner Vision",  Centers.AJNA
    _5         = "Judgment",     "Feeling",       Centers.SOLAR_PLEXUS
    _6         = "Acceptance",   "Touch",         Centers.SOLAR_PLEXUS


# BASES --------------------------------------------------------------------------------------------

class Bases(SuperEnum):
    """The 5 Bases.

    TODO: In order to have an accurate base calculation, you have to be plus or minus twenty seconds. [Ref. "Colors" (Ra Uru Hu), p7]
    """
    __NUMBERED__ = True

    __FIELDS__ = "?1?",            "?2?",             "?3?",          "?4?",    "Sense",     "?6?",             "?7?",                     "?8?",                              "?9?"
    _1         = "Individuality",  "Yang/Yang",       "Reactive",     "Where",  "Seeing",    "Location",        "Uniqueness: 'I Define'",  "To Measure, To Name",              "Movement"
    _2         = "Mind",           "Yang/Yin",        "Integrative",  "What",   "Taste",     "Identification",  "Role: 'I Remember'",      "Transgenerational Consciousness",  "Evolution"
    _3         = "Body",           "Yin/Yin",         "Objective",    "When",   "Touching",  "Collaboration",   "Genetics: 'I Am'",        "Matter is Being",                  "?"
    _4         = "Ego",            "Yin/Yang",        "Progressive",  "Why",    "Smell",     "Manifestation",   "Self: 'I Design'",        "Information Feed",                 "Design"
    _5         = "Personality",    "Space/Illusion",  "Subjective",   "Who",    "Hearing",   "Mutation",        "Presence: 'I Think'",     "Communication",                    "Space"


# ORIENTATIONS -------------------------------------------------------------------------------------

class Orientations(SuperEnum):
    """The 2 Orientations for Variables."""
    LEFT  = "Left"
    RIGHT = "Right"

    @property
    def letter(self) -> str:
        """Return the letter representing the orientation (uppercase)."""
        return self.name[0].upper()

    @classmethod
    def get(cls, value: int) -> "Orientations":
        """Return the Orientation based on this (Color) number."""
        return (cls.LEFT if value < 4
                else cls.RIGHT)


# VARIABLE ORIENTATIONS ----------------------------------------------------------------------------

class VariableOrientations(SuperEnum):
    """The 16 Variable Orientations.

    | Key | Variable Name | Imprint     | Planet     | Row    | Col   | Description                                                |
    | --- | ------------- | ----------- | ---------- | ------ | ----- | ---------------------------------------------------------- |
    | pt  | Motivation    | Personality | Sun        | Top    | Right | How we express our "light" in the world.                   |
    | pb  | Perspective   | Personality | North Node | Bottom | Right | What your Personality thinks about the world and itself.   |
    | dt  | Determination | Design      | Sun        | Top    | Left  | Genetic themes we have inherited from our Father.          |
    | db  | Environment   | Design      | North Node | Bottom | Left  | Your relationship to the environment and the people in it. |

    References:
    - "The Definitive Book of Human Design" p37.
    - TODO: "Colors in Human Design" p.
    """
    __FIELDS__ = "pt",                "pb",                "dt",                "db"
    PLL_DLL    = Orientations.LEFT,   Orientations.LEFT,   Orientations.LEFT,   Orientations.LEFT
    PLL_DLR    = Orientations.LEFT,   Orientations.LEFT,   Orientations.LEFT,   Orientations.RIGHT
    PLL_DRL    = Orientations.LEFT,   Orientations.LEFT,   Orientations.RIGHT,  Orientations.LEFT
    PLL_DRR    = Orientations.LEFT,   Orientations.LEFT,   Orientations.RIGHT,  Orientations.RIGHT
    PLR_DLL    = Orientations.LEFT,   Orientations.RIGHT,  Orientations.LEFT,   Orientations.LEFT
    PLR_DLR    = Orientations.LEFT,   Orientations.RIGHT,  Orientations.LEFT,   Orientations.RIGHT
    PLR_DRL    = Orientations.LEFT,   Orientations.RIGHT,  Orientations.RIGHT,  Orientations.LEFT
    PLR_DRR    = Orientations.LEFT,   Orientations.RIGHT,  Orientations.RIGHT,  Orientations.RIGHT
    PRL_DLL    = Orientations.RIGHT,  Orientations.LEFT,   Orientations.LEFT,   Orientations.LEFT
    PRL_DLR    = Orientations.RIGHT,  Orientations.LEFT,   Orientations.LEFT,   Orientations.RIGHT
    PRL_DRL    = Orientations.RIGHT,  Orientations.LEFT,   Orientations.RIGHT,  Orientations.LEFT
    PRL_DRR    = Orientations.RIGHT,  Orientations.LEFT,   Orientations.RIGHT,  Orientations.RIGHT
    PRR_DLL    = Orientations.RIGHT,  Orientations.RIGHT,  Orientations.LEFT,   Orientations.LEFT
    PRR_DLR    = Orientations.RIGHT,  Orientations.RIGHT,  Orientations.LEFT,   Orientations.RIGHT
    PRR_DRL    = Orientations.RIGHT,  Orientations.RIGHT,  Orientations.RIGHT,  Orientations.LEFT
    PRR_DRR    = Orientations.RIGHT,  Orientations.RIGHT,  Orientations.RIGHT,  Orientations.RIGHT

    @property
    def _name(self) -> str:
        """Return the name as `P<Top><Bottom> D<Top><Bottom>`."""
        return self.format_key(*self.orientations).replace("_", " ")

    @property
    def orientations(self) -> dict[str, Orientations]:
        """Return the Orientation of the 4 Variables."""
        return {
            "pt": self.pt,  # Motivation
            "pb": self.pb,  # Perspective
            "dt": self.dt,  # Determination
            "db": self.db,  # Environment
        }

    @classmethod
    def format_key(cls, pt: Orientations, pb: Orientations, dt: Orientations, db: Orientations) -> str:
        """Format the Variables Orientations as `P<Top><Bottom>_D<Top><Bottom>`."""
        return f"P{pt.letter}{pb.letter}_D{dt.letter}{db.letter}".upper()

    @classmethod
    def get(cls, pt: Orientations, pb: Orientations, dt: Orientations, db: Orientations) -> "VariableOrientations":
        """Retrieve a Variables Orientations based on its Gates: Personality Top & Bottom, Design Top & Bottom."""
        return cls[cls.format_key(pt, pb, dt, db)]


# SUPERENUM FOR VARIABLES --------------------------------------------------------------------------

class VariableEnum(SuperEnum):
    """Base Enum for the concrete Variables."""
    __FIELDS__ = "name",
    __NUMBERED__ = True  # Adds auto-`num` (= `name`). Allows `ENUM(<num>)`.

    __LEFT_NAME__ = None
    __RIGHT_NAME__ = None

    @property
    def orientation(self) -> Orientations:
        """Return the Orientation based on this (Color) number."""
        return Orientations.get(self.num)

    @property
    def orientation_name(self) -> str:
        """Return the name related to this Orientation."""
        return (self.__LEFT_NAME__ if self.orientation == Orientations.LEFT
                else self.__RIGHT_NAME__)

    @property
    def transference(self) -> "VariableEnum":
        """Return the transferred state.

        It's the counterpart in the hexagram: 1↔4, 2↔5, 3↔6.
        """
        transferred_state = (self.num + 2) % 6 + 1
        return self.__class__[f"_{transferred_state}"]

    @staticmethod
    def get_imprint() -> Imprints:
        """Return the related Imprint."""
        return Imprints.DESIGN

    @staticmethod
    def get_planet() -> Planets:
        """Return the related Planet."""
        return Planets.SUN


# DETERMINATIONS -----------------------------------------------------------------------------------

class Determinations(VariableEnum):
    """The 6 Determinations (Design Sun Color, top-left Variable).

    TODO: Determination or digestion? Both correct?
    TODO: - ?title?: https://youtu.be/a8NppeOSBpU?t=850
    TODO: - color_name?

    TODO: References: "Colors in Human Design" p.
    """
    # TODO:
    #   1-3: Lower, feed brain
    #   4-6: Upper, fasting OK
    #   -------
    #   1-2: Primitive, rigid
    #   3-4: Energetic, manipulative
    #   5-6: Sensitive, selective

    # v1
    # __FIELDS__ = "name",      "left",         "right",        "?title?",      "color"
    # _1         = "Appetite",  "Consecutive",  "Alternating",  "Hunter",       "?magenta?"
    # _2         = "Taste",     "Open",         "Closed",       "Gatherer",     "?orange?"
    # _3         = "Thirst",    "Hot",          "Cold",         "Transformer",  "?yellow?"
    # _4         = "Touch",     "Calm",         "Nervous",      "Determiner",   "?green?"
    # _5         = "Sound",     "High",         "Low",          "Listener",     "?blue?"
    # _6         = "Light",     "Direct",       "Indirect",     "Watcher",      "?purple?"

    # TODO: List all precise values (ex: OPEN_TASTE, CLOSED_TASTE)? So that it can be passed around as one value.
    __FIELDS__ = "name",                   "color",    "orientation",       "?title?",      "color_name"
    _1_LEFT    = "Appetite, Consecutive",  Colors._1,  Orientations.LEFT,   "Hunter",       "?magenta?"
    _1_RIGHT   = "Appetite, Alternating",  Colors._1,  Orientations.RIGHT,  "Hunter",       "?magenta?"
    _2_LEFT    = "Taste, Open",            Colors._2,  Orientations.LEFT,   "Gatherer",     "?orange?"
    _2_RIGHT   = "Taste, Closed",          Colors._2,  Orientations.RIGHT,  "Gatherer",     "?orange?"
    _3_LEFT    = "Thirst, Hot",            Colors._3,  Orientations.LEFT,   "Transformer",  "?yellow?"
    _3_RIGHT   = "Thirst, Cold",           Colors._3,  Orientations.RIGHT,  "Transformer",  "?yellow?"
    _4_LEFT    = "Touch, Calm",            Colors._4,  Orientations.LEFT,   "Determiner",   "?green?"
    _4_RIGHT   = "Touch, Nervous",         Colors._4,  Orientations.RIGHT,  "Determiner",   "?green?"
    _5_LEFT    = "Sound, High",            Colors._5,  Orientations.LEFT,   "Listener",     "?blue?"
    _5_RIGHT   = "Sound, Low",             Colors._5,  Orientations.RIGHT,  "Listener",     "?blue?"
    _6_LEFT    = "Light, Direct",          Colors._6,  Orientations.LEFT,   "Watcher",      "?purple?"
    _6_RIGHT   = "Light, Indirect",        Colors._6,  Orientations.RIGHT,  "Watcher",      "?purple?"

    __LEFT_NAME__  = "Active"
    __RIGHT_NAME__ = "Passive"

    @property
    def transference(self) -> "VariableEnum":
        """Return the transferred state.

        It's the counterpart in the hexagram: 1↔4, 2↔5, 3↔6.
        """
        transferred_state = (self.num + 2) % 6 + 1
        return self.__class__[f"_{transferred_state}_{self.orientation._key}"]

    @classmethod
    def get(cls, color: Colors, orientation: Orientations) -> "Determinations":
        """Retrieve a Determination based on Color and Orientation."""
        return getattr(cls, f"{color._key}_{orientation._key}")

    @classmethod
    def get_by_color_tone(cls, color: Colors, tone: Tones) -> "Determinations":
        """Retrieve a Determination based on Color and Tone."""
        orientation = Orientations.get(tone)
        return cls.get(color, orientation)

    @staticmethod
    def get_imprint() -> Imprints:
        """Return the related Imprint."""
        return Imprints.DESIGN

    @staticmethod
    def get_planet() -> Planets:
        """Return the related Planet."""
        return Planets.SUN

    # v1
    # @classmethod
    # def get_by_orientation_name(cls, name: str) -> "Determinations":
    # """Retrieve a Determination based on its Orientation (left/right) name."""
    #     for item in cls.items():
    #         if item.left == name or item.right == name:
    #             return item
    #
    #     raise ValueError(f"Determination '{name}' not found.")


# COGNITIONS ---------------------------------------------------------------------------------------

class Cognitions(VariableEnum):
    """The 6 Cognitions (Design Sun Tone, top-left Variable).

    TODO: References: "Colors in Human Design" p.
    """
    _1 = "Smell"
    _2 = "Taste"
    _3 = "Outer Vision"
    _4 = "Inner Vision"
    _5 = "Feeling"
    _6 = "Touch"

    @staticmethod
    def get_imprint() -> Imprints:
        """Return the related Imprint."""
        return Imprints.DESIGN

    @staticmethod
    def get_planet() -> Planets:
        """Return the related Planet."""
        return Planets.SUN


# ENVIRONMENTS -------------------------------------------------------------------------------------

class Environments(VariableEnum):
    """The 6 Environments (Design North Node Color, bottom-left Variable).

    TODO: References: "Colors in Human Design" p.
    """
    # v1
    # __FIELDS__ = "name",       "left",       "right"
    # _1         = "Caves",      "Selective",  "Blending"
    # _2         = "Markets",    "Internal",   "External"
    # _3         = "Kitchens",   "Wet",        "Dry"
    # _4         = "Mountains",  "Active",     "Passive"
    # _5         = "Valleys",    "Narrow",     "Wide"
    # _6         = "Shores",     "Natural",    "Artificial"

    __FIELDS__ = "name",                "color",    "orientation"
    _1_LEFT    = "Caves, Selective",    Colors._1,  Orientations.LEFT
    _1_RIGHT   = "Caves, Blending",     Colors._1,  Orientations.RIGHT
    _2_LEFT    = "Markets, Internal",   Colors._2,  Orientations.LEFT
    _2_RIGHT   = "Markets, External",   Colors._2,  Orientations.RIGHT
    _3_LEFT    = "Kitchens, Wet",       Colors._3,  Orientations.LEFT
    _3_RIGHT   = "Kitchens, Dry",       Colors._3,  Orientations.RIGHT
    _4_LEFT    = "Mountains, Active",   Colors._4,  Orientations.LEFT
    _4_RIGHT   = "Mountains, Passive",  Colors._4,  Orientations.RIGHT
    _5_LEFT    = "Valleys, Narrow",     Colors._5,  Orientations.LEFT
    _5_RIGHT   = "Valleys, Wide",       Colors._5,  Orientations.RIGHT
    _6_LEFT    = "Shores, Natural",     Colors._6,  Orientations.LEFT
    _6_RIGHT   = "Shores, Artificial",  Colors._6,  Orientations.RIGHT

    __LEFT_NAME__  = "Observed"
    __RIGHT_NAME__ = "Observing"

    @property
    def transference(self) -> "VariableEnum":
        """Return the transferred state.

        It's the counterpart in the hexagram: 1↔4, 2↔5, 3↔6.
        """
        transferred_state = (self.num + 2) % 6 + 1
        return self.__class__[f"_{transferred_state}_{self.orientation._key}"]

    @classmethod
    def get(cls, color: Colors, orientation: Orientations) -> "Environments":
        """Retrieve a Determination based on Color and Orientation."""
        return getattr(cls, f"{color._key}_{orientation._key}")

    @classmethod
    def get_by_color_tone(cls, color: Colors, tone: Tones) -> "Environments":
        """Retrieve a Determination based on Color and Tone."""
        orientation = Orientations.get(tone)
        return cls.get(color, orientation)

    @staticmethod
    def get_imprint() -> Imprints:
        """Return the related Imprint."""
        return Imprints.DESIGN

    @staticmethod
    def get_planet() -> Planets:
        """Return the related Planet."""
        return Planets.NORTH_NODE

    # v1
    # @classmethod
    # def get_by_orientation_name(cls, name: str) -> "Environments":
    #     for item in cls.items():
    #         if item.left == name or item.right == name:
    #             return item
    #
    #     raise ValueError(f"Environment '{name}' not found.")


# PERSPECTIVES -------------------------------------------------------------------------------------

class Perspectives(VariableEnum):
    """The 6 Perspectives (Personality North Node Color, bottom-right Variable).

    TODO: Perspective or Awareness? Both correct?

    TODO: References: "Colors in Human Design" p.
    """
    # TODO: These values seem to be for Cognition.
    _1 = "Smell"
    _2 = "Taste"
    _3 = "Outer Vision"
    _4 = "Inner Vision"
    _5 = "Feeling"
    _6 = "Touch"

    __LEFT_NAME__  = "Focused"
    __RIGHT_NAME__ = "Peripheral"

    @staticmethod
    def get_imprint() -> Imprints:
        """Return the related Imprint."""
        return Imprints.PERSONALITY

    @staticmethod
    def get_planet() -> Planets:
        """Return the related Planet."""
        return Planets.NORTH_NODE


# MOTIVATIONS --------------------------------------------------------------------------------------

class Motivations(VariableEnum):
    """The 6 Motivations (Personality Sun Color, top-right Variable).

    TODO: References: "Colors in Human Design" p.
    """
    _1 = "Fear"
    _2 = "Hope"
    _3 = "Desire"
    _4 = "Need"
    _5 = "Guilt"
    _6 = "Innocence"

    __LEFT_NAME__  = "Focused"
    __RIGHT_NAME__ = "Receptive"

    @staticmethod
    def get_imprint() -> Imprints:
        """Return the related Imprint."""
        return Imprints.PERSONALITY

    @staticmethod
    def get_planet() -> Planets:
        """Return the related Planet."""
        return Planets.SUN


# SENSES -------------------------------------------------------------------------------------------

class Senses(VariableEnum):
    """The 6 Senses (Personality Sun Tone, top-right Variable).

    TODO: References: "Colors in Human Design" p.
    """
    _1 = "Uncertainty"
    _2 = "Certainty"
    _3 = "Action"
    _4 = "Meditation"
    _5 = "Observation"
    _6 = "Acceptance"

    @staticmethod
    def get_imprint() -> Imprints:
        """Return the related Imprint."""
        return Imprints.PERSONALITY

    @staticmethod
    def get_planet() -> Planets:
        """Return the related Planet."""
        return Planets.SUN
