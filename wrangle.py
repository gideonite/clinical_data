#!/usr/bin/python

import sys
import os.path
import pandas
import re
import matplotlib
import json

# synonyms : alias -> standard
synonyms = dict([
    ("5fluorouracil", "5fu"),
    ("5fu", "5fu"),
    ("5 fu", "5fu"),
    ("5-fu", "5fu"),
    ("5 fluorouracil", "5fu"),
    ("5-fluorouracil", "5fu"),
    ("5- fu", "5fu")
    ])

# cancer_type -> [ list of drugs used on patients (*not* a unique list) ]
cancer2drugs = {}

drug2count = {}

attributes = [
        'patient.bcrpatientbarcode',
        'drugname'  # contains this?  let's find the actual names and just include them here.
        ]

patient_id = 'patient.bcrpatientbarcode'
drugname = lambda x: re.match("^.*\.drugname$", x) == None

with open(sys.argv[1]) as f:
    csv = pandas.read_csv(f, sep="\t")
    csv = csv.transpose()       # data is initially a matrix [ attr X patient ]
    csv.columns = csv.ix[0,:]   # get that first row to be the column names

    keeper_cols = filter(
        (lambda x: x == 'patient.bcrpatientbarcode' \
            or re.match("^.*\.drugname$", x) != None \
            ), csv.columns)

    extracted_cols = csv[keeper_cols]

    d = [ [ (colname, row[i]) for i, colname in enumerate(extracted_cols) ] for row in extracted_cols.values ]
    # thanks mike! <https://gist.github.com/mikedewar/1486027>

    d = d[1:]                               # the first row is a bunch of nonesense

    # make a true list of dicts
    # and add in the cancer type
    cancer_type = re.sub("\..*","", os.path.basename(sys.argv[1]))
    d = map(lambda i: dict( tuple(i + [('cancer', cancer_type)]) ), d)
    out = json.dumps(d, indent=1)
    print out
