import os
import ganga
from fixtures import *
from GangaCore.GPIDev.Base.Proxy import stripProxy, isType

from GangaCore.testlib.monitoring import run_until_completed


def test_job_create(gpi):
    os.chdir("../src/task1/")
    job = gpi.Job()
    #specifies executable to run on Grid
    job.application = gpi.Executable()
    job.application.exe = gpi.File("count-word.sh")
    #specifies pagewise arguments to the executable
    args = [["page0.pdf"],["page1.pdf"],["page2.pdf"],["page3.pdf"],["page4.pdf"],["page5.pdf"],["page6.pdf"],["page7.pdf"],["page8.pdf"],["page9.pdf"],["page10.pdf"],["page11.pdf"]]
    #splits the job
    splitter = gpi.ArgSplitter(args=args)
    job.outputfiles = [gpi.LocalFile("result.txt")]
    filelist = []
    for i in range(len(args)):
        filename = args[i][0]
        filelist.append(filename)
    job.application.args = filelist
    job.splitter = splitter
    job.inputfiles = filelist
    job.backend = "Local"
    job.postprocessors = gpi.CustomMerger(module="custom.py", files=['result.txt'])
    job.submit()
