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

# Usage: $(call org-babel,README.org,csv2bs)

temperature.csv: */README.org README.org
	@echo Building temperature.csv
	$(call org-babel,code.org,meta2temperatureCSV)

*/README.org: database.csv
	@echo Ingesting meta.bsv: $(@D)
	$(call org-babel,$(@D)/README.org,ingest_meta)
	@echo Ingesting data.csv: $(@D)
	$(call org-babel,$(@D)/README.org,ingest_data)

database.csv: README.org
	@echo Converting Google Sheet to local file
	$(call org-babel,code.org,sheet2csv)
	@echo Building meta.bsv files in subfolders
	$(call org-babel,code.org,csv2metabsv)

boreholes.kml: database.csv
	@echo Converting Google Sheet to local file
	$(call org-babel,code.org,kml)

clean:
	@echo [clean]
	@rm -rf */meta.bsv boreholes.kml database.csv README.pdf temperature.csv

FORCE: # dummy target

