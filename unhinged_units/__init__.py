"""
unhinged_units
~~~~~~~~~~~~~~

Serious unit conversion for deeply unserious people.

This package is a thin wrapper over a fork of Pint. All standard Pint
operations work unchanged — we just also ship bananas, blue whales,
and Roombas.

Example
-------
>>> from unhinged_units import Q_
>>> Q_(1, "eiffel_tower").to("banana_length")
<Quantity(1856.0..., 'banana_length')>
"""

from __future__ import annotations

from pint import UnitRegistry

from .helpers import compare, random_conversion

__all__ = [
    "ureg",
    "Q_",
    "Unit",
    "UnitRegistry",
    "compare",
    "random_conversion",
]


#: The default unhinged registry. Loads Pint's default_en.txt, which ends
#: with `@import unhinged_en.txt` — so the fun units come along for free.
ureg: UnitRegistry = UnitRegistry()

#: Quantity constructor bound to the default unhinged registry.
Q_ = ureg.Quantity

#: Unit constructor bound to the default unhinged registry.
Unit = ureg.Unit
