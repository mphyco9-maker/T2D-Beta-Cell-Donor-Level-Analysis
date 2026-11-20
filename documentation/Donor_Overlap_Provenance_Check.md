# Cross-study donor independence: preliminary provenance audit

**GSE81608:** Xin et al. (2016), GEO GSE81608, 18 named donor groups in supplied metadata (12 ND, 6 T2D). Original GEO cell/sample records include age, sex, original disease label and original donor label, but this deposit does not supply a standardized cross-study global donor identifier.

**GSE86469:** Lawlor et al. (2017), GEO GSE86469, 8 donor groups (5 ND, 3 T2D). Metadata includes age, sex, BMI, disease and study-specific alphanumeric donor IDs. It does not supply the same global identifier as Xin.

**Screen performed:** Cross-compare supplied donor rows on disease, identical age and normalized sex to find *demographic-only candidate pairs*, saved in `cross_study_donor_overlap_screen.csv`. A demographic match is neither evidence of a common donor nor proof that two studies share tissue; a nonmatch does not prove independence (age entry conventions/time points may differ).

**Additional checks needed:** Inspect donor source, organ-procurement/biobank details, provider/sample intake references and donor supplementary tables in the original publications; check original research group records and potential collaboration/tissue sharing. If identity cannot be established, label cross-study replication *exploratory with unresolved independence* rather than independent validation. Do not infer independence from different study-specific donor labels.

**Status:** original biological overlap has not been definitively verified.
Additional primary-source verification (20 November 2026)

Xin et al. (2016) report obtaining pancreatic islets from Prodo Laboratories, Inc. (Experimental Procedures, Human Islets). Lawlor et al. (2017) report procurement from ProdoLabs or the Integrated Islet Distribution Program (IIDP) (Methods, Islet acquisition). Thus, the studies share a possible tissue supplier, but there is no confirmed evidence that they used the same biological donors. Four pairs matched on age, sex and disease group in the preliminary demographic screen; these are not donor identity matches. Cross-study donor independence remains unresolved. The proposed cross-study comparison will therefore be described as exploratory replication, not confirmed independent validation.

Sources:
Xin et al. (2016), DOI: 10.1016/j.cmet.2016.08.018, Experimental Procedures, Human Islets.
Lawlor et al. (2017), https://genome.cshlp.org/content/27/2/208, Methods, Islet acquisition.
