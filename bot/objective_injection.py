"""Intermittent USER_OBJECTIVE injection (stateless per request)."""


def omit_custom_objective(
    resolved_objective: str,
    default_objective: str,
    injection_probability: float,
    roll: float,
) -> bool:
    """
    Return True if the server should pass default_objective so # OBJECTIVE # is omitted.

    :param resolved_objective: Objective from user config (may equal default_objective).
    :param default_objective: Sentinel value that suppresses the objective block.
    :param injection_probability: P(include custom objective) in [0, 1].
    :param roll: Sample from Uniform(0, 1) (include custom when roll < probability).
    """
    if resolved_objective.strip() == default_objective.strip():
        return False
    p = max(0.0, min(1.0, injection_probability))
    return roll >= p
