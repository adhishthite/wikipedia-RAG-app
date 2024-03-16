import os

from flask import Flask, jsonify
import elasticapm
from elasticapm.contrib.flask import ElasticAPM
from dotenv import load_dotenv

from . import data

load_dotenv()

app = Flask(__name__)
if os.environ['ENVIRONMENT'] == 'production':
    app.config['ELASTIC_APM'] = {
      'SERVICE_NAME': os.environ['SERVICE_NAME'],
      'SECRET_TOKEN': os.environ['SECRET_TOKEN'],
      'SERVER_URL': os.environ['SERVER_URL'],
      'ENVIRONMENT': os.environ['ENVIRONMENT'],
    }

    apm = ElasticAPM(app)


@app.route('/', methods=['GET'])
@elasticapm.capture_span()
def hello_world():
    return data.healthcheck()


@app.route('/mongo_status', methods=['GET'])
@elasticapm.capture_span()
def mongo_status():
    return jsonify(data.get_mongo_status()), 200


if __name__ == '__main__':
    app.run(debug=True, port=6062)
