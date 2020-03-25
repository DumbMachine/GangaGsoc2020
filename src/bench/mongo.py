import os
import time
import json
import utils
import matplotlib.pyplot as plt

from copy import copy
from pymongo import MongoClient
from joblib import Parallel, delayed

if not os.path.isdir("benchmarks"):
    os.makedirs("benchmarks")

filename = f"benchmarks/mongo.json"

# loading the json data
def do_work(filename):
    ITERS = 100
    INFORMATION = {
        "push": [],
        "pull": []
    }
    JOB = json.load(open("job.json", "r"))

    # starting the database instance
    client = MongoClient()
    db = client.ganga_test


    for _ in range(ITERS):
        job = copy(JOB)
        st = time.time()
        db.ganga_jobs.insert_one(job)
        dt = time.time() - st
        INFORMATION['push'].append(dt)

    # Check if the insertions were sucecessful
    st = time.time()
    rows = [*db.ganga_jobs.find()]
    INFORMATION['push'].append(time.time() - st)
    assert len(rows) == ITERS

    json.dump(
        INFORMATION,
        open(filename, "w+")
    )    
    open("benchmarks/pid", "w+").write(str(os.getpid()))
    print("Script running is now down\n")

funcs = [utils.docker_stats, do_work]


try:
    Parallel(n_jobs=2, backend="threading")(delayed(func)(filename) for func in funcs)
except Exception:
    print("Killed both threads, successfully exiting now")

