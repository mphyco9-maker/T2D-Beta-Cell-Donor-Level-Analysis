# Xin et al. (2016) GSE81608: cell-count discrepancy evidence log (updated 20 November 2026)

**Question:** Why does GEO series GSE81608 contain 1,600 expression profiles when Xin et al. (2016) report 1,492 analyzed islet cells?

## Finding: explanation identified in the original primary source
The original article together with Supplemental Information explicitly describe the final filtering step that removes **108 single-hormone-expressing cells suspected of non-islet-cell contamination**. Thus **1,600 - 108 = 1,492**. This resolves the published **count discrepancy and stated exclusion rationale**, but does **not** identify the specific 108 GSM/sample IDs.

### Original filtering flow (Figure S1, supplemental PDF p. 11)
| Stage | Number remaining | Number removed at stage | Stated reason |
|---|---:|---:|---|
| Sequenced | 3,709 | - | Starting capture/sequencing set |
| Passed viability QC | 2,881 | 828 | Low viability/dying cells |
| Passed technical QC | 2,538 | 343 | Technical read-quality/outlier/contamination QC |
| Single-hormone cells before final artifact removal | 1,600 | 938 | More than one islet hormone expressed |
| Final analyzed high-quality single-hormone islet cells | 1,492 | 108 | Single-hormone cells with non-islet contamination signatures |

The paper's **Results**, article PDF pp. 2–3 (printed pages 608–609), explain that 108 single-hormone-expressing cells had distinct expression patterns. Eight highlighted non-islet-associated genes are **COL1A1, COL1A2, COL3A1, LCN2, TACSTD2, PLVAP, PODXL, and SPARC**. The authors interpret the profiles as likely artifacts from non-islet cells (e.g., fibroblasts or endothelial cells) contaminating cell capture. **Figure S2B** (supplemental PDF pp. 12–13) visually marks the 108 cells with a black bar but does **not** supply a machine-readable GSM/Sample_N list.

The **RNA-Seq Data Analysis** methods (article PDF p. 7, printed p. 613) give additional original QC criteria, including cell viability, exon-count and mapping-ratio checks, exocrine-marker contamination, hierarchical-clustering/Seurat outliers, and hormone-based cell-type assignment. These steps involve earlier reductions from 3,709 and must not be conflated with the final 108-cell step.

### Observed beta-cell count discrepancy
Supplemental **Table S1(C)** (PDF p. 17) labels the published final cell-type totals **alpha 886, beta 472, delta 49, PP 85** (sum 1,492). The current project manifest has **503 annotated beta cells among 1,600 deposited profiles**. The beta-cell counts differ by **31**, but **the exact 31 beta-cell IDs cannot be inferred** from the published table. Differences could reflect the original last QC step; the individual cell assignments still require direct verification.

## Reproducibility status
- Current project exact metadata–expression match: **1,600/1,600 profiles**, based on the earlier Task 1/current notebook audit.
- **Count discrepancy: EXPLAINED by primary-source published QC.**
- **Exact excluded-cell manifest: NOT RECOVERED.** Do not claim exact reproduction of the published 1,492-cell set.
- The 108 cells should **not** be removed from this reanalysis simply to match the published cell count. Maintain current annotated-cell analysis for now and clearly mark it as a deposited-data exploratory cohort, not the publication's identical QC-passed cohort.
- For sensitivity: prospectively specify expression-based non-islet contamination screens based on the original markers, and where original QC measurements are unavailable state that original viability/exon-mapping QC cannot be reconstructed from RPKM alone. Assess donor-wise and beta-cell-wise changes, with no significance-driven exclusions. Keep filtered and unfiltered donor summaries separate, and require technical/biological justification.

## Sources
1. Xin Y, et al. (2016). *RNA Sequencing of Single Human Islet Cells Reveals Type 2 Diabetes Genes.* Cell Metabolism. DOI: https://doi.org/10.1016/j.cmet.2016.08.018. Article plus supplemental information (user-supplied Elsevier **Document S2**, `1-s2.0-S155041311630434X-mmc5.pdf`): article PDF pages **2–3, 7**; supplemental **Figure S1** p. **11**, **Figure S2** pp. **12–13**, and **Table S1(C)** p. **17**.
2. GEO GSE81608: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE81608 (deposited profiles).

## Suggested faculty-facing status
"We resolved the numerical Xin discrepancy using the original supplemental Figure S1: 3,709 sequenced cells underwent viability (828 excluded), technical (343 excluded), multi-hormone (938 excluded), and final non-islet contamination (108 excluded) filtering, yielding 1,492 cells. Figure S2B marks the final 108 artifacts, but exact deposited GSM/Sample_N identities are not provided in the materials reviewed. We therefore have not removed cells solely to match the publication and will report the exact-manifest limitation and pre-specified contamination sensitivity analysis."
