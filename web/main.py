from flask import Flask, abort, redirect, url_for, request, make_response, \
        render_template, session, Markup
# from urllib.parse import quote
app = Flask(__name__)
app.jinja_env.line_statement_prefix = '#'

execfile("config.py")

app.secret_key = secret_key

import os, subprocess, shlex, select, time, signal, fcntl, pipes, glob, sys

conf_dir = "configs/"

import funcs
sys.path.append("..")
import generator
import options_map

@app.route("/")
def index():
    files = funcs.get_files()
    return render_template("index.xhtml", files=files)

@app.route("/edit/<name>")
def edit(name):
    files = funcs.get_files()
    file = funcs.get_file_by_name(name)
    content = open(file['path'], "rb").read().decode("ascii")
    return render_template("edit.xhtml", file=file, content=content)

@app.route("/newfile")
def newfile():
    name = request.args["name"]
    path = funcs.make_path(name)
    open(path, "wb")
    return redirect(url_for('index'))

@app.route("/rename")
def rename():
    old = request.args["old"]
    new = request.args["new"]
    
    oldPath = funcs.get_file_by_name(old)['path']
    newPath = funcs.make_path(new)

    print(oldPath, newPath)
    if not os.path.exists(newPath):
        os.rename(oldPath, newPath)

    return redirect(url_for('index'))

@app.route("/save", methods=['POST'])
def save():
    name = request.args["name"]
    files = funcs.get_files()
    file = funcs.get_file_by_name(name)
    content = request.form['content']
    open(file['path'], "wb").write(content.encode("ascii"))
    return redirect(url_for('index'))

@app.route("/delete")
def delete():
    name = request.args["name"]
    file = funcs.get_file_by_name(name)
    os.unlink(file['path'])
    return redirect(url_for('index'))

@app.route("/options_list")
def options_list():
    options = sorted(options_map.optionsMap.keys())
    return render_template("options.xhtml", options=options)

@app.route("/generate", methods=['POST'])
def generate():
    files = request.form.getlist("file[]")
    custom = request.form['custom']
    session['custom'] = custom
    valid_files = funcs.get_files()
    print("KD", valid_files)
    files = [x["path"] for x in filter(lambda x: (x['name'] in files or x['required']) and x['state'] == 'ok', valid_files)]
    # return repr(files)
    # return "OK"

    cmd = request.form['cmd']

    if cmd == "generate":
        cnt = generator.generate(files, custom)
        name = "slicer.ini"
        resp = make_response(cnt)
        resp.headers["Content-Disposition"] = "attachment; filename={0}".format(name)
        # return "A"
        return resp
    elif cmd == "preview cfg":
        cnt = generator.generate(files, custom, forSlicer=False)
        return Markup(cnt.replace("\n", "<br/>"))
    elif cmd == "preview":
        cnt = generator.generate(files, custom, forSlicer=True)
        return Markup(cnt.replace("\n", "<br/>"))

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=3999, debug=False)
    app.run(host="0.0.0.0", port=3999, debug=True)
