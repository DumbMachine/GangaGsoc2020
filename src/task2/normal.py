"""
The is the way of implementation using
"""
import os
from decorator import decorator

@decorator
def profile_each_line(func, *args, **kwargs):
    from line_profiler import LineProfiler
    profiler = LineProfiler()
    profiled_func = profiler(func)
    try:
        return profiled_func(*args, **kwargs)
    finally:
        profiler.print_stats()

def connect_mongo():
    from pymongo import MongoClient
    """connect to defualt mongo instance at port 27017

    docker run --name mongo -p 27017:27017 mongo -d

    """

    client = MongoClient('localhost', 27017)
    db = client.ganga_test
    return db

def store_job(jid, db=None):
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

    db.jobs.insert({"jid": jid, "string": output})

def get_job(jid, db=None):
    """

    """
    if db is None:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client.ganga_eval

    return [item['string'].strip() for item in db.jobs.find({"jid": jid})]
