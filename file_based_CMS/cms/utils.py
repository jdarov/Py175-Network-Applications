import os
from werkzeug.utils import safe_join
from flask import abort, flash

BOLD = "\033[1m"
ITALIC = "\033[3m"
RESET = "\033[0m"

def list_data_files(data_dir):
    """ Returns a sorted list of file names"""
    return sorted (
        file for file in os.listdir(data_dir)
        if os.path.isfile(os.path.join(data_dir, file))
    )

def read_text_files(file_path, filename):

    if not file_path or not os.path.isfile(file_path):
        flash(f'The requested file <strong>{filename}</strong> does not exist', "error")
        abort(404)
    with open(file_path, 'r') as file:
        return file.read()

def write_to_files(data_dir, filename, contents):
    safe_path = safe_join(data_dir, filename)

    if not safe_path or not os.path.isfile(safe_path):
        flash(f'The requested file <strong>{filename}</strong> does not exist', "error")
        abort(404)
    with open(safe_path, 'w', encoding='utf-8', newline='') as file:
        written = file.write(contents)

    return written > 0 or contents == ""
