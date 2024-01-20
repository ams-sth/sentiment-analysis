from flask import Flask, render_template, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

app = Flask(__name__)

# Section 1: Function to analyse user text
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    return compound_score

# Section 2: Function to analyse sentiment in CSV file
def analyze_csv(file_path):
    df = pd.read_csv(file_path)
    df['Sentiment'] = df['Review'].apply(analyze_sentiment)
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_text = request.form['user_text']
    sentiment_score = analyze_sentiment(user_text)
    return render_template('result.html', user_text=user_text, sentiment_score=sentiment_score)

@app.route('/analyze_csv', methods=['POST'])
def analyze_csv_route():
    uploaded_file = request.files['csv_file']
    if uploaded_file.filename != '':
        file_path = "uploads/" + uploaded_file.filename
        uploaded_file.save(file_path)
        df = analyze_csv(file_path)
        
        return render_template('result_csv.html', table=df.to_html(), file_path=file_path)
    else:
        return render_template('index.html', error='Please upload a CSV file.')

if __name__ == '__main__':
    app.run(debug=True)
