from flask import Flask, abort, redirect, url_for, request, make_response, \
        render_template
# from urllib.parse import quote
app = Flask(__name__)
import os, subprocess, shlex, select, time, signal, fcntl, pipes, glob, sys

conf_dir = "configs/"

# from web import funcs
import funcs
# from . import funcs
# import web
sys.path.append("..")
import generator

@app.route("/")
def index():
    files = funcs.get_files()
    return render_template("index.xhtml", files=files)

@app.route("/edit/<name>")
def edit(name):
    files = funcs.get_files()
    file = list(filter(lambda x: x['name'] == name, files))[0]
    content = open(file['path'], "rb").read().decode("ascii")
    return render_template("edit.xhtml", file=file, content=content)

@app.route("/save", methods=['POST'])
def save():
    name = request.args["name"]
    files = funcs.get_files()
    file = list(filter(lambda x: x['name'] == name, files))[0]
    content = request.form['content']
    open(file['path'], "wb").write(content.encode("ascii"))
    return redirect(url_for('index'))

@app.route("/delete")
def delete():
    name = request.args["name"]
    return name

@app.route("/generate", methods=['POST'])
def generate():
    files = request.form.getlist("file[]")
    valid_files = funcs.get_files()
    files = [x["path"] for x in filter(lambda x: x['name'] in files, valid_files)]
    # return repr(files)
    cnt = generator.generate(files)
    # return "OK"

    name = "slicer.ini"
    resp = make_response(cnt)
    resp.headers["Content-Disposition"] = "attachment; filename={0}".format(name)
    return resp

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=3999, debug=False)
    app.run(host="0.0.0.0", port=3999, debug=True)
