"""
This uses the export() and load() functions
"""
"""
The is the way of implementation using
"""
import os
from decorator import decorator

TEMP_LOCATION = os.path.expanduser("~/temp")

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
    TEMP_LOCATION = os.path.expanduser("~/temp")
    if db is None:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client.ganga_export_load

    export(
        jobs[jid], os.path.join(TEMP_LOCATION, str(jid))
    )
    with open(os.path.join(TEMP_LOCATION, str(jid)), "r") as file:
        job_metadata = file.read()

    db.jobs.insert({"jid": jid, "string": job_metadata})

def get_job(jid, db=None):
    """

    """
    TEMP_LOCATION = os.path.expanduser("~/temp")
    if db is None:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client.ganga_export_load

    return [load(item['string']) for item in db.jobs.find({"jid": jid})]


def load_job(string_rep):
    """
    Modified version of https://github.com/ganga-devs/ganga/blob/80bc4d9a6b5cb45bd72647236a782808bb4364e2/ganga/GangaCore/GPIDev/Persistency/__init__.py#L154
    """
    lineList = []
    for line in string_rep.splitlines():
        if (line.strip().startswith("#Ganga#")):
            lineList.append("#Ganga#")
        else:
            lineList.append(line)
    itemList = ("".join(lineList)).split("#Ganga#")

    objectList = []
    for item in itemList:
        item = item.strip()
        if item:
            try:
                from GangaCore.GPIDev.Base.Proxy import getProxyInterface
                this_object = eval(str(item), getProxyInterface().__dict__)
                objectList.append(this_object)
            except NameError as x:
                pass

    return objectList


def export(item=None):
    import GangaCore.GPI
    from GangaCore.Utility.Runtime import getScriptPath, getSearchPath
    from GangaCore.GPIDev.Base.Proxy import stripProxy, isType
    from GangaCore.GPIDev.Lib.Registry.RegistrySlice import RegistrySlice
    from GangaCore.GPIDev.Lib.Registry.RegistrySliceProxy import RegistrySliceProxy
    from GangaCore.GPIDev.Lib.GangaList.GangaList import GangaList
    import GangaCore.Utility.logging
    import os
    import sys
    import time

    returnValue = False
    outFile = StringWrapper()

    item = stripProxy(item)

    if isinstance(item, list):
        objectList = [stripProxy(element) for element in item]
    elif isinstance(item, tuple):
        objectList = [stripProxy(element) for element in item]
    elif isType(item, RegistrySliceProxy) or isType(item, RegistrySlice):
        objectList = [stripProxy(element) for element in item]
    elif isType(item, GangaList):
        objectList = [stripProxy(element) for element in item]
    else:
        objectList = [item]

    lineList = [
        "#Ganga# File created by Ganga - %s\n" % (time.strftime("%c")),
        "#Ganga#\n",
        "#Ganga# Object properties may be freely edited before reloading into Ganga\n",
        "#Ganga#\n",
        "#Ganga# Lines beginning #Ganga# are used to divide object definitions,\n",
        "#Ganga# and must not be deleted\n",
        "\n"]
    outFile.writelines(lineList)

    nObject = 0
    for this_object in objectList:
        try:
            name = this_object._name
            category = this_object._category
            outFile.write("#Ganga# %s object (category: %s)\n" % (name, category))
            this_object.printTree(outFile, "copyable")
            nObject = nObject + 1

        except AttributeError as err:
            raise err
        except Exception as err:
            raise err

    outFile.close()

    return returnValue


class StringWrapper:
    def __init__(self, string=""):
        self.string = string

    def writelines(self, lines):
        for line in lines:
            self.string += line

    def write(self, thing):
        self.string+=thing

    def close(self):
        pass