"""Box selection logic.

This module is plain Python on purpose (no Django imports) so it can be
unit-tested quickly and reasoned about on its own.

Approach
--------
1. Reject invalid input (empty order, non-positive sizes/weights/quantities).
2. For every candidate box:
   a. Total weight must be <= box max weight.
   b. Total item volume must be <= box volume (cheap early rejection).
   c. Items must actually pack. We use a guillotine packer that tries all 6
      orientations of each item, largest item first. If it reports "fits",
      the items genuinely fit (no overlaps). It is a heuristic, so it can say
      "doesn't fit" for a tight arrangement that a perfect packer would find.
      That trade-off is deliberate: a false "fits" ships a box that is too
      small; a false "doesn't fit" only costs a slightly bigger box.
3. Among boxes that work, pick the cheapest. Ties -> smaller volume, then
   lower max weight, then name (so the result is deterministic).
"""
from dataclasses import dataclass
from itertools import permutations
from typing import List, Optional, Sequence, Tuple

EPS = 1e-9


class InvalidOrderError(ValueError):
    """Raised when the order or a box contains unusable data."""


@dataclass(frozen=True)
class ItemSpec:
    name: str
    length: float
    width: float
    height: float
    weight: float
    quantity: int = 1


@dataclass(frozen=True)
class BoxSpec:
    id: Optional[int]
    name: str
    length: float
    width: float
    height: float
    max_weight: float
    cost: float

    @property
    def volume(self) -> float:
        return self.length * self.width * self.height


@dataclass
class Recommendation:
    box: Optional[BoxSpec]
    total_weight: float
    total_volume: float
    reason: str
    rejected: List[Tuple[str, str]]  # (box name, why it was rejected)


def _validate_items(items: Sequence[ItemSpec]) -> None:
    if not items:
        raise InvalidOrderError("Order has no items.")
    for it in items:
        if it.quantity < 1:
            raise InvalidOrderError(f"{it.name}: quantity must be at least 1.")
        if min(it.length, it.width, it.height) <= 0:
            raise InvalidOrderError(f"{it.name}: dimensions must be positive.")
        if it.weight < 0:
            raise InvalidOrderError(f"{it.name}: weight cannot be negative.")


def _validate_box(box: BoxSpec) -> None:
    if min(box.length, box.width, box.height) <= 0:
        raise InvalidOrderError(f"Box {box.name}: dimensions must be positive.")
    if box.max_weight <= 0:
        raise InvalidOrderError(f"Box {box.name}: max weight must be positive.")
    if box.cost < 0:
        raise InvalidOrderError(f"Box {box.name}: cost cannot be negative.")


def _expand(items: Sequence[ItemSpec]) -> List[Tuple[float, float, float]]:
    """One (l, w, h) tuple per physical unit."""
    units = []
    for it in items:
        units.extend([(it.length, it.width, it.height)] * it.quantity)
    return units


MAX_SEARCH_NODES = 20000


def can_pack(units: Sequence[Tuple[float, float, float]],
             box_dims: Tuple[float, float, float]) -> bool:
    """Guillotine packing with bounded backtracking.

    Keeps a list of empty rectangular spaces. Items are placed biggest first.
    For each item we try every free space and every distinct orientation; the
    item goes in a corner of the space and the leftover is split into up to
    three non-overlapping spaces. If a choice leads to a dead end we backtrack.

    The search is capped at MAX_SEARCH_NODES. Running out of budget returns
    False, so a True answer is always a real, overlap-free packing.
    """
    ordered = sorted(units, key=lambda u: u[0] * u[1] * u[2], reverse=True)
    budget = [MAX_SEARCH_NODES]

    def place(i: int, free: List[Tuple[float, float, float]]) -> bool:
        if i == len(ordered):
            return True
        budget[0] -= 1
        if budget[0] < 0:
            return False
        for idx in sorted(range(len(free)),
                          key=lambda k: free[k][0] * free[k][1] * free[k][2]):
            sl, sw, sh = free[idx]
            for (a, b, c) in sorted(set(permutations(ordered[i]))):
                if a <= sl + EPS and b <= sw + EPS and c <= sh + EPS:
                    rest = free[:idx] + free[idx + 1:]
                    if sl - a > EPS:
                        rest.append((sl - a, sw, sh))
                    if sw - b > EPS:
                        rest.append((a, sw - b, sh))
                    if sh - c > EPS:
                        rest.append((a, b, sh - c))
                    if place(i + 1, rest):
                        return True
        return False

    return place(0, [tuple(box_dims)])


def recommend_box(items: Sequence[ItemSpec],
                  boxes: Sequence[BoxSpec]) -> Recommendation:
    _validate_items(items)
    for b in boxes:
        _validate_box(b)

    total_weight = sum(i.weight * i.quantity for i in items)
    units = _expand(items)
    total_volume = sum(l * w * h for (l, w, h) in units)

    rejected: List[Tuple[str, str]] = []
    candidates: List[BoxSpec] = []

    for box in boxes:
        if total_weight > box.max_weight + EPS:
            rejected.append((box.name, "over weight limit"))
        elif total_volume > box.volume + EPS:
            rejected.append((box.name, "not enough volume"))
        elif not can_pack(units, (box.length, box.width, box.height)):
            rejected.append((box.name, "items do not fit"))
        else:
            candidates.append(box)

    if not candidates:
        return Recommendation(None, total_weight, total_volume,
                              "No available box can hold this order.", rejected)

    best = min(candidates,
               key=lambda b: (b.cost, b.volume, b.max_weight, b.name))
    return Recommendation(best, total_weight, total_volume,
                          "Cheapest box that fits the weight and dimensions.",
                          rejected)
