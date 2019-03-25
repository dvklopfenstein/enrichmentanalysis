"""Holds population set, associations, and methods for one or more enrichment analyses."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx
from enrichmentanalysis.pvalcalc import FisherFactory
from enrichmentanalysis.multiple_testing import Methods
from enrichmentanalysis.enrich_rec import EnrichmentRecord
from enrichmentanalysis.enrich_results import EnrichmentResults


class EnrichmentRun():
    """Holds population set, associations, and methods for one or more enrichment analyses."""

    patpval = "Calculating {N:,} uncorrected p-values using {PFNC}\n"
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
        self.pop_tot = len(self.pop_ids)
        # Note: It is assumed that all GO IDs, Pathway IDs, etc. in association are valid
        # IDs->(GO|Pathway|etc.)
        self.assc = {a_id:terms for a_id, terms in associations.items() if a_id in self.pop_ids}
        self.term2popids = self._get_term2ids(self.pop_ids)
        self.pval_obj = FisherFactory().pval_obj
        # self._run_multitest = {
        #     'statsmodels':lambda iargs: self._run_multitest_statsmodels(iargs)}
        self.objmethods = Methods(self.args['methods'], self.args['alpha'])

    def run_study(self, study_ids, study_name, log=sys.stdout):
        """Run an enrichment analysis."""
        results = []
        # Get study IDs which which are present in the population
        study_in_pop = self._get_study_ids(study_ids, log)
        if not study_ids:
            return results
        # Uncorrected P-values
        results = self.get_pval_uncorr(study_in_pop, log)
        # Corrected P-values
        ntpvals_uncorr = [o.ntpval for o in results]
        pvals_corrected = self.objmethods.run_multitest_corr(ntpvals_uncorr, log)
        self._add_multitest(results, pvals_corrected)
        objres = EnrichmentResults(self, study_in_pop, results, study_name)
        return objres

    def _chk_genes(self, study):
        """Check gene sets."""
        stu_n = len(study)
        if self.pop_tot < stu_n:
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
        ntobj_mult = cx.namedtuple('NtM', ' '.join(nt.fieldname for nt in self.objmethods.methods))
        prtfmt = self._get_prtfmt()
        ntobj_results = self._get_ntobj()
        # print(ntobj_results._fields)
        for rec, pvals_corr in zip(results, zip(*pvals_corrected)):
            rec.multitests = ntobj_mult._make(pvals_corr)
            rec.prtfmt = prtfmt
            rec.ntobj = ntobj_results

    def get_pval_uncorr(self, study_in_pop, log=sys.stdout):
        """Calculate the uncorrected pvalues for study items."""
        results = []
        pop_tot, study_tot = self.pop_tot, len(study_in_pop)

        _get_ntpval = self.pval_obj.get_nt
        term2stuids = self._get_term2ids(study_in_pop)
        allterms = set(term2stuids).union(self.term2popids)
        if log:
            log.write(self.patpval.format(N=len(allterms), PFNC=self.pval_obj.name))
        for goid in allterms:
            study_items = term2stuids.get(goid, set())
            study_cnt = len(study_items)
            pop_items = self.term2popids.get(goid, set())
            pop_cnt = len(pop_items)

            one_record = EnrichmentRecord(
                goid,
                ntpval=_get_ntpval(study_cnt, study_tot, pop_cnt, pop_tot),
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

    def _get_ntobj(self):
        """Create namedtuple object for enrichment results records."""
        return cx.namedtuple('ntresults', ' '.join([
            ' '.join(EnrichmentRecord.flds),
            self.objmethods.get_fields(),
            'stu_items']))

    def _get_prtfmt(self):
        """Return format pattern for printing this record as text."""
        if 'prtfmt' not in self.args:
            return '{FMT} {M}'.format(
                FMT=' '.join(EnrichmentRecord.fld2fmt.values()),
                M=self.objmethods.get_patfmt())
        return self.args['prtfmt']


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
