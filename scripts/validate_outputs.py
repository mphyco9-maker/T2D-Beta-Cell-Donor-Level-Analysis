"""Validate saved current outputs without re-running numeric processing."""
from pathlib import Path
import pandas as pd, hashlib, re
r=Path(__file__).resolve().parents[1]
inv=pd.read_csv(r/'documentation/dataset_inventory_CURRENT.csv')
assert len(inv)==2 and set(inv.dataset)=={'GSE81608','GSE86469'}
for _,row in inv.iterrows():
 assert hashlib.sha256((r/row.expression_file).read_bytes()).hexdigest()==row.expression_sha256
 assert hashlib.sha256((r/row.metadata_file).read_bytes()).hexdigest()==row.metadata_sha256
qc=pd.read_csv(r/'results/qc/expression_qc_CURRENT.csv')
assert qc.set_index('dataset').loc['GSE81608','markers_verified_in_matrix']=='GCG,INS,PPY,SST'
assert qc.set_index('dataset').loc['GSE86469','markers_verified_in_matrix']=='GCG,INS,PPY,SST'
assert qc.beta_cells.sum()==767
assert qc.donors.sum()==26
m=pd.read_csv(r/'documentation/cell_manifest_with_provenance_CURRENT.csv')
assert len(m)==2238 and m.is_beta.sum()==767
for ds, filename, shape in [
 ('GSE81608','GSE81608_donor_mean_log2_RPKM_plus1.csv',(39851,19)),
 ('GSE86469','GSE86469_donor_sum_RSEM_expected_counts_fractional.csv',(26616,9))]:
 p=r/'results/donor_matrices'/filename
 df=pd.read_csv(p)
 assert df.shape==shape,(ds,df.shape)
 assert df.gene_id.notna().all()
assert len(pd.read_csv(r/'results/qc/donor_group_demographics_CURRENT.csv'))==4
print('VALIDATED: input hashes, CSV inventory, 2238 matched cells, 767 beta cells, 26 donors, 4 marker IDs per dataset, donor matrix dimensions.')
