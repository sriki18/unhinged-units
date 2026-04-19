"""Smoke tests for the unhinged-units package.

These verify:
  1. Every unit in unhinged_en.txt loads without error.
  2. A handful of conversions produce the expected magnitudes.
  3. `compare` and `random_conversion` work end-to-end.
  4. Pint's own behaviour still works (fork hasn't broken upstream).
"""

from __future__ import annotations

import math

import pytest

from unhinged_units import Q_, compare, random_conversion, ureg
from unhinged_units.helpers import fun_unit_names


# ---------------------------------------------------------------------------
# Every unit in the definition file should be parseable.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name", fun_unit_names())
def test_every_fun_unit_loads(name: str) -> None:
    ureg.Unit(name)


# ---------------------------------------------------------------------------
# Spot-check conversions — magnitudes should match the documented factors.
# ---------------------------------------------------------------------------

CONVERSION_CASES = [
    # (input_qty, input_unit, target_unit, expected_magnitude, rel_tol)
    (1, "banana_length", "centimeter", 17.78, 1e-6),
    (1, "football_field", "meter", 91.44, 1e-6),
    (1, "eiffel_tower", "meter", 330.0, 1e-6),
    (1, "blue_whale", "kilogram", 150_000.0, 1e-6),
    (1, "banana_mass", "gram", 118.0, 1e-6),
    (1, "pomodoro", "minute", 25.0, 1e-6),
    (1, "weekend", "day", 2.0, 1e-6),
    (1, "dog_year", "year", 7.0, 1e-3),  # folk formula, 7*365.25 / 365.25
    (1, "tweet", "byte", 280.0, 1e-6),
    (1, "banana_calorie", "kcal", 105.0, 1e-6),
    (1, "usain_bolt", "meter/second", 10.44, 1e-6),
]


@pytest.mark.parametrize("value,src,dst,expected,tol", CONVERSION_CASES)
def test_conversions(value, src, dst, expected, tol) -> None:
    result = Q_(value, src).to(dst).magnitude
    assert math.isclose(result, expected, rel_tol=tol), f"{value} {src} -> {dst}"


# ---------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------

def test_compare_returns_string_with_fun_units() -> None:
    out = compare(Q_(10, "km"))
    assert "10 km" in out
    # At least one known length unit should appear in the output.
    assert any(
        name in out
        for name in ("eiffel_tower", "football_field", "banana_length")
    )


def test_compare_with_no_matching_units() -> None:
    # Luminous intensity has no fun units defined.
    out = compare(Q_(1, "candela"))
    assert "dimensionally uncharted" in out


def test_random_conversion_returns_a_fun_unit() -> None:
    result = random_conversion(Q_(1, "mile"))
    # Output format: "1 mi = <magnitude> <unit_name>"
    assert "=" in result
    unit_name = result.rsplit(" ", 1)[-1]
    assert unit_name in fun_unit_names()


# ---------------------------------------------------------------------------
# Upstream Pint sanity: we haven't broken the standard catalog.
# ---------------------------------------------------------------------------

def test_pint_still_works() -> None:
    assert math.isclose(Q_(1, "mile").to("meter").magnitude, 1609.344, rel_tol=1e-6)
    assert math.isclose(Q_(1, "pound").to("gram").magnitude, 453.59237, rel_tol=1e-6)
