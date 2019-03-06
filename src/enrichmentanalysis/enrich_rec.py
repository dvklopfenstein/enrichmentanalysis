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

    pat = ('{TERM_ID} {STU_CNT:3} {STU_TOT:3} {POP_CNT:5} {POP_TOT:5} '
           '{PVAL:8.2e} {MULT} '
          )

    def __init__(self, termid, pval_args, pval_uncorr, stu_items, pop_items, **kws):
        self.termid = termid
        self.ntpvalargs = pval_args
        self.pval_uncorr = pval_uncorr
        self.stu_items = stu_items
        self.pop_items = pop_items
        self.multitests = None  # namedtuple
        self.kws = kws

    def __str__(self):
        """Return string representation for this record."""
        pat = self.kws.get('pat', self.pat)
        ntpvals = self.ntpvalargs
        multidct = self.multitests._asdict()
        return pat.format(
            TERM_ID=self.termid,
            STU_CNT=ntpvals.study_count,
            STU_TOT=ntpvals.study_n,
            STU_RATIO=float(ntpvals.study_count)/ntpvals.study_n,
            POP_CNT=ntpvals.pop_count,
            POP_TOT=ntpvals.pop_n,
            POP_RATIO=float(ntpvals.pop_count)/ntpvals.pop_n,
            PVAL=self.pval_uncorr,
            MULT=self.multitests,
            **multidct,
        )



# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
