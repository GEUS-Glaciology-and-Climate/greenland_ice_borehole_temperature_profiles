SHELL := bash
DIR = $(shell pwd)
MAJOR_VERSION = $(shell git describe --abbrev=0 --tags)
# MINOR_VERSION = $(shell  git rev-list ${MAJOR_VERSION}.. --count)
MINOR_VERSION = $(shell git describe --always --dirty='*')
VERSION = ${MAJOR_VERSION}.${MINOR_VERSION}

org-babel = emacsclient --eval "(progn			\
	(find-file \"$(1)\") 				\
	(org-babel-goto-named-src-block \"$(2)\")	\
	(org-babel-execute-src-block)			\
	(save-buffer))"

# Usage: $(call org-babel,<file.org>,<named_babel_block>)

BOREHOLES := boreholes/*

all: FORCE
	make data/temperature.csv
	make data/boreholes.kml
	make figs

data/temperature.csv: boreholes/*
	@echo Building temperature.csv
	python ./src/temperature_csvs.py
	python ./src/merge_boreholes.py


boreholes/*: data/meta.csv
	@echo Building $@/meta.bsv
	python ./src/csv2meta_bsv.py $@
	@echo Updating $<
	$(call org-babel,$@/README.org,ingest_meta)
	$(call org-babel,$@/README.org,ingest_data)

data/meta.csv:
	python ./src/googlesheet2csv.py

data/boreholes.kml: data/meta.csv
	@echo Building KML of borehole locations
	python ./src/borehole_kml.py

figs: fig/temperature.png fig/temperature_dnorm.png

fig/temperature.png fig/temperature_dnorm.png: data/temperature.csv data/temperature_dnorm.csv
	@echo Generating figures
	python ./src/figs.py

clean:
	@echo [clean]
	@rm -rf boreholes/*/meta.bsv data/*

FORCE: # dummy target
