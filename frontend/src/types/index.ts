export type SentimentLabel = "Positive" | "Neutral" | "Negative";

export interface TextResult {
  text: string;
  score: number;
  label: SentimentLabel;
}

export interface SentimentBreakdown {
  positive: number;
  neutral: number;
  negative: number;
}

export interface HistogramBin {
  range: string;
  count: number;
}

export interface Comment {
  comment: string;
  score: number;
}

export interface TableRow {
  review: string;
  sentiment: number;
}

export interface CsvResult {
  avg_sentiment: number;
  num_reviews: number;
  total_rows_in_file: number;
  overall_sentiment: SentimentLabel;
  sentiment_breakdown: SentimentBreakdown;
  score_histogram: HistogramBin[];
  positive_comments: Comment[];
  negative_comments: Comment[];
  raw_data: string[];
  cleaned_data: string[];
  table_data: TableRow[];
}

export interface CsvPreview {
  columns: string[];
  filename: string;
  recommended: string | null;
}
