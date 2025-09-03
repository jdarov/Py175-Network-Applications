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

def read_text_files(data_dir, filename):
    safe_path = safe_join(data_dir, filename)

    if not safe_path or not os.path.isfile(safe_path):
        flash(f'The requested file <strong>{filename}</strong> does not exist', "error")
        abort(404)
    with open(safe_path, 'r') as file:
        return file.readlines()
    
