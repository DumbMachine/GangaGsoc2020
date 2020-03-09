"""
Make shift testing the task1 script
"""

import os
import time
import io
import sys
#starts new job
job = Job()
#specifies executable to run on Grid
job.application = Executable()
job.application.exe = File("count-word.sh")
#specifies pagewise arguments to the executable
args = [["page0.pdf"],["page1.pdf"],["page2.pdf"],["page3.pdf"],["page4.pdf"],["page5.pdf"],["page6.pdf"],["page7.pdf"],["page8.pdf"],["page9.pdf"],["page10.pdf"],["page11.pdf"]]
#splits the job
splitter = ArgSplitter(args=args)
job.outputfiles = [LocalFile("result.txt")]
filelist = []
for i in range(len(args)):
	filename = args[i][0]
	filelist.append(filename)
job.application.args = filelist
job.splitter = splitter
job.inputfiles = filelist
job.backend = "Local"
job.postprocessors = CustomMerger(module="./custom.py", files=['result.txt'])
job.submit()

time.sleep(5)

while True:
    print(job.status)
    if job.status == "completed":

        stdout = sys.stdout
        sys.stdout = io.StringIO()

        job.peek("result.txt", "more") 

        # get output and restore sys.stdout
        output = sys.stdout.getvalue()
        sys.stdout = stdout

        assert "399" in output
        print("OK")
        break
    elif job.status == "failed":
        assert False
        print("NOt OK")
        break

"""
from GangaCore.GPIDev.Lib.Job import Job
from GangaCore.GPIDev.Lib.File import File 
from GangaCore.GPIDev.Lib.File import LocalFile
from GangaCore.Lib.Mergers.Merger import CustomMerger
"""