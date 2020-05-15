from flask import Flask, render_template, url_for, request, redirect,jsonify
from pathlib import Path
from collections import defaultdict
import os
import json
import requests
import logging

app = Flask(__name__)

PQMAX = 5

data_folder = Path(os.path.dirname(__file__)) / "data"
prefix_data = data_folder / "prefix_dict.json"
global prefix_dict
prefix_dict = defaultdict(list)

#### read from local json file. change code to DB later on.
with open(prefix_data,"r",encoding='UTF8') as json_file:
    data = json.load(json_file)
    prefix_dict.update(data)

@app.route('/', methods=['POST', 'GET'])
def index():
    global prefix_dict
    if request.method == "POST":
        if 'content' in request.form:
            word_list = prefix_dict[request.form['content']]
            
            recommend_list = word_list
            return render_template("index.html", recommend_list = recommend_list)
        
        if 'prefix' in request.form:
            if 'update' in request.form:
                url = request.base_url[:-1]+url_for('update',prefix = request.form['prefix'])
                res = requests.post(url,json = {'word' :request.form['word']})
            if 'delete' in request.form:
                print("call delete")
                url = request.base_url[:-1]+url_for('delete',prefix = request.form['prefix'])
                res = requests.delete(url,json = {'word' :request.form['word']})

            return render_template("index.html")

    if request.method == "GET":
        return render_template("index.html")
            


@app.route('/search/<prefix>', methods=['GET'])
def search(prefix):
    global prefix_dict
    recommend_list = prefix_dict[prefix]
    return jsonify(recommend_list)

@app.route('/admin/index/reload', methods=['POST'])
def reload():
    global prefix_dict
    with open(prefix_data,"r") as json_file:
        data = json.load(json_file)
        prefix_dict = data
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


@app.route('/admin/index/<prefix>', methods=['POST'])
def update(prefix):
    global prefix_dict
    word = request.json['word']
    # print("in the update func.")
    if not word:
        return jsonify(success=True,status_code=200)

    prefix_dict[prefix].append(word)

    with open(prefix_data,"w") as json_file:
        json.dump(prefix_dict,json_file)

    return jsonify(success=True)

@app.route('/admin/index/<prefix>', methods=['DELETE'])
def delete(prefix):
    global prefix_dict
    word = request.json['word']
    print("in the remove func.")
    if not word:
        return jsonify(success=True,status_code=200)

    if prefix in prefix_dict:
        word_index = prefix_dict[prefix].index(word)
        del prefix_dict[prefix][word_index]

    with open(prefix_data,"w") as json_file:
        json.dump(prefix_dict,json_file)

    return jsonify(success=True)


if __name__ == "__main__":
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(debug=True)