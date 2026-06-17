from adaptive_tutor.rag.question_retriever import (
    QuestionRetriever,
)

from adaptive_tutor.llm.ollama_client import (
    OllamaClient,
)


class DifficultyAgent:

    def __init__(self):

        self.retriever = QuestionRetriever()
        self.llm = OllamaClient()

    def generate_hard_question(
        self,
        topic: str,
        question: str,
        context: str = "",
    ):

        related_questions = (
            self.retriever.build_context(
                question,
                k=5,
            )
        )

        prompt = f"""
You are an expert university examiner.

Topic:
{topic}

Current Question:
{question}

Learning Context:
{context}

Previous Similar Questions:
{related_questions}

Generate a significantly harder version.

Requirements:

- analytical
- scenario based
- multi-step reasoning
- difficult distractors
- higher bloom level
- not a paraphrase

Return JSON:

{{
    "question":"",
    "answer":"",
    "difficulty":"Hard"
}}
"""

        return self.llm._chat(
            [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

    def generate_expert_question(
        self,
        topic: str,
        question: str,
        context: str = "",
    ):

        expert_context = (
            self.retriever.build_expert_question_context(
                topic,
                k=5,
            )
        )

        prompt = f"""
You are creating a question for advanced students.

Topic:
{topic}

Current Question:
{question}

Learning Context:
{context}

Expert Question History:
{expert_context}

Generate an expert-level question.

Requirements:

- synthesis
- evaluation
- reasoning
- multiple concepts
- interview quality
- real-world tradeoffs
- edge cases

Return JSON:

{{
    "question":"",
    "answer":"",
    "difficulty":"Expert"
}}
"""

        return self.llm._chat(
            [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )