from flask import Flask
from flask_cors import CORS
from api.routes import api

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
