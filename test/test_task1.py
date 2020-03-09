import os
import sys
import time
import pytest
import subprocess

from glob import glob

sys.path.insert(0, "../src/task1/")
sys.path.insert(0, "../src/task2/")

def test_split_pdfs():
    if "CERN.pdf" in os.listdir("../src/task1/"):
        from split_pdf import splitpdf
        splitpdf("../src/task1/CERN.pdf")
        if len(glob("./*.pdf")) == 12:
            for file in glob("./*.pdf"):
                os.remove(file)
            assert True
        else:
            assert False
    else:
        assert False


def test_reading_thes():
    filename = "../src/task1/page0.pdf"
    cmd = f"pdftotext {filename} -| sed -e 's/ /\\n/g' |grep -ci 'the'"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    if ps.communicate()[0] == b'23\n':
        assert True
    else:
        assert False

def test_mergefiles():
    from custom import mergefiles
    # creating tem files:
    filelist = ['1.txt', '2.txt', '3.txt']
    outfile = "result.txt"
    for idx, file in enumerate(filelist):
        open(file, 'w').write(str(idx))

    mergefiles(filelist, outfile)
    if open(outfile, 'r').read().strip().split(" ") == ['3\n#', 'Custom', 'Merger', 'Success', '#']:
        assert True
    else:
        assert False

    # cleaning up
    for file in filelist + [outfile]:
        os.remove(file)

# def test_ganga_job():
#     import ganga
#     from GangaCore.GPIDev.Lib.Job import Job

#     # from GangaCore.GPI import Job, Executable, Local, File, LocalFile


#     j = Job()
#     j.submit()
#     time.sleep(2)
#     if j.status == "completed":
#         assert True
#     else:
#         assert False