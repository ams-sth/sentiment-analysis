from flask import render_template, request
from analysis import analyze_sentiment, analyze_csv, calculate_summary_statistics
from visualizations import create_sentiment_visualizations

def setup_routes(app):
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

            avg_sentiment, sentiment_counts, distribution_of_scores, num_reviews, most_positive_comment, most_negative_comment = calculate_summary_statistics(df)

            overall_sentiment = "Positive" if avg_sentiment >= 0 else "Negative" if avg_sentiment < 0 else "Neutral"

            chart_url_pie, chart_url_bar, chart_url_histogram = create_sentiment_visualizations(sentiment_counts)

            return render_template('result_csv.html', table=df.to_html(), file_path=file_path, avg_sentiment=avg_sentiment,
                        distribution_of_scores=distribution_of_scores, num_reviews=num_reviews,
                            chart_url_bar=chart_url_bar, chart_url_pie=chart_url_pie, chart_url_histogram=chart_url_histogram,
                            most_positive_comment=most_positive_comment, most_negative_comment=most_negative_comment,
                        overall_sentiment=overall_sentiment)
        else:
            return render_template('index.html', error='Please upload a CSV file.')