
import os

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