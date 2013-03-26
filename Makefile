all: all_drugs wrangle

# gets all the drugs names out of the appropriate files
all_drugs:
	find data -name '*.clin.merged.txt' | xargs grep 'drugname' >all_drugs.tsv

# gives a json [list of { cancer, drug,  count } ]
wrangle: all_drugs
	./wrangle.py all_drugs.tsv >vis/data.json

# downloads data from broad
download:
	./download.py

# starts up a server for the d3 vis
vis: wrangle
	python -m SimpleHTTPServer

push: all
	cp -r vis clinical
	scp -r clinical gideon@gideond.com:gideond.com
	rm -r clinical
