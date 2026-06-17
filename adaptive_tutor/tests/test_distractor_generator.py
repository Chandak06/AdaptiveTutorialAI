import json

from adaptive_tutor.assessment.distractor_generator import (
    DistractorGenerator,
)


def test_generate_returns_response():

    generator = DistractorGenerator()

    result = generator.generate(
        question="What does DFS stand for?",
        answer="Depth First Search",
    )

    assert result is not None
    assert isinstance(result, str)


def test_generate_json_response():

    generator = DistractorGenerator()

    result = generator.generate(
        question="What does BFS stand for?",
        answer="Breadth First Search",
    )

    try:

        payload = json.loads(result)

        assert isinstance(
            payload,
            dict,
        )

    except Exception:

        assert False, (
            "Distractor generator "
            "did not return valid JSON."
        )


def test_contains_four_options():

    generator = DistractorGenerator()

    result = generator.generate(
        question="What is a Stack?",
        answer="LIFO",
    )

    payload = json.loads(result)

    assert len(payload) >= 4


def test_option_keys_exist():

    generator = DistractorGenerator()

    result = generator.generate(
        question="What is Queue?",
        answer="FIFO",
    )

    payload = json.loads(result)

    expected = {
        "A",
        "B",
        "C",
        "D",
    }

    assert expected.issubset(
        payload.keys()
    )