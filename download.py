#!/usr/bin/python

"""
Downloads clinical data that has filesnames that end in one of the *postfixes*
from <http://gdac.broadinstitute.org/runs/stddata__2013_02_03>
"""

import os.path
from urllib2 import urlopen, HTTPError, URLError

def get_baseurl(cancer_type):
    """
    example path
    http://gdac.broadinstitute.org/runs/stddata__2013_02_03/data/BRCA/20130203/
    """
    return "http://gdac.broadinstitute.org/runs/stddata__2013_02_03/data/" + \
            cancer_type + "/20130203/"

cancer_types = ["COADREAD", "BLCA", "BRCA", "CESC", "COAD", "DLBC", "ESCA", \
"GBM", "HNSC", "KICH", "KIRC", "KIRP", "LAML", "LGG", "LIHC", "LUAD", "LUSC", \
"OV", "PAAD", "PRAD", "READ", "SARC", "SKCM", "STAD", "THCA", "UCEC"]

# clinical files that I'm going to download
postfixes = [ ".Clinical_Pick_Tier1.Level_4.2013020300.0.0.tar.gz", \
".Clinical_Pick_Tier1.aux.2013020300.0.0.tar.gz", \
".Clinical_Pick_Tier1.mage-tab.2013020300.0.0.tar.gz", \
".Merge_Clinical.Level_1.2013020300.0.0.tar.gz", \
".Merge_Clinical.aux.2013020300.0.0.tar.gz", \
".Merge_Clinical.mage-tab.2013020300.0.0.tar.gz" ]

print "fetching clinical data that is like this:", postfixes

"""
For each clinical file type in each cancer type, download the file
"""
for type in cancer_types:
    for postfix in postfixes:
        print "downloading clinical data for ", type
        try:
            baseurl = get_baseurl(type)
            #url = baseurl + "gdac.broadinstitute.org_" + type + \
            #".Clinical_Pick_Tier1.Level_4.2013020300.0.0.tar.gz"

            url = baseurl + "gdac.broadinstitute.org_" + type + postfix
            f = urlopen(url)
        except HTTPError, e:
            print "HTTP Error: ", type, e.code
        except URLError, e:
            print "URL Error: ", type, e.reason
        local_file = open(os.path.basename(url), "wb")
        local_file.write(f.read())

# sample of what's in a directory

# gdac.broadinstitute.org_BRCA.Clinical_Pick_Tier1.Level_4.2013020300.0.0.tar.gz
# gdac.broadinstitute.org_BRCA.Clinical_Pick_Tier1.Level_4.2013020300.0.0.tar.gz.md5
# gdac.broadinstitute.org_BRCA.Clinical_Pick_Tier1.aux.2013020300.0.0.tar.gz
# gdac.broadinstitute.org_BRCA.Clinical_Pick_Tier1.aux.2013020300.0.0.tar.gz.md5
# gdac.broadinstitute.org_BRCA.Clinical_Pick_Tier1.mage-tab.2013020300.0.0.tar.gz
# gdac.broadinstitute.org_BRCA.Clinical_Pick_Tier1.mage-tab.2013020300.0.0.tar.gz.md5
# gdac.broadinstitute.org_BRCA.Merge_Clinical.Level_1.2013020300.0.0.tar.gz
# gdac.broadinstitute.org_BRCA.Merge_Clinical.Level_1.2013020300.0.0.tar.gz.md5
# gdac.broadinstitute.org_BRCA.Merge_Clinical.aux.2013020300.0.0.tar.gz
# gdac.broadinstitute.org_BRCA.Merge_Clinical.aux.2013020300.0.0.tar.gz.md5
# gdac.broadinstitute.org_BRCA.Merge_Clinical.mage-tab.2013020300.0.0.tar.gz
