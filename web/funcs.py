import glob, os, yaml

conf_dir = os.path.abspath("configs/") + "/"

def get_files():
    files = []
    print(conf_dir)
    for path in glob.glob(conf_dir + "*.yaml"):
        obj = {
            'path': path,
            'name': os.path.basename(path).split(".")[0],
        }
        load_file(obj, path)
        files.append(obj)
    return files

def load_file(obj, path):
    data = yaml.load(open(path))
    try:
        meta = data['meta']
        obj['category'] = meta['category']
        obj['required'] = meta.get('required', False)
        obj['state'] = 'ok'
    except TypeError:
        obj['state'] = 'error'

def get_file_by_name(name):
    files = get_files()
    return list(filter(lambda x: x['name'] == name, files))[0]

def make_path(name):
    path = os.path.realpath(conf_dir + "/" + name)
    # print(path, conf_dir)
    if not path.startswith(conf_dir):
        raise Exception("invalid name " + name)

    if not path.endswith(".yaml"):
        if "." in path:
            raise Exception("invalid name " + name)
        else:
            path += ".yaml"

    return path
