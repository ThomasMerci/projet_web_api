#pip install flask-cors
from flask import Flask, render_template
from flask_cors import CORS
from python.lecture import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('app.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)

