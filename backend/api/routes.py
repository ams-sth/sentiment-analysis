import json
import os
from flask import Blueprint, Response, request, jsonify, stream_with_context
from werkzeug.utils import secure_filename
from core.analysis import analyze_sentiment, analyze_csv, analyze_csv_stream, get_csv_columns

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or not data.get("text", "").strip():
        return jsonify({"error": "No text provided"}), 400
    return jsonify(analyze_sentiment(data["text"]))


@api.route("/csv/preview", methods=["POST"])
def csv_preview():
    """Save the uploaded CSV and return its column names + auto-detected recommendation."""
    if "csv_file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["csv_file"]
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    file.save(file_path)

    try:
        info = get_csv_columns(file_path)
        return jsonify({
            "columns": info["columns"],
            "filename": filename,
            "recommended": info["recommended"],
        })
    except Exception as e:
        try:
            os.remove(file_path)
        except OSError:
            pass
        return jsonify({"error": str(e)}), 500


@api.route("/csv/analyze", methods=["POST"])
def csv_analyze():
    """Stream SSE progress events while analysing a previously uploaded CSV."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    filename = data.get("filename", "").strip()
    column = data.get("column", "").strip()
    if not filename or not column:
        return jsonify({"error": "filename and column are required"}), 400

    file_path = os.path.join(UPLOAD_DIR, secure_filename(filename))
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found — please re-upload"}), 404

    def generate():
        try:
            for event in analyze_csv_stream(file_path, column):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        finally:
            try:
                os.remove(file_path)
            except OSError:
                pass

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


# Legacy route kept for backward compatibility
@api.route("/analyze/csv", methods=["POST"])
def analyze_csv_route():
    if "csv_file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["csv_file"]
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    file.save(file_path)

    try:
        return jsonify(analyze_csv(file_path))
    except KeyError as e:
        return jsonify({"error": str(e).strip("'")}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.remove(file_path)
        except OSError:
            pass
