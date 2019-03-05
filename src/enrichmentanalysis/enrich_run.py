"""Enrichment object."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
import sys
import collections as cx
from enrichmentanalysis.pvalcalc import FisherFactory
from enrichmentanalysis.multiple_testing import Methods
from enrichmentanalysis.enrich_rec import EnrichmentRecord
from enrichmentanalysis.enrich_results import EnrichmentResults


class EnrichmentRun():
    """Do Enrichment."""

    headers = 'TermID     Stu Tot Stu/Tot   Pop   Tot Pop/Tot P-uncorr  '
    patrec = ('{TERM_ID:10} '
              '{STU_CNT:3} {STU_TOT:3} {STU_RATIO:7.5f} '
              '{POP_CNT:5} {POP_TOT:5} {POP_RATIO:7.5f} '
              '{PVAL:8.2e} '
             )

    patpval = "Calculating {N:,} uncorrected p-values using {PFNC}\n"
    ntpval = cx.namedtuple('NtPvalArgs', 'study_count study_n pop_count pop_n')
    kw_dict = {
        'alpha':0.05,
        'methods':('fdr_bh'),
        'min_overlap':0.7}

    def __init__(self, population_ids, associations, **kws):
        # Save all population IDs and associations
        self.args = self._init_args(population_ids, associations, **kws)
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
        # self._run_multitest = {
        #     'statsmodels':lambda iargs: self._run_multitest_statsmodels(iargs)}
        self.objmethods = Methods(self.args['methods'], self.args['alpha'])

    def prt_results(self, results, prt=sys.stdout):
        """Print enrichment results in a text format."""
        prt.write(self._get_hdrs())
        for rec in results:
            prt.write(str(rec))

    def run_study(self, study_ids, log=sys.stdout):
        """Run an enrichment."""
        results = []
        # Get study IDs which which are present in the population
        study_in_pop = self._get_study_ids(study_ids, log)
        if not study_ids:
            return results
        # Uncorrected P-values
        results = self.get_pval_uncorr(study_in_pop, log)
        # Corrected P-values
        pvals_uncorr = [o.pval_uncorr for o in results]
        pvals_corrected = self.objmethods.run_multitest_corr(pvals_uncorr, log)
        # pvals_corr = self.objmethods.run_multipletests(pvals_uncorr)
        self._add_multitest(results, pvals_corrected)
        objres = EnrichmentResults(self, study_in_pop, results)
        return objres

    def _chk_genes(self, study):
        """Check gene sets."""
        stu_n = len(study)
        if self.pop_n < stu_n:
            exit("\nERROR: The study file contains more elements than the population file. "
                 "Please check that the study file is a subset of the population file.\n")
        # check the fraction of genomic ids that overlap between study and population
        overlap = float(len(study & self.pop_ids)) / stu_n
        if overlap < 0.95:
            sys.stderr.write("\nWARNING: only {} fraction of genes/proteins in study are found in "
                             "the population  background.\n\n".format(overlap))
        if overlap <= self.args.min_overlap:
            exit("\nERROR: only {} of genes/proteins in the study are found in the "
                 "background population. Please check.\n".format(overlap))

    def _add_multitest(self, results, pvals_corrected):
        """Add multiple-test correction results to each result record."""
        ntobj = cx.namedtuple('NtM', ' '.join(nt.fieldname for nt in self.objmethods.methods))
        for rec, pvals_corr in zip(results, zip(*pvals_corrected)):
            ntm = ntobj._make(pvals_corr)
            rec.multitests = ntm

    def get_pval_uncorr(self, study_in_pop, log=sys.stdout):
        """Calculate the uncorrected pvalues for study items."""
        results = []
        pop_n, study_n = self.pop_n, len(study_in_pop)

        _calc_pvalue = self.pval_obj.calc_pvalue
        term2stuids = self._get_term2ids(study_in_pop)
        allterms = set(term2stuids).union(self.term2popids)
        if log:
            log.write(self.patpval.format(N=len(allterms), PFNC=self.pval_obj.name))
        patfmt = self._get_patfmt()
        for goid in allterms:
            study_items = term2stuids.get(goid, set())
            study_count = len(study_items)
            pop_items = self.term2popids.get(goid, set())
            pop_count = len(pop_items)

            one_record = EnrichmentRecord(
                goid,
                pval_args=self.ntpval._make([study_count, study_n, pop_count, pop_n]),
                pval_uncorr=_calc_pvalue(study_count, study_n, pop_count, pop_n),
                stu_items=study_items,
                pop_items=pop_items,
                pat=patfmt)

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

    def _init_args(self, pop_ids, assc, **kws_usr):
        """Read arguments, Set options."""
        kws_set = {k:v for k, v in kws_usr.items() if k in self.kw_dict}
        # Set defaults if necessary
        for key, val in self.kw_dict.items():
            if val is not None and key not in kws_set:
                if key == 'methods':
                    kws_set[key] = tuple(val)
                else:
                    kws_set[key] = val
        kws_set['pop_ids'] = pop_ids
        kws_set['assc'] = assc
        return kws_set

    def _get_patfmt(self):
        """Get pattern format for printing results in a text format."""
        return '{PAT} {METHODS}\n'.format(
            PAT=self.patrec,
            METHODS=self.objmethods.get_patfmt())

    def _get_hdrs(self):
        """Get headers for printing results in a text format."""
        return self.headers + self.objmethods.get_headers() + '\n'


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
