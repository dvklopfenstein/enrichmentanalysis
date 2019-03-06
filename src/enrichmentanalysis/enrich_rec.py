"""Enrichment object."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
import collections as cx
# from enrichmentanalysis.pvalcalc import FisherFactory
# from enrichmentanalysis.multiple_testing import Methods


class EnrichmentRecord():
    """Enrichment object."""

    flds = (
        'TermID',
        'stu_num',
        'stu_tot',
        'stu_rato',
        'pop_num',
        'pop_tot',
        'pop_ratio',
        'pval_uncorr')

    fld2fmt = cx.OrderedDict([
        ('TermID', '{TermID:10}'),
        ('stu_num', '{stu_num:3}'),
        ('stu_tot', '{stu_tot:3}'),
        ('stu_ratio', '{stu_ratio:7.5f}'),
        ('pop_num', '{pop_num:5}'),
        ('pop_tot', '{pop_tot:5}'),
        ('pop_ratio', '{pop_ratio:7.5f}'),
        ('pval_uncorr', '{pval_uncorr:8.2e}'),
    ])

    def __init__(self, termid, pval_args, pval_uncorr, stu_items, pop_items):
        self.termid = termid
        self.ntpvalargs = pval_args
        self.pval_uncorr = pval_uncorr
        self.stu_items = stu_items
        self.pop_items = pop_items
        self.multitests = None  # namedtuple
        self.prtfmt = None
        self.ntobj = None

    def __str__(self):
        """Return string representation for this record."""
        ntpvals = self.ntpvalargs
        multidct = self.multitests._asdict()
        if self.prtfmt is None:
            self.prtfmt = self._get_prtfmt()
        return self.prtfmt.format(
            TermID=self.termid,
            stu_num=ntpvals.study_count,
            stu_tot=ntpvals.study_n,
            stu_ratio=float(ntpvals.study_count)/ntpvals.study_n,
            pop_num=ntpvals.pop_count,
            pop_tot=ntpvals.pop_n,
            pop_ratio=float(ntpvals.pop_count)/ntpvals.pop_n,
            pval_uncorr=self.pval_uncorr,
            **multidct,
        )

    def get_nt_prt(self):
        """Print namedtuple containing record information."""
        pass

    def _get_ntobj(self):
        """Create namedtuple object for enrichment results records."""
        mults = ' '.join(self.multitests._fields)
        return cx.namedtuple('ntresults',
                             ' '.join(self.flds) + \
                             ' '.join(self.multitests._fields) + \
                             'stu_items pop_items')
    def _get_prtfmt(self):
        """Create print format."""
        return '{FMT} {M}'.format(
            FMT=' '.join(self.fld2fmt.values()),
            M=' '.join(['{{{M}:8.2e}'.format(M=m) for m in self.multitests._fields]))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
