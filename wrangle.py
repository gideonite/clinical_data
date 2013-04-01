#!/usr/bin/python

import sys
import os.path
import pandas
import re
import json
import csv
from subprocess import call
from itertools import chain

SAMPLE_ID = "sample_id"
CANCER = "cancer"
# aliases : alias -> standard
aliases = dict([
    ("5fluorouracil", "5fu"),
    ("5fu", "5fu"),
    ("5 fu", "5fu"),
    ("5-fu", "5fu"),
    ("5 fluorouracil", "5fu"),
    ("5-fluorouracil", "5fu"),
    ("5- fu", "5fu"),
    ("patient.bcrpatientbarcode", SAMPLE_ID)
    ])

def alias(input):
    '''
    If there is an alias for a given input string, return alias given the by
    aliases dictionary, otherwise return the original input.
    '''
    try:
        return aliases[input]
    except KeyError:
        return input


# cancer_type -> [ list of drugs used on patients (*not* a unique list) ]
cancer2drugs = {}

drug2count = {}

DRUGNAME = re.compile("^.*\.drugname$")
NA = "NA"

def update_keepers(row, keepers):
    '''
    if a row is a keeper, add it to keepers.
    Does *not* change state of keepers

    return  a new list = keepers + [ new keepers ]
    '''
    feature = row[0]
    to_return = keepers

    if feature == SAMPLE_ID:
        to_return.append(row)

    if DRUGNAME.match(row[0]) != None:
        to_return.append(row)

    return to_return

def row2dict(row, headers, cancer):
    to_return = dict(zip(headers, row))

    to_return[CANCER] = cancer

    return to_return

def raw_data(filename):
    '''
    return a [ list of dicts ], each of which looks something like this:
    {   "sample_id": "tcga-k4-a3ws",
        "cancer": "BRCA"
        "patient.drugs.drug.drugname": some-value (or "NA") }
    '''

    with open(filename) as f:
        rows = csv.reader(f, delimiter="\t")

        keepers = []
        for row in rows:
            row = map(alias, row)       # not efficient
            keepers = update_keepers(row, keepers)

        zipped = zip(*keepers)
        headers = zipped[0]     # "pop" from the front of the list
        zipped = zipped[1:]

        cancer = re.sub("\..*","", os.path.basename(sys.argv[1]))

        return map(lambda row: row2dict(row, headers, cancer), zipped)

def update_dict(d, k, v):
    '''
    params      dict, key, value

    helper function for drug2patients
    creates a new (key, value) pair if one doesn't exist, otherwise append the
    value to the list stored in the key k

    return      updated_dict
    '''
    e = d
    try:
        e[k] += [v]
    except KeyError:
        e[k] = [v]
    return e

def drug2patients(raw_data):
    '''
    params      raw_data - output of raw_data function
                drugs2patients - dict of drug to patients, defaults to empty dict

    return      { cancer, drug, [list of samples], count = len of samples }
    '''

    # make a map : drug -> [list of patients]
    d2p = {}

    for d in raw_data:
        for k in d.keys():
            if DRUGNAME.match(k) and d[k] != "NA":
                d2p = update_dict(d2p, d[k], d[SAMPLE_ID])

    # map: d2p -> [ list of { cancer, [list of samples], drug } ]
    return map(lambda k: dict( [ ('cancer', raw_data[0][CANCER]), ('drug', k), ('samples', d2p[k]), ('count', len(d2p[k])) ]), d2p.keys())

def main():
    '''
    args are a list of file names turn that list into one big drug2patients
    dictionary

    flattens the list of lists of drug2patients for each input file
    '''
    to_return = list(chain.from_iterable(map(lambda i: drug2patients(raw_data(i)), sys.argv[1:])))

    print json.dumps(to_return, indent=1)

if __name__ == "__main__": main()
