"""Enrichment object."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
import sys
import collections as cx
from enrichmentanalysis.pvalcalc import FisherFactory
from enrichmentanalysis.multiple_testing import Methods
from enrichmentanalysis.enrich_rec import EnrichmentRecord


class EnrichmentRun():
    """Do Enrichment."""

    patpval = "Calculating {N:,} uncorrected p-values using {PFNC}\n"
    ntpval = cx.namedtuple('NtPvalArgs', 'study_count study_n pop_count pop_n')

    def __init__(self, population_ids, associations, alpha=.05, methods=None, log=sys.stdout):
        # Save all population IDs and associations
        self.all = {'pop_ids': population_ids, 'assc':associations}
        assert population_ids, "NO POPULATION IDs: {A}".format(A=population_ids)
        assert associations, "EMPTY ASSOCIATION: {A}".format(A=associations)
        # Save the population IDs that are in the association
        self.pop_ids = population_ids.intersection(set(associations))
        self._prt_perc_found('population', 'assocation', self.pop_ids, population_ids)
        assert self.pop_ids, "NO POPULATION IDs IN ASSOCIATIONS: {A}".format(A=self.pop_ids)
        self.pop_n = len(self.pop_ids)
        # Note: It is assumed that all GO IDs, Pathway IDs, etc. in association are valid
        # IDs->(GO|Pathway|etc.)
        self.assc = {a_id:terms for a_id, terms in associations.items() if a_id in self.pop_ids}
        self.term2popids = self._get_term2ids(self.pop_ids)
        self.pval_obj = FisherFactory().pval_obj
        if methods is None:
            methods = ['fdr_bh']
        self.methods = Methods(methods)

    def run_study(self, study_ids, log=sys.stdout):
        """Run an enrichment."""
        results = []

        # Get study IDs which which are present in the population
        study_in_pop = self._get_study_ids(study_ids, log)
        if not study_ids:
            return results

        pval_uncorr = self.get_pval_uncorr(study_ids, log)
        return results

    def get_pval_uncorr(self, study_in_pop, log=sys.stdout):
        """Calculate the uncorrected pvalues for study items."""
        results = []
        pop_n, study_n = self.pop_n, len(study_in_pop)

        _calc_pvalue = self.pval_obj.calc_pvalue
        term2stuids = self._get_term2ids(study_in_pop)
        allterms = set(term2stuids).union(self.term2popids)
        if log:
            log.write(self.patpval.format(N=len(allterms), PFNC=self.pval_obj.name))
        for goid in allterms:
            study_items = term2stuids.get(goid, set())
            study_count = len(study_items)
            pop_items = self.term2popids.get(goid, set())
            pop_count = len(pop_items)

            one_record = EnrichmentRecord(
                goid,
                pval_args = self.ntpval._make([study_count, study_n, pop_count, pop_n]),
                pval_uncorr=_calc_pvalue(study_count, study_n, pop_count, pop_n),
                stu_items=study_items,
                pop_items=pop_items)

            results.append(one_record)

        return results

    def _get_study_ids(self, study_ids, prt):
        """Get the study IDs which are in the association and in the population."""
        if not study_ids:
            return {}
        study_in_pop = set(study_ids).intersection(self.pop_ids)
        self._prt_perc_found('study', 'population and association', study_in_pop, study_ids, prt)
        return study_in_pop

    def _get_term2ids(self, geneset):
        """Get the terms in the IDs group"""
        term2ids = cx.defaultdict(set)
        _assc = self.assc
        genes_in_assc = geneset.intersection(_assc)  # [g for g in geneset if g in assoc]
        for gene in genes_in_assc:
            for goid in _assc[gene]:
                term2ids[goid].add(gene)
        return {t:ids for t, ids in term2ids.items()}

    @staticmethod
    def _prt_perc_found(strcur, strtot, ids_cur, ids_tot, prt=sys.stdout):
        """Print percentage IDs found in the association."""
        num_cur = len(ids_cur)
        num_tot = len(ids_tot)
        perc = 100.0*num_cur/num_tot if num_tot != 0 else 0.0
        prt.write("{P:3.0f}% {N:>6,} of {M:>6,} {CUR} IDs found in {TOT}\n".format(
            CUR=strcur, TOT=strtot, N=num_cur, M=num_tot, P=perc))

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
