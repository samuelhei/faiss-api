import os
import sys
import flask
import os
import numpy as np
import re

from flask import Flask
from flask import make_response
from flask import request
from werkzeug.utils import secure_filename

import faiss
import config

def load_index():
    index = faiss.read_index(config.CONFIG_INDEX['index'])
    keys = []

    keys_path  = config.CONFIG_INDEX['keys']
    if len(keys_path) > 0 and os.path.isfile(keys_path):
        keys = np.load(config.CONFIG_INDEX['keys'])

    return index, keys

def create_app():
    app = Flask(__name__)
    index, keys  = load_index()

    @app.route('/ping', methods=['GET'])
    def ping():
        return flask.jsonify(ping='pong')

    @app.route("/get_similarities", methods=["POST"])
    def get_similarities():
        result = {}
        n = 5

        if 'n' in request.form and request.form['n'].isnumeric():
            n = int(request.form['n'])
            if n < 1: 
                n = 1

        vector = str(request.form['vector'])

        if len(vector) == 0:
            result['status'] = 'error'
            result['message'] = 'empty value'
            return flask.jsonify(result), 400

        new_vector = []
        vector = vector.split(',')

        if len(vector) != config.CONFIG_INDEX['index_vector_len']:
            result['status'] = 'error'
            result['message'] = 'expected a vector with {} length obtained one with {}'.format(config.CONFIG_INDEX['index_vector_len'], len(vector)) 
            return flask.jsonify(result), 400

        for v in vector:
            if re.match(r'[^0-9\.]', v):
                result['status'] = 'error'
                result['message'] = 'the sended vector is not valid'
                return flask.jsonify(result), 400
            new_vector.append(float(v))

        vector =  new_vector
        vector = np.array(vector).astype('float32')
        vector = np.expand_dims(vector,axis=0)

        d,I = index.search(vector, n) 
        result['status'] = 'ok'
        
        if len(keys) > 0:
            result['keys'] = list(keys[I[0]])
        else:
            result['keys'] = I[0].tolist()

        return flask.jsonify(result), 200

    @app.errorhandler(404)
    def error_404(e):
        result = {}
        result['status'] = 'error'
        result['message'] = '404 - the requested URL is not available with this method'
        
        return flask.jsonify(result)  

    @app.errorhandler(500)
    def error_500(e):
        result = {}
        result['status'] = 'error'
        result['message'] = '500 - internal error'
        return flask.jsonify(result)

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(host='0.0.0.0')