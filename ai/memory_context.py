from models.learning_state import learning_state

def add_to_history(role, content):

    learning_state["conversation_history"].append({

        "role": role,

        "content": content
    })


def get_recent_history(limit=5):

    return learning_state["conversation_history"][-limit:]