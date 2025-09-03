from uuid import uuid4
from functools import wraps
import os, os.path as path
from markdown import markdown

from flask import (
    flash,
    Flask,
    g, 
    redirect, 
    render_template, 
    request,
    session,
    url_for, 
)
from cms.utils import (
    list_data_files,
    read_text_files,
)

app = Flask(__name__)
app.secret_key = 'secret1'

DATA_DIR = os.path.join(app.root_path, "cms", "data")


@app.before_request
def load_files():
    g.files = list_data_files(DATA_DIR)

def markdown_text(text, file_name):
    return markdown(text) if file_name.endswith(".md") else text

app.jinja_env.filters['markdown_text'] = markdown_text

@app.route("/files/<file_name>")
def file_contents(file_name):
    contents = read_text_files(DATA_DIR, file_name)

    return render_template('contents.html',
                           file_name=file_name,
                           contents=contents)

@app.route("/files/<file_name>/edit")
def edit_page(file_name):
    
    
@app.route("/")
def index():

    return render_template('home.html', files=g.files)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True, port=5003)