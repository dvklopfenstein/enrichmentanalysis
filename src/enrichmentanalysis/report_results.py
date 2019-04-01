"""Enrichment object."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from enrichmentanalysis.wr_tbl import wr_xlsx
from enrichmentanalysis.wr_tbl import wr_tsv


class ReportResults():
    """Report results in various formats."""

    headers = 'ep TermID    Stu Tot Stu/Tot   Pop   Tot Pop/Tot P-uncorr'

    fld2col_widths_dflts = {
        'enrichment': 2,
        'TermID': 12,
        'stu_num': 4,
        'stu_tot': 5,
        'stu_ratio': 7,
        'pop_num': 6,
        'pop_tot': 6,
        'pop_ratio': 7,
    }

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

    def wrtsv(self, fout_tsv):
        """Write results into tsv file."""
        if self.nts is None:
            self.nts = self.get_nts()
        kws = {}
        wr_tsv(fout_tsv, self.nts, **kws)
        #### print('  WROTE: {TSV}'.format(TSV=fout_tsv))

    def wrcsv(self, fout_csv):
        """Write results into csv file."""
        if self.nts is None:
            self.nts = self.get_nts()
        kws = {'sep':','}
        wr_tsv(fout_csv, self.nts, **kws)
        #### print('  WROTE: {CSV}'.format(CSV=fout_csv))

    def wrxlsx(self, fout_xlsx):
        """Write results into xlsx file."""
        if self.nts is None:
            self.nts = self.get_nts()
        kws = {
            'fld2col_widths': self.fld2col_widths_dflts,
        }
        wr_xlsx(fout_xlsx, self.nts, **kws)
        #### print('  WROTE: {XLSX}'.format(XLSX=fout_xlsx))

    def get_nts(self):
        """Return namedtuples associated with results."""
        return [rec.get_nt_prt() for rec in self.results]


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
