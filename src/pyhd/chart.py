"""
Chart: The BodyGraph – Design & Personality Imprints.
"""

import dataclasses
from datetime import datetime
from functools import cached_property
from typing import Iterable

from .activation import Activation
from .constants import (
    CLASSIC_PROJECTOR_CENTERS,
    MENTAL_PROJECTOR_CENTERS,
    MOTOR_CENTERS,
    NON_SACRAL_MOTOR_CENTERS,
    NUM_LINES,
    Authorities,
    Centers,
    Channels,
    ChannelTypes,
    CircuitGroups,
    Circuits,
    Cognitions,
    Crosses,
    DefinitionTypes,
    Destinies,
    Determinations,
    Environments,
    Gates,
    Geometries,
    Imprints,
    Motivations,
    NotSelfThemes,
    Perspectives,
    Planets,
    Profiles,
    Senses,
    Signatures,
    Strategies,
    Types,
    VariableOrientations,
)
from .imprint import Imprint
from .models import ChartLightModel, ChartModel
from .utils import (
    format_datetime,
    get_design_datetime,
    print_h2,
    print_kv,
    print_num_list,
    print_table,
    print_value,
)


class Chart:
    """The BodyGraph – the circuit matrix of human differentiation.

    Based on Personality and Design Imprints – the Activations for all planetary bodies at birth
    and when the Sun is at 88° before birth.

    Reference: "The Definitive Book of Human Design"
    - Glossary: p424
    """

    PROPS = (
        # Note: personality & design are handled specifically.
        "authority", "centers", "channel_types", "channels", "circuit_groups", "circuits",
        "creative_channels", "geometry", "cross", "definitions", "definition_type", "destiny",
        "gates", "not_self_theme", "profile", "signature", "strategy", "type",
        "variable_activations", "variable_orientations", "variables",
        "determination", "cognition", "environment", "perspective", "motivation", "sense",
    )

    def __init__(self, dt: datetime) -> None:
        design_dt, design_lon = get_design_datetime(dt)
        self.design = Imprint(design_dt)
        self.personality = Imprint(dt)

        # To get by Imprint.
        self._imprints = {
            Imprints.DESIGN: self.design,
            Imprints.PERSONALITY: self.personality,
        }

    @property
    def short_description(self):
        return f"{self.profile} {self.authority} {self.type}, {self.cross.full_name}"

    # CHARACTERISTICS ------------------------------------------------------------------------------

    @cached_property
    def authority(self) -> Authorities:
        """Return the Authority.

        1. If no Defined Centers ⇒ Lunar. [Ref. p111]
        2. Based on Defined Center: [Ref. p107-108]
           2.1. If Solar Plexus is Defined ⇒ Solar Plexus.
           2.2. If Sacral is Defined ⇒ Sacral.
           2.3. If Spleen is Defined ⇒ Splenic.
        3. If Heart connected to Throat (via 21-45)⇒ Ego Manifested. [Ref. p109]
        4. If Heart connected to G (via 25-51) ⇒ Ego Projected. [Ref. p109]
        5. If G connected to Throat (via 1-8, 7-31, 10-20, 13-33) ⇒ Self-Projected. [Ref. p110]
        6. If Ajna connected to Head (via 4-63, 24-61, 47-64)
           OR Ajna connected to Throat (via 11-56, 17-62, 23-43)
           OR Head, Ajna, Throat all connected ⇒ Outer (no authority). [Ref. p110]
        """
        # 1. No Defined Centers. [Ref. p111]
        if self.num_centers == 0:
            return Authorities.LUNAR

        # 2. Based on a specific Defined Center. [Ref. p107-108]
        if self.has_center(Centers.SOLAR_PLEXUS):
            return Authorities.SOLAR_PLEXUS

        if self.has_center(Centers.SACRAL):
            return Authorities.SACRAL

        if self.has_center(Centers.SPLENIC):
            return Authorities.SPLENIC

        # 3. Heart connected to Throat (via 21-45). [Ref. p109]
        if self.has_any_channel(Channels.connecting_centers(Centers.HEART, Centers.THROAT)):
            return Authorities.EGO_MANIFESTED

        # 4. Heart connected to G (via 25-51). [Ref. p109]
        if self.has_any_channel(Channels.connecting_centers(Centers.HEART, Centers.G)):
            return Authorities.EGO_PROJECTED

        # 5. G connected to Throat (via 1-8, 7-31, 10-20, 13-33). [Ref. p110]
        if self.has_any_channel(Channels.connecting_centers(Centers.G, Centers.THROAT)):
            return Authorities.SELF_PROJECTED

        # 6. Ajna connected to Head (via 4-63, 24-61, 47-64)
        #    OR Ajna connected to Throat (via 11-56, 17-62, 23-43)
        #    OR Head, Ajna, Throat all connected. [Ref. p110]
        return Authorities.OUTER_AUTHORITY

    @cached_property
    def centers(self) -> tuple[Centers]:
        """Return the list of Defined Centers."""
        # Collect all unique centers from all defined channels.
        # Note: Centers have multiple Channels ⇒ must "unique" (via `set`).
        return tuple(sorted(set(
            center
            for channel in self.channels
            for center in channel.centers
        )))

    @cached_property
    def channel_types(self) -> tuple[ChannelTypes]:
        """Return the list of Channel Types."""
        return tuple({channel.channel_type for channel in self.channels})

    @cached_property
    def channels(self) -> tuple[Channels]:
        """Return the list of Defined Channels."""
        # Note: A Channel is Defined if both its Gates are Activated (i.e. in `self.gates`).
        return tuple(
            channel for channel in Channels
            if all((gate in self.gates) for gate in channel.gates)
        )

    @cached_property
    def circuit_groups(self) -> tuple[CircuitGroups]:
        """Return the list of Circuit Groups."""
        # Note: Multiple Channels can have the same Circuit Group ⇒ must "unique" (via `set`).
        return tuple(sorted(set(channel.circuit_group for channel in self.channels)))

    @cached_property
    def circuits(self) -> tuple[Circuits]:
        """Return the list of Circuits."""
        # Note: Multiple Channels can have the same Circuit ⇒ must "unique" (via `set`).
        return tuple(sorted(set(channel.circuit for channel in self.channels)))

    @cached_property
    def creative_channels(self) -> tuple[Channels]:
        """Return the list of Defined Creative Channels."""
        # Note: Just filtering `self.channels` => already unique and sorted.
        return tuple(channel for channel in self.channels if channel.is_creative)

    @cached_property
    def cross(self) -> Crosses:
        """Return the Incarnation Cross."""
        return Crosses.get(
            ps=self.personality[Planets.SUN].gate,
            pe=self.personality[Planets.EARTH].gate,
            ds=self.design[Planets.SUN].gate,
            de=self.design[Planets.EARTH].gate,
            geometry=self.geometry,
        )

    @cached_property
    def definitions(self) -> tuple[tuple[Centers]]:
        """Return the list of Definitions (i.e. groups of connected Centers)."""
        if not self.centers:
            return tuple()

        # Build adjacency graph: Center -> connected Centers.
        graph = {center: set() for center in self.centers}
        for channel in self.channels:
            c1, c2 = channel.centers
            graph[c1].add(c2)
            graph[c2].add(c1)

        # Count connected components using BFS/DFS (Breadth-First/Depth-First Searches).
        visited = set()
        groups = []

        for center in self.centers:
            if center in visited:
                continue

            # Start a new group.
            group = []  # Tuple to always have the same order.

            # Visit all connected centers.
            stack = [center]
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                if current not in group:
                    group.append(current)
                stack.extend(graph[current] - visited)

            # Add this group.
            groups.append(tuple(group))

        return tuple(groups)

    @cached_property
    def definition_type(self) -> DefinitionTypes:
        """Return the Definition Type.

        - No Definition: Reflector and no Centers defined.
        - Single Definition: All defined Channels and defined Centers are connected in one
          continuous flow.
        - Split Definition: Two separate areas of definition that are not connected to each other.
            - Simple-Split Definition: When the two areas are separated by a single Gate.
            - Wide-Split Definition: When the two areas are separated by multiple Gates or a Channel
              through the Throat.
        - Triple-Split Definition: Three separate areas of definition that are not connected to each
          other.
        - Quadruple-Split Definition: Four separate areas of definition that are not connected to
          each other.
        """
        match self.num_definitions:
            case 0:
                return DefinitionTypes.NO
            case 1:
                return DefinitionTypes.SINGLE
            case 2:
                if self._is_simple_split():
                    return DefinitionTypes.SIMPLE_SPLIT
                return DefinitionTypes.WIDE_SPLIT
            case 3:
                return DefinitionTypes.TRIPLE_SPLIT
            case 4:
                return DefinitionTypes.QUADRUPLE_SPLIT

        raise Exception(f"Invalid number of Definitions ({self.num_definitions}; not in 0-4).")

    def _is_simple_split(self) -> bool:
        """Check if two Definitions are separated by a single Gate."""
        if self.num_definitions != 2:
            raise Exception("This can only be called for Split Definitions.")

        # Loop over each Undefined Channel of each Center of the first Definition
        # and check if it's connected with a Center in the second Definition.
        # If so, it's a direct connection, so Simple-Split.
        definition1, definition2 = self.definitions
        for center in definition1:
            for channel in center.channels:
                # Skip if Channel is defined.
                if channel in self.channels:
                    continue

                # Get the Center at the opposite of this Channel.
                harmonic_center = channel.harmonic_center(center)

                # Skip if Harmonic Center is in the same group.
                if harmonic_center in definition1:
                    continue

                # If Harmonic Center is in the other Definition, it's a direct connection.
                if harmonic_center in definition2:
                    return True

        # Arriving here means there were no direction connections.
        return False

    @property
    def destiny(self) -> Destinies:
        """Return the Destiny."""
        return self.profile.destiny

    @cached_property
    def gates(self) -> tuple[Gates]:
        """Return the list of all Activated Gates, from both Imprints."""
        # Merge Gates from Design and Personality.
        # Note: Some Gates (10, 20, 34, 57) are in multiple Channels ⇒ must "unique" (via `set`).
        return tuple(sorted(set(self.design.gates + self.personality.gates)))

    @cached_property
    def harmonic_gates(self) -> tuple[Gates]:
        """Return the list of the Harmonic Gates of all Activated Gates."""
        # Note: Some Gates (10, 20, 34, 57) are in multiple Channels ⇒ must "unique" (via `set`).
        return tuple(sorted(set(gate.harmonic_gate for gate in self.gates)))

    @cached_property
    def channeled_gates(self) -> tuple[Gates]:
        """Return the list of Channeled Gates.

        Channeled: Activated Gate with an Activated Harmonic Gate (so in a Defined Channel).
        """
        # TODO: Review what Claude did.
        # Merge Gates from Defined Channels.
        # Note: Some Gates (10, 20, 34, 57) are in multiple Channels ⇒ must "unique" (via `set`).
        return tuple(sorted(set(
            gate
            for channel in self.channels  # Defined Channels
            for gate in channel.gates     # Get both Gates
        )))

    @cached_property
    def hanging_gates(self) -> tuple[Gates]:
        """Return the list of Hanging Gates.

        Hanging: Activated Gate with an Unactivated Harmonic Gate (so in an Undefined Channel),
          in a Defined Center (so the Center has an other Channel Defined).
        """
        # TODO: Review what Claude did.
        # Note: Just filtering `self.gates` => already unique and sorted.
        return tuple(
            gate for gate in self.gates                    # Activated Gates
            if (gate.center in self.centers                # In a Defined Center
                and gate.harmonic_gate not in self.gates)  # Unactivated Harmonic Gate
        )

    @cached_property
    def dormant_gates(self) -> tuple[Gates]:
        """Return the list of Dormant Gates.

        Dormant: Activated Gate with an Unactivated Harmonic Gate (so in an Undefined Channel),
          in an Undefined Center.
        """
        # TODO: Review what Claude did.
        # Note: If the Center is Undefined, the Harmonic Gate is Unactivated.
        return tuple(sorted(
            gate for gate in self.gates         # Activated Gates
            if gate.center not in self.centers  # In Undefined Center
        ))

    @cached_property
    def bridging_gates(self) -> tuple[Gates]:
        """Return the list of Bridging Gates.

        Bridging: Unactivated Gate with an Activated Harmonic Gate (so in an Undefined Channel),
          in a Channel that would merge two Split Definitions if Activated.
        """
        # TODO: Review what Claude did.
        bridging = []

        # Check all Channels to find Unactivated Gates whose Harmonic Gate is Activated.
        for channel in Channels:
            gate1, gate2 = channel.gates
            gate1_is_activated = gate1 in self.gates
            gate2_is_activated = gate2 in self.gates

            # If one Gate is Activated but not the other, the Unactivated Gate is Bridging.
            if gate1_is_activated and gate2_is_activated:
                bridging.append(gate2)
            elif gate2_is_activated and gate1_is_activated:
                bridging.append(gate1)

        return tuple(sorted(bridging))


    @cached_property
    def harmonic_hanging_gates(self) -> tuple[Gates]:
        """Return the list of Harmonic Hanging Gates.

        Harmonic Hanging: Unactivated Gate with a Hanging Harmonic Gate (so in an Undefined Channel),
        in a Defined Center.
        """
        # Note: Some Gates (10, 20, 34, 57) are in multiple Channels ⇒ must "unique" (via `set`).
        return tuple(sorted(set(gate.harmonic_gate for gate in self.hanging_gates)))

    @cached_property
    def harmonic_dormant_gates(self) -> tuple[Gates]:
        """Return the list of Harmonic Dormant Gates.

        Harmonic Dormant: Unactivated Gate with a Dormant Harmonic Gate (so in an Undefined Channel),
        in an Undefined Center.
        """
        # Note: Some Gates (10, 20, 34, 57) are in multiple Channels ⇒ must "unique" (via `set`).
        return tuple(sorted(set(gate.harmonic_gate for gate in self.dormant_gates)))

    @property
    def geometry(self) -> Geometries:
        """Return the Geometry."""
        return self.profile.geometry

    @property
    def not_self_theme(self) -> NotSelfThemes:
        """Return the Not-Self Theme."""
        return self.type.not_self_theme

    @property
    def profile(self) -> Profiles:
        """Return the Profile."""
        return Profiles.get(self.personality.line, self.design.line)

    @property
    def signature(self) -> Signatures:
        """Return the Signature."""
        return self.type.signature

    @property
    def strategy(self) -> Strategies:
        """Return the Strategy."""
        return self.type.strategy

    @cached_property
    def type(self) -> Types:
        """Return the Type.

        - Manifestor: [Ref. p116]
            - Sacral undefined.
            - Direct or indirect connection between Throat and one of the three remaining motor
              centers Root, Solar Plexus, Heart.
        - Generator: [Ref. p123]
            - Sacral defined.
            - Pure Generator: No Motor Centers connected directly to Throat.
            - Manifesting Generator: A Motor Center connected to Throat.
        - Projector: [Ref. p129, 131]
            - Sacral undefined.
            - No Motor Centers connected to Throat.
            - Mental Projector: Throat, Ajna or Head Defined; no Defined Centers below the Throat.
            - Energy Projector: 1+ Motor Centers Defined.
            - Classic Projector: 1+ Non-Motor Centers Defined below the Throat.
        - Reflector: [Ref. p137]
            - All nine Centers are Undefined.
        """
        # Reflectors.
        if self.num_centers == 0:
            return Types.REFLECTOR

        has_throat_connection = self.is_connected(Centers.THROAT, NON_SACRAL_MOTOR_CENTERS)

        # Generators.
        if self.has_center(Centers.SACRAL):
            if has_throat_connection:
                return Types.MANIFESTING_GENERATOR

            return Types.PURE_GENERATOR

        # Manifestors.
        if has_throat_connection:
            return Types.MANIFESTOR

        # Projectors.
        if self.has_motor:
            return Types.ENERGY_PROJECTOR

        if self.has_any_center(CLASSIC_PROJECTOR_CENTERS):
            other_defined_centers = (
                center for center in self.centers
                if center not in CLASSIC_PROJECTOR_CENTERS
            )
            if not other_defined_centers:
                return Types.CLASSIC_PROJECTOR

        if self.has_any_center(MENTAL_PROJECTOR_CENTERS):
            other_defined_centers = (
                center for center in self.centers
                if center not in MENTAL_PROJECTOR_CENTERS
            )
            if not other_defined_centers:
                return Types.MENTAL_PROJECTOR

        # Not identified.
        raise ValueError("Type cannot be identified.")

    @property
    def variable_activations(self) -> dict[str, Activation]:
        """Return the Activations for the 4 Variables.

        See `VARIABLE_ORIENTATIONS`.
        """
        return {
            "pt": self.personality[Planets.SUN],
            "pb": self.personality[Planets.NORTH_NODE],
            "dt": self.design[Planets.SUN],
            "db": self.design[Planets.NORTH_NODE],
        }
        # TODO: Is this really better?
        # return {
        #     "pt": self._imprints[Motivations.get_imprint()][Motivations.get_planet()],
        #     "pb": self._imprints[Perspectives.get_imprint()][Perspectives.get_planet()],
        #     "dt": self._imprints[Determinations.get_imprint()][Determinations.get_planet()],
        #     "db": self._imprints[Environments.get_imprint()][Environments.get_planet()],
        # }

    @property
    def variable_orientations(self) -> VariableOrientations:
        """Return the 4 Variables Orientations (i.e. P-- D--)."""
        return VariableOrientations.get(
            pt=self.motivation.orientation,
            pb=self.perspective.orientation,
            dt=self.determination.orientation,
            db=self.environment.orientation,
        )

    # CONCRETE VARIABLES ---------------------------------------------------------------------------

    @property
    def determination(self) -> Determinations:
        """Return the Determination (Design Sun Color, top-left Variable)."""
        activation = self.variable_activations["dt"]
        return Determinations.get_by_color_tone(activation.color, activation.tone)

    @property
    def cognition(self) -> Cognitions:
        """Return the Cognition (Design Sun Tone, top-left Variable)."""
        # TODO
        # tone = self.design[PLANETS.SUN].tone
        tone = self.variable_activations["dt"].tone
        return Cognitions(tone.num)

    @property
    def environment(self) -> Environments:
        """Return the Environment (Design North Node Color, bottom-left Variable)."""
        activation = self.variable_activations["db"]
        return Environments.get_by_color_tone(activation.color, activation.tone)

    @property
    def perspective(self) -> Perspectives:
        """Return the Perspective (Personality North Node Color, bottom-right Variable)."""
        # TODO
        # color = self.personality[PLANETS.NORTH_NODE].color
        color = self.variable_activations["pb"].color
        return Perspectives(color.num)

    @property
    def motivation(self) -> Motivations:
        """Return the Motivation (Personality Sun Color, top-right Variable)."""
        # TODO
        # color = self.personality[PLANETS.SUN].color
        color = self.variable_activations["pt"].color
        return Motivations(color.num)

    @property
    def sense(self) -> Senses:
        """Return the Sense (Personality Sun Tone, top-right Variable)."""
        # TODO
        # tone = self.personality[PLANETS.SUN].tone
        tone = self.variable_activations["pt"].tone
        return Senses(tone.num)

    # BOOL TESTS -----------------------------------------------------------------------------------

    def has_any_center(self, centers: Iterable[Centers]) -> bool:
        """Return whether this Chart has any of the given Centers Defined."""
        return any(self.has_center(center) for center in centers)

    def has_any_channel(self, channels: Iterable[Channels]) -> bool:
        """Return whether this Chart has any of the given Channels Defined."""
        return any(self.has_channel(channel) for channel in channels)

    def has_center(self, center: Centers) -> bool:
        """Return whether this Chart has the given Center Defined."""
        return center in self.centers

    def has_channel(self, channel: Channels) -> bool:
        """Return whether this Chart has the given Channel Defined."""
        return channel in self.channels

    def is_connected(self, center: Centers, target_centers: Iterable[Centers]) -> bool:
        """
        Return whether there's a direct or indirect connection between the given Center and any of
        the target Centers.
        """
        # If a Center is Undefined, it has no Defined Channel, and therefore no connection.
        if center not in self.centers:
            return False

        # Filter out Undefined Centers.
        targets = [center for center in target_centers if center in self.centers]
        if not targets:
            return False

        # Find which Definition contains the Center.
        for definition in self.definitions():
            if center in definition:
                # Check if any target Center is in the same Definition.
                return any((target in definition) for target in targets)

        return False

    def has_motor(self) -> bool:
        """Return whether there's 1+ Defined Motor Center."""
        return self.has_any_center(MOTOR_CENTERS)

    def has_motor_to(self, center: Centers) -> bool:
        """Return whether the given Center if connected to any Defined Motor Center."""
        defined_motor_centers = (center for center in MOTOR_CENTERS if center in self.centers)
        return self.is_connected(center, defined_motor_centers)

    # HELPERS --------------------------------------------------------------------------------------

    @property
    def line_counts(self) -> tuple[int]:
        """Return stats for each Line."""
        stats = {i: 0 for i in range(1, NUM_LINES+1)}
        for imprint in (self.design, self.personality):
            for activation in imprint.activations.values():
                if activation.line is not None:
                    line = activation.line.num
                    stats[line] += 1
        return stats

    @property
    def num_centers(self) -> int:
        """Return the number of Defined Centers."""
        return len(self.centers)

    @property
    def num_channels(self) -> int:
        """Return the number of Defined Channels."""
        return len(self.channels)

    @property
    def num_definitions(self) -> int:
        """Return the number of Definitions."""
        return len(self.definitions)

    @property
    def num_gates(self) -> int:
        """Return the number of Activated Gates."""
        return len(self.gates)

    # TODO
    # FOR TRANSITS:
    # - Num Activated Gates for a Center.
    # - Num Activated Gates pointing toward a Center.

    # EXPORT ---------------------------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a dict representation of this Chart."""
        return {
            "personality": self.personality.to_dict(),
            "design": self.design.to_dict(),
            **{prop: getattr(self, prop) for prop in self.PROPS},
        }

    def to_light_model(self) -> ChartLightModel:
        """Capture current computed state as an immutable model."""
        props = {prop: getattr(self, prop) for prop in self.PROPS}
        props["variable_activations"] = {
            key: activation.to_light_model()
            for key, activation in self.variable_activations.items()
        }
        return ChartLightModel(**props)

    def to_model(self) -> ChartModel:
        """Capture current computed state as an immutable model."""
        return ChartModel(
            personality=self.personality.to_model(),
            design=self.design.to_model(),
            **{
                field.name: getattr(self, field.name)
                for field in dataclasses.fields(self.to_light_model())
            },
        )

    # DISPLAY --------------------------------------------------------------------------------------

    def print(self) -> None:
        ARROWS = {"LEFT": "⬅", "RIGHT": "⮕", "UP": "▲", "DOWN": "▼"}

        print()
        print_h2(self.short_description)

        print()
        print_kv("Birth Date ", format_datetime(self.personality.dt))
        print_kv("Design Date", format_datetime(self.design.dt))

        print()
        print_kv("Profile", self.profile.full_name)
        print_kv("Authority", self.authority.full_name)
        print_kv("Type", self.type.full_name)
        print_kv("Strategy", self.strategy.full_name, indent=1)
        print_kv("Signature", self.signature.full_name, indent=1)
        print_kv("Not-Self Theme", self.not_self_theme.full_name, indent=1)

        print()
        print_kv("Cross", self.cross.full_name)
        print_kv("Geometry", self.geometry.full_name)
        print_kv("Destiny", self.destiny.full_name)

        # Lists.
        print()
        props = ("centers", "channels", "gates", "channel_types", "circuit_groups", "circuits")
        for prop in props:
            title = prop.replace("_", " ").title()
            items = [item.full_name for item in getattr(self, prop)]
            print_num_list(title, items)

        # Definitions.
        print()
        print_h2("Definitions:")
        print_kv("Definition Type", self.definition_type.full_name, indent=1)
        items = [
            ", ".join(str(definition_type) for definition_type in definition)
            for definition in self.definitions
        ]
        print_num_list(None, items)

        # Activations.
        print()
        table = [ ["Planet", "Design", "Personality"] ]
        for planet in self.design.activations.keys():
            table.append([
                str(planet),
                str(self.design.activations[planet]),
                str(self.personality.activations[planet]),
            ])
        print_h2("Activations:")
        print_table(table, formats=[None, ">w", ">w"])

        # Variables.
        print()
        print_h2("Variables:", end=" ")
        print_value(self.variables)

        # Variables: Activations.
        variable_activations = {}
        for key, a in self.variable_activations.items():
            arrow = ARROWS[self.variable_orientations[key]._key]
            variable_activations[key] = f"{arrow}  {a.color}.{a.tone}.{a.base}"
        table = [
            [variable_activations["dt"], variable_activations["pt"]],
            [variable_activations["db"], variable_activations["pb"]],
        ]
        print_table(table, header_rows=0, header_cols=0, formats=[">w", ">w"])

        # Variables: Named.
        print()
        print_kv("Determination", self.determination)
        print_kv("Cognition", self.cognition)
        print_kv("Environment", self.environment)
        print_kv("Perspective", self.perspective)
        print_kv("Motivation", self.motivation)
        print_kv("Sense", self.sense)

        print()
