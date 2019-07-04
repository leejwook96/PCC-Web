import json
import os
import math

PATH3 = './rtt_fairness3/'
PATH4 = './rtt_fairness4/'

def get_time_thpt_from_json(json_file):
    points = []
    json_obj = json.load(open(json_file, 'r'))
    start_time = float(json_obj['Events'][0]['Time'])
    mean_thrput = 0
    for e in json_obj['Events']:
        data = {'Time':float(e['Time']) - start_time, 'Throughput':e['Throughput'], 'Avg Rtt': e['Avg Rtt']}
        mean_thrput += float(e['Throughput'])
        points.append(data)

    return points, mean_thrput / len(json_obj['Events'])

def jain_index(mean_thrput):
    sum_sq = sum(mean_thrput) ** 2
    sqrd_sum = sum([math.pow(x, 2) for x in mean_thrput])

    return sum_sq / (len(mean_thrput) * sqrd_sum)

def get_rtt3():
    for scheme in os.listdir(PATH3):
        path = PATH3 + scheme
        if os.path.isdir(path):
            print(scheme)
            path2 = PATH3 + scheme + "/raw_data/"
            for data in os.listdir(path2):
                if "DS_Store" in data:
                    continue;
                # print(data)
                all_points = {}
                rtt_name = data.split('.')[1]
                # print(rtt_name)
                if os.path.isdir(path2 + data):
                    mean_thrput = []
                    for file in sorted(os.listdir(path2 + data)):
                        path3 = path2 + data + '/'
                        if (file.endswith(".json")) and ("orig" not in file) and ("metadata" not in file):
                            points, thpt = get_time_thpt_from_json(path3 + file)
                            #print(points)
                            mean_thrput.append(thpt)
                            flow_name = file.split('.')[1]
                            all_points['flow'+flow_name[-1]] = points
                print(rtt_name)

                flows = rtt_name.split('_to_')
                flows = [int(x[:-2]) for x in flows]
                i = 1
                for flow in flows:
                    all_points['flow'+str(i)+" lat"] = flow
                    i += 1
                all_points['Ratio'] = flows[1] / flows[0]
                all_points['Jain idx'] = jain_index(mean_thrput)

                filename = PATH3 + scheme + "/" + rtt_name + ".json"
                with open(filename, 'w') as f:
                    json.dump(all_points, f, indent=4)

def get_rtt4():
    for scheme in os.listdir(PATH4):
        path = PATH4 + scheme
        if os.path.isdir(path):
            print(scheme)
            path2 = PATH4 + scheme + "/raw_data/"
            for data in os.listdir(path2):
                if "DS_Store" in data:
                    continue;
                # print(data)
                all_points = {}
                rtt_name = data.split('.')[1]
                # print(rtt_name)
                if os.path.isdir(path2 + data):
                    mean_thrput = []
                    for file in sorted(os.listdir(path2 + data)):
                        path3 = path2 + data + '/'
                        if (file.endswith(".json")) and ("orig" not in file) and ("metadata" not in file):
                            points, thpt = get_time_thpt_from_json(path3 + file)
                            #print(points)
                            mean_thrput.append(thpt)
                            flow_name = file.split('.')[1]
                            all_points['flow'+flow_name[-1]] = points
                print(rtt_name)

                flows = rtt_name.split('_to_')
                flows = [int(x[:-2]) for x in flows]
                i = 1
                for flow in flows:
                    all_points['flow'+str(i)+" lat"] = flow
                    i += 1
                all_points['Ratio'] = flows[1] / flows[0]
                all_points['Jain idx'] = jain_index(mean_thrput)

                filename = PATH4 + scheme + "/" + rtt_name + ".json"
                with open(filename, 'w') as f:
                    json.dump(all_points, f, indent=4)

get_rtt3()
get_rtt4()
