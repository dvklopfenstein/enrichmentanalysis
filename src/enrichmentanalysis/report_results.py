"""Enrichment object."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
import sys
# import collections as cx
# from enrichmentanalysis.pvalcalc import FisherFactory
# from enrichmentanalysis.multiple_testing import Methods


class ReportResults():
    """Report results in various formats."""

    headers = 'TermID     Stu Tot Stu/Tot   Pop   Tot Pop/Tot P-uncorr  '

    def __init__(self, results):
        self.results = results
        self.nts = None

    def prt_results(self, prt=sys.stdout):
        """Print enrichment results in a text format."""
        prt.write('{HDR}\n'.format(HDR=self._get_hdrs()))
        for rec in self.results:
            prt.write('{REC}\n'.format(REC=rec))

    def _get_hdrs(self):
        """Get headers for printing results in a text format."""
        if self.results:
            rec = self.results[0]
            multi = ['{METHOD:8}'.format(METHOD=m) for m in rec.multitests._fields]
            return self.headers + ' '.join(multi)

    def wrcsv(self, fout_csv):
        """Write results into csv file."""
        if self.nts is None:
            self.nts = self.get_nts()
        print('  WROTE: {CSV}'.format(CSV=fout_csv))

    def wrxlsx(self, fout_csv):
        """Write results into csv file."""
        if self.nts is None:
            self.nts = self.get_nts()
        print('  WROTE: {XLSX}'.format(XLSX=fout_csv))

    def get_nts(self):
        """Return namedtuples associated with results."""
        return [rec.get_nt_prt() for rec in self.results]


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
