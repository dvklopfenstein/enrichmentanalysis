#!/usr/bin/env python3
"""Enrichment analysis with user-provided population and associations.

Usage:
    run_enrichment.py <study_ids> <population_ids> <associations> [options]

Options:
  -h --help       Show usage
  -a --alpha=A    Alpha for multiple-test correction [default: 0.05]
  -m --methods=M1,M2  Methods for multiple-test correction [default: fdr_bh]
  --xlsx=XLSX     Write enrichment analysis into a xlsx file [default: enrichment.xlsx]
  --tsv=TSV       Write enrichment analysis into a tsv file
  --csv=CSV       Write enrichment analysis into a csv file
  --ids0=NF       Write list of identifiers that were not found [default: ids_found.csv]
  --ids1=F        Write list of identifiers that were found [default: ids_notfound.csv]
  --prefix=PREFIX  Add a prefix to all output files
  --pval=MAX           Only print results with uncorrected p-value < PVAL
  --pval_field=METHOD  Only print results when PVAL_FIELD < PVAL
"""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
from docopt import docopt
from enrichmentanalysis.file_utils import read_ids
from enrichmentanalysis.file_utils import prepend
from enrichmentanalysis.file_utils import clean_args
from enrichmentanalysis.report_results import ReportResults
from enrichmentanalysis.cli import get_enrichment_run


def main():
    """Enrichment analysis with user-provided population and associations."""
    docargs = docopt(__doc__)
    args = clean_args(docargs)
    print(args)

    objrun = get_enrichment_run(args)  # EnrichmentRun
    # Run Enrichment
    stu_dct = read_ids(args['study_ids'])
    stu_ids = stu_dct['ids']
    objresults = objrun.run_study(stu_ids, stu_dct.get('name'))  # EnrichmentResults
    # Write IDs found and not found to files
    prefix = args['prefix'] if 'prefix' in args else None
    objresults.wr_found(prepend(prefix, args['ids1']))
    objresults.wr_notfound(prepend(prefix, args['ids0']),
                           stu_ids.union(objrun.args['pop_ids']))
    # Write Pathway Enrichment Analysis to a file
    pval = float(args['pval']) if 'pval' in args else None
    results = objresults.get_results_cond(pval, args.get('pval_field'))
    # Print results
    objrpt = ReportResults(results)  #, objrun.objmethods)
    objrpt.prt_results()
    if 'xlsx' in args:
        objrpt.wrxlsx(args['xlsx'])
    if 'tsv' in args:
        objrpt.wrtsv(args['tsv'])
    if 'csv' in args:
        objrpt.wrcsv(args['csv'])


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
