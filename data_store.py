"""
Knowledge base: CSV read/write (Knowledge Representation).
"""
import os
from datetime import date
from typing import Any, Dict, List

import pandas as pd

CSV_NAME = "study_data.csv"
DEFAULT_COLUMNS = [
    "topic",
    "concept",
    "difficulty",
    "date_studied",
    "last_reviewed",
    "next_review_due",
]


def csv_path(base_dir: str) -> str:
    return os.path.join(base_dir, CSV_NAME)


def ensure_csv(path: str) -> None:
    if os.path.isfile(path):
        return
    df = pd.DataFrame(columns=DEFAULT_COLUMNS)
    df.to_csv(path, index=False)


def load_study_data(path: str) -> pd.DataFrame:
    ensure_csv(path)
    df = pd.read_csv(path)
    for col in DEFAULT_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[DEFAULT_COLUMNS]


def save_study_data(path: str, df: pd.DataFrame) -> None:
    df = df[DEFAULT_COLUMNS].copy()
    df.to_csv(path, index=False)


def add_concept(
    path: str,
    topic: str,
    concept: str,
    difficulty: str,
    today: date,
) -> None:
    df = load_study_data(path)
    t = today.strftime("%Y-%m-%d")
    new_row: Dict[str, Any] = {
        "topic": topic.strip(),
        "concept": concept.strip(),
        "difficulty": difficulty.strip(),
        "date_studied": t,
        "last_reviewed": t,
        "next_review_due": "",
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_study_data(path, df)


def update_row(path: str, index: int, updates: Dict[str, Any]) -> None:
    df = load_study_data(path)
    for k, v in updates.items():
        df.at[index, k] = v
    save_study_data(path, df)


def rows_to_dicts(df: pd.DataFrame) -> List[Dict[str, Any]]:
    return df.to_dict("records")
