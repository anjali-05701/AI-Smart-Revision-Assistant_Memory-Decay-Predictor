"""
Quiz Evaluator — simple keyword check + manual override for viva demo.
You can type y/n for correct; optional auto-check uses a few keywords from the concept.
"""


def simple_auto_score(student_answer: str, concept: str) -> bool:
    """Very simple heuristic: answer mentions part of concept name (demo only)."""
    a = student_answer.lower().strip()
    parts = [p for p in concept.lower().replace("-", " ").split() if len(p) > 2]
    if not parts:
        return len(a) > 5
    return any(p in a for p in parts)


def explain_feedback(was_correct: bool) -> str:
    if was_correct:
        return "Correct — memory reinforced. Next revision scheduled after more days (adaptive)."
    return "Incorrect — next revision scheduled sooner (tomorrow) to strengthen memory."
