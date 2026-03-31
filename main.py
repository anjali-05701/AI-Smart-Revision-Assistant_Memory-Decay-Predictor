"""
AI Smart Revision Assistant (Memory Decay Predictor)
CLI: text input/output — no web app.

Agent cycle: Observe → Predict → Decide → Act → Learn
"""
import json
import os
import sys
from datetime import date, timedelta
from typing import Any, Dict, List

from data_store import add_concept, csv_path, load_study_data, save_study_data, update_row
from memory_model import memory_retention
from question_generator import pick_question
from quiz_evaluator import explain_feedback, simple_auto_score
from scheduler import days_between, needs_revision, parse_date

STATS_FILE = "stats.json"
TITLE = "AI Smart Revision Assistant (Memory Decay Predictor)"


def base_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def load_stats(path: str) -> Dict[str, Any]:
    if not os.path.isfile(path):
        return {
            "concepts_studied": 0,
            "revisions_completed": 0,
            "quiz_correct": 0,
            "quiz_attempts": 0,
        }
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_stats(path: str, stats: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


def current_retention_row(row: Dict[str, Any], today: date) -> float:
    last = parse_date(str(row["last_reviewed"]))
    d = days_between(last, today)
    return memory_retention(d, str(row.get("difficulty", "Medium")))


def list_revision_indices(df, today: date) -> List[int]:
    idx = []
    for i, row in df.iterrows():
        r = row.to_dict()
        if needs_revision(r, today):
            idx.append(int(i))
    return idx


def print_banner() -> None:
    print("\n" + "=" * 56)
    print(TITLE)
    print("=" * 56)


def menu() -> None:
    print(
        """
Choose an option:
  1  Log what you studied today (Knowledge Tracker)
  2  Show today's revision tasks (Predict + Decide)
  3  Take revision quiz on due concepts (Act + Learn)
  4  Show full study table + memory % (Observe)
  5  Performance summary
  6  Demo sample output (for report / screenshots)
  0  Exit
"""
    )


def option_add_concept(csv_p: str, stats_p: str, today: date) -> None:
    print("\n--- Log new study ---")
    topic = input("Topic (e.g. Machine Learning): ").strip()
    concept = input("Concept you studied (e.g. Regression): ").strip()
    if not concept:
        print("Concept cannot be empty.")
        return
    diff = input("Difficulty [Easy/Medium/Hard] (default Medium): ").strip() or "Medium"
    if diff not in ("Easy", "Medium", "Hard"):
        diff = "Medium"
    add_concept(csv_p, topic, concept, diff, today)
    st = load_stats(stats_p)
    st["concepts_studied"] = st.get("concepts_studied", 0) + 1
    save_stats(stats_p, st)
    print(f"\nSaved: [{topic}] {concept} ({diff}) on {today.isoformat()}")
    print("The agent will remind you to revise when predicted memory drops below 60%.")


def option_show_tasks(csv_p: str, today: date) -> None:
    df = load_study_data(csv_p)
    if df.empty:
        print("\nNo concepts yet. Use option 1 to log what you studied.")
        return
    due = list_revision_indices(df, today)
    print(f"\n--- Today's revision tasks ({today.isoformat()}) ---")
    if not due:
        print("No concepts below the 60% retention threshold today. Great job!")
        return
    for n, i in enumerate(due, 1):
        row = df.iloc[i]
        r = current_retention_row(row.to_dict(), today)
        q = pick_question(str(row["concept"]), n - 1)
        print(f"  {n}. [{row['topic']}] {row['concept']}  |  predicted retention: {r*100:.1f}%")
        print(f"      Question: {q}")
    print(f"\nTotal due today: {len(due)}")


def option_quiz(csv_p: str, stats_p: str, today: date) -> None:
    df = load_study_data(csv_p)
    if df.empty:
        print("\nNo data. Use option 1 first.")
        return
    due = list_revision_indices(df, today)
    if not due:
        print("\nNothing due for revision right now (memory above threshold).")
        return
    st = load_stats(stats_p)
    print("\n--- Revision quiz (one question per due concept) ---")
    for i in due:
        row = df.iloc[i]
        concept = str(row["concept"])
        q = pick_question(concept, i)
        print(f"\nTopic: {row['topic']}  |  Concept: {concept}")
        print(f"Q: {q}")
        ans = input("Your answer (short): ").strip()
        use_auto = input("Use auto-check? [y/n] (n = you say if correct): ").strip().lower()
        if use_auto == "y":
            ok = simple_auto_score(ans, concept)
            print(f"Auto-check result: {'CORRECT' if ok else 'WRONG'} (simple keyword demo)")
        else:
            ok = input("Was your answer correct? [y/n]: ").strip().lower() == "y"
        print(explain_feedback(ok))
        st["quiz_attempts"] = st.get("quiz_attempts", 0) + 1
        if ok:
            st["quiz_correct"] = st.get("quiz_correct", 0) + 1
            st["revisions_completed"] = st.get("revisions_completed", 0) + 1
            # Correct → next revision later: clear forced date; refresh last_reviewed
            nxt = (today + timedelta(days=5)).strftime("%Y-%m-%d")
            update_row(
                csv_p,
                i,
                {
                    "last_reviewed": today.strftime("%Y-%m-%d"),
                    "next_review_due": nxt,
                },
            )
            print("Scheduled: next forced check on or after", nxt, "(adaptive: longer interval).")
        else:
            # Wrong → revise sooner
            tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
            update_row(
                csv_p,
                i,
                {
                    "last_reviewed": today.strftime("%Y-%m-%d"),
                    "next_review_due": tomorrow,
                },
            )
            print("Scheduled: must revise again on or after", tomorrow, "(adaptive: sooner).")
    save_stats(stats_p, st)
    print("\nQuiz round finished.")


def option_table(csv_p: str, today: date) -> None:
    df = load_study_data(csv_p)
    if df.empty:
        print("\nNo rows in study_data.csv")
        return
    print(f"\n--- All concepts (memory since last review, as of {today}) ---")
    for i, row in df.iterrows():
        r = current_retention_row(row.to_dict(), today)
        due = "YES" if needs_revision(row.to_dict(), today) else "no"
        print(
            f"  {i+1}. {row['topic']} | {row['concept']} | {row['difficulty']} | "
            f"retention ~{r*100:.1f}% | revision due: {due}"
        )


def option_stats(csv_p: str, stats_p: str, today: date) -> None:
    st = load_stats(stats_p)
    df = load_study_data(csv_p)
    n = len(df)
    scores = [current_retention_row(df.iloc[i].to_dict(), today) for i in range(n)] if n else []
    avg_r = (sum(scores) / len(scores) * 100) if scores else 0.0
    print("\n--- Performance ---")
    print(f"  Concepts logged (all time): {st.get('concepts_studied', 0)}")
    print(f"  Rows in database now: {n}")
    print(f"  Revisions completed (quizzes): {st.get('revisions_completed', 0)}")
    print(f"  Quiz score: {st.get('quiz_correct', 0)} / {st.get('quiz_attempts', 0)} correct")
    print(f"  Average predicted retention (today): {avg_r:.1f}%")
    print("\nRule: retention < 60% → revision task; quiz result adapts next review date.")


def option_demo() -> None:
    print(
        """
--- Sample terminal output (copy for report) ---

AI Smart Revision Assistant (Memory Decay Predictor)

Today's revision tasks
  1. [Machine Learning] Regression  |  predicted retention: 52.0%
      Question: What is Regression?
  2. [Machine Learning] Overfitting  |  predicted retention: 48.0%
      Question: Explain the concept of Overfitting.

Performance
  Concepts Studied: 10
  Concepts Revised: 6
  Retention Score (avg): 78%

--- End sample ---
"""
    )


def main() -> None:
    bd = base_dir()
    csv_p = csv_path(bd)
    stats_p = os.path.join(bd, STATS_FILE)
    today = date.today()

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        option_demo()
        return

    print_banner()
    print("Tip: Tell the system what you studied (option 1); open daily and use 2–3.")
    while True:
        menu()
        choice = input("Enter choice: ").strip()
        if choice == "1":
            option_add_concept(csv_p, stats_p, today)
        elif choice == "2":
            option_show_tasks(csv_p, today)
        elif choice == "3":
            option_quiz(csv_p, stats_p, today)
        elif choice == "4":
            option_table(csv_p, today)
        elif choice == "5":
            option_stats(csv_p, stats_p, today)
        elif choice == "6":
            option_demo()
        elif choice == "0":
            print("Goodbye — revise smart!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
