import os
import time
import json
import utils
import sqlalchemy
import matplotlib.pyplot as plt

from copy import copy
from sqlalchemy import ( Binary, Column, ForeignKey, Integer, String, Table, JSON )

from joblib import Parallel, delayed

if not os.path.isdir("benchmarks"):
    os.makedirs("benchmarks")

filename = f"benchmarks/postgres.json"

# loading the json data
def do_work(filename):
    ITERS = 100
    INFORMATION = {
        "push": [],
        "pull": []
    }
    JOB = json.load(open("job.json", "r"))

    # starting the database instance

    user, password, db, host, port = 'postgres', 'ganga', 'jobs', 'localhost', 5432

    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    try:
        con = sqlalchemy.create_engine(url, client_encoding='utf8',  executemany_mode='batch')
        meta = sqlalchemy.MetaData(bind=con, reflect=True)
    except Exception as e:
        if "does not exist" in str(e):
            url = 'postgresql://{}:{}@{}:{}/template1'
            url = url.format(user, password, host, port)
            con = sqlalchemy.create_engine(url, client_encoding='utf8')
            meta = sqlalchemy.MetaData(bind=con, reflect=True)
        else:
            raise e



    JOBS = Table(
        "jsontable", meta,
        Column("outputsandbox", String),
        Column("comment", String),
        Column("id", String, primary_key=True),
        Column("status", String),
        Column("name", String),
        Column("inputdir", String),
        Column("outputdir",String),
        Column("do_auto_resubmit", String),
        Column("parallel_submit", String),
        Column("inputsandbox", String),
        Column("info", JSON),
        Column("time", JSON),
        Column("application", JSON),
        Column("backend", JSON),
        Column("inputfiles", JSON),
        Column("outputfiles", JSON),
        Column("splitter", JSON),
        Column("postprocessors", JSON),
        Column("metadata", JSON),
        Column("non_copyable_outputfiles", String),
        Column("inputdata", String),
        Column("outputdata", String),
        Column("subjobs", String),
        Column("virtualization", String),
        extend_existing=True
            )

    meta.create_all()

    for _ in range(ITERS):
        job = copy(JOB)
        job['id'] = _
        st = time.time()
        statement = JOBS.insert().values(job)
        con.execute(statement)
        dt = time.time() - st
        INFORMATION['push'].append(dt)
    # Check if the insertions were sucecessful
    st = time.time()
    rows = [*con.execute("SELECT * FROM jsontable")]
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

