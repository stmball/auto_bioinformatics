from flask import Flask, request, jsonify

from src.scalers import REGISTERED_SCALERS
from src.normalizers import REGISTERED_NORMALIZERS
from src.reducers import REGISTERED_REDUCERS
from src.imputers import REGISTERED_IMPUTERS


app = Flask(__name__)

@app.route('/api')
def index():
    return 'Hello World!'

@app.route('/api/list_normalizers')
def normalisers():
    pass

@app.route('/api/list_imputers')
def imputers():
    pass

@app.route('/api/list_reducers')
def reducers():
    pass

@app.route('/api/list_scalers')
def scalers():
    pass


@app.route('/api/analyze', methods=['POST'])
def analyze():

    # Get the JSON data from the POST request
    data = request.get_json()

    # Get the config from the JSON data
    config = data['config']

    # Get the data from the JSON data
    data = data['data']






if __name__ == '__main__':
    app.run(debug=True)



