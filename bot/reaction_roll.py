"""Random message reaction sampling (stateless per message)."""


def should_add_random_reaction(probability: float, roll: float) -> bool:
    """
    Return True to add a reaction to this message.

    :param probability: Chance in [0, 1]; 0 disables.
    :param roll: Sample from Uniform(0, 1).
    """
    if probability <= 0:
        return False
    p = max(0.0, min(1.0, probability))
    return roll < p
