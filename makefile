# Enrichemt Analysis
PY := python3

run_go:
	@echo RUN AN ENRICHMENT ANALYSIS EXAMPLE
	$(PY) src/bin/run_enrichment.py data/exgo/study data/exgo/population data/exgo/association -m fdr_bh --pval=0.05 --pval_field=fdr_bh

run_m:
	src/bin/run_enrichment.py data/exgo/study data/exgo/population data/exgo/association -m bonferroni,sidak,holm-sidak,holm,simes-hochberg,hommel,fdr_bh,fdr_by,fdr_tsbh,fdr_tsbky

run:
	src/bin/run_enrichment.py data/ex/study001.txt data/ex/population.txt data/ex/population.txt

pylint:
	@git status -uno | perl -ne 'if (/(\S+.py)/) {printf "echo $$1\npylint -r no %s\n", $$1}' | tee tmp_pylint
	chmod 755 tmp_pylint
	tmp_pylint

vim_:
	vim -p \
	src/bin/run_enrichment.py \
	src/enrichmentanalysis/enrich_run.py \
	src/enrichmentanalysis/enrich_rec.py \
	src/enrichmentanalysis/enrich_results.py \
	src/enrichmentanalysis/report_results.py \
	src/enrichmentanalysis/file_utils.py \
	src/enrichmentanalysis/multiple_testing.py \
	src/enrichmentanalysis/pvalcalc.py \
	src/enrichmentanalysis/wr_tbl.py \
	src/enrichmentanalysis/wr_tbl_class.py \
	src/enrichmentanalysis/cli.py \
	src/tests/test_enrichment0.py


# --------------------------------------------------------------------------------
# Modify version in src/enrichmentanalysis/__init__.py
vim_pip:
	vim -p src/enrichmentanalysis/__init__.py setup.py makefile

bdist_wheel:
	#python3 -m pip install --user --upgrade setuptools wheel
	make clean_dist
	python3 setup.py sdist bdist_wheel
	ls -lh dist

upload_pip:
	python3 -m twine upload dist/* --verbose

bdist_conda:
	python setup.py bdist_conda

test_conda:
	conda remove --name myenv --all
	conda create --name myenv
	conda activate myenv
	conda install -c dvklopfenstein enrichmentanalysis_dvklopfenstein
	run_enrichment.py
	run_enrichment.py data/exgo/study data/exgo/population data/exgo/association

# --------------------------------------------------------------------------------
upload_pypi_test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest

clean_dist:
	rm -rf dist build enrichmentanalysis.egg-info

clean_pyc:
	find . -name \*.pyc | xargs rm -f
	find . -name \*.st\*p | xargs rm -f

clean:
	rm -f enrichment.xlsx
	rm -f *.csv
	rm -f tmp_pylint


# Copyright (C) 2015-2019, DV Klopfenstein. All rights reserved.
