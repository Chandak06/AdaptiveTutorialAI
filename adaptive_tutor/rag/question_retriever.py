from adaptive_tutor.rag.question_memory import QuestionMemory


class QuestionRetriever:

    def __init__(self):
        self.memory = QuestionMemory()

    # =====================================
    # Similar Questions
    # =====================================

    def get_related_questions(
        self,
        question: str,
        k: int = 5,
    ):
        return self.memory.retrieve(
            question,
            k=k,
        )

    # =====================================
    # Similar Questions With Scores
    # =====================================

    def get_related_questions_with_scores(
        self,
        question: str,
        k: int = 5,
    ):
        return self.memory.retrieve_with_scores(
            question,
            k=k,
        )

    # =====================================
    # Topic Questions
    # =====================================

    def get_topic_questions(
        self,
        topic: str,
        k: int = 10,
    ):
        return self.memory.retrieve_topic_questions(
            topic,
            k=k,
        )

    # =====================================
    # Hard Questions
    # =====================================

    def get_hard_questions(
        self,
        topic: str,
        k: int = 5,
    ):
        return self.memory.retrieve_hard_questions(
            topic,
            k=k,
        )

    # =====================================
    # Expert Questions
    # =====================================

    def get_expert_questions(
        self,
        topic: str,
        k: int = 5,
    ):
        return self.memory.retrieve_expert_questions(
            topic,
            k=k,
        )

    # =====================================
    # Build Context String
    # =====================================

    def build_context(
        self,
        query: str,
        k: int = 5,
    ) -> str:

        docs = self.get_related_questions(
            query,
            k=k,
        )

        return "\n\n".join(
            getattr(doc, "page_content", str(doc))
            for doc in docs
        )

    # =====================================
    # Hard Question Context
    # =====================================

    def build_hard_question_context(
        self,
        topic: str,
        k: int = 5,
    ) -> str:

        docs = self.get_hard_questions(
            topic,
            k=k,
        )

        return "\n\n".join(
            getattr(doc, "page_content", str(doc))
            for doc in docs
        )

    # =====================================
    # Expert Question Context
    # =====================================

    def build_expert_question_context(
        self,
        topic: str,
        k: int = 5,
    ) -> str:

        docs = self.get_expert_questions(
            topic,
            k=k,
        )

        return "\n\n".join(
            getattr(doc, "page_content", str(doc))
            for doc in docs
        )