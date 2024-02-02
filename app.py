from flask import Flask
from routes import setup_routes

app = Flask(__name__)


def enumerate_filter(iterable, start=0):
    return enumerate(iterable, start=start)


app.jinja_env.filters["enumerate"] = enumerate_filter


app.jinja_env.filters["enumerate"] = enumerate_filter


# Setup routes from routes.py
setup_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
