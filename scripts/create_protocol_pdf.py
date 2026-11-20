from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

root=Path(__file__).resolve().parents[1]
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font_bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVu',font));pdfmetrics.registerFont(TTFont('DejaVu-Bold',font_bold))
styles={
 'title':ParagraphStyle('title',fontName='DejaVu-Bold',fontSize=14.4,leading=19,spaceAfter=6,textColor=colors.HexColor('#16415c')),
 'sub':ParagraphStyle('sub',fontName='DejaVu-Bold',fontSize=9.1,leading=13,spaceBefore=10,spaceAfter=2,textColor=colors.HexColor('#16415c')),
 'body':ParagraphStyle('body',fontName='DejaVu',fontSize=8.3,leading=12.4,spaceAfter=5),
 'tiny':ParagraphStyle('tiny',fontName='DejaVu',fontSize=7.1,leading=10.5,spaceAfter=3),
}
filename=root/'protocol'/'Two_Page_Statistical_Protocol_FOR_REVIEW.pdf'
filename.parent.mkdir(parents=True,exist_ok=True)
doc=SimpleDocTemplate(str(filename),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=17*mm,bottomMargin=17*mm)
flow=[]
def title(s):flow.append(Paragraph(s,styles['title']))
def sub(s):flow.append(Paragraph(s,styles['sub']))
def p(s):flow.append(Paragraph(s,styles['body']))
def t(s):flow.append(Paragraph(s,styles['tiny']))

title('Statistical Analysis Protocol | Pancreatic β-cells and Type 2 Diabetes')
t('<b>Status:</b> PROPOSED FOR SUPERVISOR REVIEW — no differential-expression or pathway tests run. 20 November 2026. | Two studies analysed separately.')
sub('1. Primary question and contribution')
p('Among originally annotated pancreatic β-cells, which candidate T2D-associated gene-expression differences persist when inference uses <b>biological donors</b> rather than cells, accounts cautiously for donor age, and is assessed for robustness to influential or low-cell donors? The contribution is a reproducible, cross-study <b>stability assessment</b>, not merely another list of associated genes. Associations are neither causal nor diagnostic.')
sub('2. Dataset roles, donors and provenance')
p('<b>Discovery, provisional:</b> Xin et al., GSE81608: 39,851 numeric (putatively NCBI GeneID) features × 1,600 cells; 503 annotated β-cells; 12 ND and 6 T2D donors. Values are already normalized <b>RPKM</b>. BMI and batch unavailable in the submitted metadata.')
p('<b>Exploratory replication, provisional:</b> Lawlor et al., GSE86469: 26,616 Ensembl-style features × 638 cells; 264 annotated β-cells; 5 ND and 3 T2D donors. The GEO file is named <b>RSEM raw expected counts</b>; numeric data include fractional values. Original RSEM scaling/quantification assumptions must be verified before count-based DE. BMI is present; batch unavailable. These expression scales <b>must not be pooled</b>.')
sub('3. Selection, annotation and feature filtering — pre-specified')
p('Include cells with original study annotation exactly <b>β/beta</b> and complete matching GEO sample ID, donor ID and ND/T2D label. Preserve an auditable cell-to-donor manifest; do not reclassify cells solely using INS expression. Retain all donors for the primary exploratory stage. Define a small-β-cell flag for ≤10 annotated cells/donor; any later exclusion requires independent documented technical or biological grounds.')
p('Before DE, map numeric Xin GeneIDs to stable Ensembl gene IDs using a versioned human NCBI gene2ensembl reference. Report one-to-one, unmapped and ambiguous IDs separately; do not silently collapse ambiguous mappings. Lawlor ENSG identifiers require assembly/version confirmation. Evaluate marker crosswalk for INS, GCG, SST, PPY. Pre-specify non-disease-based low-expression filtering using donor detection (for example ≥3 donors expressing a gene); finalize the exact metric and threshold on both scales prior to DE, then show sensitivity to reasonable alternative cutoffs.')
sub('4. Aggregation and transformations (already executable, descriptive stage)')
p('<b>GSE81608:</b> for each gene and donor, compute mean[log₂(1 + RPKM)] over that donor’s original β-cells. This donor-by-gene transformed matrix is <b>not a raw-count pseudobulk</b>. Use it for exploratory distributions and PCA; do not apply count-based negative-binomial methods to RPKM.')
p('<b>GSE86469:</b> for each gene and donor, sum unrounded per-cell RSEM expected counts. For exploratory figures only, compute per-donor total-count CPM followed by log₂(1 + CPM). Preserve fractional expected counts; do not round arbitrarily. Count-based inference is <b>conditional</b> on confirming that these are unnormalized expected counts and agreeing on suitability of a donor-level count model.')
flow.append(PageBreak())
title('Statistical Analysis Protocol | Planned Inference and Sensitivity')
t('<b>Review gate:</b> Statistical methods below are proposals only. Get written supervisor approval before DE; pathway analysis follows established DE.')
sub('5. Planned donor-level statistical models — separate by dataset')
p('<b>Xin discovery:</b> For gene-wise donor mean log₂(1+RPKM), propose a donor-level linear model with empirical-Bayes moderated variance (e.g., limma), using disease status and donor age. Consider a disease-only comparison as sensitivity. Check design rank, age overlap, residuals, leverage and effect estimates. With 18 donors, a model containing age, sex, BMI, cell count and batch simultaneously is not justified; BMI and batch are unavailable.')
p('<b>Lawlor exploratory replication:</b> If unnormalized RSEM expected counts are validated, consider library-size normalization of donor-aggregated numeric expected counts and a suitable donor-level count workflow (e.g., voom/limma with appropriate precision weights, subject to method assessment). The fractional entries remain numeric, not artificially rounded. If count assumptions cannot be justified, report descriptive log-CPM effect sizes or a separately justified continuous-summary analysis <b>without</b> presenting unvalidated count-model p-values. Three T2D donors make inference unstable; compare disease-only and disease-plus-age models as sensitivity, not a crowded covariate set.')
sub('6. Covariates, multiplicity and robustness')
p('Age is the priority potential confounder: average T2D donor age is higher in both datasets. Summarize age and sex per donor by disease group and BMI where available. Check collinearity, sparse groups and leverage before interpreting age-adjusted effects. Correct discovery gene-wise p-values using Benjamini–Hochberg FDR (provisional q < 0.05); report effect sizes, intervals and all tested-gene denominators, including nonsignificant genes. Do not claim a gene is robust from raw p-values alone.')
p('Pre-specified sensitivities: disease-only versus age-adjusted analysis; leave-one-donor-out effects for every donor (not selective removals); re-estimation after omitting <b>all</b> ≤10-β-cell donors under a documented threshold, while retaining them in the primary analysis; alternate expression filters; influence diagnostics; and, if resolvable, the original Xin cell exclusions. Avoid donor exclusions chosen by improved significance.')
sub('7. Cross-study agreement without cherry-picking')
p('Once version-consistent one-to-one gene identifiers and both study models are available, define the <b>entire intersecting tested-gene universe</b> before inspecting hits. Report sign concordance, effect-size scatterplots, rank correlations and estimates of uncertainty for all comparable genes, not just discoveries. Then separately show the proportion of Xin FDR candidates with matching effect direction, effect-size stability and available Lawlor uncertainty, explicitly flagging the low replication power. Show both successes and disagreements. Do not merge RPKM with expected counts, and do not describe demographic-only donor comparison as proof of independence.')
sub('8. Analysis gates and outputs')
p('Before DE: corrected inventory; SHA-256 input manifest; executed reproducible notebook; original cell/donor provenance; full gene-ID crosswalk with ambiguity counts; Xin 1,600-vs-1,492 investigation; study donor-provenance assessment; group demographics; donor expression matrices; QC, PCA/MDS, distribution and influence plots. Any unresolved question remains a documented limitation. <b>Stop before DE until supervisor reviews this protocol.</b>')
sub('References / data sources')
t('Xin et al. Cell Metab (2016), doi:10.1016/j.cmet.2016.08.018; GEO GSE81608. Lawlor et al. Genome Res (2017), doi:10.1101/gr.212720.116; GEO GSE86469. Squair et al. Nat Commun (2021), doi:10.1038/s41467-021-25960-2. Marques et al. J Diabetes (2022), doi:10.1111/1753-0407.13236.')

def footer(c,d):
 c.saveState();w,h=A4;c.setStrokeColor(colors.HexColor('#b9c9d1'));c.line(18*mm,14*mm,w-18*mm,14*mm)
 c.setFont('DejaVu',7.3);c.setFillColor(colors.HexColor('#526675'))
 c.drawString(18*mm,10.5*mm,'T2D β-cell donor-level analysis — supervisor review draft')
 c.drawRightString(w-18*mm,10.5*mm,f'Page {d.page} of 2');c.restoreState()
doc.build(flow,onFirstPage=footer,onLaterPages=footer)
print(filename)
