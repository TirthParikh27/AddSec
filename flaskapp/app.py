from flask import Flask
from flask_cors import CORS
import yaml

app = Flask(__name__)
CORS(app)

steps_list = []

@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route("/pipeline")
def secure():swwww


if __name__ == '__main__':
  app.run(debug=True)