import os
from os import listdir
from os.path import isfile, join

from flask import Flask, request, abort, jsonify, send_from_directory
from flask import render_template, url_for, redirect, flash

ROOT = os.getcwd()
UPLOAD_DIRECTORY = "{}/posts_and_requests/api_uploaded_files".format(ROOT)

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def get_files(filter_key):
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path) and (filter_key in filename):
            files.append(filename)
    n_of_files = len([name for name in os.listdir(UPLOAD_DIRECTORY) \
        if os.path.isfile(os.path.join(UPLOAD_DIRECTORY, name))])
    return [files, n_of_files]

api = Flask(__name__)

@api.route('/')
def default():
    [files, n_of_files] = get_files("")
    return render_template('index.html', muuttuja=n_of_files, files=files)

@api.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@api.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201
@api.route("/delete/<path:path>")
def delete_file(path):
    try:
        os.remove(UPLOAD_DIRECTORY+'/'+path)
        return redirect('/')
    except OSError:
        return redirect('/')
"""
@api.route("/filter/<filter_value>")
def filter_page(filter_value):
    [n_of_files, files] = get_files(filter_value)
    return render_template('index.html', muuttuja=n_of_files, files=files)
"""
if __name__ == "__main__":
    api.run(debug=True, port=8000)