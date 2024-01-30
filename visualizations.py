import base64
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd

def create_sentiment_visualizations(sentiment_counts):
    plt.figure(figsize=(8, 6))
    sentiment_series = pd.Series(sentiment_counts)

    sentiments = list(sentiment_counts.keys())
    counts = list(sentiment_counts.values())
    plt.pie(counts, labels=sentiments, autopct='%1.1f%%', startangle=140, colors=['lightcoral', 'lightgreen', 'skyblue'])
    plt.title('Sentiment Distribution (Pie Chart)')
    plt.tight_layout()
    img_pie = BytesIO()
    plt.savefig(img_pie, format='png')
    img_pie.seek(0)
    chart_url_pie = base64.b64encode(img_pie.getvalue()).decode()
    plt.close()

    plt.figure(figsize=(8, 6))
    sentiment_series = pd.Series(sentiment_counts)
    sentiment_series.plot(kind='bar', color='skyblue')
    plt.title('Sentiment Distribution (Bar Chart)')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Number of Reviews')
    plt.xticks(rotation=0)
    plt.tight_layout()
    img_bar = BytesIO()
    plt.savefig(img_bar, format='png')
    img_bar.seek(0)
    chart_url_bar = base64.b64encode(img_bar.getvalue()).decode()
    plt.close()

    plt.figure(figsize=(8, 6))
    plt.hist(sentiment_series, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Sentiment Distribution (Histogram)')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Number of Reviews')
    plt.tight_layout()
    img_hist = BytesIO()
    plt.savefig(img_hist, format='png')
    img_hist.seek(0)
    chart_url_histogram = base64.b64encode(img_hist.getvalue()).decode()
    plt.close()

    return chart_url_pie, chart_url_bar, chart_url_histogram
