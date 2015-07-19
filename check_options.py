import options_map

cnt = open("base.ini", "rb").read().decode('ascii').split("\n")
got = (options_map.optionsMap.values())


for item in cnt:
    item = item.strip().replace(" = ", "=")
    if len(item)==0:
        continue
    (name, val) = item.split("=")

    if not name in got:

        print(name)
