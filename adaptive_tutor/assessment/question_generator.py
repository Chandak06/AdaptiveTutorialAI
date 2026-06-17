from rag.question_retriever import QuestionRetriever


retriever = QuestionRetriever()


# =====================================================
# Standard Question Generation
# =====================================================

def build_question_prompt(
    topic,
    level,
    context,
):
    """
    Generate normal adaptive questions.
    """

    related_questions = retriever.build_context(
        topic,
        k=5,
    )

    return f"""
You are an expert adaptive tutor.

Topic:
{topic}

Bloom Level:
{level}

Learning Context:
{context}

Previously Generated Questions:
{related_questions}

Generate:

1 MCQ
1 True/False
1 Short Answer

Rules:

- Questions must be unique.
- Questions must not be copied from context.
- Questions should match the Bloom level.
- MCQ must contain exactly 4 options.
- Include answer key.
- Include explanation.

Return STRICT JSON:

{{
    "mcq": {{
        "question": "",
        "options": {{
            "A": "",
            "B": "",
            "C": "",
            "D": ""
        }},
        "answer": "",
        "explanation": ""
    }},
    "true_false": {{
        "question": "",
        "answer": "",
        "explanation": ""
    }},
    "short_answer": {{
        "question": "",
        "answer": "",
        "explanation": ""
    }}
}}
"""


# =====================================================
# Hard Question Generation
# =====================================================

def build_hard_question_prompt(
    topic,
    level,
    context,
):
    """
    Generate harder questions using RAG.
    """

    hard_context = (
        retriever.build_hard_question_context(
            topic,
            k=5,
        )
    )

    return f"""
You are an expert university examiner.

Topic:
{topic}

Bloom Level:
{level}

Learning Context:
{context}

Previous Hard Questions:
{hard_context}

Generate:

1 Hard MCQ
1 Problem Solving Question
1 Descriptive Question

Requirements:

- Multi-step reasoning
- Analytical thinking
- Scenario based
- Difficult distractors
- Not copied from context

Include answers and explanations.

Return STRICT JSON.
"""


# =====================================================
# Expert Question Generation
# =====================================================

def build_expert_question_prompt(
    topic,
    context,
):
    """
    Generate expert-level questions.
    """

    expert_context = (
        retriever.build_expert_question_context(
            topic,
            k=5,
        )
    )

    return f"""
You are creating questions for top-tier CS students.

Topic:
{topic}

Context:
{context}

Previous Expert Questions:
{expert_context}

Generate:

1 Expert MCQ
1 Expert Problem Solving Question
1 Expert Reasoning Question

Requirements:

- Deep reasoning
- Evaluation
- Synthesis
- Cross-topic thinking
- Interview quality

Include answers and explanations.

Return STRICT JSON.
"""


# =====================================================
# Distractor Generator
# =====================================================

def build_distractor_prompt(
    question,
    correct_answer,
):
    """
    Generate confusing MCQ options.
    """

    return f"""
Question:
{question}

Correct Answer:
{correct_answer}

Generate 3 highly confusing distractors.

Requirements:

- Technically plausible
- Similar length to answer
- Common misconception based
- Not obviously incorrect

Return STRICT JSON:

{{
    "A": "",
    "B": "",
    "C": "",
    "D": ""
}}

Mark which option is correct.
"""


# =====================================================
# Ranking Agent Prompt
# =====================================================

def build_ranking_prompt(
    question,
):
    """
    Rank question difficulty.
    """

    return f"""
Analyze the question.

Question:
{question}

Return:

1. Bloom Level
2. Difficulty Score (1-100)
3. Complexity Score (1-100)
4. Misconception Potential (1-100)
5. Final Difficulty

Difficulty Categories:

Easy
Medium
Hard
Expert

Return STRICT JSON:

{{
    "bloom_level": "",
    "difficulty_score": 0,
    "complexity_score": 0,
    "misconception_score": 0,
    "difficulty": ""
}}
"""