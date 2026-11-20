"""Donor-aware, DESCRIPTIVE exploratory workflow. No DE tests performed.
Run at repository root: python scripts/run_exploratory.py
All expression values are processed in gene-wise chunks (bounded memory).
"""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, json, re, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; OUT=ROOT/'results'; DOC=ROOT/'documentation'
for x in [OUT/'figures',OUT/'donor_matrices',OUT/'qc',DOC]:x.mkdir(parents=True,exist_ok=True)
SETS = {
 'GSE81608': {'expression':'GSE81608_expression_RPKM.csv','metadata':'GSE81608_GEO_sample_metadata.csv','unit':'RPKM','idtype':'NCBI GeneID','analysis':'mean_log2_1p_RPKM','gene_column':'gene.id'},
 'GSE86469': {'expression':'GSE86469_expression_RSEM_expected_counts.csv','metadata':'GSE86469_GEO_sample_metadata.csv','unit':'RSEM expected counts','idtype':'Ensembl stable gene ID','analysis':'sum_fractional_expected_counts','gene_column':'Unnamed: 0'},
}
MARKERS={'INS':('3630','ENSG00000254647'),'GCG':('2641','ENSG00000115263'),'SST':('6750','ENSG00000157005'),'PPY':('5539','ENSG00000108849')}

def sha256(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def expr_cell_id(ds,title):
 s=str(title).strip()
 if ds=='GSE81608':
  m=re.fullmatch(r'Pancreatic islet cell sample\s+(\d+)',s,flags=re.I)
  if not m:raise ValueError(f'Unrecognized Xin GEO sample title: {s}')
  return 'Sample_'+m.group(1)
 return s

def saveplot(name):
 plt.tight_layout();plt.savefig(OUT/'figures'/name,dpi=160,bbox_inches='tight');plt.close()

all_donors=[]; all_manifests=[]; audits=[]; qc_rows=[]; inventory=[]; marker_long=[]; other_summary=[]
for ds,cfg in SETS.items():
 print('Processing',ds,flush=True)
 fexpr=DATA/'expression'/cfg['expression']; fmeta=DATA/'metadata'/cfg['metadata']
 m=pd.read_csv(fmeta,low_memory=False)
 m['cell_id']=m.original_sample_title.map(lambda s:expr_cell_id(ds,s))
 with fexpr.open(encoding='utf-8-sig',newline='') as fin:
  header=next(csv.reader(fin))
 cols=header[1:]
 if len(set(cols))!=len(cols) or m.cell_id.duplicated().any() or set(cols)!=set(m.cell_id):
  raise ValueError(f'{ds}: unmatched or duplicated expression and metadata cell IDs')
 m=m.set_index('cell_id').loc[cols].reset_index()
 m['is_beta']=m.original_cell_type.astype(str).str.fullmatch('beta',case=False)
 manifest=m.copy()
 manifest.insert(0,'expression_source',cfg['expression']);manifest['gene_id_system']=cfg['idtype']
 all_manifests.append(manifest)
 donor=m.groupby('donor_id',sort=True).agg(
  disease_status=('disease_group','first'),total_cells=('cell_id','size'),beta_cells=('is_beta','sum'),
  age=('age','first'),sex=('sex','first'),bmi=('bmi','first')
 ).reset_index().rename(columns={'disease_status':'disease_group'})
 donor.insert(0,'dataset',ds)
 for d,g in m.groupby('donor_id'):
  for field in ['disease_group','age','sex','bmi']:
   if g[field].nunique(dropna=True)>1:raise ValueError(f'{ds}/{d}: conflicting {field}')
 all_donors.append(donor)
 groups=[]
 for dn in donor.donor_id:
  groups.append(np.flatnonzero(m.is_beta.to_numpy() & (m.donor_id.to_numpy()==dn)))
 if not all(len(g)>0 for g in groups):raise ValueError('Donor with zero beta cells')
 # Read gene matrices in batches. RPKM per cell is first log2(RPKM+1), then donor-average.
 # Lawlor expected counts are aggregated by DONOR without arbitrary rounding.
 chunks=[]; gene_ids=[]; samplevals=[]; marker_count=0; seen=set(); duplicate=0
 missing=negative=zero=total=0;fractional=0; positive=0
 for piece in pd.read_csv(fexpr,chunksize=200,low_memory=False):
  ids=piece.iloc[:,0].astype(str).str.strip().str.replace(r'\.\d+$','',regex=True)
  for x in ids:
   if x in seen:duplicate+=1
   seen.add(x)
  ar=piece.iloc[:,1:].to_numpy(dtype=np.float64)
  if ar.shape[1]!=len(cols):raise ValueError('Column count mismatch')
  finite=np.isfinite(ar); valid=ar[finite]
  missing+=int((~finite).sum());negative+=int((valid<0).sum());zero+=int((valid==0).sum()); total+=int(ar.size)
  pos=valid[valid>0]; positive+=pos.size; fractional+=int(np.count_nonzero(np.abs(pos-np.rint(pos))>1e-6))
  if not finite.all() or np.any(valid<0):raise ValueError(f'{ds}: negative/missing/nonfinite expression values; abort donor matrix generation')
  samplecols=np.linspace(0,len(cols)-1,min(24,len(cols)),dtype=int)
  sampled=np.log2(1+ar[:,samplecols]).ravel()
  samplevals.extend(sampled.tolist())
  if ds=='GSE81608':
   transformed=np.log2(1+ar)
   aggr=np.column_stack([transformed[:,ix].mean(axis=1) for ix in groups])
  else:
   aggr=np.column_stack([ar[:,ix].sum(axis=1) for ix in groups])
  chunks.append(aggr.astype(np.float64))
  gene_ids.extend(ids.tolist())
  for gene,(ent,ens) in MARKERS.items():
   target=ent if ds=='GSE81608' else ens
   positions=np.flatnonzero(ids.to_numpy()==target)
   for loc in positions:
    marker_count+=1
    for cid,ct,status,donorid,v in zip(m.cell_id,m.original_cell_type,m.disease_group,m.donor_id,ar[loc]):
     marker_long.append({'dataset':ds,'gene_symbol':gene,'gene_id':target,'cell_id':cid,'donor_id':donorid,'cell_type':ct,'disease_group':status,'expression':float(v)})
  del ar, aggr
 if duplicate:raise ValueError(f'{ds}: duplicated gene IDs, inspect before aggregation')
 arr=np.vstack(chunks)
 assert arr.shape==(len(gene_ids),len(donor))
 md= pd.DataFrame(arr,columns=donor.donor_id.tolist());md.insert(0,'gene_id',gene_ids)
 if ds=='GSE81608':
  md.to_csv(OUT/'donor_matrices'/'GSE81608_donor_mean_log2_RPKM_plus1.csv',index=False)
  transformed_donor=arr.astype(np.float64)
  # Explicit annotation mapping STATUS. Only NCBI-verified marker pairs available offline.
  markerid={v[0]:(sym,v[1]) for sym,v in MARKERS.items()}
  maps=pd.DataFrame({'dataset':ds,'source_gene_id':gene_ids,'source_id_system':'NCBI GeneID'})
  maps['ensembl_gene_id']=maps.source_gene_id.map(lambda s:markerid.get(s,('',''))[1])
  maps['symbol']=maps.source_gene_id.map(lambda s:markerid.get(s,('',''))[0])
  maps['mapping_status']=np.where(maps.ensembl_gene_id.ne(''),'verified_marker_only','pending_external_NCBI_gene2ensembl')
  maps['mapping_reference']='NCBI Gene / ftp.ncbi.nlm.nih.gov/gene/DATA/gene2ensembl.gz'
 else:
  md.to_csv(OUT/'donor_matrices'/'GSE86469_donor_sum_RSEM_expected_counts_fractional.csv',index=False)
  total_by_donor=arr.sum(axis=0).astype(float)
  if np.any(total_by_donor<=0):raise ValueError('Lawlor zero donor sum')
  cpm=arr.astype(np.float64)/total_by_donor[None,:]*1e6
  transformed_donor=np.log2(1+cpm)
  pd.DataFrame(np.column_stack((np.asarray(gene_ids,dtype=object), transformed_donor)),columns=['gene_id']+donor.donor_id.tolist()).to_csv(OUT/'donor_matrices'/'GSE86469_donor_log2_CPM_plus1_exploratory.csv',index=False)
  maps=pd.DataFrame({'dataset':ds,'source_gene_id':gene_ids,'source_id_system':'Ensembl gene ID'})
  maps['ensembl_gene_id']=maps.source_gene_id
  maps['symbol']=maps.source_gene_id.map({v[1]:k for k,v in MARKERS.items()}).fillna('')
  maps['mapping_status']='original_stable_Ensembl_ID_unvalidated_version'
  maps['mapping_reference']='GSE86469 GEO processed expected-counts matrix; genome-build/version to verify'
 maps.to_csv(DOC/(ds+'_gene_identifier_mapping.csv'),index=False)
 # PCA across donors using beta-cell profiles, without disease labels in PCA construction.
 # Per-gene centering; remove invariant genes and high-abundance extreme median bias in reports.
 keep=np.isfinite(transformed_donor).all(axis=1) & (transformed_donor.var(axis=1)>1e-12)
 Y=transformed_donor[keep].T
 Y=Y-Y.mean(axis=0,keepdims=True)
 gram=Y@Y.T
 eigv,eigvec=np.linalg.eigh(gram); order=np.argsort(eigv)[::-1]
 eigv=np.maximum(0,eigv[order]); eigvec=eigvec[:,order]
 scores=eigvec*np.sqrt(eigv)[None,:]
 # PC sign is immaterial; align sign by largest magnitude score for deterministic orientation.
 for j in range(2):
  if scores[np.argmax(np.abs(scores[:,j])),j]<0:scores[:,j]*=-1
 pc=pd.DataFrame({'dataset':ds,'donor_id':donor.donor_id,'disease_group':donor.disease_group,'beta_cells':donor.beta_cells,
                   'PC1':scores[:,0],'PC2':scores[:,1], 'PC1_var_pct':100*eigv[0]/eigv.sum(),'PC2_var_pct':100*eigv[1]/eigv.sum()})
 pc.to_csv(OUT/'qc'/(ds+'_donor_PCA_coordinates.csv'),index=False)
 plt.figure(figsize=(8,5.4))
 for status,c in [('ND','#2676a3'),('T2D','#d98521')]:
  sel=pc.disease_group.eq(status)
  plt.scatter(pc.loc[sel,'PC1'],pc.loc[sel,'PC2'],label=status,c=c,s=55,alpha=.85)
 for _,r in pc.iterrows():plt.annotate(str(r.donor_id),(r.PC1,r.PC2),xytext=(3,4),textcoords='offset points',fontsize=6)
 plt.xlabel(f'PC1 ({pc.PC1_var_pct.iloc[0]:.1f}% variance)');plt.ylabel(f'PC2 ({pc.PC2_var_pct.iloc[0]:.1f}% variance)')
 plt.title(f'{ds}: donor-level PCA (descriptive; no donor exclusions)');plt.legend()
 saveplot(ds+'_donor_PCA.png')
 # donor-wise distribution: all genes summarized at the donor level, not plotting cells as replicates
 plt.figure(figsize=(max(9,len(donor)*.5),5))
 distributions=[transformed_donor[:,i] for i in range(len(donor))]
 plt.boxplot(distributions,showfliers=False,tick_labels=donor.donor_id.tolist())
 plt.xticks(rotation=75,fontsize=7);plt.ylabel('Mean log2(1+RPKM)' if ds=='GSE81608' else 'log2(1+donor CPM)')
 plt.title(ds+': donor-level expression distributions');saveplot(ds+'_donor_expression_distributions.png')
 plt.figure(figsize=(7,4))
 plt.hist(np.asarray(samplevals),bins=65)
 plt.title(f'{ds}: input expression distribution (24 sampled cells per gene)')
 plt.xlabel('log2(1+input expression)');plt.ylabel('Sampled entries');saveplot(ds+'_cell_expression_distribution.png')
 # Marker plots: median within ORIGINAL cell annotation (all cells, not just beta).
 mk=pd.DataFrame([r for r in marker_long if r['dataset']==ds])
 fig,axs=plt.subplots(1,4,figsize=(15,4.1))
 for ax,gene in zip(axs,MARKERS):
  t=mk[mk.gene_symbol==gene]
  if t.empty:
   ax.text(.5,.5,'NOT FOUND',ha='center',va='center',transform=ax.transAxes)
   continue
  median=t.groupby('cell_type').expression.median().sort_values(ascending=False)
  ax.bar(range(len(median)),np.log2(1+median.values),color='#367a99')
  ax.set_xticks(range(len(median)),median.index,rotation=70,fontsize=7)
  ax.set_title(gene);ax.set_ylabel('log2(1+median input value)')
 fig.suptitle(ds+' marker consistency check: original annotations')
 fig.tight_layout();fig.savefig(OUT/'figures'/(ds+'_marker_annotation_check.png'),dpi=160,bbox_inches='tight');plt.close(fig)
 # Prespecified descriptive outlier-screening only (no DE-driven exclusion)
 donor_medians=np.median(transformed_donor,axis=0)
 def robust_abs_z(v):
  med=np.median(v); mad=np.median(np.abs(v-med))
  return np.abs((v-med)/(1.4826*mad)) if mad>1e-10 else np.full_like(v,np.nan,dtype=float)
 donor['median_donor_expression']=donor_medians
 donor['PC1_robust_abs_z']=robust_abs_z(scores[:,0]);donor['median_expr_robust_abs_z']=robust_abs_z(donor_medians)
 donor['low_beta_cells_le_10']=donor.beta_cells.le(10)
 donor['descriptive_outlier_flag']=donor[['PC1_robust_abs_z','median_expr_robust_abs_z']].gt(3.5).any(axis=1)
 donor['review_not_exclude']=donor.low_beta_cells_le_10 | donor.descriptive_outlier_flag
 donor.to_csv(OUT/'qc'/(ds+'_donor_metadata_and_flags.csv'),index=False)
 audit={'dataset':ds,'expression_columns':len(cols),'metadata_rows':len(m),'matched_cells':len(cols),'unmatched_expression':0,'unmatched_metadata':0,
        'duplicate_expression_ids':len(cols)-len(set(cols)),'duplicate_metadata_ids':int(m.cell_id.duplicated().sum()),'donor_conflicts':0,'header_match_verified':True}
 audits.append(audit)
 qc_rows.append({'dataset':ds,'genes':len(gene_ids),'cells':len(cols),'duplicate_gene_ids':duplicate,'missing_or_nonfinite_values':missing,
  'negative_values':negative,'zero_values':zero,'zero_fraction':zero/total,'fractional_positive_entries':fractional,'positive_entries':positive,
  'fractional_positive_fraction':fractional/max(1,positive),'markers_verified_in_matrix':','.join(sorted(mk.gene_symbol.unique())),'marker_rows_found':marker_count,
  'beta_cells':int(m.is_beta.sum()),'donors':len(donor),'units':cfg['unit']})
 inventory.append({'dataset':ds,'study':'Xin et al. 2016' if ds=='GSE81608' else 'Lawlor et al. 2017',
  'geo_url':f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={ds}',
  'expression_file':'data/expression/'+cfg['expression'],'expression_sha256':sha256(fexpr),
  'metadata_file':'data/metadata/'+cfg['metadata'],'metadata_sha256':sha256(fmeta),
  'gene_identifier_column':header[0],'gene_identifier_system':cfg['idtype'],'expression_units':cfg['unit'],
  'genes':len(gene_ids),'expression_cells':len(cols),'matched_metadata_cells':len(m),'donors':len(donor),
  'beta_cells':int(m.is_beta.sum()),'disease_ND_donors':int((donor.disease_group=='ND').sum()),'disease_T2D_donors':int((donor.disease_group=='T2D').sum()),
  'aggregation':cfg['analysis'],'unresolved':'Xin published 1492 vs GEO 1600' if ds=='GSE81608' else 'RSEM pipeline/count-scale verification ongoing'})
 print(f'{ds}: {len(gene_ids):,} genes, {len(cols)} cells, {len(donor)} donors, {int(m.is_beta.sum())} beta cells; {marker_count} markers; fractional positive={fractional}/{positive}',flush=True)

pd.concat(all_manifests,ignore_index=True).to_csv(DOC/'cell_manifest_with_provenance_CURRENT.csv',index=False)
all_donors=pd.concat(all_donors,ignore_index=True)
all_donors.to_csv(DOC/'donor_summary_CURRENT.csv',index=False)
pd.DataFrame(audits).to_csv(OUT/'qc'/'matching_audit_CURRENT.csv',index=False)
pd.DataFrame(qc_rows).to_csv(OUT/'qc'/'expression_qc_CURRENT.csv',index=False)
pd.DataFrame(marker_long).to_csv(OUT/'qc'/'marker_expression_long_CURRENT.csv',index=False)
pd.DataFrame(inventory).to_csv(DOC/'dataset_inventory_CURRENT.csv',index=False)
for ds,d in all_donors.groupby('dataset'):
 for group,g in d.groupby('disease_group'):
  other_summary.append({'dataset':ds,'disease_group':group,'donors':len(g),'total_cells':int(g.total_cells.sum()),'beta_cells':int(g.beta_cells.sum()),
   'age_mean':round(g.age.mean(),2),'age_sd':round(g.age.std(ddof=1),2),'age_min':g.age.min(),'age_max':g.age.max(),
   'sex_F':int(g.sex.astype(str).str.upper().isin(['F','FEMALE']).sum()),'sex_M':int(g.sex.astype(str).str.upper().isin(['M','MALE']).sum()),
   'BMI_n':int(g.bmi.notna().sum()),'BMI_mean':round(g.bmi.mean(),2) if g.bmi.notna().any() else np.nan,
   'BMI_sd':round(g.bmi.std(),2) if g.bmi.notna().sum()>1 else np.nan})
pd.DataFrame(other_summary).to_csv(OUT/'qc'/'donor_group_demographics_CURRENT.csv',index=False)
plt.figure(figsize=(13,5))
order=all_donors.sort_values(['dataset','disease_group','donor_id'])
color=np.where(order.disease_group.eq('T2D'),'#d98521','#2676a3')
plt.bar(np.arange(len(order)),order.beta_cells,color=color)
plt.xticks(np.arange(len(order)),[x[-3:]+': '+y for x,y in zip(order.dataset,order.donor_id)],rotation=80,fontsize=7)
plt.ylabel('Original-annotation beta cells');plt.title('Beta-cell representation by donor (no exclusions)')
saveplot('all_donors_beta_cell_counts.png')
manifest= pd.concat(all_manifests,ignore_index=True)
print('\nCURRENT SUMMARY (donor-level, not cell-weighted):')
print(pd.DataFrame(other_summary).to_string(index=False))
print('All outputs saved to',ROOT)
