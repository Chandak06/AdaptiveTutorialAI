from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BKTState:
    mastery: float = 0.2
    slip: float = 0.08
    guess: float = 0.22
    learn: float = 0.12


def bkt_update(state: BKTState, correct: bool) -> float:
    p_l = max(1e-6, min(1 - 1e-6, state.mastery))
    p_s = state.slip
    p_g = state.guess
    p_t = state.learn

    if correct:
        posterior = (p_l * (1 - p_s)) / (p_l * (1 - p_s) + (1 - p_l) * p_g)
    else:
        posterior = (p_l * p_s) / (p_l * p_s + (1 - p_l) * (1 - p_g))

    updated = posterior + (1 - posterior) * p_t
    return max(0.0, min(1.0, updated))
