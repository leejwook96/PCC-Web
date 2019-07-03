import os
import sys
import json
import numpy as np

data_dir_to_merge = sys.argv[1]

def validate_attr(data_list, attr):
    if attr is None:
        raise ValueError("Attr cannot be None")
        return
    if attr not in data_list[0]:
        raise KeyError()
        return

def get_sum_of_attr(data_list, attr=None):
    validate_attr(data_list, attr)
    return sum([float(x[attr]) for x in data_list])

def get_mean_of_attr(data_list, attr=None):
    validate_attr(data_list, attr)
    arr = []
    for x in data_list:
        d = float(x[attr])
        if d != -1:
            arr.append(d)
        else:
            arr.append(0)
    return np.mean(arr)

def get_ith_time(event, i):
    return float(event[i]["Time"])

def get_batch_size(data_dict, nearest=1):
    nearest_ms = nearest * 1000
    time_til_now = 0

    events = data_dict['Events']
    i = 0
    while time_til_now < nearest_ms:
        time_til_now += (get_ith_time(events, i + 1) - get_ith_time(events, i))
        i += 1

    return i

def merge_n_logs(data_list):
    """
    Given n events it merges the events into 1 event
    'Five Percent Rtt', 'Name', 'Avg Rtt', 'Max Rtt', 'Min Rtt' are neglected
    """
    data_dict = {"Loss Rate": get_mean_of_attr(data_list, "Loss Rate"),
                 "Avg Rtt": get_mean_of_attr(data_list, "Avg Rtt"),
                 "Acks Received": get_sum_of_attr(data_list, "Acks Received"),
                 "Target Rate": get_mean_of_attr(data_list, "Target Rate"),
                 "Rtt Inflation": get_mean_of_attr(data_list, "Rtt Inflation"),
                 "Throughput" : get_mean_of_attr(data_list, "Throughput"),
                 "Packets Sent": get_sum_of_attr(data_list, "Packets Sent"),
                 "Time": data_list[0]["Time"],
                 }

    return data_dict

def merge_logs_by_batch_size(data_dict, batch_size):
    all_data = []
    i = 0
    data_list = data_dict['Events']
    while i < len(data_list):
        all_data.append(merge_n_logs(data_list[i : i + batch_size]))
        i += batch_size
    if len(data_list[i:]) > 0:
        all_data.append(merge_n_logs(data_list[i:]))

    return {"Events" : all_data}

def merge_logs_in_dir(dir_to_merge):
    for scheme in os.listdir(dir_to_merge):
        if os.path.isdir(dir_to_merge + '/' + scheme):
            dir = dir_to_merge + '/' + scheme + '/raw_data/'
            for data in os.listdir(dir):
                if os.path.isdir(dir + data):
                    for file in os.listdir(dir + data):
                        base_dir = dir + data + '/'
                        if not file.startswith(".DS_") and file.endswith('.json') and 'metadata' not in file:
                            with open(base_dir + file) as f:
                                orig_data = json.load(f)

                            batch_size = get_batch_size(orig_data)
                            merged_data = merge_logs_by_batch_size(orig_data, batch_size)

                            with open(base_dir + file[:-5] + '_orig.json', 'w') as f:
                                json.dump(orig_data, f, indent=4)

                            with open(base_dir + file[:-5] + '.json', 'w') as f:
                                json.dump(merged_data, f, indent=4)

if __name__ == '__main__':
    merge_logs_in_dir(data_dir_to_merge)
