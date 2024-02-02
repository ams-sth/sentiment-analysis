from flask import render_template, request
from analysis import (
    analyze_sentiment,
    analyze_csv,
    calculate_summary_statistics,
    get_top_comments,
)
from visualizations import create_sentiment_visualizations


def setup_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/analyze", methods=["POST"])
    def analyze():
        user_text = request.form["user_text"]
        sentiment_score = analyze_sentiment(user_text)
        return render_template(
            "result.html", user_text=user_text, sentiment_score=sentiment_score
        )

    @app.route("/analyze_csv", methods=["POST"])
    def analyze_csv_route():
        uploaded_file = request.files["csv_file"]
        if uploaded_file.filename != "":
            file_path = "uploads/" + uploaded_file.filename
            uploaded_file.save(file_path)

            # Analyze CSV and get DataFrame, raw data, and cleaned data
            df, raw_data, cleaned_data = analyze_csv(file_path)

            # Calculate summary statistics
            (
                avg_sentiment,
                sentiment_counts,
                distribution_of_scores,
                num_reviews,
                most_positive_comment,
                most_negative_comment,
            ) = calculate_summary_statistics(df)

            # Determine overall sentiment
            overall_sentiment = (
                "Positive"
                if avg_sentiment >= 0
                else "Negative" if avg_sentiment < 0 else "Neutral"
            )

            positive_comments = get_top_comments(df, positive=True)
            negative_comments = get_top_comments(df, positive=False)

            # Create sentiment visualizations
            chart_url_pie, chart_url_bar, chart_url_histogram = (
                create_sentiment_visualizations(sentiment_counts)
            )

            # Pass data to template
            return render_template(
                "result_csv.html",
                table=df.to_html(),
                file_path=file_path,
                avg_sentiment=avg_sentiment,
                distribution_of_scores=distribution_of_scores,
                num_reviews=num_reviews,
                chart_url_bar=chart_url_bar,
                chart_url_pie=chart_url_pie,
                chart_url_histogram=chart_url_histogram,
                most_positive_comment=most_positive_comment,
                most_negative_comment=most_negative_comment,
                positive_comments=positive_comments,
                negative_comments=negative_comments,
                overall_sentiment=overall_sentiment,
                raw_data=raw_data,
                cleaned_data=cleaned_data,
            )
        else:
            return render_template("index.html", error="Please upload a CSV file.")
