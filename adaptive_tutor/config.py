from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

SESSION_PATH = BASE_DIR / "storage" / "session_data.json"

DEFAULT_MODEL_NAME = os.getenv(
    "ADAPTIVE_TUTOR_MODEL",
    "qwen3:4b"
)

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://127.0.0.1:11434"
)

OLLAMA_TIMEOUT_SECONDS = int(
    os.getenv(
        "OLLAMA_TIMEOUT_SECONDS",
        "45"
    )
)

LLM_MAX_RETRIES = int(
    os.getenv(
        "ADAPTIVE_TUTOR_LLM_RETRIES",
        "3"
    )
)

MAX_HISTORY = 20

MASTERY_ACCURACY_THRESHOLD = 80.0

MIN_MASTERY_ATTEMPTS = 3

REVISION_COOLDOWN_TURNS = 2

QUESTION_TYPE_LADDER = {
    0: ["mcq", "true_false", "fill_blank"],
    1: ["mcq", "fill_blank", "short_answer"],
    2: ["fill_blank", "short_answer"],
    3: ["one_liner", "short_answer"],
    4: ["scenario", "one_liner"],
    5: ["coding", "scenario"],
    6: ["long_form", "scenario"],
    7: ["exam_style", "long_form"],
    8: ["problem_solving", "coding"],
    9: ["expert_reasoning", "problem_solving"],
}

QUESTION_LABELS = {
    "mcq": "MCQ",
    "true_false": "True/False",
    "fill_blank": "Fill in the blank",
    "short_answer": "Short answer",
    "one_liner": "One-line reasoning",
    "scenario": "Scenario-based",
    "coding": "Coding",
    "long_form": "Long descriptive answer",
    "exam_style": "University exam style",
    "problem_solving": "Problem solving",
    "expert_reasoning": "Expert reasoning",
}

VECTOR_DB_PATH = BASE_DIR / "storage" / "vector_db"

QUESTION_MEMORY_PATH = (
    BASE_DIR / "storage" / "question_memory"
)

QUESTION_MEMORY_COLLECTION = "adaptive_questions"

QUESTION_MEMORY_TOP_K = 5

QUESTION_MEMORY_SIMILARITY_THRESHOLD = 0.75

ENABLE_DIFFICULTY_GENERATION = True

HARD_QUESTION_COUNT = 2

HARD_CONFIDENCE_THRESHOLD = 75

EXPERT_CONFIDENCE_THRESHOLD = 90

ENABLE_SMART_DISTRACTORS = True

DISTRACTOR_COUNT = 3

ENABLE_QUESTION_RANKING = True

RANKING_WEIGHTS = {
    "bloom": 0.40,
    "complexity": 0.30,
    "rarity": 0.15,
    "misconception": 0.15,
}

ENABLE_MISCONCEPTION_TRACKING = True

MAX_MISCONCEPTIONS_PER_TOPIC = 20

MISCONCEPTION_CONFIDENCE_THRESHOLD = 60