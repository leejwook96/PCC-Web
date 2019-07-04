import json
import os
import sys
import numpy as np
from pprint import pprint

file = '/Users/jaewooklee/pcc-web/web/results/bandwidth_sweep_test/data/pcc/raw_data/' + \
'bandwidth_sweep.2mbps/pcc_test_scheme.flow_1.json'

data_dir = sys.argv[1]
BW = False
LAT = False

default_bw = 30;
default_lat = 30;
if '--bw' in sys.argv:
    BW = True
elif '--lat' in sys.argv:
    LAT = True

with open(file) as f:
    data = json.load(f)

# pprint(data)
# 1. Thrput(link utilization, avg thrput/link capacity)
# 2. 95% percentile Queueing delay(observed latency - base latency[average rtt])
# 3. loss(average of loss rate) Panthon for reference
# 4. Kleinrock's power metric(log(mean throughput / mean 95th percentile delay))

def get95QueueDelay(data, base_latency=30):
    events = data["Events"]
    queueing_delay = []
    for event in events:
        avg_rtt = event['Avg Rtt']
        queueing_delay.append(avg_rtt - base_latency)

    return np.percentile(queueing_delay, 95)

def getAvgThrput(data):
    events = data["Events"]
    thrput = np.array([event['Throughput'] for event in events])
    return np.mean(thrput)

def getLinkUtilization(data, link_capacity=30): #link capacity in mbps
    avgThrput = getAvgThrput(data)
    return avgThrput / (link_capacity * 1e3) * 100

def get95Lat(data):
    events = data["Events"]
    lat = np.array([event['Avg Rtt'] for event in events])
    return np.percentile(lat, 95)

def getAvgLat(data):
    events = data["Events"]
    lat = np.array([event['Avg Rtt'] for event in events])
    return np.mean(lat)

def getAvgLoss(data):
    events = data["Events"]
    loss = np.array([event['Loss Rate'] for event in events])
    return np.mean(loss)

def getKleinrock(data):
    return np.log(getAvgThrput(data) / get95Lat(data))

def getBwFromName(name):
    mbps = name.split('.')[-1]
    mbps = int(mbps.split('mbps')[0])

    return mbps

def getLatFromName(name):
    pass

def getMetricScore(data, name):
    bw = default_bw
    lat = default_lat
    if BW:
        bw = getBwFromName(name)
    elif LAT:
        lat = getLatFromName(name)

    return (getLinkUtilization(data, bw), get95QueueDelay(data, lat), getAvgLoss(data), getKleinrock(data))

print(f"Link Utilization(Average): {getLinkUtilization(data)}")
print(f"95% Queueing Delay: {get95QueueDelay(data)}")
print(f"Average Loss: {getAvgLoss(data)}")
print(f"Kleinrock's Power Metric (Overall): {getKleinrock(data)}")

def getJsonFromData(data, name):
    thrput, lat, loss, overall = getMetricScore(data, name)
    return {"Link Utilization":thrput, "95 Queueing delay":lat, "Avg Loss":loss, "Overall":overall, 'name':name}

def compute_metric_score(dir):
    testname = dir.split('/')[0]
    metrics = {"Metrics" : {testname: {}}}
    for scheme in os.listdir(dir):
        # print(scheme)
        path = dir + '/' + scheme
        if os.path.isdir(path):
            metrics["Metrics"][testname][scheme] = []
            data_dir = path + '/raw_data/'
            for file in os.listdir(data_dir):
                file_path = data_dir + file
                if os.path.isdir(file_path):
                    for logdata in os.listdir(file_path):
                        if logdata.endswith('json') and 'metadata' not in logdata and 'orig' not in logdata:
                            filedir = file_path + '/' + logdata
                            with open(filedir) as f:
                                data = json.load(f)
                            metrics["Metrics"][testname][scheme].append(getJsonFromData(data, file))
    pprint(metrics)

    outfile = dir.split('/')[0] + '/metrics.json'
    with open(outfile, 'w') as f:
        f.write(json.dumps(metrics, indent=4))

compute_metric_score(data_dir)
