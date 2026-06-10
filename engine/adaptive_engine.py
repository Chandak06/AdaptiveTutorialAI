from models.learning_state import learning_state

def get_difficulty(topic):

    confidence = learning_state["topics"][topic]["confidence"]

    if confidence <= 25:
        return "Beginner"

    elif confidence <= 50:
        return "Intermediate"

    elif confidence <= 75:
        return "Advanced"

    return "Expert"