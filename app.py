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

# Section 3: Summary Statistics - Calculate and display summary statistics
  #  for the entire dataset, such as the average sentiment score, distribution 
     # of scores, and the number of reviews in each sentiment category.
def calculate_summary_statistics(df):
    avg_sentiment = df['Sentiment'].mean()
    sentiment_counts = df['Sentiment'].value_counts().sort_index()
    distribution_of_scores = dict(sentiment_counts)
    num_reviews = df.shape[0]

    return avg_sentiment, sentiment_counts.to_dict(), distribution_of_scores, num_reviews

# Section 4: Visualizations - Bar charts, Pie charts and Histrograms
# def create_sentiment_distribution_chart(sentiment_counts):
    # plt.figure(figsize=(8, 6))
    # sentiment_counts.plot(kind='bar', color='skyblue')
    # plt.title('Sentiment Distribution')
    # plt.xlabel('Sentiment Score')
    # plt.ylabel('Number of Reviews')
    # plt.xticks(rotation=0)
    # plt.tight_layout()

    # # Save the plot to a BytesIO object
    # img = BytesIO()
    # plt.savefig(img, format='png')
    # img.seek(0)

    # # Encode the image as base64 and convert it to a string to embed in HTML
    # chart_url = base64.b64encode(img.getvalue()).decode()
    # plt.close()

    # return chart_url

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

         # Calculate summary statistics
        avg_sentiment, sentiment_count, distribution_of_scores, num_reviews = calculate_summary_statistics(df)

        # chart_url = create_sentiment_distribution_chart(sentiment_counts)

        
        return render_template('result_csv.html', table=df.to_html(), file_path=file_path, avg_sentiment = avg_sentiment,distribution_of_scores=distribution_of_scores,
                               num_reviews=num_reviews, 
                            #    chart_url=chart_url
                               )
    else:
        return render_template('index.html', error='Please upload a CSV file.')

if __name__ == '__main__':
    app.run(debug=True)
