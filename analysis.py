import re
import pandas as pd
import nltk

nltk.download("punkt", "stopwords")
nltk.download("wordnet")
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores["compound"]
    return compound_score


def clean_text(text):
    cleaned_text = text.lower()
    cleaned_text = re.sub(r"http\S+", "", cleaned_text)
    cleaned_text = re.sub(r"\d+", "", cleaned_text)
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", "", cleaned_text)
    words = word_tokenize(cleaned_text)
    stop_words = set(stopwords.words("english"))
    cleaned_words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    cleaned_words = [lemmatizer.lemmatize(word) for word in cleaned_words]
    cleaned_text = " ".join(cleaned_words)
    return cleaned_text


def analyze_csv(file_path):
    df = pd.read_csv(file_path)

    raw_data = df["Review"].to_frame().to_html()
    df["Review"] = df["Review"].apply(clean_text)
    df["Sentiment"] = df["Review"].apply(analyze_sentiment)
    cleaned_data = df["Review"].to_frame().to_html()

    return df, raw_data, cleaned_data


def calculate_summary_statistics(df):
    avg_sentiment = df["Sentiment"].mean()
    sentiment_counts = df["Sentiment"].value_counts().sort_index().to_dict()
    distribution_of_scores = sentiment_counts
    num_reviews = df.shape[0]

    most_positive_comment = df.loc[df["Sentiment"].idxmax(), "Review"]
    most_negative_comment = df.loc[df["Sentiment"].idxmin(), "Review"]

    return (
        avg_sentiment,
        sentiment_counts,
        distribution_of_scores,
        num_reviews,
        most_positive_comment,
        most_negative_comment,
    )


def get_top_comments(df, positive=True, num_comments=5):
    if positive:
        sorted_comments = df[df["Sentiment"] > 0].sort_values(
            by="Sentiment", ascending=False
        )
    else:
        sorted_comments = df[df["Sentiment"] < 0].sort_values(
            by="Sentiment", ascending=True
        )
    top_comments = sorted_comments["Review"].head(num_comments).tolist()
    return top_comments
