from flask import Flask, render_template, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    return compound_score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_text = request.form['user_text']
    sentiment_score = analyze_sentiment(user_text)
    return render_template('result.html', user_text=user_text, sentiment_score=sentiment_score)

if __name__ == '__main__':
    app.run(debug=True)
