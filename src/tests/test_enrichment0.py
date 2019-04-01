#!/usr/bin/env python3
"""Enrichment analysis with user-provided population and associations."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
from enrichmentanalysis.file_utils import read_ids
from enrichmentanalysis.report_results import ReportResults
from enrichmentanalysis.cli import get_enrichment_run

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")


def test_enrichment():
    """Test an enrichment."""
    kws_init = {
        'population_ids': os.path.join(REPO, 'data/exgo/population'),
        'associations':   os.path.join(REPO, 'data/exgo/association'),
        'methods': 'fdr_bh',
        'alpha': 0.05,
        'name': 'Test0',
    }
    args = {
        'study_ids': os.path.join(REPO, 'data/exgo/study'),
        'pval': 0.05,
        'pval_field': 'fdr_bh',
        'ids1': 'test0_found.txt',
        'ids0': 'test0_not_found.txt',
        'xlsx': 'test0.xlsx',
        'csv': 'test0.csv',
        'tsv': 'test0.tsv',
    }
    objrun = get_enrichment_run(kws_init)  # EnrichmentRun
    # Run Enrichment
    stu_dct = read_ids(args['study_ids'])
    stu_ids = stu_dct['ids']
    objresults = objrun.run_study(stu_ids, stu_dct.get('name'))  # EnrichmentResults
    # Write IDs found and not found to files
    objresults.wr_found(args['ids1'])
    objresults.wr_notfound(args['ids0'],
                           stu_ids.union(objrun.args['pop_ids']))
    # Write Pathway Enrichment Analysis to a file
    results = objresults.get_results_cond(args['pval'], args['pval_field'])
    # Print results
    objrpt = ReportResults(results)  #, objrun.objmethods)
    objrpt.prt_results()
    objrpt.wrxlsx(args['xlsx'])
    objrpt.wrtsv(args['tsv'])
    objrpt.wrcsv(args['csv'])


if __name__ == '__main__':
    test_enrichment()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
