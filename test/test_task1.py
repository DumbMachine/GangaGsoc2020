import os
import sys
import time
import pytest
import subprocess

from glob import glob


def test_split_pdfs():
    sys.path.insert(0, "../src/task1/")
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
    sys.path.insert(0, "../src/task1/")
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