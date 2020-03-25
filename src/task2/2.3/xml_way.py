"""
This is WIP
"""
"""
The is the way of implementation using
"""
import os
import io
import sys

from tqdm import tqdm
from pymongo import MongoClient
from GangaCore.Core.GangaRepository.VStreamer import to_file, from_file
from GangaCore.GPIDev.Base.Proxy import addProxy, stripProxy


def store_job(jid, bind_id, db=None):
    """

    """

    if db is None:
        client = MongoClient('localhost', 27017)
        db = client.ganga_xml

    job = stripProxy(jobs[jid])

    stdout = sys.stdout
    sys.stdout = io.StringIO()

    to_file(job)

    # get output and restore sys.stdout
    output = sys.stdout.getvalue()
    sys.stdout = stdout

    db.jobs.insert({"jid": bind_id, "string": output})

def get_job(jid, db=None):
    """

    """

    class StringJob:
        def __init__(self, string_rep):
            self.string_rep = string_rep

        def read(self):
            return self.string_rep.strip()

    if db is None:
        client = MongoClient('localhost', 27017)
        db = client.ganga_xml

    rows = [StringJob(item['string']) for item in db.jobs.find({"jid": jid})]

    return [addProxy(from_file(job)[0]) for job in rows]



def main(asrt=True):
    import random
    jid = -1
    bind_id = random.randint(0, 1000)
    job = jobs[-1]
    store_job(jid)
    db_job = get_job(jid)[0]
    assert db_job == job
    print("INFO Assertion was complete and successful")



def stress_test(iterations=1000, sleep=0):
    import time
    times = []
    with tqdm(total=iterations) as progress:
        for itr in range(iterations):
            itr_time = {
                "store_job": 0,
                "get_job": 0,
                "total_time": 0
            }
            time.sleep(sleep)
            st = time.time()
            jid = -1
            bind_id = itr
            job = jobs[-1]
            store_job(jid, bind_id=itr)
            itr_time['store_job'] = time.time() - st
            db_job = get_job(itr)[0]
            itr_time['get_job'] = (time.time() - itr_time['store_job']) - st
            itr_time['total_time'] = time.time() - st
            times.append(list(itr_time.values()))
# assert db_job == job
            progress.update(1)

    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
    plt.plot([i[0] for i in times], "-b", label="store_job")
    plt.plot([i[1] for i in times], "-r", label="get_job")
    plt.plot([i[2] for i in times], "-g", label="total_time")
    plt.yticks(np.arange(0, np.max(times), step=0.008))
    plt.ylim(0, 0.025)
    plt.title("Xml Method")
    plt.xlabel("iteration")
    plt.ylabel("time (in seconds)")
    plt.legend(loc="best")
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(8,8)
    plt.savefig(f'data/mongo-method-xml -{iterations}-time_interval-{sleep}.png', dpi=100)
# stress_test()
stress_test()
