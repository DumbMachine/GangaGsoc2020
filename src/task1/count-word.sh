#!/bin/sh
# SOLUTION TO TASK 1B
# GSoC 2019
# AUTHOR - TARUN RAHEJA
# SCRIPT TO COUNT WORDS FROM PDF

pdftotext $1 -| sed -e 's/ /\n/g' |grep -ci 'the' > result.txt
