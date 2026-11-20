"""Complete Xin NCBI GeneID -> Ensembl stable-ID crosswalk via official NCBI gene2ensembl.
This is intentionally NOT part of the offline exploratory workflow; requires network.
Run from repository root: python scripts/complete_gene_crosswalk.py
Does NOT silently choose mappings or collapse genes.
"""
from pathlib import Path
import hashlib, json, urllib.request, gzip
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
REF=ROOT/'reference';REF.mkdir(exist_ok=True)
URL='https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2ensembl.gz'
path=REF/'gene2ensembl.gz'
if not path.exists():
 print('Downloading',URL)
 urllib.request.urlretrieve(URL,path)
h=hashlib.sha256(path.read_bytes()).hexdigest()
# gene2ensembl includes tax_id, GeneID, Ensembl_gene_identifier among its columns
ref=pd.read_csv(path,sep='\t',compression='gzip',dtype=str,low_memory=False)
if '#tax_id' not in ref.columns or 'GeneID' not in ref.columns or 'Ensembl_gene_identifier' not in ref.columns:
 raise ValueError('Unexpected official reference structure; inspect columns before proceeding')
ref=ref[(ref['#tax_id']=='9606') & ref.Ensembl_gene_identifier.str.match(r'^ENSG\d+',na=False)]
lookup=ref.groupby('GeneID')['Ensembl_gene_identifier'].agg(lambda x:sorted(set(x)))
source=pd.read_csv(ROOT/'documentation/GSE81608_gene_identifier_mapping.csv',dtype=str)
def row_map(gid):
 ids=lookup.get(gid,[])
 if not ids:return ('','unmapped_in_NCBI_reference',0)
 if len(ids)>1:return (';'.join(ids),'ambiguous_multiple_Ensembl_gene_IDs',len(ids))
 return (ids[0],'unique_mapping',1)
mapped=source.source_gene_id.map(row_map)
source['ensembl_gene_id']=mapped.map(lambda x:x[0]);source['mapping_status']=mapped.map(lambda x:x[1]);source['number_of_targets']=mapped.map(lambda x:x[2]);source['mapping_reference']=URL
source['verified_against_marker_reference']=''
known={'3630':'ENSG00000254647','2641':'ENSG00000115263','6750':'ENSG00000157005','5539':'ENSG00000108849'}
for gid,target in known.items():
 idx=source.source_gene_id==gid
 source.loc[idx,'verified_against_marker_reference']=source.loc[idx,'ensembl_gene_id'].map(lambda x: 'match' if target in x.split(';') else 'MISMATCH_REVIEW')
source.to_csv(ROOT/'documentation/GSE81608_gene_identifier_mapping_COMPLETED.csv',index=False)
(REF/'NCBI_gene2ensembl_metadata.json').write_text(json.dumps({'url':URL,'sha256':h,'file_bytes':path.stat().st_size,'taxon':'Homo sapiens 9606','reference':'Current NCBI mapping; compare original GRCh37 annotation before using'} ,indent=2))
print(source.mapping_status.value_counts(dropna=False).to_string())
print('Markers:',source.loc[source.source_gene_id.isin(known),['source_gene_id','ensembl_gene_id','verified_against_marker_reference']].to_string(index=False))
