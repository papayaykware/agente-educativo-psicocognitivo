def next_review_interval(score: float):
    if score < 0.5:
        return 1
    if score < 0.8:
        return 3
    return 7
