"""
This uses the export() and load() functions
"""
"""
The is the way of implementation using
"""
import os
import sys
import time

from tqdm import tqdm
from pymongo import MongoClient
from GangaCore.GPIDev.Base.Proxy import isType, stripProxy
from GangaCore.GPIDev.Lib.GangaList.GangaList import GangaList
from GangaCore.GPIDev.Lib.Registry.RegistrySlice import RegistrySlice
from GangaCore.GPIDev.Lib.Registry.RegistrySliceProxy import RegistrySliceProxy
from GangaCore.Utility.Runtime import getScriptPath, getSearchPath


def store_job(jid, bind_id, db=None):
    """

    """

    def custom_export(item=None):

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

        return outFile.string

    if db is None:
        client = MongoClient('localhost', 27017)
        db = client.ganga_export_load

    string_rep = custom_export(jobs[jid])

    db.jobs.insert({"jid": bind_id, "string": string_rep})

def get_job(jid, db=None):
    """

    """
    def custom_load(string_rep):
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

        return objectList[0]

    if db is None:
        client = MongoClient('localhost', 27017)
        db = client.ganga_export_load

    return [custom_load(item['string']) for item in db.jobs.find({"jid": jid})]



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
            assert db_job == job
            progress.update(1)


    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
    plt.plot([i[0] for i in times], "-b", label="store_job")
    plt.plot([i[1] for i in times], "-r", label="get_job")
    plt.plot([i[2] for i in times], "-g", label="total_time")
    plt.yticks(np.arange(0, np.max(times), step=0.05))
    plt.title("Mongo Bench")
    plt.legend(loc="best")
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.savefig(f'data/mongo-method-export-{iterations}-time_interval-{sleep}.png')
stress_test()
# stress_test(sleep=2)
