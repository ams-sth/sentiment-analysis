# Sentiment Analysis

Analyze sentiment in plain text or bulk-process an entire CSV dataset. Built with a Flask JSON API backend and a React + TypeScript frontend.

## Features

- **Text analysis** — paste any text and get an instant VADER compound score with a Positive / Neutral / Negative label
- **CSV analysis** — upload a CSV, auto-detect the review column (or pick one), and stream real-time progress while scoring up to 5,000 rows
- **Results dashboard** — score histogram, sentiment breakdown, top positive/negative excerpts, and a cleaned-text view

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python · Flask · VADER · NLTK · pandas |
| Frontend | React 18 · TypeScript · Vite · Tailwind CSS v4 · Recharts |
| Tooling | pnpm 11 workspaces · Biome · uv |

## Running locally

**Prerequisites:** Node.js 18+, pnpm 11+, Python 3.12+, [uv](https://docs.astral.sh/uv/)

```sh
# Install dependencies
pnpm install
uv sync

# Start both servers (Flask :5000 + Vite :5173)
pnpm dev
```

Open [http://localhost:5173](http://localhost:5173).
