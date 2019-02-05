from flask import Flask
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/webhook')
def test_world():
    dumData = json.loads('data/MOCK_DATA.json')
    return dumData

if __name__ == '__main__':
    # app.run()
    app.run(debug = True)
