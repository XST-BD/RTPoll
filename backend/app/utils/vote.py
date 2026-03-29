def vote_percentages(
    votes: dict[str, int], option_ids: list[str],
) -> list[float]:

    total = sum(votes.values())
    if total == 0:
        return [0.0] * len(option_ids)
    
    return [
        round(votes.get(opt_id, 0) / total * 100, 1)
        for opt_id in option_ids
    ]