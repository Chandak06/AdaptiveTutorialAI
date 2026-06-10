import random

QUESTION_TYPES = [
    "mcq",
    "true_false",
    "one_liner",
    "fill_blank"
]

def get_random_question_type():

    return random.choice(
        QUESTION_TYPES
    )
