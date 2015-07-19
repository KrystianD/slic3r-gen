#!/usr/bin/python
import yaml, argparse, os
import options_map
from io import StringIO

includedPaths = []

def mergeSettings(a, b):
    for k, v in b.items():
        if k == "include":
            continue
        if isinstance(v, dict):
            if k not in a:
                a[k] = {}
            mergeSettings(a[k], v)
        else:
            a[k] = v

def processInclude(path):
    path = os.path.realpath(path)
    # if path in includedPaths:
        # print("path {0} already included".format(path))
        # exit(1)
    includedPaths.append(path)
    data = yaml.load(open(path))
    newData = {}
    # if "include" in data:
        # for incl in data["include"]:
            # tmp = processInclude(incl + ".yaml")
            # mergeSettings(newData, tmp)
    mergeSettings(newData, data)
    return newData

def traverseSettings(f, v, path=""):
    for k, v in v.items():
        spath = (path + "." + k).lstrip(".")
        if isinstance(v, dict):
            traverseSettings(f, v, spath)
        else:
            processSetting(f, spath, v)

def convertSetting(v):
    if isinstance(v, str):
        v = v.replace("\n", "\\n")
        return v
    if isinstance(v, bool):
        if v:
            return "1"
        else:
            return "0"
    return v

def processSetting(f, k, v):
    if k in options_map.optionsMap:
        slicerName = options_map.optionsMap[k]
        v = convertSetting(v)
        f.write(u"{0} = {1}\n".format(slicerName, v))
    else:
        raise Exception("no setting " + k)

def makeTree(name, value):
    tree = {}
    if "." in name:
        (name, sub) = name.split(".", 1)
        tree[name] = makeTree(sub, value)
    else:
        tree[name] = value
    return tree

def generate(files, custom = ""):
    data = {}
    # print(custom)
    for path in files:
        newData = processInclude(path)
        mergeSettings(data, newData)

    for custom in custom.split("\n"):
        custom = custom.strip()
        if len(custom) == 0:
            continue
        (name, value) = custom.split("=", 1)
        newData = makeTree(name, value)
        mergeSettings(data, newData)
    # print(data)
    # print(yaml.dump(data))

    f = StringIO()
    traverseSettings(f, data)
    cnt = f.getvalue()
    f.close()
    return cnt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--custom', type=str)
    parser.add_argument('files', metavar='config_file', type=str, nargs='+')
    args = parser.parse_args()

    f = open("/tmp/slicer.ini", "wb")
    f.write(generate(args.files, args.custom).encode("ascii"))
    f.close()
