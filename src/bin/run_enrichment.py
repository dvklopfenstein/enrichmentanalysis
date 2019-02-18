#!/usr/bin/env python
"""Enrichment analysis with user-provided population and associations.

Usage:
    run_enrichment.py <study_ids> <population_ids> <associations> [options]

Options:
  -h --help             Show usage
  -a --alpha=A  Alpha for multiple-test correction [default: 0.05]
  -m --methods=M1,M2  Methods for multiple-test correction [default: fdr_bh]
  --csv=CSV  Write enrichment analysis into a csv file [default: enrichment.csv]
  --csv0=NF  Write list of identifiers that were not found [default: ids_found.csv]
  --csv1=F   Write list of identifiers that were found [default: ids_notfound.csv]
  -b --base  Prepend a basename to all output files
"""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
from docopt import docopt
from enrichmentanalysis.file_utils import read_ids
from enrichmentanalysis.file_utils import read_associations
from enrichmentanalysis.enrich_run import EnrichmentRun


def main():
    """Enrichment analysis with user-provided population and associations."""
    args = docopt(__doc__)
    print(args)

    stu_ids = read_ids(args['<study_ids>'])
    pop_ids = read_ids(args['<population_ids>'])
    assc = read_associations(args['<associations>'])
    methods = args['--methods'].split(',')
    obj = EnrichmentRun(pop_ids, assc, float(args['--alpha']), methods)
    objresults = obj.run_study(stu_ids)
    # Write Pathway Enrichment Analysis to a file
    # ana.csv_pathways(args['--csv'], token, resource='TOTAL')
    # ana.csv_found(args['--csv0'], token, resource='TOTAL')
    # ana.csv_notfound(args['--csv1'], token)


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
