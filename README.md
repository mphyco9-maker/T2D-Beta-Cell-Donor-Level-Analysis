# CURRENT — Human pancreatic β-cell T2D donor-level exploratory workflow

**Current checkpoint:** 21 November 2026 (Task 1 corrections and Task 2 exploratory preparation)
**Status:** Donor-level exploratory workflow and numerical aggregation checks completed; **no differential-expression (DE) or pathway analysis performed**. Two-page statistical protocol awaits supervisor review.
**Scope:** GSE81608 (Xin et al., 2016) is provisionally the discovery study; GSE86469 (Lawlor et al., 2017) is exploratory replication. Expression data are **not pooled**, and biological donor independence across studies remains unverified.

## 1. Research question and contribution

Assess whether candidate associations between type 2 diabetes (T2D) and pancreatic β-cell gene expression remain consistent across two studies after respecting the **donor as biological replicate**, considering age differences and influential/low-cell-count donors. The intended contribution is an auditable *cross-study stability analysis*, not a diagnostic, causal, or independently validated gene signature.

## 2. Corrections since Task 1

- Repaired the formerly malformed dataset inventory as `documentation/dataset_inventory_CURRENT.csv` (readable with `pandas.read_csv`).
- Regenerated numerical QC, cell-to-metadata matching, and nonempty marker plots; INS, GCG, SST, and PPY identifiers are present in both matrices.
- Consolidated the executable exploratory workflow in `scripts/run_exploratory.py`; an executed notebook is included at `notebooks/T2D_Task2_Exploratory_EXECUTED.ipynb` (rerun before final submission to confirm its stored outputs match the current release). Prior outputs are retained locally under `archive_previous/`, excluded from GitHub via `.gitignore`, and not treated as current.
- Created separate donor-level β-cell matrices, donor metadata, PCA, expression distributions, and outlier-review flags. **No donors were excluded.**
- Replaced the requested core literature comparison with **Xin (2016), Lawlor (2017), and Squair (2021)**; Marques (2022) and other papers are additional literature.
- Removed the unsupported **“94.1% agreement”** statement.
- Updated Xin's 108-cell discrepancy evidence log, donor-source provenance, NCBI gene mapping summary, and the two-page **review** protocol. Some final biological-provenance questions remain unresolved; see Section 8.

## 3. Input datasets and study roles

| Dataset / role | Converted local expression file (`data/expression/`) | Scale | Cells | Features | Donors (ND/T2D) | Annotated β-cells (ND/T2D) |
|---|---|---|---:|---:|---:|---:|
| [GSE81608](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE81608) / provisional discovery | `GSE81608_expression_RPKM.csv` | Already-normalized RPKM | 1,600 | 39,851 | 12/6 | 207/296 |
| [GSE86469](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE86469) / exploratory replication | `GSE86469_expression_RSEM_expected_counts.csv` | RSEM estimated counts; fractional values retained | 638 | 26,616 | 5/3 | 168/96 |

Metadata: `data/metadata/GSE81608_GEO_sample_metadata.csv` and `data/metadata/GSE86469_GEO_sample_metadata.csv`. Cell-to-donor links and sample provenance: `documentation/cell_manifest_with_provenance_CURRENT.csv`.

The supplied local converted CSVs were validated against metadata, with **2,238 matched cells, 767 annotated β-cells, and 26 donor groups** across the two studies. This does not certify the original publications' final QC subsets.

### Original GEO supplementary sources

- Xin RPKM: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE81nnn/GSE81608/suppl/GSE81608_human_islets_rpkm.txt.gz
- Lawlor RSEM: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE86nnn/GSE86469/suppl/GSE86469_GEO.islet.single.cell.processed.data.RSEM.raw.expected.counts.csv.gz

**Integrity caveat:** `documentation/INPUT_SHA256SUMS.txt` checksums correspond to the **converted local CSV inputs**, not original GEO `.gz` archives. The downloaded originals and conversion procedure must be separately documented and checked if used to reconstruct the local files. `python scripts/download_GEO_inputs.py` downloads original compressed inputs; it does **not** by itself recreate byte-identical converted CSVs.

### Retrieve large expression datasets (required for reproduction)

**Current GitHub repository (private):** https://github.com/mphyco9-maker/T2D-Beta-Cell-Donor-Level-Analysis (branch `main`; initial local commit `199701a` was pushed and the online file listing was inspected). Authorized collaborators need GitHub access.

**Google Drive folder (restricted):** https://drive.google.com/drive/folders/1MXyVBVMwaqwMadmcqe7IQgHroHUdVXNE?usp=sharing

1. Ask the repository/data owner to grant your Google account **Viewer** permission to the Drive folder. Having the link alone does not grant access.
2. Download both files **as CSV** without opening/re-saving or converting them through Google Sheets:
   - `GSE81608_expression_RPKM.csv` (Xin; approx. 169.3 MB shown in Drive)
   - `GSE86469_expression_RSEM_expected_counts.csv` (Lawlor; approx. 46.1 MB shown in Drive)
3. In your cloned/extracted repository, create `data/expression/` if necessary and place the downloaded files there with these **exact filenames**. This path is excluded from Git by `.gitignore`.
4. From the repository root, validate the **downloaded** bytes against the SHA-256 values below before running any analysis. On Windows Command Prompt:

   ```cmd
   certutil -hashfile "data\expression\GSE81608_expression_RPKM.csv" SHA256
   certutil -hashfile "data\expression\GSE86469_expression_RSEM_expected_counts.csv" SHA256
   ```

   On macOS/Linux use `shasum -a 256 data/expression/*.csv` or `sha256sum data/expression/*.csv` (depending on system).

   | Converted CSV file | Required SHA-256 |
   |---|---|
   | `GSE81608_expression_RPKM.csv` | `8699e29653c0fa223b5d2ba577900a56a51fa857e878f3575cefeeaf6b244f57` |
   | `GSE86469_expression_RSEM_expected_counts.csv` | `61aed6a8f8905f047232ef447f40e42623e6b5b4a2bc6d46e5914ac91bb73f43` |

5. Once the checksums match, follow the commands in Section 4. If either hash differs, **do not proceed**; re-download and investigate the mismatch.

**Verification boundary:** These SHA-256 values were verified against the two **local converted CSVs** on 21 November 2026. The Google Drive listing shows both files, but the hashes of files downloaded back from Drive have **not yet been independently verified**. These hashes are not for the GEO `.gz` originals. Access for the supervisor remains to be granted if not already shared. The research/analysis is still subject to supervisor approval for DE.


## 4. Reproducibility and current outputs

From the extracted project root (`T2D_Task2_Current`):

```bash
python -m pip install -r requirements.txt
python scripts/run_exploratory.py
python scripts/validate_outputs.py
```

The Windows user run on 20 November 2026 completed with Python **3.14.7** and reported `VALIDATED` after rerunning `scripts/run_exploratory.py`. The packaged `documentation/run_environment.json` records a **different, earlier execution environment**; update the environment record for the final submitted rerun rather than claiming it describes the Windows run. Main dependencies in `requirements.txt` are NumPy, pandas, Matplotlib, nbformat, nbclient and ipykernel. Jupyter users should execute the notebook from the repository root and save all outputs.

### Main files

- `documentation/dataset_inventory_CURRENT.csv`: loadable dataset inventory.
- `documentation/cell_manifest_with_provenance_CURRENT.csv`: cell ID, donor ID, β-cell flag, original GEO sample reference and source metadata.
- `documentation/donor_summary_CURRENT.csv`: per-donor records (18 Xin; 8 Lawlor).
- `results/qc/matching_audit_CURRENT.csv`, `expression_qc_CURRENT.csv`, `donor_group_demographics_CURRENT.csv`: current QC and descriptive summaries.
- `results/qc/GSE81608_donor_metadata_and_flags.csv` and `GSE86469_donor_metadata_and_flags.csv`: age, sex, available BMI, β-cell counts and descriptive review flags.
- `results/donor_matrices/GSE81608_donor_mean_log2_RPKM_plus1.csv`: average of `log2(1 + RPKM)` **within each donor's annotated β-cells**, not raw-count pseudobulk.
- `results/donor_matrices/GSE86469_donor_sum_RSEM_expected_counts_fractional.csv`: sum of **fractional** expected counts across each donor's annotated β-cells; **no arbitrary integer rounding**.
- `results/donor_matrices/GSE86469_donor_log2_CPM_plus1_exploratory.csv`: transformed donor-level visualization only; not an approved DE input.
- `results/figures/`: donor PCA, expression distributions, marker checks and β-cell-count plot.
- `documentation/GSE81608_gene_identifier_mapping_COMPLETED.csv`: later NCBI-based GeneID-to-Ensembl crosswalk, distinct from the original preliminary mapping file.
- `documentation/GSE86469_gene_identifier_mapping.csv`: 26,616 supplied Ensembl stable-format gene IDs; original annotation documented as Ensembl v70, GRCh37; individual reference membership still needs version-specific review.
- `reference/NCBI_gene2ensembl_metadata.json`: download URL and SHA-256 for the NCBI mapping reference generated during the user's mapping run. The `.gz` reference itself is ignored by Git and must be retrievable.
- `documentation/Xin_108_cell_search_log.md`: **updated** primary-source explanation; the earlier `Xin_108_cell_search_log_PREVIOUS.md` is stored locally in `archive_previous/` (not tracked in GitHub).
- `documentation/Donor_Overlap_Provenance_Check.md`: updated source comparison and unresolved independence status.
- `protocol/Two_Page_Statistical_Protocol_UPDATED_FOR_REVIEW.pdf`: **current protocol for supervisor review**. The earlier `Two_Page_Statistical_Protocol_PREVIOUS.pdf` is stored locally in `archive_previous/` (not tracked in GitHub).
- `documentation/Literature_Comparison.md`, `documentation/Contribution_and_Open_Issues.md`: requested papers, contribution and remaining limitations.

The version-controlled paths above describe the **current GitHub `main` branch** after manual updates, not the untouched Task 1 ZIP. Locally archived previous outputs are intentionally absent from that GitHub branch.

### Numerical verification completed during the Windows run

| Check | Recalculated result |
|---|---|
| GSE81608 donor matrix from 503 annotated β-cells, 18 donors, 39,851 genes | `Aggregation matches: True`; maximum absolute difference ≈ `1.776e-15` |
| GSE86469 donor matrix from 264 annotated β-cells, 8 donors, 26,616 genes | `Aggregation matches: True`; maximum absolute difference ≈ `4.6566e-10` |
| GSE86469 cell-level matrix | No missing or negative values; **3,188,219 positive fractional entries** |

Floating-point differences are within verification tolerances. These checks show computational agreement with the **supplied local matrices**; they do not independently establish source-file identity, historical annotations, or donor independence.

## 5. Gene-ID annotation and provenance

**Xin (GSE81608):** 39,851 numeric NCBI/Entrez-style gene identifiers. `python scripts/complete_gene_crosswalk.py` was **run successfully on the user's Windows computer** using the official NCBI `gene2ensembl.gz` human reference. Its resulting current-reference mapping was:

| Mapping status | Number of identifiers |
|---|---:|
| Unique one-to-one mapping | 30,160 |
| Unmapped in current NCBI reference | 9,668 |
| Multiple Ensembl targets (ambiguous) | 23 |
| **Total** | **39,851** |

The mapping script retains all ambiguous alternatives. Four marker crosswalks matched: **INS** (NCBI 3630 → ENSG00000254647), **GCG** (2641 → ENSG00000115263), **SST** (6750 → ENSG00000157005), **PPY** (5539 → ENSG00000108849). This is a **current-reference crosswalk**, not proof of identical annotation to the original Xin **GRCh37** pipeline. Review unmapped/ambiguous features, stable-ID uniqueness, and original-version compatibility before cross-study gene matching or DE.

**Lawlor (GSE86469):** all 26,616 supplied gene IDs have valid ENSG stable-ID syntax, with **0 missing IDs, 0 duplicate IDs, and 0 version suffixes**. Original GEO **Data processing** specifies **GRCh37 / Ensembl v70**, Bowtie2 mapping and RSEM quantification. Actual membership of each ID in the original Ensembl v70 catalog and any version-associated remapping issues should be checked rather than treating format validation as full annotation validation.

## 6. Xin 1,600-versus-1,492 cell discrepancy

**Published rationale resolved; exact excluded identities unresolved.** Xin et al.'s article and supplemental Figure S1 describe 3,709 initially sequenced cells, then exclusions of 828 (viability), 343 (technical QC), 938 (multi-hormone expression), and finally **108 single-hormone cells with distinct non-islet contamination signatures**, yielding **1,492** analyzed cells. Supplemental Figure S2 highlights the likely contaminating cells (including fibroblast/endothelial-associated expression) but no recovered list identifies their exact GSM/sample IDs.

The publication's final summary reports **472 β-cells**; the present 1,600-cell deposited-data manifest marks **503 β-cells**. The **31-cell β difference cannot be assigned to specific cells** without a reproducible original exclusion manifest. No 108 cells were removed solely to match the paper. The intended sensitivity check will use documented, pre-specified contamination-marker criteria and report changes in β-cell and donor representations; unavailable original QC measurements cannot be reconstructed from RPKM alone.

Evidence and references: `documentation/Xin_108_cell_search_log.md`; Xin et al. (2016), DOI https://doi.org/10.1016/j.cmet.2016.08.018, article Results and Methods, Supplemental Figures S1–S2 and Table S1.

## 7. Donor provenance, exploratory observations and analysis gates

- **Procurement sources:** Xin Methods describe islets from **Prodo Laboratories, Inc.**; Lawlor Methods describe islets from **ProdoLabs or the Integrated Islet Distribution Program (IIDP)**. A shared possible supplier is **not** evidence of a shared donor, but independence cannot be assumed.
- **Demographic screening:** four pairs match disease group, recorded age and sex in `documentation/cross_study_donor_overlap_screen.csv`. These are **candidates for documentation review, not identity matches**. No global cross-study donor identifier has been verified. Treat study-to-study findings as **exploratory replication**, not confirmed independent validation.
- **Influential donors:** `ACEK420A` (Lawlor) is a clear PCA review candidate with 10 annotated β-cells; `ACHY057` and `ACCR015A` also merit descriptive review. Xin `Non T2D 3` (10 cells), `Non T2D 6` (7), `Non T2D 9` (7) merit low-cell-count review. **None are excluded** on PCA appearance or statistical significance.
- **Confounding:** T2D donors are older on average in both studies; sample sizes are small. Age-adjusted and disease-only sensitivity models, leave-one-donor-out analysis, low-cell-count sensitivity and FDR correction must follow the supervisor-approved protocol.
- **Statistics:** Xin RPKM summaries are **not** raw-count pseudobulk; do not apply unmodified raw-count negative-binomial methods to them. Lawlor's GEO file is explicitly named raw RSEM expected counts, and the local converted matrix contains many fractional values. Verify conversion integrity and suitability of the planned count-statistical model before inferential use. **No differential-expression or pathway analysis has been run.**

Current proposed analysis is specified in `protocol/Two_Page_Statistical_Protocol_UPDATED_FOR_REVIEW.pdf`. **Submit the protocol for supervisor review before any DE tests**; pathway analysis follows only after the method and DE stage are established.

## 8. Outstanding requirements before final submission

1. Confirm original Xin annotations/assembly compatibility; assess unmapped and ambiguous gene mapping, and verify Lawlor gene-ID membership against versioned Ensembl v70.
2. Attempt to recover the original Xin excluded 108 cell IDs (or document the limitation and pre-specified sensitivity analysis).
3. Resolve biological donor overlap where possible from procurement or intake records; otherwise retain explicit uncertainty.
4. Rerun and save **the executed notebook** with the final current documents, figures, manifest and environment record; ensure the README, protocol and submission status identify one consistent version.
5. **Repository pushed to private GitHub, and the restricted Google Drive folder link is recorded in Section 3.** Still required: grant supervisor access to both GitHub and Drive; independently re-download the shared CSVs and verify their recorded SHA-256 checksums; confirm reconstruction instructions work on a fresh machine.
6. Assign actual four-member names to the deliverables and ensure each member can explain the full workflow.
7. Obtain supervisor review of the statistical protocol **before** running DE; defer pathway analysis.

### Deliverable owners (enter actual member names before submission)

| Deliverable | Responsibility | Owner |
|---|---|---|
| Core paper comparison and two-page protocol | Literature + planned statistics | Member 1 — **name pending** |
| Inventory, provenance, gene mapping, Xin cell discrepancy, donor overlap | Data provenance | Member 2 — **name pending** |
| Donor matrices, demographics, PCA, QC assessment and sensitivity plan | Exploratory analysis | Member 3 — **name pending** |
| Executed notebook, QC files, README, GitHub release and data retrieval | Integration + reproducibility | Member 4 — **name pending** |
| Contribution statement and unresolved-issues list | Joint review | Members 1 and 4 — **names pending** |

All four members must understand the entire workflow.

## Core references

- Xin et al. (2016), *Cell Metabolism*. https://doi.org/10.1016/j.cmet.2016.08.018
- Lawlor et al. (2017), *Genome Research*. https://doi.org/10.1101/gr.212720.116
- Squair et al. (2021), *Nature Communications*. https://doi.org/10.1038/s41467-021-25960-2
- Marques et al. (2022), additional cross-study literature. https://doi.org/10.1111/1753-0407.13236
