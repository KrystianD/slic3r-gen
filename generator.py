#!/usr/bin/python
import yaml, argparse, os, re
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

def processInclude(path, allow_include=False):
    path = os.path.realpath(path)
    if allow_include:
        if path in includedPaths:
            print("path {0} already included".format(path))
            exit(1)
    includedPaths.append(path)
    content = fixYaml(open(path).read())
    data = yaml.load(content)
    newData = {}
    if allow_include:
        if "include" in data:
            for incl in data["include"]:
                tmp = processInclude(incl + ".yaml")
                mergeSettings(newData, tmp)
    mergeSettings(newData, data)
    return newData

def traverseSettings(f, v, path="", forSlicer=True):
    for k, v in v.items():
        spath = (path + "." + k).lstrip(".")
        if isinstance(v, dict):
            traverseSettings(f, v, spath, forSlicer=forSlicer)
        else:
            processSetting(f, spath, v, forSlicer=forSlicer)

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

def processSetting(f, k, v, forSlicer=True):
    if k in options_map.optionsMap:
        if forSlicer:
            k = options_map.optionsMap[k]
        v = convertSetting(v)
        f.write(u"{0} = {1}\n".format(k, v))
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

def makeValidYamlTree(tree):
    
    print(tree)
    for opt in tree.keys():
        print("A", opt)
        if "." in opt:
            q = makeTree(opt, tree[opt])
            tree.update(q)
            del tree[opt]

        else:
            if isinstance(tree[opt], dict):
                makeValidYamlTree(tree[opt])

    return tree

def fixYaml(txt):
    out = ""
    for line in txt.split("\n"):
        if "=" in line:
            line = re.sub("\s*=\s*", ": ", line)
        out += line + "\n"
    return out

def generate(files, custom="", forSlicer=True):
    data = {}
    # print(custom)
    for path in files:
        newData = processInclude(path)
        mergeSettings(data, newData)

    print("C", custom)
    custom = fixYaml(custom)
    customConfig = yaml.load(custom)
    if customConfig is None:
        customConfig = {}
    print("F", customConfig)
    customConfig = makeValidYamlTree(customConfig)
    print("K", customConfig)

    mergeSettings(data, customConfig)
    # print(data)
    # print(yaml.dump(data))

    f = StringIO()
    traverseSettings(f, data, forSlicer=forSlicer)
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
