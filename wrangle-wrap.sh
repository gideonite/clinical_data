#!/bin/bash

#for f in `find data -name '*.clin.merged.txt'`
#do
#    ./wrangle.py $f
#done

FILES=$(find data -name '*.clin.merged.txt')

./wrangle.py $(printf '%s ' ${FILES[@]})
