"""Helper functions for unhinged-units: `compare` and `random_conversion`.

Both helpers auto-discover the set of "fun" units by parsing
`pint/unhinged_en.txt` at import time — so adding a new unit to that file
automatically makes it a candidate here.
"""

from __future__ import annotations

import pathlib
import random
import re
from functools import cache

from pint import UnitRegistry
from pint.errors import DimensionalityError

__all__ = ["compare", "random_conversion", "fun_unit_names"]


# Path to the definition file that lists every unhinged unit.
_UNHINGED_DEFS_PATH = (
    pathlib.Path(__file__).resolve().parent.parent / "pint" / "unhinged_en.txt"
)

# Match the canonical name at the start of each unit-definition line.
# Accepts identifiers like `banana_length`, `t_rex_bite`, `light_in_vacuum_...`.
_DEF_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=")


@cache
def fun_unit_names() -> tuple[str, ...]:
    """Return the canonical names of every unit defined in unhinged_en.txt.

    Skips @alias / @import / @system lines and comments.
    """
    text = _UNHINGED_DEFS_PATH.read_text(encoding="utf-8")
    lines = (line.split("#", 1)[0].strip() for line in text.splitlines())
    # Exclude @-directives (@alias, @import, etc.) and blank lines.
    matches = (
        _DEF_LINE.match(line)
        for line in lines
        if line and not line.startswith("@")
    )
    return tuple(m.group(1) for m in matches if m is not None)


def _candidates_for(quantity, ureg: UnitRegistry) -> list[tuple[str, float]]:
    """Return [(unit_name, magnitude)] for every fun unit that shares `quantity`'s dimension.

    Uses a generator + try/except because Pint raises on dimensionality mismatch
    and that's cheaper than pre-computing every unit's dimensionality.
    """
    def _try(name: str) -> tuple[str, float] | None:
        try:
            return name, quantity.to(name).magnitude
        except (DimensionalityError, Exception):  # noqa: BLE001
            return None

    results = (_try(name) for name in fun_unit_names())
    return [r for r in results if r is not None]


def compare(quantity, ureg: UnitRegistry | None = None, n: int = 5) -> str:
    """Explain `quantity` in terms of several absurd units that share its dimension.

    Parameters
    ----------
    quantity : pint.Quantity
        The value to explain.
    ureg : pint.UnitRegistry, optional
        Registry to use. Defaults to the module-level `ureg`.
    n : int, default 5
        Maximum number of fun units to include.

    Returns
    -------
    str
        A human-readable multi-line string.
    """
    if ureg is None:
        from . import ureg as _default_ureg
        ureg = _default_ureg

    candidates = _candidates_for(quantity, ureg)
    if not candidates:
        return f"{quantity:~P} is dimensionally uncharted territory. No fun units match."

    # Prefer magnitudes in a "grokkable" range (0.1 to 10_000), sorted by that
    # preference, then by magnitude closest to 1.
    def _score(item: tuple[str, float]) -> tuple[int, float]:
        _, mag = item
        in_range = 0 if 0.1 <= abs(mag) <= 10_000 else 1
        return in_range, abs(abs(mag) - 1)

    top = sorted(candidates, key=_score)[:n]
    header = f"{quantity:~P} is approximately:"
    body = "\n".join(f"  {mag:>12.3f}  {name}" for name, mag in top)
    return f"{header}\n{body}"


def random_conversion(quantity, ureg: UnitRegistry | None = None) -> str:
    """Pick one random fun unit matching `quantity`'s dimension and return the conversion."""
    if ureg is None:
        from . import ureg as _default_ureg
        ureg = _default_ureg

    candidates = _candidates_for(quantity, ureg)
    if not candidates:
        return f"{quantity:~P}: no fun units match this dimension."

    name, mag = random.choice(candidates)
    return f"{quantity:~P} = {mag:.3f} {name}"
