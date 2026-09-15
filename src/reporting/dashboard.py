"""Internal reporting dashboard.

Maps to default rules:
  python-flask-debug-true
  python-jinja2-autoescape-false
"""
from flask import Flask
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

# python-jinja2-autoescape-false: renders merchant-supplied fields
env = Environment(loader=FileSystemLoader("templates"), autoescape=False)


@app.route("/reports/<merchant_id>")
def report(merchant_id):
    return env.get_template("report.html").render(merchant_id=merchant_id)


if __name__ == "__main__":
    # python-flask-debug-true: Werkzeug debugger exposed
    app.run(host="0.0.0.0", port=8081, debug=True)
