from datasets import datasets
from flask import Flask, abort, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', title='Katalog')

@app.route("/datasets")
def sets():
    return render_template('datasets.html', title='Lista zbiorów', sets=datasets)

@app.route("/details/<int:id>")
def details(id):
    dataset = None
    for ds in datasets:
        if ds["id"] == id:
            dataset = ds
    if dataset == None:
        abort(404)

    return render_template('details.html', set=dataset)


app.run(debug=True)
