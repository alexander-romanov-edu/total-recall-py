import random


def mask_word(word: str) -> str:
    n = max(1, len(word) // 3)
    indices = random.sample(range(len(word)), n)

    chars = list(word)
    for i in indices:
        chars[i] = "_"

    return "".join(chars)
