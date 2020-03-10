#!/bin/sh
pdftotext $1 -| sed -e 's/ /\n/g' |grep -ci 'the' > result.txt
