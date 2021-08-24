#!/bin/sh

cd assets/1/tmp/
head -n 1 0.csv > aggregated_linux.csv_
for FILE in *.csv; do 
    tail -n +2 "$FILE" # remove the header for remaining files
done >> aggregated_linux.csv_
