# Enrichment Analysis

Do enrichment analysis on anything if you provide:
  * IDs of the population 
  * IDs of the study set
  * Associations between the IDs and the terms of interest

## The Enrichment Analysis Steps
  1. Generate pvalues using Fishers exact test
  2. Do multipletest correction with any of the statsmodels functions:    
    * `sm_bonferroni`, bonferroni one-step correction
    * `sm_sidak`, sidak one-step correction
    * `sm_holm-sidak`, holm-sidak step-down method using Sidak adjustments
    * `sm_holm`, holm step-down method using Bonferroni adjustments
    * `simes-hochberg`, simes-hochberg step-up method (independent)
    * `hommel`, hommel closed method based on Simes tests (non-negative)
    * `fdr_bh`, fdr correction with Benjamini/Hochberg (non-negative)
    * `fdr_by`, fdr correction with Benjamini/Yekutieli (negative)
    * `fdr_tsbh`, two stage fdr correction (non-negative)
    * `fdr_tsbky`, two stage fdr correction (non-negative)

Copyright (C) 2015-2019, DV Klopfenstein. All rights reserved.
