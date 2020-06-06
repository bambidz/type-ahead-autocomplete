import click
from typeahead.app import app
from indexing.index_generator import IndexGen
from indexing.word_counter import word_count

pqsize = app.config.get("PQSIZE")
@app.cli.command("index")
@click.argument("input_file")
@click.argument("version")
def index(input_file, version):
    indexGen = IndexGen(readfile = input_file, pqsize = pqsize, version = version)
    indexGen.load()
    indexGen.save()

@app.cli.command("count")
@click.argument("input_file_name")
@click.argument("output_file_name")
def count(input_file_name, output_file_name):   # path is added to file_name in the function
    word_count(input_file_name,output_file_name)
