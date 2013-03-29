all: wrangle

# gives a json [list of { cancer, drug-1, drug-2, etc, patient-id } ]
wrangle:
	rm vis/data.json
	./wrangle-wrap.sh >>vis/data.json

# downloads data from broad
download: FORCE
	./download.py

# starts up a server for the d3 vis
vis: FORCE
	python -m SimpleHTTPServer

FORCE:

push: all
	cp -r vis clinical
	scp -r clinical gideon@gideond.com:gideond.com
	rm -r clinical
