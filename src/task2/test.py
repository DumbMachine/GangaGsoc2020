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

@profile_each_line
def store_job(jid, db=None):

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

    db.jobs.insert({str(jid): output})

@profile_each_line
def connect_mongo():
    from pymongo import MongoClient
    """connect to defualt mongo instance at port 27017

    docker run --name mongo -p 27017:27017 mongo -d

    """

    client = MongoClient('localhost', 27017)
    db = client.ganga_test
    return db

def add_jobs_mongo(db, jobs=None, blobs=None, batch_size=False):
    """inserts the jobs in mongo instance"""
    # jobs = [{"data":row} for i, row in enumerate(jobs)]
    if jobs:
        if not batch_size or batch_size > len(jobs):
            try:
                db.jobs.insert_many(jobs)
            except pymongo.errors.BulkWriteError as bwe:
                print(bwe.details)
                raise

            return

        with tqdm(total=len(jobs)/batch_size) as progress:
            start = 0
            for batch in range(batch_size, len(jobs)+1, batch_size):
                try:
                    db.jobs.insert_many(jobs[start:batch])
                except pymongo.errors.BulkWriteError as bwe:
                    print(bwe.details)
                    raise

                start = batch
                progress.update(1)