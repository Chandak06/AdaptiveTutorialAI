import random


QUESTION_TYPES = [
    "mcq",
    "true_false",
    "one_liner",
    "fill_blank"
]


def get_random_question_type(
    last_type=None
):

    available = QUESTION_TYPES.copy()

    if (
        last_type in available
        and len(available) > 1
    ):

        available.remove(last_type)

    return random.choice(available)
