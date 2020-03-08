"""
The is the way of implementation using
"""
import os
from tqdm import tqdm
TIMES = {}

def profile_func(func, store):
    """
    A timer decorator
    """
    def function_timer(*args, **kwargs):
        """
        A nested function for timing other functions
        """
        import time
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

def store_job(jid, bind_id, db=None):
    """

    """
    if db is None:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client.ganga_eval

    import io
    import sys
    job = jobs[jid]
    stdout = sys.stdout
    sys.stdout = io.StringIO()

    full_print(job)

    # get output and restore sys.stdout
    output = sys.stdout.getvalue()
    sys.stdout = stdout

    db.jobs.insert({"jid": bind_id, "string": output})

def get_job(jid, db=None):
    """

    """
    if db is None:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client.ganga_eval

    return [item['string'].strip() for item in db.jobs.find({"jid": jid})]

def main(asrt=True):
    jid = -1
    job = jobs[-1]
    store_job(jid)
    db_job = get_job(jid)

    # Comparing the jobs
    import io
    import sys
    job = jobs[jid]
    stdout = sys.stdout
    sys.stdout = io.StringIO()

    full_print(job)

    # get output and restore sys.stdout
    output = sys.stdout.getvalue()
    sys.stdout = stdout

    if asrt:
        assert output.strip() == db_job[0].strip()
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
            progress.update(1)

    import matplotlib.pyplot as plt
    import numpy as np
    plt.plot([i[0] for i in times], "-b", label="store_job")
    plt.plot([i[1] for i in times], "-r", label="get_job")
    plt.plot([i[2] for i in times], "-g", label="total_time")
    plt.yticks(np.arange(0, 1, step=0.1))
    plt.title("Mongo Bench")
    plt.legend(loc="best")
    plt.savefig(f'data/mongo-method-full_print-{iterations}-time_interval-{sleep}.png')
    plt.clf()

    plt.plot([i[0] for i in times[2:]], "-b", label="store_job")
    plt.plot([i[1] for i in times[2:]], "-r", label="get_job")
    plt.plot([i[2] for i in times[2:]], "-g", label="total_time")
    plt.yticks(np.arange(0, 0.5, step=0.1))
    plt.title("Mongo Bench")
    plt.legend(loc="best")
    plt.savefig(f'data/[modded]mongo-method-full_print-{iterations}-time_interval-{sleep}.png')


# stress_test()
stress_test()


"""
sudo docker stop mongo; sudo docker rm mongo;
sudo docker stop postgres; sudo docker rm postgres;

sudo docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=ganga -d postgres
sudo docker run --name mongo -p 27017:27017 -d mongo;
"""