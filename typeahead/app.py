from flask import Flask, render_template, url_for, request, redirect, jsonify
from pathlib import Path
from indexing.index_manager import PrefixIndex
from typeahead import app
import os
import json
import requests
import logging
import click

prefixIndex = PrefixIndex()

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
            recommend_list = prefixIndex.search(request.form['content'])
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
    return jsonify({prefix:prefixIndex.search(prefix)})

@app.route('/admin/index/reload', methods=['POST','GET'])
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

    prefixIndex.update({prefix:word})

    return jsonify(success = True)

@app.route('/admin/index/<prefix>', methods=['DELETE'])
def delete(prefix):

    word = request.json['word']
    #print("in the remove func.")
    if not word:
        return jsonify(success = False, status_code = 503)

    prefixIndex.delete({prefix:word})

    return jsonify(success = True)

