"""Enrichment object."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
# import collections as cx
# from enrichmentanalysis.pvalcalc import FisherFactory
# from enrichmentanalysis.multiple_testing import Methods


class EnrichmentRecord():
    """Enrichment object."""

    def __init__(self, termid, pval_args, pval_uncorr, stu_items, pop_items):
        self.termid = termid
        self.ntpvalargs = pval_args
        self.pval_uncorr = pval_uncorr
        self.stu_items = stu_items
        self.pop_items = pop_items
        self.multitests = None  # namedtuple

        

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
