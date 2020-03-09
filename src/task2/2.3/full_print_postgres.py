"""
The is the way of implementation using
"""
import os
import sqlalchemy
from sqlalchemy import Binary, Column, ForeignKey, Integer, String, Table

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

def create_table(con, meta):
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

    import io
    import sys
    job = jobs[jid]
    stdout = sys.stdout
    sys.stdout = io.StringIO()

    full_print(job)

    # get output and restore sys.stdout
    output = sys.stdout.getvalue()
    sys.stdout = stdout

    con.execute(JOBS.insert(), {"jid": bind_id, "jstring": output})

def get_job(jid, db=None):
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

    rows = [*con.execute(f"""
        SELECT * from jobs
        WHERE jid = {jid}
    """)]

    return [item['jstring'].strip() for item in rows]

def main(asrt=True):
    import random
    jid = -1
    bind_id = random.randint(0, 1000)
    job = jobs[-1]
    store_job(jid, bind_id=bind_id)
    db_job = get_job(bind_id)

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
    import matplotlib
    import numpy as np
    plt.plot([i[0] for i in times], "-b", label="store_job")
    plt.plot([i[1] for i in times], "-r", label="get_job")
    plt.plot([i[2] for i in times], "-g", label="total_time")
    plt.yticks(np.arange(0, np.max(times), step=0.05))
    plt.title("Postgres Bench")
    plt.legend(loc="best")
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.savefig(f'data/postgres-method-full_print-{iterations}-time_interval-{sleep}.png', dpi=100)
# stress_test()
stress_test()
