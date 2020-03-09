"""
This file shows the solution to the following:

- Demonstrate that you can read the blob back and re-create a job object.

"""

# Using the last created ganga job as the specimenL
import time
from sqlalchemy import Binary, Column, ForeignKey, Integer, String, Table
from GangaCore.GPIDev.Base.Proxy import isType, stripProxy
from GangaCore.GPIDev.Lib.GangaList.GangaList import GangaList
from GangaCore.GPIDev.Lib.Registry.RegistrySlice import RegistrySlice
from GangaCore.GPIDev.Lib.Registry.RegistrySliceProxy import RegistrySliceProxy
from GangaCore.Utility.Runtime import getScriptPath, getSearchPath


def custom_export(job=None):

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

    item = stripProxy(job)

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

# Getting the string representation of the object:
job = jobs[-1]
string_rep = custom_export(job=job)
job_from_string_rep = custom_load(string_rep=string_rep)
assert  job == job_from_string_rep
print("Asertion was successful")