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

    def prt_results(self, prt=sys.stdout):
        """Print enrichment results in a text format."""
        prt.write('{HDR}\n'.format(HDR=self._get_hdrs()))
        for rec in self.results:
            prt.write(str(rec))

    def _get_hdrs(self):
        """Get headers for printing results in a text format."""
        if self.results:
            rec = self.results[0]
            multi = ['{METHOD:8}'.format(METHOD=m) for m in rec.multitests._fields]
            return self.headers + ' '.join(multi)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
