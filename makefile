run_go:
	src/bin/run_enrichment.py data/exgo/study data/exgo/population data/exgo/association

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
	src/enrichmentanalysis/file_utils.py \
	src/enrichmentanalysis/multiple_testing.py \
	src/enrichmentanalysis/pvalcalc.py

# Copyright (C) 2015-2019, DV Klopfenstein. All rights reserved.
