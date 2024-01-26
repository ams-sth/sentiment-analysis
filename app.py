# Import necessary libraries
import base64
from io import BytesIO
from flask import Flask, render_template, request
from matplotlib import pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# Create Flask app
app = Flask(__name__)

# Section 1: Function to analyze user text
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    return compound_score

# Section 2: Function to analyze sentiment in CSV file
def analyze_csv(file_path):
    df = pd.read_csv(file_path)
    df['Sentiment'] = df['Review'].apply(analyze_sentiment)
    return df

# Section 3: Summary Statistics - Calculate and display summary statistics
def calculate_summary_statistics(df):
    avg_sentiment = df['Sentiment'].mean()
    sentiment_counts = df['Sentiment'].value_counts().sort_index().to_dict()
    distribution_of_scores = sentiment_counts  
    num_reviews = df.shape[0]

    # Most positive and most negative comments
    most_positive_comment = df.loc[df['Sentiment'].idxmax(), 'Review']
    most_negative_comment = df.loc[df['Sentiment'].idxmin(), 'Review']

    return avg_sentiment, sentiment_counts, distribution_of_scores, num_reviews, most_positive_comment, most_negative_comment

# Section 4: Visualizations - Bar charts, Pie charts, and Histograms
def create_sentiment_visualizations(sentiment_counts):
    # Create Pie Chart
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

    # Create Bar Chart
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

    # Create Histogram
    plt.figure(figsize=(8, 6))
    plt.hist(sentiment_series, bins=20, color='skyblue', edgecolor='black', alpha=0.7)  # Use sentiment_series directly
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



# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for analyzing user text
@app.route('/analyze', methods=['POST'])
def analyze():
    user_text = request.form['user_text']
    sentiment_score = analyze_sentiment(user_text)
    return render_template('result.html', user_text=user_text, sentiment_score=sentiment_score)

# Route for analyzing CSV file
@app.route('/analyze_csv', methods=['POST'])
def analyze_csv_route():
    uploaded_file = request.files['csv_file']
    if uploaded_file.filename != '':
        file_path = "uploads/" + uploaded_file.filename
        uploaded_file.save(file_path)
        df = analyze_csv(file_path)

        # Calculate summary statistics
        avg_sentiment, sentiment_counts, distribution_of_scores, num_reviews, most_positive_comment, most_negative_comment = calculate_summary_statistics(df)

        # Inside analyze_csv_route function
        overall_sentiment = "Positive" if avg_sentiment >= 0 else "Negative" if avg_sentiment < 0 else "Neutral"

        chart_url_pie, chart_url_bar, chart_url_histogram = create_sentiment_visualizations(sentiment_counts)


    

        return render_template('result_csv.html', table=df.to_html(), file_path=file_path, avg_sentiment=avg_sentiment,
                       distribution_of_scores=distribution_of_scores, num_reviews=num_reviews,
                        chart_url_bar=chart_url_bar, chart_url_pie=chart_url_pie, chart_url_histogram=chart_url_histogram,
                        most_positive_comment=most_positive_comment, most_negative_comment=most_negative_comment,
                       overall_sentiment=overall_sentiment)
    else:
        return render_template('index.html', error='Please upload a CSV file.')
    
    


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
