import glob, os

conf_dir = "configs/"

def get_files():
    files = []
    for path in glob.glob(conf_dir + "*.yaml"):
        files.append({
            'path': path,
            'name': os.path.basename(path),
        })
    return files
