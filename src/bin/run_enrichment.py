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
  --ids1=NF       Write list of identifiers that were not found [default: ids_found.csv]
  --ids0=F        Write list of identifiers that were found [default: ids_notfound.csv]
  -b --base=BASE  Prepend a basename to all output files
  --pval=MAX           Only print results with uncorrected p-value < PVAL
  --pval_field=METHOD  Only print results when PVAL_FIELD < PVAL
"""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
from docopt import docopt
from enrichmentanalysis.file_utils import read_ids
from enrichmentanalysis.file_utils import read_associations
from enrichmentanalysis.file_utils import prepend
from enrichmentanalysis.enrich_run import EnrichmentRun
from enrichmentanalysis.report_results import ReportResults


def main():
    """Enrichment analysis with user-provided population and associations."""
    args = docopt(__doc__)
    print(args)

    base = args['--base'] if args['--base'] else None
    stu_ids = read_ids(args['<study_ids>'])
    pop_ids = read_ids(args['<population_ids>'])
    assc = read_associations(args['<associations>'])
    methods = args['--methods'].split(',')
    # Run Enrichment
    objrun = EnrichmentRun(pop_ids, assc, alpha=float(args['--alpha']), methods=methods)
    objresults = objrun.run_study(stu_ids)
    # Write IDs found and not found to files
    objresults.wr_found(prepend(base, args['--csv0']))
    objresults.wr_notfound(prepend(base, args['--csv1']), stu_ids.intersection(pop_ids))
    # Write Pathway Enrichment Analysis to a file
    pval = float(args['--pval']) if args['--pval'] else None
    results = objresults.get_results_cond(pval, args['--pval_field'])
    # Print results
    objrpt = ReportResults(results)  #, objrun.objmethods)
    objrpt.prt_results()
    if '--xlsx' in args:
        objrpt.wrxlsx(args['--xlsx'])
    if '--tsv' in args:
        objrpt.wrtsv(args['--tsv'])
    if '--csv' in args:
        objrpt.wrcsv(args['--csv'])

    print('{N} results'.format(N=len(results)))


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
