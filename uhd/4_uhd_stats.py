import json
import os
import time

import keyboard
import requests
from tabulate import tabulate

port_names = [
    "Port 1", "Port 2",
    #"Port 3", "Port 4", "Port 5", "Port 6", "Port 7", "Port 8", 
    #"Port 9", "Port 10", "Port 11", "Port 12", "Port 13", "Port 14", "Port 15", "Port 16",
    "Port 25", "Port 26", "Port 27", "Port 28", "Port 29", "Port 30", "Port 31", "Port 32",
]
metrics = ["frames_received_all", "frames_received_unicast", "frames_transmitted_all", "frames_transmitted_unicast", "frames_dropped_egress"]
metricssss = [
    "bytes_received_all",
    "bytes_transmitted_all",
    "frames_dropped_egress",
    "frames_received_all",
    "frames_received_broadcast",
    "frames_received_errors",
    "frames_received_length_1024_1518",
    "frames_received_length_128_255",
    "frames_received_length_1519_2047",
    "frames_received_length_2048_4095",
    "frames_received_length_256_511",
    "frames_received_length_512_1023",
    "frames_received_length_64",
    "frames_received_length_65_127",
    "frames_received_multicast",
    "frames_received_pause",
    "frames_received_priority_pause",
    "frames_received_unicast",
    "frames_transmitted_all",
    "frames_transmitted_broadcast",
    "frames_transmitted_length_1024_1518",
    "frames_transmitted_length_128_255",
    "frames_transmitted_length_1519_2047",
    "frames_transmitted_length_2048_4095",
    "frames_transmitted_length_256_511",
    "frames_transmitted_length_512_1023",
    "frames_transmitted_length_64",
    "frames_transmitted_length_65_127",
    "frames_transmitted_multicast",
    "frames_transmitted_pause",
    "frames_transmitted_priority_pause",
    "frames_transmitted_unicast",
#    "link_status"
]

url = 'http://10.36.79.210:80/connect/api/v1/metrics/operations/query'
stats = {
    "port_metrics": {
        "port_names": port_names,
        "select_metrics": metrics
    }
}

headers = {"content-type": "application/json"}


print('init stats to 0')
resp = requests.post(url=url, data=json.dumps(stats), headers=headers, verify=False)
start_stats = resp.json()
# pprint.pprint(start_stats)

print(resp.url)


def clear():

    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


while True:
    if keyboard.is_pressed("q"):
        print("stat collection stopped")
        break
    if keyboard.is_pressed("c"):
        print("stat cleared")
        resp = requests.post(url=url, data=json.dumps(stats), headers=headers, verify=False)
        start_stats = resp.json()

    resp = requests.post(url=url, data=json.dumps(stats), headers=headers, verify=False)
    now_stats = resp.json()

    table = []

    for metric in metrics:
        row = []
        row.append(metric)
        for port_name in port_names:
            try:
                for start_stat in start_stats['port_metrics']['metrics']:
                    if port_name == start_stat['port_name']:
                        start_value = start_stat['metrics'][metric]
                for now_stat in now_stats['port_metrics']['metrics']:
                    if port_name == now_stat['port_name']:
                        row.append(int(now_stat['metrics'][metric]) - int(start_value))
            except KeyError:
                print(start_stats)

        table.append(row)

    clear()
    print(tabulate(table, headers=port_names, tablefmt="github"))

    time.sleep(1)