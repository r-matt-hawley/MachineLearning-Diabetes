import os
import sys
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home:
    print('Hello world!', file=sys.stderr)
    return render_template("templates/index.html")

if __name__ == "__main__":
    app.run()
