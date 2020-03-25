import copy
import json
import os
import pickle
import subprocess
import time
from glob import glob
from threading import Thread

import matplotlib.pyplot as plt
import pymongo
from joblib import Parallel, delayed
from pymongo import MongoClient
from tqdm import tqdm

import docker

TIMES = {}

def bench_func(func):
    """
    A timer decorator
    """
    def function_timer(*args, **kwargs):
        """
        A nested function for timing other functions
        """
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        msg = "The runtime for {func} was {time} seconds."
        print(msg.format(func=func.__name__,
                         time=runtime))
        TIMES[func.__name__] = runtime
        return value
    return function_timer


@bench_func
def load_pickle_data(size=100000):
    jobs = pickle.load(open("../../data/rows.pkl", "rb"))[:size]
    jobs= [[i]+row[1:] for i, row in enumerate(jobs)]

    _blobs = pickle.load(open("../../data/blobs.pkl", "rb"))[:size]
    blobs = []
    for i, blo in enumerate(_blobs):
        blob = copy.deepcopy(blo)
        blob["jid"] = i
        blobs.append(blob)
    return jobs, blobs




@bench_func
def load_pickle_data_batch(size=100000):
    jobs = pickle.load(open("../../data/rows.pkl", "rb"))[:size]
    rows = []
    for itr, job in enumerate(jobs):
        row = {}
        for header, value in zip(
            ['jid', 'status', 'name', 'subjobs', 'application',
            'backend', 'backend_actualCE', 'comment'],
            job
        ):
            row[header] = value

        row["jid"] = itr
        rows.append(row)
    jobs = rows


    _blobs = pickle.load(open("../../data/blobs.pkl", "rb"))[:size]
    blobs = []
    for i, blo in enumerate(_blobs):
        # FIXME: Dirty patch, for some reason any change to a single element fof blobs array, goes to all the elements. I decided to create copies after failing to debug this at that time.
        blob = copy.deepcopy(blo)
        blob["jid"] = i
        blobs.append(blob)
    return jobs, blobs

# def docker_stats(name, interval, filename):
#     client = docker.from_env()
#     if not os.path.isfile(filename):
#         json.dump({"stats": []}, open(filename, "w"))
#     while True:
#         found_container = False
#         time.sleep(interval)

#         for container in client.containers.list():
#             if container.name == name:
#                 try:
#                     found_container = True
#                     data = json.load(open(filename, "r"))
#                     data["stats"].append(container.stats(stream=False))
#                     json.dump(data, open(filename, "w+"))
#                 except json.decoder.JSONDecodeError:
#                     print(f"I guess you have stopped {name} container now")

#         if not found_container:
#             print("Coudn't find the container, exiting now")
#             exit(0)


def docker_stats(filename):
    print("Docker thread is listening now")
    filename = filename.replace(".json", "-resources.json")
    name="mongo"
    interval = 0
    things = {
        'CONTAINER ID': None,
        'NAME': None,
        'CPU %': None,
        'MEM USAGE/LIMIT': None,
        'MEM %': None,
        'NET I/O': None,
        'BLOCK I/O': None,
        'PIDS': None
    }
    if not os.path.isfile(filename):
        json.dump({"stats": []}, open(filename, "w+"))

    proc = subprocess.Popen(["sudo", "docker",  "stats"],stdout=subprocess.PIPE)
    while True:
        # time.sleep(interval)
        line = proc.stdout.readline()
        if not line:
            break
        if "CPU %" not in line.decode("utf-8"):
            items = line.decode("utf-8").split()
            things["CONTAINER ID"] = items[0]
            things['NAME'] = items[1]
            things['CPU %'] = items[2]
            things['MEM USAGE/LIMIT'] = " ".join(items[3:6])
            things['MEM %'] = items[6]
            things['NET I/O'] = " ".join(items[7:10])
            things['BLOCK I/O'] = " ".join(items[10:-2])
            things['PIDS'] = items[-1]
            things['TIME'] = time.time()

            data = json.load(open(filename, "r"))
            data["stats"].append(things)
            json.dump(data, open(filename, "w+"))


        pids = glob("benchmarks/pid")
        if pids:
            for pid in pids:
                os.remove(pid)
            print("exiting the docker thread nw")
            raise Exception
            os._exit()
