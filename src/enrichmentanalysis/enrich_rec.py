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
        'enrichment',
        'TermID',
        'stu_num',
        'stu_tot',
        'stu_ratio',
        'pop_num',
        'pop_tot',
        'pop_ratio',
        'pval_uncorr')

    fld2fmt = cx.OrderedDict([
        ('enrichment', '{enrichment}'),
        ('TermID', '{TermID:10}'),
        ('stu_num', '{stu_num:3}'),
        ('stu_tot', '{stu_tot:3}'),
        ('stu_ratio', '{stu_ratio:7.5f}'),
        ('pop_num', '{pop_num:5}'),
        ('pop_tot', '{pop_tot:5}'),
        ('pop_ratio', '{pop_ratio:7.5f}'),
        ('pval_uncorr', '{pval_uncorr:8.2e}'),
    ])

    def __init__(self, termid, ntpval, stu_items, pop_items):
        self.termid = termid
        self.ntpval = ntpval
        self.stu_items = stu_items
        self.pop_items = pop_items
        self.multitests = None  # namedtuple
        self.prtfmt = None
        self.ntobj = None

    def __str__(self):
        """Return string representation for this record."""
        ntpval = self.ntpval
        multidct = self.multitests._asdict()
        if self.prtfmt is None:
            self.prtfmt = self._get_prtfmt()
        return self.prtfmt.format(
            enrichment=ntpval.enrichment,
            TermID=self.termid,
            stu_num=ntpval.study_cnt,
            stu_tot=ntpval.study_tot,
            stu_ratio=ntpval.study_ratio,
            pop_num=ntpval.pop_cnt,
            pop_tot=ntpval.pop_tot,
            pop_ratio=ntpval.pop_ratio,
            pval_uncorr=ntpval.pval_uncorr,
            **multidct)

    def get_nt_prt(self):
        """Print namedtuple containing record information."""
        if self.ntobj is None:
            self.ntobj = self._get_ntobj()
        ntp = self.ntpval
        multidct = {m:'{:8.2e}'.format(v) for m, v in self.multitests._asdict().items()}
        return self.ntobj(
            enrichment=ntp.enrichment,
            TermID=self.termid,
            stu_num=ntp.study_cnt,
            stu_tot=ntp.study_tot,
            stu_ratio=self.fld2fmt['stu_ratio'].format(stu_ratio=ntp.study_ratio),
            pop_num=ntp.pop_cnt,
            pop_tot=ntp.pop_tot,
            pop_ratio=self.fld2fmt['pop_ratio'].format(pop_ratio=ntp.pop_ratio),
            pval_uncorr=self.fld2fmt['pval_uncorr'].format(pval_uncorr=ntp.pval_uncorr),
            stu_items=self._get_items_str(self.stu_items, ';'),
            **multidct)

    @staticmethod
    def _get_items_str(items, divider):
        """Return one string containing all items."""
        if items:
            if isinstance(next(iter(items)), str):
                return divider.join(items)
            else:
                return divider.join(str(e) for e in items)
        return ''

    def _get_ntobj(self):
        """Create namedtuple object for enrichment results records."""
        return cx.namedtuple('ntresults',
                             ' '.join(self.flds) + \
                             ' '.join(self.multitests._fields) + \
                             'stu_items')
    def _get_prtfmt(self):
        """Create print format."""
        # pylint: disable=bad-format-string
        return '{FMT} {M}'.format(
            FMT=' '.join(self.fld2fmt.values()),
            M=' '.join(['{{{M}:8.2e}'.format(M=m) for m in self.multitests._fields]))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
