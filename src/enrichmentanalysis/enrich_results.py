"""Store and manage enrichment results."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
# import collections as cx
# from enrichmentanalysis.pvalcalc import FisherFactory
# from enrichmentanalysis.multiple_testing import Methods


class EnrichmentResults():
    """Store and manage enrichment results."""

    def __init__(self, objearun, study_in_pop, results, name):
        self.name = name
        # Save the population IDs that are in the association
        self.objearun = objearun  # pop_ids pop_tot
        self.study_ids = study_in_pop
        self.study_tot = len(self.study_ids)
        # Note: It is assumed that all GO IDs, Pathway IDs, etc. in association are valid
        # IDs->(GO|Pathway|etc.)
        self.assc = objearun.assc
        self.term2popids = objearun.term2popids
        self.nt_methods = objearun.objmethods.methods
        # Results
        self.results = results

    @staticmethod
    def sortby_eaobj(obj):
        """Sortby function for sorted."""
        return [obj.ntpval.enrichment, obj.ntpval.pval_uncorr]

    def get_results_cond(self, max_pval, pval_field, sortby=None):
        """Get sorted results below specified pvalue or FDR."""
        if sortby is None:
            sortby = self.sortby_eaobj
        return sorted(self._get_results_cond(max_pval, pval_field), key=sortby)

    def _get_results_cond(self, max_pval, pval_field):
        """Get the subset of results which are under a specified p-value."""
        if max_pval is None:
            return self.results
        elif not pval_field:
            return self.get_pvals_uncorr_subset(max_pval)
        return self.get_pvals_corr_subset(max_pval, pval_field)

    def get_pvals_corr_subset(self, max_pval, pval_field):
        """Return all results for pvalues less than a specified max."""
        results = []
        for rec in sorted(self.results, key=lambda o: o.ntpval.pval_uncorr):
            ntm = rec.multitests
            if getattr(ntm, pval_field) < max_pval:
                results.append(rec)
            else:
                return results
        return results

    def get_pvals_uncorr_subset(self, max_pval):
        """Return all results for pvalues less than a specified max."""
        results = []
        for rec in sorted(self.results, key=lambda o: o.ntpval.pval_uncorr):
            if rec.pval_uncorr < max_pval:
                results.append(rec)
            else:
                return results
        return results

    def wr_found(self, fout_txt):
        """Write the found study genes."""
        with open(fout_txt, 'w') as prt:
            for study_id in self.study_ids:
                prt.write('{ID}\n'.format(ID=study_id))
            print('  {N:6} Study IDs found.                WROTE: {TXT}'.format(
                N=self.study_tot, TXT=fout_txt))

    def wr_notfound(self, fout_txt, pop_stu_genes):
        """Write the found study genes."""
        not_found = pop_stu_genes.difference(self.assc)
        with open(fout_txt, 'w') as prt:
            for gene_id in not_found:
                prt.write('{ID}\n'.format(ID=gene_id))
            print('  {N:6} study/population IDs not found. WROTE: {TXT}'.format(
                N=len(not_found), TXT=fout_txt))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
