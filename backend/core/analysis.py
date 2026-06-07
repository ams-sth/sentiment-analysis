import re
import pandas as pd
import nltk
from typing import Generator

for _pkg in ("punkt", "punkt_tab", "stopwords", "wordnet"):
    nltk.download(_pkg, quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()
_lemmatizer = WordNetLemmatizer()
_stop_words = set(stopwords.words("english"))

MAX_ROWS = 5_000
MAX_RESPONSE_ROWS = 500
_SCORE_BATCH = 200

_REVIEW_CANDIDATES = [
    "review_text", "review", "text", "comment", "comments", "body", "content", "description"
]


def _label(score: float) -> str:
    if score >= 0.05:
        return "Positive"
    if score <= -0.05:
        return "Negative"
    return "Neutral"


def analyze_sentiment(text: str) -> dict:
    score = round(_analyzer.polarity_scores(text)["compound"], 4)
    return {"text": text, "score": score, "label": _label(score)}


def _clean_for_display(text: str) -> str:
    """Lightweight clean used only for the 'Cleaned Data' display panel."""
    text = re.sub(r"http\S+", "", text.lower())
    text = re.sub(r"[^a-z\s]", "", text)
    words = [
        _lemmatizer.lemmatize(w)
        for w in word_tokenize(text)
        if w not in _stop_words
    ]
    return " ".join(words)


def get_csv_columns(file_path: str) -> dict:
    """Read only the header row and return column names + auto-detected recommendation."""
    df = pd.read_csv(file_path, nrows=0, encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.replace("﻿", "", regex=False)
    columns = list(df.columns)
    col_map = {c.lower(): c for c in columns}
    recommended = next((col_map[c] for c in _REVIEW_CANDIDATES if c in col_map), None)
    return {"columns": columns, "recommended": recommended}


def analyze_csv_stream(file_path: str, column: str) -> Generator[dict, None, None]:
    """
    Generator that yields SSE-style dicts during analysis then a final complete event.
    Yields: {"type": "progress", "percent": int, "message": str}
    Final:  {"type": "complete", "result": dict}
    Error:  {"type": "error", "message": str}
    """
    yield {"type": "progress", "percent": 5, "message": "Loading file…"}

    df = pd.read_csv(file_path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.replace("﻿", "", regex=False)

    # Case-insensitive column lookup
    if column not in df.columns:
        col_map = {c.lower(): c for c in df.columns}
        if column.lower() in col_map:
            column = col_map[column.lower()]
        else:
            yield {
                "type": "error",
                "message": f"Column '{column}' not found — available: {list(df.columns)}",
            }
            return

    total_rows = len(df)
    if total_rows > MAX_ROWS:
        df = df.head(MAX_ROWS)
    n = len(df)

    yield {"type": "progress", "percent": 10, "message": f"Loaded {n:,} rows — scoring sentiment…"}

    # Score in small batches so the frontend receives real-time progress
    scores: list[float] = []
    for start in range(0, n, _SCORE_BATCH):
        end = min(start + _SCORE_BATCH, n)
        batch = df[column].iloc[start:end].astype(str)
        scores.extend(_analyzer.polarity_scores(t)["compound"] for t in batch)
        percent = 10 + int((end / n) * 75)
        yield {
            "type": "progress",
            "percent": percent,
            "message": f"Scored {end:,} / {n:,} reviews…",
        }

    df["Sentiment"] = scores

    yield {"type": "progress", "percent": 88, "message": "Computing statistics…"}

    avg = round(float(df["Sentiment"].mean()), 4)
    positive = int((df["Sentiment"] >= 0.05).sum())
    negative = int((df["Sentiment"] <= -0.05).sum())
    neutral = n - positive - negative

    edges = [round(-1.0 + i * 0.1, 1) for i in range(21)]
    histogram = []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        is_last = i == len(edges) - 2
        mask = (df["Sentiment"] >= lo) & (
            df["Sentiment"] <= hi if is_last else df["Sentiment"] < hi
        )
        count = int(mask.sum())
        if count:
            histogram.append({"range": f"{lo:.1f}", "count": count})

    top_pos = df[df["Sentiment"] >= 0.05].nlargest(5, "Sentiment")[[column, "Sentiment"]]
    top_neg = df[df["Sentiment"] <= -0.05].nsmallest(5, "Sentiment")[[column, "Sentiment"]]

    sample_count = min(n, MAX_RESPONSE_ROWS)
    yield {
        "type": "progress",
        "percent": 93,
        "message": f"Cleaning {sample_count:,} sample reviews for display…",
    }

    raw_texts: list[str] = df[column].astype(str).tolist()
    cleaned_texts: list[str] = [_clean_for_display(t) for t in raw_texts[:MAX_RESPONSE_ROWS]]

    yield {"type": "progress", "percent": 99, "message": "Finalizing…"}

    table_data = (
        df[[column, "Sentiment"]]
        .head(MAX_RESPONSE_ROWS)
        .rename(columns={column: "review", "Sentiment": "sentiment"})
        .round({"sentiment": 4})
        .to_dict("records")
    )

    result = {
        "avg_sentiment": avg,
        "num_reviews": n,
        "total_rows_in_file": total_rows,
        "overall_sentiment": _label(avg),
        "sentiment_breakdown": {"positive": positive, "neutral": neutral, "negative": negative},
        "score_histogram": histogram,
        "positive_comments": [
            {"comment": r[column], "score": round(r["Sentiment"], 4)}
            for _, r in top_pos.iterrows()
        ],
        "negative_comments": [
            {"comment": r[column], "score": round(r["Sentiment"], 4)}
            for _, r in top_neg.iterrows()
        ],
        "raw_data": raw_texts[:MAX_RESPONSE_ROWS],
        "cleaned_data": cleaned_texts,
        "table_data": table_data,
    }

    yield {"type": "complete", "result": result}


def analyze_csv(file_path: str) -> dict:
    """Legacy synchronous wrapper — collects all stream events and returns the result."""
    result: dict = {}
    for event in analyze_csv_stream(file_path, _auto_detect_column(file_path)):
        if event["type"] == "complete":
            result = event["result"]
        elif event["type"] == "error":
            raise KeyError(event["message"])
    return result


def _auto_detect_column(file_path: str) -> str:
    info = get_csv_columns(file_path)
    if info["recommended"]:
        return info["recommended"]
    cols = info["columns"]
    if not cols:
        raise KeyError("CSV has no columns")
    return cols[0]
