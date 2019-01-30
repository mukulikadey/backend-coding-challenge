
from flask import Flask, request, jsonify, render_template
from flask_restful import Api
import queries

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/suggestions', methods=['GET'])
def api_name():
    name = request.args.get('name', None)
    population = int(request.args.get('population', 0))
    lat = float(request.args.get('lat', 0.0))
    long = float(request.args.get('long', 0.0))

    sorted_results = queries.get_results(name, population, lat, long)

    return jsonify(sorted_results)


app.run(debug=True, use_reloader=False)
