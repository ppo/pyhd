from dataclasses import dataclass
from datetime import datetime
from typing import Mapping

from .constants import (
    Authorities,
    Bases,
    Centers,
    Channels,
    ChannelTypes,
    CircuitGroups,
    Circuits,
    Cognitions,
    Colors,
    Crosses,
    DefinitionTypes,
    Destinies,
    Determinations,
    Environments,
    Gates,
    Geometries,
    Lines,
    Motivations,
    NotSelfThemes,
    Perspectives,
    Planets,
    Profiles,
    Senses,
    Signatures,
    Strategies,
    Tones,
    Types,
    VariableOrientations,
)


@dataclass(frozen=True)
class ActivationLightModel:
    """Model class to freeze the state of `Activation` objects within `Imprint`."""
    longitude: float
    angle: float
    gate: Gates
    line: Lines
    color: Colors
    tone: Tones
    base: Bases
    color_percentage: float
    tone_percentage: float
    base_percentage: float
    # TODO: is_retrograde: bool


@dataclass(frozen=True)
class ActivationModel(ActivationLightModel):
    """Model class to freeze the state of `Activation` objects."""
    planet: Planets
    dt: datetime


@dataclass(frozen=True)
class ImprintModel:
    """Model class to freeze the state of `Imprint` objects."""
    dt: datetime
    activations: Mapping[Planets, ActivationModel]


@dataclass(frozen=True)
class ChartLightModel:
    """Model class to freeze the state of `Chart` objects, without the `Imprint`s."""
    authority: Authorities
    centers: tuple[Centers]
    channel_types: tuple[ChannelTypes]
    channels: tuple[Channels]
    circuit_groups: tuple[CircuitGroups]
    circuits: tuple[Circuits]
    creative_channels: tuple[Channels]
    cross: Crosses
    definition_type: DefinitionTypes
    definitions: tuple[set[Centers]]
    destiny: Destinies
    gates: tuple[Gates]
    geometry: Geometries
    not_self_theme: NotSelfThemes
    profile: Profiles
    signature: Signatures
    strategy: Strategies
    type: Types
    variables: VariableOrientations
    variable_activations: tuple[ActivationLightModel]

    determination: Determinations
    cognition: Cognitions
    environment: Environments
    perspective: Perspectives
    motivation: Motivations
    sense: Senses


@dataclass(frozen=True)
class ChartModel(ChartLightModel):
    """Model class to freeze the state of `Chart` objects."""
    personality: ImprintModel
    design: ImprintModel
