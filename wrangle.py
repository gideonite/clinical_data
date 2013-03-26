#!/usr/bin/python

import sys
import os.path
import re
import matplotlib
import json

# cancer_type -> [ list of drugs used on patients (*not* a unique list) ]
cancer2drugs = {}

drug2count = {}

with open(sys.argv[1]) as all_drugs:
    for line in all_drugs.readlines():
        line = line.split("\t")
        cancer_type = re.sub("\..*","", os.path.basename(line[0]))
        drugs_per_patient = filter(lambda x: x != "NA",         # filter out NAs
                map(lambda x: x.strip(), line[1:]))             # after having stripped everything

        # fill the dict cancer2drugs
        if not cancer2drugs.has_key(cancer_type):
            cancer2drugs[cancer_type] = drugs_per_patient
        else:
            cancer2drugs[cancer_type] = cancer2drugs[cancer_type] + drugs_per_patient

l = []      # [ list of { 'cancer', 'drug', 'count' } ]
for cancer in cancer2drugs.keys():
    drugs = cancer2drugs[cancer]
    drugs2count = dict( (i, drugs.count(i)) for i in drugs )

    for drug in drugs2count.keys():
        l.append(dict( (('cancer', cancer), ('drug', drug), ('count', drugs2count[drug])) ))

print json.dumps(l)
