# Three-paper comparison requested by supervisor (CURRENT)

**Updated:** 21 November 2026
**Scope:** Xin et al. (2016), Lawlor et al. (2017) and Squair et al. (2021), with Marques et al. (2022) as additional literature. This is a literature/methods comparison, **not** the result of differential-expression analysis in the current project.

| Dimension | Xin et al. (2016) | Lawlor et al. (2017) | Squair et al. (2021) |
|---|---|---|---|
| Paper | *RNA Sequencing of Single Human Islet Cells Reveals Type 2 Diabetes Genes*. **Cell Metabolism 24(4):608–615**. DOI: [10.1016/j.cmet.2016.08.018](https://doi.org/10.1016/j.cmet.2016.08.018) | *Single-cell transcriptomes identify human islet cell signatures and reveal cell-type-specific expression changes in type 2 diabetes*. **Genome Research 27(2):208–222**. DOI: [10.1101/gr.212720.116](https://doi.org/10.1101/gr.212720.116) | *Confronting false discoveries in single-cell differential expression*. **Nature Communications 12:5692**. DOI: [10.1038/s41467-021-25960-2](https://doi.org/10.1038/s41467-021-25960-2) |
| Central question | Which islet cell-type expression patterns and genes differ in T2D? | What are the signatures of islet cell types and which T2D-associated changes are revealed at single-cell resolution? | Which DE methods avoid false discoveries caused by ignoring biological-replicate variability? |
| Study/data type | Human pancreatic islet single-cell RNA-seq | Human pancreatic islet single-cell RNA-seq, also compared with paired whole-islet libraries | Benchmark/methodology study across datasets; **not a third pancreatic-islet dataset** |
| Original sampling and published findings | 12 ND and 6 T2D organ donors; 1,492 high-quality analyzed endocrine cells; paper reports 245 T2D-associated genes across cell types, including 48 in beta cells | 5 ND and 3 T2D organ donors; GSE86469 contains 638 processed single-cell profiles; paper reports cell-type signatures and T2D-associated changes, including 248 beta-cell DE genes under its own methodology | Compared methods on benchmark datasets and found that disregarding variation between biological replicates can produce false-positive DE results; methods aggregating cells **within true biological replicates** performed well |
| Matrices supplied for this thesis | GSE81608: **39,851 numeric GeneID features × 1,600 cells**, normalized RPKM; originally annotated beta cells **207 ND + 296 T2D = 503** | GSE86469: **26,616 Ensembl-style features × 638 cells**, RSEM fractional expected counts; annotated beta cells **168 ND + 96 T2D = 264** | No expression matrix from Squair is being used in this project |
| Original processing/annotation context | Reads aligned to **GRCh37**; RPKM expression reported. Full mapping to modern NCBI/Ensembl IDs needs historic-annotation caution | **GRCh37, Ensembl v70**, Bowtie2 read mapping, RSEM expression estimation; supplementary file labelled **RSEM raw expected counts**; detailed source-to-local conversion and count-model suitability still require confirmation | Main principle is biological-replicate-aware inference, not a mandate to apply a raw-count pseudobulk model to already normalized RPKM |
| Key limitation for this project | GEO supplies 1,600 cells, whereas paper analyzes 1,492: 108 apparent contaminant single-hormone cells removed in original paper. **Exact excluded GSM/cell list not recovered**; published final beta count 472 vs 503 in local original annotations. Crosswalk from current NCBI reference does not establish historic GRCh37 mapping equivalence | Only **three T2D donors**; fractional expected counts; limited covariates and potential influential donors; biological independence from Xin remains unverified | Establishes methodological risk but cannot itself verify either dataset's gene associations, donor independence or correct model specification |
| Role in planned thesis | **Discovery (provisional)**: donor mean of `log2(1+RPKM)`, analyzed using a suitable linear model once approved; **not raw-count pseudobulk** | **Exploratory replication (provisional)**: donor-level fractional RSEM expected-count sums, with count model only after validating count provenance and method suitability | Motivation for using donors as the unit of biological replication and assessing false positives / robustness |

## Evidence and project-specific corrections documented after Task 1

1. **Xin published-cell discrepancy:** Original publication and supplemental QC describe 108 single-hormone-expressing cells with expression patterns consistent with non-islet contamination (including fibroblast/endothelial-associated markers). **This explains the numerical difference, not the identities of the excluded cells.** No arbitrary 108-cell or 31-beta-cell deletion has been made. See `Xin_108_cell_search_log.md` and Xin et al. (2016), Results and supplemental Figure S1/S2.
2. **Gene crosswalk:** The current NCBI `gene2ensembl` lookup of 39,851 numeric Xin features gives **30,160 unique**, **9,668 unmapped**, **23 ambiguous** mappings; marker references for **INS/GCG/SST/PPY** match. These counts are **modern-reference results**, not proof that the original GRCh37 annotation has been fully reconciled. Current mapping: `GSE81608_gene_identifier_mapping_COMPLETED.csv`.
3. **Lawlor identifier check:** All 26,616 IDs match stable Ensembl ID format, with no duplicates or missing IDs in the submitted mapping table. The original study describes **GRCh37 / Ensembl v70**. ID format alone does **not** validate gene identity against that precise release. See `GSE86469_gene_identifier_mapping.csv`.
4. **Aggregation audit:** GSE81608's 503 beta cells / 18 donor means of `log2(1+RPKM)` matched recomputation (max absolute difference approximately **1.78e-15**). GSE86469's 264 beta cells / 8 donor expected-count sums matched recomputation (max absolute difference approximately **4.66e-10**). These are numerical checks, **not statistical inference**. The fractional RSEM counts were not rounded.
5. **Donor overlap:** Xin reports islets from **Prodo Laboratories**; Lawlor reports **ProdoLabs or IIDP**. Four pairs share age, sex and disease label, but this is **demographic-only matching**, not biological donor identification. Cross-study independence remains unverified. See `Donor_Overlap_Provenance_Check.md` and `cross_study_donor_overlap_screen.csv`.

## Additional literature — distinct from the requested three papers

**Marques et al. (2022)**. *Relationships between type 2 diabetes, cell dysfunction, and redox signaling: A meta-analysis of single-cell gene expression of human pancreatic alpha- and beta-cells*. **Journal of Diabetes 14(1):34–51**. DOI: [10.1111/1753-0407.13236](https://doi.org/10.1111/1753-0407.13236). Analyzed annotated single-cell datasets from **six studies**, assessed alpha- and beta-cell changes, and emphasized redox signaling including NFE2L2-related responses. The present thesis **will not claim novelty simply because it combines studies**; the proposed distinct contribution is a pre-specified assessment of **candidate association stability under donor-level inference, age adjustment where estimable, influential-donor sensitivity, and unresolved provenance**.

**Suleiman et al. (2025):** retained as secondary literature from the prior submission; bibliographic details and relevance should be verified before final citation.

## Proposed contribution — claim only after the analyses are completed

**Research question:** Which candidate T2D-associated beta-cell expression differences have consistent directions and reasonably stable effect estimates across Xin discovery and Lawlor exploratory replication when the **donor** is the inferential unit, age confounding and influential/low-cell donors are examined, and all eligible genes (rather than only favourable hits) are considered?

Pre-specify the cross-study gene universe and mapping rule; report complete direction concordance, effect sizes, scatterplots, rank correlation and uncertainty, including failures to replicate. The two expression scales remain separate and **must not be merged directly**. Candidate associations are **not** validated biomarkers, causal effects, or diagnostic tests.

## Open issues / no-DE gate

- Historic GRCh37-compatible feature crosswalk and Ensembl v70 ID verification need final audit.
- Precise Xin 108 excluded-cell identifiers are not recovered; evaluate a documented QC sensitivity without forcing 1,492.
- Donor identity overlap between studies cannot be ruled in or out from current records.
- Validate original-vs-local RSEM expected-count provenance, sample-level scaling and suitability of proposed donor-level count modeling; do not round fractional counts.
- Faculty/supervisor must review and approve the **two-page statistical protocol** before DE; pathway work follows established DE methods. **No DE or pathway analysis has been run in the current project.**

## Direct primary sources

- Xin publication: https://doi.org/10.1016/j.cmet.2016.08.018 ; GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE81608
- Lawlor open-access paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC5287227/ ; GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE86469
- Squair open-access paper: https://www.nature.com/articles/s41467-021-25960-2
- Marques open-access paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC8746116/
