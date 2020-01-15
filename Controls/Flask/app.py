from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    x = 0
    return ("Yes" + x + "no")
if __name__ == "__main__":
    app.run(host='0.0.0.0')
