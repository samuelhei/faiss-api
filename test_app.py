import pytest
from flask import url_for
import config

def generate_vector():
    return ('0.0,' * config.CONFIG_INDEX['index_vector_len'])[:-1]

def generate_missformated_vector():
    return ('a,' * config.CONFIG_INDEX['index_vector_len'])[:-1]

def generate_different_len_vector():
    return ('0.0,' * (config.CONFIG_INDEX['index_vector_len'] - 1))[:-1]

class TestApp:
    def test_ping(self, client):
        res = client.get(url_for('ping'))
        assert res.status_code == 200
        assert res.json == {'ping': 'pong'}

    def test_get_similarities(self, client):
        data = {}
        data['vector'] = generate_vector()
        data['n'] = 7
        response = client.post(
            url_for('get_similarities'), data=data, follow_redirects=True
        )
        assert response.status_code == 200
        assert response.json['status'] == 'ok'
        assert len(response.json['keys']) == 7

    def test_missformated_string_similarities(self, client):
        data = {}
        data['vector'] = generate_missformated_vector()
        data['n'] = 7
        response = client.post(
            url_for('get_similarities'), data=data, follow_redirects=True
        )
        assert response.status_code == 400
        assert response.json['status'] == 'error'

    def test_empty_string_similarities(self, client):
        data = {}
        data['vector'] = ''
        data['n'] = 7
        response = client.post(
            url_for('get_similarities'), data=data, follow_redirects=True
        )
        assert response.status_code == 400
        assert response.json['status'] == 'error'

    def test_different_len_similarities(self, client):
        data = {}
        data['vector'] = generate_different_len_vector()
        data['n'] = 7
        response = client.post(
            url_for('get_similarities'), data=data, follow_redirects=True
        )
        assert response.status_code == 400
        assert response.json['status'] == 'error'