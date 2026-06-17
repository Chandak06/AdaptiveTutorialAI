import unittest

from adaptive_tutor.llm.parser import (
    JSONParseError,
    coerce_lesson_payload,
    parse_json_object,
)


class ParserTests(unittest.TestCase):
    def test_parse_json_object_extracts_fenced_json(self) -> None:
        raw_text = """```json
        {"message": "hi", "question": {"type": "mcq", "prompt": "Q", "options": ["a", "b", "c", "d"], "answer": "a", "rubric": []}}
        ```"""

        payload = parse_json_object(raw_text)

        self.assertEqual(payload["message"], "hi")

    def test_coerce_lesson_payload_rejects_wrong_question_type(self) -> None:
        request = {
            "question_type": "mcq",
            "concept_name": "Stack",
        }
        payload = {
            "message": "hello",
            "question": {
                "type": "true_false",
                "prompt": "Q",
                "options": [],
                "answer": "True",
                "rubric": [],
            },
        }

        with self.assertRaises(JSONParseError):
            coerce_lesson_payload(payload, request)


if __name__ == "__main__":
    unittest.main()
