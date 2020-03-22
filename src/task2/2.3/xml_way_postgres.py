"""
This is WIP
"""
"""
The is the way of implementation using
"""
import os
import io
import sys
import sqlalchemy

from tqdm import tqdm
from GangaCore.Core.GangaRepository.VStreamer import to_file, from_file
from GangaCore.GPIDev.Base.Proxy import addProxy, stripProxy


def create_table(con, meta):
    from sqlalchemy import Binary, Column, ForeignKey, Integer, String, Table
    JOBS = Table(
        f"jobs", meta,
        Column("jid", Integer, primary_key=True),
        Column("jstring", String),
        extend_existing=True
    )
    meta.create_all(con)
    return JOBS

def store_job(jid, bind_id, JOBS=None):
    """

    """
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

    if JOBS is None:
        JOBS = create_table(con, meta)


    job = stripProxy(jobs[jid])
    stdout = sys.stdout
    sys.stdout = io.StringIO()
    to_file(job)
    output = sys.stdout.getvalue()
    sys.stdout = stdout

    con.execute(JOBS.insert(), {"jid": bind_id, "jstring": output})

def get_job(jid, db=None):
    """

    """

    class StringJob:
        def __init__(self, string_rep):
            self.string_rep = string_rep

        def read(self):
            return self.string_rep.strip()

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

    rows = [StringJob(item['jstring'].strip()) for item in con.execute(
        f"""SELECT * from jobs
            WHERE jid = {jid}
        """)]

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
    plt.yticks(np.arange(0, np.max(times), step=0.05))
    plt.title("Postgres Bench")
    plt.xlabel("iteration")
    plt.ylabel("time(seconds)")
    plt.legend(loc="best")
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(8,8)
    plt.savefig(f'data/postgres-method-xml-{iterations}-time_interval-{sleep}.png')
# stress_test()
stress_test()
