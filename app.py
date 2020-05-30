from flask import Flask, render_template, url_for, request, redirect, jsonify
from pathlib import Path
from indexing.index_generator import PrefixIndex
from config import IndexConfig,ServerConfig
import os
import json
import requests
import logging
import click
#import pytest

app = Flask(__name__)
prefixIndex = PrefixIndex(**IndexConfig)
logging.basicConfig(filename='error.log',level=logging.DEBUG)

# build the prefix dictionary from word_count.txt
@app.cli.command("load")
@app.before_first_request
def load():               
    prefixIndex.load()

# POST method is used to send POST and DELETE requests to server
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        if 'content' in request.form:
            word_list = prefixIndex.index[request.form['content']]
            
            recommend_list = word_list
            return render_template("index.html", recommend_list = recommend_list)
        
        if 'prefix' in request.form:
            if 'update' in request.form:
                url = request.base_url[:-1]+url_for('update',prefix = request.form['prefix'])
                requests.post(url,json = {'word' :request.form['word']})
            if 'delete' in request.form:
                print("call delete")
                url = request.base_url[:-1]+url_for('delete',prefix = request.form['prefix'])
                requests.delete(url,json = {'word' :request.form['word']})

            return render_template("index.html")

    if request.method == "GET":
        return render_template("index.html")
            
## when dictionary is returned, error happens. so jsonify was used
@app.route('/search/<prefix>', methods=['GET'])
def search(prefix):
    recommend_list = prefixIndex.index[prefix]
    return jsonify({prefix:recommend_list})

@app.route('/admin/index/reload', methods=['POST'])
def reload():
    prefixIndex.load()
    return jsonify(success = True)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify(success = True)

@app.route('/admin/index/<prefix>', methods=['POST'])
def update(prefix):

    word = request.json['word']
    # print("in the update func.")
    if not word:
        return jsonify(success = False, status_code = 503)

    prefixIndex.index[prefix].append(word)
    prefixIndex.update({prefix:word})

    return jsonify(success = True)

@app.route('/admin/index/<prefix>', methods=['DELETE'])
def delete(prefix):

    word = request.json['word']
    #print("in the remove func.")
    if not word:
        return jsonify(success = False, status_code = 503)

    if prefix in prefixIndex.index:
        word_index = prefixIndex.index[prefix].index(word)
        del prefixIndex.index[prefix][word_index]

    prefixIndex.delete({prefix:word})

    return jsonify(success = True)


if __name__ == "__main__":
    app.run(debug=True,**ServerConfig)