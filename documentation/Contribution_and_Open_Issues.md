# Contribution statement and unresolved issues (CURRENT)

## Proposed contribution
Rather than reproducing a list of T2D-associated beta-cell genes, we aim to evaluate whether **candidate donor-level beta-cell transcriptomic associations** are directionally and quantitatively stable across distinct human islet studies when biological donors, age imbalance, uneven cell representation and influential samples are accounted for. Discovery in GSE81608 and exploratory replication in GSE86469 remain provisional, and the datasets' different expression scales must be analyzed separately. Results cannot establish causality or clinical diagnostics.

## Confirmed current input/output facts
- 1,600 expression columns match 1,600 metadata cells in GSE81608, with 503 originally annotated beta cells from 18 donors (12 ND/6 T2D).
- 638 expression columns match 638 metadata cells in GSE86469, with 264 originally annotated beta cells from 8 donors (5 ND/3 T2D).
- Four NCBI-verified marker IDs are present in both matrices: INS, GCG, SST, PPY. Previous summary's missing marker figures are superseded.
- GSE81608 produces donor-level **means of log2(1+RPKM)**; these are *not* raw-count pseudobulks.
- GSE86469 produces donor-level **sums of fractional RSEM expected counts** and log2(1+CPM) only for exploratory visualization. No arbitrary rounding is applied.
- GSE86469's `ACEK420A` is flagged for descriptive review by low beta-cell representation (10 cells) and strong PCA deviation. This is **not a donor exclusion**.

## Unresolved issues requiring documented follow-up
1. **Xin 1,600 vs 1,492:** GEO includes 1,600 records; the published series summary describes 1,492 analyzed. The exact omitted GSM list is not in this submission. Inspect original publication methods, supplement, author material/contact or sample-level filtering records; never remove 108 arbitrarily. If unrecoverable, report this limitation and compare analyses retaining all annotated beta cells vs transparently defined technical QC thresholds. A *later* paper's 1,492 retained profiles is not proof of Xin's original 108 exclusions.
2. **Xin numeric GeneID to Ensembl:** Present mapping is complete only for four NCBI-verified markers and other GeneIDs are explicitly `pending_external_NCBI_gene2ensembl`, not incorrectly `unmapped`. Run `python scripts/complete_gene_crosswalk.py` with a network connection; record source checksum, ambiguous mappings and assembly/annotation compatibility (Xin used GRCh37/hg19).
3. **Lawlor gene annotation reference:** Original Ensembl-like ENSG IDs need an exact Ensembl release/assembly check. The file contains stable-like IDs but that alone does not prove version/provenance.
4. **Lawlor RSEM counts:** GEO labels the supplied file `RSEM.raw.expected.counts`, and many positive entries are fractional, consistent with expected counts. Confirm underlying RSEM quantification and *absence of normalized scaling* against original methods and deposited files **before count-based DE**.
5. **Donor overlap:** Distinct labels do not prove independent donors. Compare original supplier/biobank provenance and supplementary donor information. No definitive cross-study identity linkage has been established here. See `cross_study_donor_overlap_screen.csv` for limited demographic matches only; matches or nonmatches there are not evidence of identity or independence.
6. **Age imbalance:** In both submitted datasets T2D donors are older on average; primary age-adjusted models must be checked for collinearity and leverage. BMI missing entirely in GSE81608, and small donor counts argue against many simultaneous covariates.
7. **Outlier/small-cell sensitivity:** Four donors have <=10 original beta cells. Report preplanned sensitivity analyses; never discard a donor based on whether their removal improves p-values.
8. **Agreement statistic:** The unexplained `94.1% agreement` statement from earlier materials has no documented denominator, method or raw calculation here and has been REMOVED from current claims.
9. **GitHub and shared storage:** This archive has been prepared locally; GitHub upload is **not completed**. Large CSVs are excluded from git with `.gitignore`. Add actual shared-storage URLs before external submission, or retrieve files from GEO with verification.
10. **Supervisor approval:** Protocol review is required **before** any DE tests, then pathway analysis follows only after a defensible DE method is established.

## Suggested division among 4 members (replace placeholders with names)
- Member 1 — Literature, novelty, two-page protocol (owner of protocol deliverable).
- Member 2 — Inventory, crosswalk, provenance, Xin discrepancy and donor overlap (owner of documentation deliverable).
- Member 3 — Aggregation, donor metadata, PCA, outlier figures (owner of matrices/figures deliverable).
- Member 4 — Execute notebook, consolidate QC, README and GitHub release (owner of repository/notebook deliverable).
- Member 1 + Member 4 jointly check the contribution/open-issues deliverable. **All four must reproduce and explain the end-to-end workflow.**
