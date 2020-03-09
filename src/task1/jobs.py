'''
For using TESSERACT to find the occurance of the's
'''
# j = Job(name='FindThe')
# j.application.exe = File('tessract.py')
# j.backend = Local()
# j.inputfiles = [LocalFile("./pdfs/page{}.pdf".format(i)) for i in range(2)]
# j.outputfiles = [LocalFile("something.txt")]
# j.splitter = GenericSplitter()
# j.splitter.attribute = 'application.args'
# j.splitter.values = ["page{}.pdf".format(i) for i in range(2)]
# j.postprocessors.append(CustomMerger(module = './mymerger.py', files = ['something.txt']))
# j.submit()


'''
For using PDFTOTEXT to find the occurance of the's
'''
j = Job()
j.application.exe = File("count-word.sh")
j.backend = Local()
# j.inputfiles = [LocalFile("pdfs/page{}.pdf".format(i)) for i in range(12)]
args = [["page0.pdf"],["page1.pdf"],["page2.pdf"],["page3.pdf"],["page4.pdf"],["page5.pdf"],["page6.pdf"],["page7.pdf"],["page8.pdf"],["page9.pdf"],["page10.pdf"],["page11.pdf"]]
j.outputfiles = [LocalFile("something.txt")]
#splits the job
splitter = ArgSplitter(args=args)
#creates list of file names
filelist = []
for i in range(len(args)):
	filename = args[i][0]
	filelist.append(filename)
#assigns filelist to job applicatio arguments
j.application.args = filelist
#assigns splitter to job application
j.splitter = splitter
#assigns filelist to inputfiles
j.inputfiles = filelist
#specifies backend
j.backend = "Local"
j.postprocessors = TextMerger(files=['something.txt'])
# j.postprocessors = CustomMerger(module = './custommerge.py', files = ['something.txt'])
# j.postprocessors.append(CustomMerger(module = 'custommerge.py'))
# j.postprocessors = RootMerger(files=['something.text'], overwrite=True)
j.submit()
