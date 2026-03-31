# AI Smart Revision Assistant (Memory Decay Predictor)

A **CLI-based Smart Revision Assistant** that helps you revise more effectively by:

- **Tracking** what you studied in a small local database (`study_data.csv`)
- **Predicting** forgetting using an exponential memory decay model \(R(t)=e^{-kt}\)
- **Scheduling** revision when predicted retention drops below **60%**
- **Adapting** the next revision date based on your quiz performance

This project is intentionally lightweight (no web app) so it can run anywhere with Python.

## What problem it solves

In day-to-day studying, it’s hard to remember **what** to revise and **when**. This tool uses a simple memory model + rule-based scheduling to generate a daily list of “due for revision” concepts and then reinforces learning with a quick quiz loop.

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
