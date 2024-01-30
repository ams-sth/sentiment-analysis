import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    return compound_score

def analyze_csv(file_path):
    df = pd.read_csv(file_path)
    df['Sentiment'] = df['Review'].apply(analyze_sentiment)
    return df

def calculate_summary_statistics(df):
    avg_sentiment = df['Sentiment'].mean()
    sentiment_counts = df['Sentiment'].value_counts().sort_index().to_dict()
    distribution_of_scores = sentiment_counts
    num_reviews = df.shape[0]

    most_positive_comment = df.loc[df['Sentiment'].idxmax(), 'Review']
    most_negative_comment = df.loc[df['Sentiment'].idxmin(), 'Review']

    return avg_sentiment, sentiment_counts, distribution_of_scores, num_reviews, most_positive_comment, most_negative_comment
