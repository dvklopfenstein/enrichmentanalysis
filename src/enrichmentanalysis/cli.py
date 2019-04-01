"""Return EnrichmentRun containing population IDs, association, alpha ane methods."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from enrichmentanalysis.file_utils import read_ids
from enrichmentanalysis.file_utils import read_associations
from enrichmentanalysis.enrich_run import EnrichmentRun


def get_enrichment_run(args):
    """Return EnrichmentRun containing population IDs, association, alpha ane methods."""
    pop_dct = read_ids(args['population_ids'])
    assc = read_associations(args['associations'])
    methods = args['methods'].split(',')
    return EnrichmentRun(pop_dct['ids'], assc,
                         alpha=float(args['alpha']),
                         methods=methods,
                         name=pop_dct.get('name'))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
