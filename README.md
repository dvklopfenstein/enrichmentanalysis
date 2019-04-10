# Enrichment Analysis

Do enrichment analysis on anything if you provide:
  * IDs of the population 
  * IDs of the study set
  * Associations between the IDs and the terms of interest

[Example data](https://github.com/dvklopfenstein/enrichmentanalysis/tree/master/data/exgo)

## The enrichment analysis steps performed by this repo's code
  1. Generate pvalues using Fishers exact test
  2. Do multipletest correction with any of SciPy's statsmodel functions:    

| multicorrect   | Description
|----------------|--------------------------------------
|`sm_bonferroni` | bonferroni one-step correction    
|`sm_sidak`      | sidak one-step correction    
|`sm_holm-sidak` | holm-sidak step-down method using Sidak adjustments    
|`sm_holm`       | holm step-down method using Bonferroni adjustments    
|`simes-hochberg`| simes-hochberg step-up method (independent)    
|`hommel`        | hommel closed method based on Simes tests (non-negative)    
|`fdr_bh`        | fdr correction with Benjamini/Hochberg (non-negative)    
|`fdr_by`        | fdr correction with Benjamini/Yekutieli (negative)    
|`fdr_tsbh`      | two stage fdr correction (non-negative)    
|`fdr_tsbky`     | two stage fdr correction (non-negative)    

## To Cite
This code is a generalized version of selected code from the [GOATOOLS](https://github.com/tanghaibao/goatools) repository,
which is used to run gene ontology enrichment analysis. 

### Citation
_Please cite the following research paper if you use this repo in your research_:

Klopfenstein DV, Zhang L, Pedersen BS, ... Tang H
[**GOATOOLS: A Python library for Gene Ontology analyses**](https://www.nature.com/articles/s41598-018-28948-z)    
_Scientific reports_ | (2018) 8:10872 | DOI:10.1038/s41598-018-28948-z

Copyright (C) 2016-2019, DV Klopfenstein. All rights reserved.
