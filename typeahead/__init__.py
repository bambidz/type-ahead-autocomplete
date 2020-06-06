import os
from pathlib import Path
from flask import Flask
import click

app = Flask(__name__)

if os.environ.get('TYPEAHEAD_SETTINGS'):
    app.config.from_envvar('TYPEAHEAD_SETTINGS')
else:
    # default
    default_config = Path(os.path.dirname(__file__)) / "config.py"
    if os.path.isfile(default_config):
        app.config.from_pyfile(default_config)
    else:
        print("No config file")
        exit(-1)


# # doesn't work when in seperate file..
# import click
# # from typeahead import app
# from indexing.index_generator import IndexGen
# from indexing.word_counter import word_count

# pqsize = app.config["PQSIZE"]
# @app.cli.command("index")
# @click.argument("input_file")
# @click.argument("version")
# def index(input_file, version):
#     indexGen = IndexGen(readfile = input_file, pqsize = pqsize, version = version)
#     indexGen.load()
#     indexGen.save()

# @app.cli.command("count")
# @click.argument("input_file_name")
# @click.argument("output_file_name")
# def count(input_file_name, output_file_name):   # path is added to file_name in the function
#     word_count(input_file_name,output_file_name)