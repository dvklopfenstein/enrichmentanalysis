"""Multiple test correction."""

# import sys
# import random
# import numpy as np
import collections as cx
from statsmodels.sandbox.stats.multicomp import multipletests

__copyright__ = "Copyright (C) 2015-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"


# pylint: disable=old-style-class,too-few-public-methods
class MethodsAll():
    """All methods."""

    # https://github.com/statsmodels/statsmodels/blob/master/statsmodels/stats/multitest.py
    all_methods = [
        ("statsmodels", (
            'bonferroni',     #  0) Bonferroni one-step correction
            'sidak',          #  1) Sidak one-step correction
            'holm-sidak',     #  2) Holm-Sidak step-down method using Sidak adjustments
            'holm',           #  3) Holm step-down method using Bonferroni adjustments
            'simes-hochberg', #  4) Simes-Hochberg step-up method  (independent)
            'hommel',         #  5) Hommel closed method based on Simes tests (non-negative)
            'fdr_bh',         #  6) FDR Benjamini/Hochberg  (non-negative)
            'fdr_by',         #  7) FDR Benjamini/Yekutieli (negative)
            'fdr_tsbh',       #  8) FDR 2-stage Benjamini-Hochberg (non-negative)
            'fdr_tsbky',      #  9) FDR 2-stage Benjamini-Krieger-Yekutieli (non-negative)
            )),
    ]
    prefixes = {'statsmodels':'sm_'}

    def __init__(self):
        self.srcmethod2fieldname = self._init_srcmethod2fieldname()

    def getmsg_valid_methods(self):
        """Return a string containing valid method names."""
        msg = []
        msg.append("    Available methods:")
        for method_source, methods in self.all_methods:
            msg.append("        {SRC}(".format(SRC=method_source))
            for method in methods:
                attrname = self.srcmethod2fieldname[(method_source, method)]
                msg.append("            {ATTR}".format(ATTR=attrname))
            msg.append("        )")
        return "\n".join(msg)

    def _init_srcmethod2fieldname(self):
        """Return an OrderedDict with key, (method_src, method), and value, attrname."""
        srcmethod_fieldname = []
        ctr = self._get_method_cnts()
        for method_source, methods in self.all_methods:
            for method in methods:
                prefix = self.prefixes.get(method_source, "")
                prefix = prefix if ctr[method] != 1 else ""
                fieldname = "{P}{M}".format(P=prefix, M=method.replace('-', '_'))
                srcmethod_fieldname.append(((method_source, method), fieldname))
        return cx.OrderedDict(srcmethod_fieldname)

    def _get_method_cnts(self):
        """Count the number of times a method is seen."""
        ctr = cx.Counter()
        for source_methods in self.all_methods:
            for method in source_methods[1]:
                ctr[method] += 1
        return ctr


class Methods():
    """Class to manage multipletest methods from both local and remote sources."""

    ntresstat = cx.namedtuple('NtStat', 'reject_lst, pvals_corrected, alphacSidak, alphacBonf')

    def __init__(self, usr_methods=None, alpha=0.05):
        self.alpha = alpha
        assert 0 < alpha < 1, "Test-wise alpha must fall between (0, 1)"
        self.all = MethodsAll()
        _ini = _Init(self.all)
        self._srcmethod2fieldname = _ini.srcmethod2fieldname
        self.statsmodels_multicomp = multipletests
        if usr_methods is None:
            usr_methods = ['fdr_bh']
        self.methods = _ini.get_methods(usr_methods)

    def run_multitest_corr(self, ntpvals_uncorr, log):
        """Do multiple-test corrections on uncorrected pvalues."""
        # ntobj = cx.namedtuple("ntobj", "results pvals_uncorr alpha nt_method study")
        pvals_corrected = []
        pvals_uncorr = [nt.pval_uncorr for nt in ntpvals_uncorr]
        for nt_method in self.methods:  # usrmethod_flds:
            # NtMethodInfo(source='statsmodels', method='bonferroni', fieldname='bonferroni'))
            # NtMethodInfo(source='statsmodels', method='fdr_bh', fieldname='fdr_bh'))
            ntres = self._run_multitest_statsmodels(pvals_uncorr, nt_method.method)
            # attr_mult = "p_{M}".format(M=self.get_fieldname(nt_method.source, nt_method.method))
            pvals_corrected.append(ntres.pvals_corrected)
            if log is not None:
                self._log_multitest_corr(log, ntres, ntpvals_uncorr, nt_method)
        assert len(pvals_corrected) == len(self.methods)
        return pvals_corrected

    def _log_multitest_corr(self, log, ntres, ntpvals_uncorr, nt_method):
        """Print information regarding multitest correction results."""
        _alpha = self.alpha
        eps = [nt.enrichment for pf, nt in zip(ntres.reject_lst, ntpvals_uncorr) if pf]
        sig_cnt = len(eps)
        ctr = cx.Counter(eps)
        log.write("{N:8,} terms ".format(N=sig_cnt))
        log.write('({E:3} enriched + {P:3} purified) '.format(E=ctr['e'], P=ctr['p']))
        log.write("found significant with alpha({A}): {MSRC} {METHOD}\n".format(
            A=self.alpha, MSRC=nt_method.source, METHOD=nt_method.method))

    def _run_multitest_statsmodels(self, pvals_uncorr, method):
        """Use multitest mthods that have been implemented in statsmodels."""
        # print(len(pvals_uncorr), self.alpha, method)
        results = self.statsmodels_multicomp(pvals_uncorr, self.alpha, method)
        # self._update_pvalcorr(ntmt, pvals_corrected)
        return self.ntresstat(
            reject_lst=results[0],
            pvals_corrected=results[1],
            alphacSidak=results[2],
            alphacBonf=results[3])

    # def run_multipletests(self, pvals_uncorr):
    #     """Run multiple-test correction."""
    #     return self.statsmodels_multicomp(pvals_uncorr, self.alpha,

    def get_fieldname(self, method_source, method):
        """Get the name of the method used to create namedtuple fieldnames which store floats."""
        return self._srcmethod2fieldname[(method_source, method)]

    #### def get_statsmodels_multipletests(self):
    ####     if self.statsmodels_multicomp is not None:
    ####         return self.statsmodels_multicomp
    ####     self.statsmodels_multicomp = multipletests
    ####     return self.statsmodels_multicomp

    def get_patfmt(self):
        """Get pattern format for values in each method."""
        return ' '.join(['{{{METHOD}:8.2e}}'.format(METHOD=m.fieldname) for m in self.methods])

    def get_headers(self):
        """Get pattern format for column headers in each method."""
        return ' '.join(['{METHOD:<8}'.format(METHOD=m.fieldname) for m in self.methods])

    def get_fields(self):
        """Get pattern format for method fields."""
        return ' '.join(['{METHOD}'.format(METHOD=m.fieldname) for m in self.methods])


class _Init():
    """Initialize Methods object."""

    NtMethodInfo = cx.namedtuple("NtMethodInfo", "source method fieldname")

    def __init__(self, obj_all_methods):
        self.obj = obj_all_methods
        self.srcmethod2fieldname = obj_all_methods.srcmethod2fieldname


    def get_methods(self, usr_methods):
        """From the methods list, set list of methods to be used during GOEA."""
        return [self._add_method(usr_method) for usr_method in usr_methods]

    def _add_method(self, method, method_source=None):
        """Determine method source if needed. Add method to list."""
        try:
            # print('METHOD SOURCE: {S} METHOD: {M}'.format(S=method_source, M=method))
            if method_source is not None:
                return self._add_method_src(method_source, method)
            else:
                return self._add_method_nosrc(method)
        except Exception as inst:
            raise Exception("{ERRMSG}".format(ERRMSG=inst))

    def _add_method_nosrc(self, usr_method):
        """Add method source, method, and fieldname to list of methods."""
        for method_source, available_methods in self.obj.all_methods:
            if usr_method in available_methods:
                fieldname = self.get_fldnm_method(usr_method)
                return self.NtMethodInfo(method_source, usr_method, fieldname)
        for src, prefix in self.obj.prefixes.items():
            if usr_method.startswith(prefix):
                method_source = src
                method = usr_method[len(prefix):]
                return self.NtMethodInfo(method_source, method, usr_method)
        raise self._rpt_invalid_method(usr_method)

    def _add_method_src(self, method_source, usr_method, fieldname=None):
        """Add method source and method to list of methods."""
        fieldname = self.srcmethod2fieldname.get((method_source, usr_method), None)
        if fieldname is not None:
            return self.NtMethodInfo(method_source, usr_method, fieldname)
        else: raise Exception("ERROR: FIELD({FN}) METHOD_SOURCE({MS}) AND METHOD({M})".format(
            FN=fieldname, MS=method_source, M=usr_method))

    def _rpt_invalid_method(self, usr_method):
        """Report which methods are available."""
        msgerr = "FATAL: UNRECOGNIZED METHOD({M})".format(M=usr_method)
        msg = [msgerr, self.obj.getmsg_valid_methods(), msgerr]
        raise Exception("\n".join(msg))

    @staticmethod
    def get_fldnm_method(method):
        """Given method and source, return fieldname for method."""
        fieldname = method.replace('-', '_')
        return fieldname


# Copyright (C) 2015-2019, DV Klopfenstein. All rights reserved.
