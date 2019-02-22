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

    def __init__(self, objearun, study_ids, results):
        # Save the population IDs that are in the association
        self.pop_ids = objearun.pop_ids
        self.pop_n = objearun.pop_n
        self.study_ids = study_ids
        # Note: It is assumed that all GO IDs, Pathway IDs, etc. in association are valid
        # IDs->(GO|Pathway|etc.)
        self.assc = objearun.assc
        self.term2popids = objearun.term2popids
        self.nt_methods = objearun.objmethods.methods
        # Results
        self.results = results


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
