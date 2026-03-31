"""
Rule-based question templates (simple NLP-style patterns).
"""


def generate_questions(concept: str) -> list:
    c = concept.strip()
    return [
        f"What is {c}?",
        f"Explain the concept of {c}.",
        f"Define {c}.",
        f"Why is {c} important?",
    ]


def pick_question(concept: str, index: int = 0) -> str:
    qs = generate_questions(concept)
    return qs[index % len(qs)]
