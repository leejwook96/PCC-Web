import os
import json
from pprint import pprint
import numpy as np

PATH1 = "/Users/jaewooklee/pcc-web/web/results/rtt_fairness_test/rtt_fairness3/"
PATH2 = "/Users/jaewooklee/pcc-web/web/results/rtt_fairness_test/rtt_fairness4/"

def merge_files_in_path(path, name):
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

                        for dp in dataPoints:
                            ratio = dp['x']
                            if ratio == x:
                                dp['y'].append(y)
                                continue

                        dataPoints.append({"x":x,"y":[y]})

            wrapper[scheme] = dataPoints

    for scheme, datas in wrapper.items():
        for data in datas:
            data['y'] = np.mean(data['y'])

    with open(path + "../jain_" + name + ".json", 'w') as f:
        json.dump(wrapper, f, indent=4)


merge_files_in_path(PATH1, 'rtt_fairness3')
merge_files_in_path(PATH2, 'rtt_fairness4')
