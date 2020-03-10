from PyPDF2 import PdfFileWriter, PdfFileReader

def splitpdf(path):
    inputpdf = PdfFileReader(open(path, "rb"))

    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open("page%s.pdf" % i, "wb") as outputStream:
            output.write(outputStream)


if __name__ == "__main__":
    splitpdf("CERN.pdf")