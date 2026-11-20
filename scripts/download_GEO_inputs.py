"""Fetch original GEO supplementary files (network required) to data/geo_downloads.
The supplied verified converted CSVs are the inputs for the current executed workflow.
Do NOT claim downloaded .gz files are byte-identical to converted CSVs.
"""
from pathlib import Path
from urllib.request import urlretrieve
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'data'/'geo_downloads';folder.mkdir(parents=True,exist_ok=True)
urls={
 'GSE81608_human_islets_rpkm.txt.gz':'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE81nnn/GSE81608/suppl/GSE81608_human_islets_rpkm.txt.gz',
 'GSE86469_GEO.islet.single.cell.processed.data.RSEM.raw.expected.counts.csv.gz':'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE86nnn/GSE86469/suppl/GSE86469_GEO.islet.single.cell.processed.data.RSEM.raw.expected.counts.csv.gz',
}
for name,url in urls.items():
 dest=folder/name
 if not dest.exists(): print('Download:',url);urlretrieve(url,dest)
 print('Downloaded:',dest,'bytes',dest.stat().st_size)
print('Convert to data/expression/ CSV matching the study columns and verify against documentation/dataset_inventory_CURRENT.csv before executing.')
