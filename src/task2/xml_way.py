"""
The is the way of implementation using XML
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

@profile_each_line
def connect_mongo():
    from pymongo import MongoClient
    """connect to defualt mongo instance at port 27017

    docker run --name mongo -p 27017:27017 mongo -d

    """

    client = MongoClient('localhost', 27017)
    db = client.ganga_test
    return db

