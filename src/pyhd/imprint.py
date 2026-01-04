"""
Imprint Layer: Activation for each planet at a given time.
"""

from datetime import datetime
from types import MappingProxyType
from typing import ItemsView

from .activation import Activation
from .constants import Gates, Lines, Planets
from .models import ImprintModel

# TODO: from .utils.data import filter_list


class Imprint:
    """Activation for each planet at a given time."""

    def __init__(self, dt: datetime) -> None:
        self.dt = dt
        self.activations: dict[Planets, Activation] = {}

        for planet in Planets:
            self.activations[planet] = Activation(planet, dt)

    def __getitem__(self, planet: Planets) -> Activation:
        """Return the Activation of the given planet."""
        return self.activations[planet]

    def __contains__(self, planet: Planets) -> bool:
        """Return whether the given planet is in the list of Activations."""
        return planet in self.activations

    def __len__(self) -> int:
        """Return the number of Activations."""
        return len(self.activations)

    def __iter__(self):
        """Iterate over Activations."""
        return iter(self.activations)

    @property
    def line(self) -> Lines:
        """Return the main Line (i.e. from Sun)."""
        return self.activations[Planets.SUN].line

    @property
    def gates(self) -> tuple[Gates]:
        """Return the list of Gates from all Activations."""
        # Get the Gate of each Activation | unique | sort | tuple.
        return tuple(sorted({a.gate for a in self.activations.values()}))

    def items(self) -> ItemsView[Planets, Activation]:
        """Return items view (planet: activation)."""
        return self.activations.items()

    def keys(self) -> tuple[str]:
        return self.activations.keys()

    def values(self) -> tuple[Activation]:
        return self.activations.values()

    # EXPORT ---------------------------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a dict representation of this Imprint."""
        return {
            "dt": self.dt,
            "activations": {
                p: a.to_dict(exclude=["planet", "dt"]) for p, a in self.activations.items()
            },
        }

    def to_model(self) -> ImprintModel:
        """Capture current computed state as an immutable model."""
        return ImprintModel(
            dt=self.dt,
            activations=MappingProxyType({
                p: a.to_light_model() for p, a in self.activations.items()
            }),
        )
