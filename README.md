# AI Smart Revision Assistant (Memory Decay Predictor)

A **CLI-based Smart Revision Assistant** that helps you revise more effectively by:

- **Tracking** what you studied in a small local database (`study_data.csv`)
- **Predicting** forgetting using an exponential memory decay model \(R(t)=e^{-kt}\)
- **Scheduling** revision when predicted retention drops below **60%**
- **Adapting** the next revision date based on your quiz performance

This project is intentionally lightweight (no web app) so it can run anywhere with Python.

## What problem it solves

In day-to-day studying, it’s hard to remember **what** to revise and **when**. This tool uses a simple memory model + rule-based scheduling to generate a daily list of “due for revision” concepts and then reinforces learning with a quick quiz loop.

## Research gap (motivation)

Most existing study tools (such as flashcard apps or simple to-do lists) rely on **manual revision scheduling**. They typically do not predict *when* a learner is likely to forget information.

Human memory naturally follows a forgetting pattern where recall decreases over time if knowledge is not reinforced. However, many students revise randomly rather than at the optimal time.

While spaced repetition systems exist, they can involve complex interfaces and/or assumptions that are not transparent to the learner.

This project addresses this gap by implementing a **lightweight intelligent revision assistant** that predicts memory retention and schedules revision automatically using a simple and explainable memory decay model.

## Key features

- **Knowledge tracker**: log topic, concept, difficulty, and study date
- **Memory prediction**: estimates retention as a percentage from time since last review
- **Revision decision rule**: retention < **60%** → concept becomes “due”
- **Revision quiz**: one short question per due concept
- **Adaptive rescheduling**:
  - Correct → schedule next check **5 days later**
  - Incorrect → schedule next check **tomorrow**

## Setup (Windows / PowerShell)

### Prerequisites

- **Python 3.10+** installed from [python.org](https://www.python.org) (during install, check **Add Python to PATH**)

### Install

From this folder:

```text
pip install -r requirements.txt
```

## Run

```text
python main.py
```

You’ll see a menu:

- **1**: Log what you studied today
- **2**: Show today’s revision tasks (due concepts + predicted retention + a question)
- **3**: Take revision quiz on due concepts (updates schedule based on result)
- **4**: Show full study table + memory %
- **5**: Performance summary (quiz stats + average retention)
- **6**: Print demo output (useful for screenshots/report)

## Demo output (for report / screenshots)

```text
python main.py --demo
```

## Data files (what gets saved where)

- **`study_data.csv`**: your concept database (topic, concept, difficulty, dates)
- **`stats.json`**: counts for concepts studied, quiz attempts/correct, revisions completed

These files are read/written locally in the same folder as `main.py`.

## Project structure

| File | Role |
|------|------|
| `main.py` | CLI menu, user flow, quiz loop, stats summary |
| `data_store.py` | CSV creation/loading/saving + row updates |
| `memory_model.py` | Forgetting curve and difficulty→rate mapping |
| `scheduler.py` | “needs revision?” rule + date utilities |
| `question_generator.py` | Question templates and selection |
| `quiz_evaluator.py` | Manual scoring flow + optional simple auto-check |
| `study_data.csv` | Example stored concepts |
| `stats.json` | Example usage stats |

## How the “AI”/AIML concepts show up (course mapping)

- **Knowledge representation**: structured concept store in CSV, converted to records/rows
- **Modeling**: exponential decay model for retention prediction
- **Rule-based agent**: Observe → Predict → Decide → Act → Learn loop (implemented in CLI flow)
- **Adaptation**: next review date changes based on quiz outcome

## Memory prediction algorithm

The project uses the **Exponential Forgetting Curve Model**:

\[
R(t) = e^{-kt}
\]

Where:

- **\(R(t)\)**: retention probability (converted to a percentage in the CLI)
- **\(t\)**: time since last review (in days)
- **\(k\)**: forgetting rate (higher means faster forgetting)

Difficulty levels adjust the forgetting rate \(k\):

| Difficulty | Forgetting Rate (k) |
|-----------|----------------------|
| Easy | 0.20 |
| Medium | 0.30 |
| Hard | 0.45 |

Hard concepts decay faster than easy ones, so they become “due for revision” earlier.

## AI agent architecture (intelligent agent cycle)

This system behaves like an **Intelligent Agent** using the cycle:

**Observe → Predict → Decide → Act → Learn**

| Stage | Implementation |
|------|----------------|
| Observe | Load study data from CSV |
| Predict | Calculate retention using the forgetting curve |
| Decide | If retention < 60%, schedule revision |
| Act | Generate a quiz question |
| Learn | Update revision schedule based on quiz result |

## Architecture diagram

```text
User
 ↓
CLI Interface
 ↓
Data Storage (CSV)
 ↓
Memory Prediction Model
 ↓
Revision Scheduler
 ↓
Question Generator
 ↓
Quiz Evaluation
 ↓
Adaptive Scheduling
```

## Experimental results (example output)

```text
Today's Revision Tasks

1. Machine Learning - Regression
Predicted Retention: 52%

Question:
What is Regression?

2. Machine Learning - Overfitting
Predicted Retention: 48%

Question:
Explain the concept of Overfitting.

Performance summary:

Concepts Studied: 10
Revisions Completed: 6
Average Retention: 78%
```

## System evaluation

The system was tested using several concepts from **Artificial Intelligence** and **Machine Learning** topics.

The results show that the revision assistant correctly identifies when retention falls below the threshold and generates revision tasks accordingly.

The adaptive quiz scheduling helps reinforce learning by adjusting revision intervals based on user performance.

## Contribution

This project demonstrates how a simple mathematical memory model combined with rule-based decision making can create an effective intelligent learning assistant without requiring complex machine learning infrastructure.

The system shows that meaningful AI-based tools can be built using interpretable algorithms and lightweight architectures.

## Future work

Future improvements may include:

- Personalized forgetting rates learned from user behaviour
- Natural language answer evaluation using semantic similarity
- Graphical user interface for easier interaction
- Integration with learning platforms
- Mobile app version for daily reminders

## Limitations (current scope)

- The “auto-check” is deliberately simple (keyword-based) and mainly for demo; manual scoring is supported.
- Retention model parameters (difficulty rates and 60% threshold) are tuned for interpretability, not medical/psych research accuracy.
- No user accounts; data is stored locally in files.

## Troubleshooting

- **`pip` not recognized**: reopen PowerShell after installing Python, or reinstall with “Add Python to PATH”.
- **Pandas install issues**: upgrade pip first:

```text
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Report

See `PROJECT_REPORT.md` for the full project report (problem, approach, decisions, challenges, learning, and future work).
