#!/usr/bin/python
import yaml
import options_map
# from . import options_map

def mergeSettings(a, b):
	for k,v in b.items():
		if k == "include":
			continue
		if isinstance(v, dict):
			if k not in a:
				a[k] = {}
			mergeSettings(a[k], v)
		else:
			a[k] = v

def processInclude(path):
	data = yaml.load(open(path))
	newData = {}
	if "include" in data:
		for incl in data["include"]:
			tmp = processInclude(incl + ".yaml")
			mergeSettings(newData, tmp)
	mergeSettings(newData, data)
	return newData

def traverseSettings(f, v, path = ""):
	for k,v in v.items():
		spath = (path + "." + k).lstrip(".")
		if isinstance(v, dict):
			traverseSettings(f, v, spath)
		else:
			processSetting(f, spath, v)
	
def processSetting(f, k, v):
	if k in options_map.optionsMap:
		slicerName = options_map.optionsMap[k]
		f.write("{0} = {1}\n".format(slicerName, v).encode("ascii"))
	else:
		raise Exception("no setting " + k)
		# print(slicerName, v)

data = processInclude("settings.yaml")
print(data)
print(yaml.dump(data))

f = open("/tmp/slicer.settings", "wb")
traverseSettings(f, data)
f.close()
