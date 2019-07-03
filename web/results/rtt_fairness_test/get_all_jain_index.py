import os
import json
from pprint import pprint

PATH1 = "./rtt_fairness3/"
PATH2 = "./rtt_fairness4/"

def merge_files_in_path(path):
    wrapper = {}
    for scheme in os.listdir(path):
        dir = path + scheme
        dataPoints = []
        if os.path.isdir(dir):
            for file in os.listdir(dir):
                file_dir = dir + "/" + file
                if file_dir.endswith(".json"):
                    with open(file_dir) as f:
                        tmp = json.loads(f.read())
                        x = tmp["Ratio"]
                        y = tmp["Jain idx"]
                        dataPoints.append({"x":x,"y":y})
            wrapper[scheme] = dataPoints

    with open("jain_" + path[2:-1] + ".json", 'w') as f:
        json.dump(wrapper, f, indent=4)

merge_files_in_path(PATH1)
merge_files_in_path(PATH2)
