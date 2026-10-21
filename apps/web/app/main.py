from flask import Flask
import platform

app = Flask(__name__)


@app.route("/")
def hello():
    return f"""
    <!DOCTYPE html>
    <html>
      <head><title>Hello Web</title></head>
      <body>
        <h1>Hello World from Web!</h1>
        <p>Python version: {platform.python_version()}</p>
      </body>
    </html>
    """


@app.route("/health")
def health():
    return {"status": "healthy"}
