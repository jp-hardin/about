# -*- coding: utf-8 -*-
import re, os, json, statistics
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'root', 'project')
WEB = globals().get('WEB', False)  # web.py sets this to build the site-native page from the same content
os.makedirs(OUT, exist_ok=True)

KNOT='/_blob/0ec74a82d64ca48c5a0589fe8fbe222d'; LOGO='/_blob/4dd1bb932520e4f56865210abba6a736'
HEAD='/_blob/70432026c2e1430aa486f0faff90dbbc'; CHECK='/_blob/1d7f94a786903f20b9d47f2fcd162c77'; SIGN='/_blob/105394f6390d48fe915e189cfcb19e4b'
COVER='/_blob/65fe92bc106839551a16bba4f2408e75'
ICON={'clinic':'/_blob/0a5c9a57d9b791d3da0806b1290d9dc8','lab':'/_blob/caf2706ce08ce0c463cd583f7848bd77','device':'/_blob/519a1d1ba78bc3f533cc00c35b1f924d','pharmacy':'/_blob/b797df47030fde4b9619240a457d5109'}
SERIF="font-family: 'Newsreader', 'Le Monde Livre Std', Georgia, serif"
CINZEL="font-family: 'Cinzel', 'Trajan Pro', Georgia, serif"
RUN='HEALTHCARE · Q4 2026'

def L(t,u): return f'<a href="{u}">{t}</a>'
def esc(s): return re.sub(r'&(?!(amp|#\d+|[a-z]+);)', '&amp;', s)

U = dict(
 pb='https://pitchbook.brightspotcdn.com/7b/53/6ae3fbf84f12bfd344a7ae0a691a/q2-2026-healthcare-services-report-gusting-macroeconomic-headwinds-impede-progress.pdf',
 pbf='https://www.fiercehealthcare.com/finance/projected-healthcare-services-deal-count-be-lowest-2017-pitchbook-finds',
 pbasc='https://www.beckersasc.com/asc-transactions-and-valuation-issues/why-asc-deals-are-outperforming-the-rest-of-healthcare-ma-in-2026-8-things-to-know/',
 pwchs='https://www.fiercehealthcare.com/finance/health-services-deal-value-remained-resilient-2026-higher-bar-investment-pwc',
 levin='https://www.beckersasc.com/?p=106799',
 kh='https://www.kaufmanhall.com/news/hospital-and-health-system-ma-activity-among-highest-q2-levels-2019',
 pwcph='https://www.fiercebiotech.com/pharma/ma-volume-and-value-indicate-biopharma-ecosystem-back-full-health-pwc',
 pwcmt='https://www.medtechdive.com/news/medtech-ma-maintains-momentum-following-decade-high-2025-pwc/823113/',
 bain='https://www.bain.com/about/media-center/press-releases/2026/global-healthcare-private-equity-hits-record-$190-billion-deal-value-in-2025bain--company/',
 nhe='https://healthexec.com/topics/healthcare-management/healthcare-economics/cms-projects-healthcare-spending-reach-9t-2034',
 alt='https://altarum.org/sites/default/files/Altarum-August-2026-HSEI-Brief-Combined.pdf',
 bls='https://www.bls.gov/news.release/archives/empsit_10022026.htm',
 fed='https://federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm',
 tsy='https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202610',
 pbpe='https://pitchbook.brightspotcdn.com/40/42/bbeb88094080abaea3d7c87530b8/q2-2026-us-pe-breakdown.pdf',
 gf='https://www.acg.org/news-trends/news/gf-data-reports-show-steady-middle-market-deal-flow-amid-more-selective',
 ibba='https://www.ibba.org/wp-content/uploads/2026/08/mp-highlights-q2-2026.pdf',
 ibbar='https://www.webull.com/news/15462423712777216',
 srs='https://www.fasken.com/en/knowledge/2026/05/private-ma-deal-trends-to-watch-key-takeaways-from-srs-acquioms-2026-study',
 taxf='https://taxfoundation.org/data/all/federal/2026-tax-brackets/',
 hbk='https://hbkcpa.com/insights/one-big-beautiful-bill-act-business-value-2025/',
 ama='https://www.ama-assn.org/system/files/select-provisions-implementation-dates-obbba-summary.pdf',
 kff='https://www.kff.org/quick-insights/aca-marketplace-enrollment-is-down-by-3-million-after-big-jump-in-premium-payments/',
 pfs='https://www.ecgmc.com/insights/blog/cms-issues-cy-2027-medicare-physician-fee-schedule-proposed-rule',
 opps='https://www.hklaw.com/en/insights/publications/2026/07/cms-issues-sweeping-cy-2027-hospital-opps',
 hh='https://www.cms.gov/newsroom/fact-sheets/calendar-year-cy-2027-home-health-prospective-payment-system-proposed-rule-fact-sheet-cms-1844-p',
 ma='https://www.aha.org/news/headline/2026-04-06-cms-finalizes-medicare-advantage-rates-cy-2027',
 tele='https://telehealth.org/news/federal-telehealth-policy-in-2026-what-the-medicare-extensions-mean/',
 cr='https://www.astho.org/advocacy/federal-government-affairs/leg-alerts/2026/summary-of-fy27-continuing-resolution/',
 t232='https://www.crowell.com/en/insights/client-alerts/trump-administration-imposes-section-232-tariffs-on-patented-pharmaceutical-imports-tiered-rate-structure-takes-effect-beginning-july-31-2026',
 wh232='https://www.wilmerhale.com/en/insights/client-alerts/05132026-onshoring-pharmaceutical-manufacturing-procedures-to-apply-for-onshoring-agreements-to-reduce-section-232-tariffs',
 dev232='https://idataresearch.com/news-medical-device-tariffs-in-2026/',
 ieepa='https://www.barnesdennig.com/section-122-tariffs-ieepa-refunds-update/',
 state='https://www.bakerlaw.com/insights/healthcare-and-private-equity-transactions-continue-to-be-under-state-scrutiny/',
 ca1415='https://www.nixonpeabody.com/insights/alerts/2026/05/27/ohcas-proposed-emergency-regulations-clarify-ab-1415-notice-requirements',
 or951='https://www.reedsmith.com/articles/oregon-enacts-strict-new-corporate/',
 pe13='https://www.beckersasc.com/asc-transactions-and-valuation-issues/private-equity-under-the-microscope-13-updates/',
 closing='https://www.beckersasc.com/asc-transactions-and-valuation-issues/why-physician-practices-are-closing-even-as-pe-keeps-paying-record-prices-to-buy-them/',
 nonc='https://www.reedsmith.com/our-insights/blogs/employment-law-watch/102mrd5/from-rulemaking-to-enforcement-the-ftcs-non-compete-campaign-enters-a-new-phase/',
 va='https://knowledge.dlapiper.com/dlapiperknowledge/globalemploymentlatestdevelopments/2026/virginia-ban-on-non-competes-for-health-care-professionals-goes-into-effect-july-1-2026',
 usap='https://www.healthcaredive.com/news/ftc-us-anesthesia-partners-usap-settlement-texas-welsh-carson/818406/',
 hw='https://www.harriswilliams.com/our-insights/hcls-2026-industry-outlook-m&a-trends-healthcare-life-sciences',
 hwph='https://www.harriswilliams.com/our-insights/hcls-pharma-services-rebounding-performance-deal-momentum',
 hl='https://cdn.hl.com/pdf/2026/payor-technology-deep-dive-summer-2026.pdf',
 wb='https://www.williamblair.com/Insights/The-Home-as-the-Future-of-Senior-Care',
 # provider
 hca='https://www.sec.gov/Archives/edgar/data/0000860730/000119312526302539/hca-ex99_1.htm',
 hcatx='https://www.healthcaredive.com/news/hca-texas-medclinic-acquisition-urgent-care/826917/',
 hcauc='https://www.beckersasc.com/asc-transactions-and-valuation-issues/hcas-urgent-care-acquisition-spree/',
 jucm='https://www.jucm.com/?p=86881',
 carbon='https://www.sfnet.com/home/chapters/canada/news-detail/2026/02/03/carbon-health-files-for-chapter-11-bankruptcy-relief-with-more-than-$100m-in-debt',
 usph='https://www.sec.gov/Archives/edgar/data/0000885978/000088597826000042/ex99-1.htm',
 usphd='https://www.boardroomalpha.com/sec/usph-8-k-2026-05-11-0000885978-26-000024/ex99-2.htm',
 con='https://www.sec.gov/Archives/edgar/data/0002014596/000201459626000055/cghpearningsrelease-6302026.htm',
 conr='https://www.businesswire.com/news/home/20260119063302/en/Concentra-Acquires-Reliant-Immediate-Care-from-MBI-Industrial-Medicine/',
 dva='https://www.sec.gov/Archives/edgar/data/0000927066/000092706626000105/dva63026ex991.htm',
 fme='https://www.biospace.com/press-releases/fresenius-medical-care-accelerates-income-growth-to-23-in-the-second-quarter-of-2026-while-advancing-its-strategic-agenda',
 ecp='https://www.businesswire.com/news/home/20260928896885/en/EyeCare-Partners-Announces-Sale-of-Optometry-Business',
 amap='https://www.medicaleconomics.com/view/ama-physician-private-practice-unraveling-due-to-low-payment-high-costs-administrative-burdens',
 addus='https://www.sec.gov/Archives/edgar/data/0001468328/000143774926030348/ex_1015828.htm',
 addq='https://www.sec.gov/Archives/edgar/data/0001468328/000143774926025448/ex_997368.htm',
 enh='https://hlth.com/insights/news/home-health-and-hospice-provider-enhabit-to-go-private-in-1-1b-deal-2026-02-24',
 avah='https://finviz.com/news/381666/aveanna-healthcare-holdings-announces-second-quarter-financial-results-and-revised-2026-guidance',
 gmr='https://www.jems.com/ems-management/global-medical-response-raises-479m-in-stock-sale-cuts-companys-valuation-by-over-1b/',
 amb='https://www.ems1.com/legislation-funding/congress-extends-medicare-ambulance-add-on-payments-for-23-months',
 esrd='https://www.cms.gov/newsroom/fact-sheets/calendar-year-cy-2027-end-stage-renal-disease-esrd-prospective-payment-system-proposed-rule',
 achc='https://www.sec.gov/Archives/edgar/data/0001520697/000143774926024693/ex_994474.htm',
 haven='https://bhbusiness.com/2026/04/10/exclusive-mkh-capital-partners-acquires-haven-health-management-names-new-ceo/',
 brew='https://www.healthcare-brew.com/stories/2026-biggest-healthcare-deals-so-far',
 phys5='https://www.beckersasc.com/asc-transactions-and-valuation-issues/whos-driving-physician-ma-in-2026-5-deals-to-know/',
 pcems='https://www.thehealthcareinvestor.com/2026/01/articles/healthcare-services-investing/healthcare-life-sciences-private-equity-deal-tracker-grant-avenue-acquires-patientcare/',
 pespj='https://pestakeholder.org/news/private-equity-health-care-acquisitions-january-2026/',
 pespjn='https://pestakeholder.org/news/private-equity-healthcare-acquisitions-june-2026/',
 # life sci
 dgx='https://newsroom.questdiagnostics.com/2026-07-23-Quest-Diagnostics-Reports-Second-Quarter-2026-Financial-Results-Raises-Revenue-and-EPS-Guidance-for-Full-Year-2026',
 lh10q='https://www.sec.gov/Archives/edgar/data/0000920148/000092014826000175/lh-20260630.htm',
 lhchs='https://www.businesswire.com/news/home/20251202307359/en',
 lhec='https://ir.labcorp.com/news-releases/news-release-details/labcorp-completes-acquisition-select-assets-empire-city',
 clia='https://www.cms.gov/files/document/laboratory-statistics.pdf',
 pama='https://myadlm.org/cln/The-Lab-Advocate/2026/August/ADLM-Continues-Push-for-Permanent-PAMA-Reform',
 ldt='https://www.aabb.org/news-resources/news/article/2025/09/19/fda-formally-vacates-ldt-final-rule',
 tmo='https://www.marketbeat.com/instant-alerts/thermo-fisher-scientific-q2-earnings-call-highlights-2026-07-23/',
 iqv='https://www.biospace.com/press-releases/iqvia-reports-second-quarter-2026-results',
 icon='https://www.biospace.com/press-releases/icon-reports-second-quarter-2026-results',
 medp='https://www.sec.gov/Archives/edgar/data/0001668397/000166839726000023/medp-2026722exx991.htm',
 crl='https://www.sec.gov/Archives/edgar/data/0001100682/000110068226000115/crl2q26earningsrelease.htm',
 bio='https://biopharmadive.com/news/biotech-venture-capital-funding-2026-first-half/824881',
 nih='https://www.everycrsreport.com/files/2026-04-17_IN12516_be9b78de7dbbb7220ddf69779afc193119178fe5.html',
 iqvrd='https://www.iqvia.com/insights/the-iqvia-institute/reports/global-trends-in-r-and-d',
 head='https://www.prnewswire.com/news-releases/headlands-research-expands-california-presence-with-acquisition-of-clinical-trials-research-302814202.html',
 summit='https://www.prnewswire.com/news-releases/summit-clinical-research-solutions-expands-pinnacle-site-network-with-acquisition-of-dallas-research-institute-302874775.html',
 cat='https://medcitynews.com/2026/01/worldwide-clinical-trials-to-buy-catalyst-another-ma-deal-between-private-equity-backed-cros/',
 ftre='https://www.fiercebiotech.com/cro/fortrea-boosts-early-phase-platform-45-million-cro-acquisition',
 clario='https://www.sec.gov/Archives/edgar/data/97745/000009774526000066/a03242026_thermofisherscie.htm',
 tech='https://www.sec.gov/Archives/edgar/data/0000842023/000199937126013429/ex99-1.htm',
 statlab='https://peprofessional.com/2026/07/statlab-sold-to-danahers-leica-biosystems/',
 exas='https://abbott.mediaroom.com/2026-03-23-Abbott-completes-acquisition-of-Exact-Sciences',
 mt10='https://www.medtechdive.com/news/top-10-medtech-deals-in-the-first-half-of-2026/824435/',
 dcat='https://www.dcatvci.org/features/cdmo-cmo-the-key-moves-in-2026/',
 biosec='https://www.akingump.com/en/insights/alerts/biosecure-act-becomes-law',
 skin='https://www.polsinelli.com/health-care/publications/cms-finalizes-reforms-skin-substitute-payments-rising-costs-enforcement-activity',
 mpo='https://www.mpo-mag.com/exclusives/2026-medical-device-industry-ma-roundup/',
 # med products
 syk='https://www.sec.gov/Archives/edgar/data/0000310764/000031076426000048/sykex991earningsq22026.htm',
 mdt='https://news.medtronic.com/2026-09-01-Medtronic-reports-first-quarter-fiscal-2027-results-delivers-broad-based-portfolio-performance-and-raises-fiscal-2027-guidance',
 zbh='https://www.sec.gov/Archives/edgar/data/0001136869/000119312526333761/zbh-ex99_1.htm',
 ste='https://www.biospace.com/press-releases/steris-announces-financial-results-for-fiscal-2027-first-quarter',
 hfma='https://www.hfma.org/fast-finance/health-system-capital-investment-strategy-2026/',
 hsic='https://www.businesswire.com/news/home/20260731616019/en/',
 xray='https://investor.dentsplysirona.com/news-releases/news-release-details/dentsply-sirona-reports-second-quarter-2026-results',
 nvst='https://pulse2.com/envista-12-6-million-ieepa-tariff-refund-arrives-as-adjusted-ebitda-rises-28/',
 ultra='https://www.beckersdental.com/supply-chain/ultradent-to-be-acquired-by-japanese-manufacturing-company-for-900m/',
 apex='https://www.beckersdental.com/supply-chain/dental-lab-group-receives-private-equity-investment/',
 ada='https://adanews.ada.org/huddles/dental-fiscal-squeeze-continues-into-2026/',
 mdlnipo='https://www.fiercehealthcare.com/medtech/medline-makes-nasdaq-debut-raising-626b-years-largest-ipo',
 mdln='https://www.sec.gov/Archives/edgar/data/0002046386/000204638626000049/ex9912q26pressrelease.htm',
 omi='https://www.sec.gov/Archives/edgar/data/75252/000119312525338325/d36369dex991.htm',
 mck='https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000232/mck_exhibit991x6302026.htm',
 cahhme='https://www.hmenews.com/article/cardinal-health-expands-supplies-business-with-two-tuck-in-acquisitions',
 qmsr='https://www.ropesgray.com/en/insights/alerts/2026/02/a-qmsr-state-of-mind-fda-adopts-new-inspection-approach-for-medical-devices',
 ruhof='https://www.businesswire.com/news/home/20260122220937/en/Aspen-Surgical-Acquires-Ruhof-Healthcare-and-Expands-Global-Infection-Prevention-and-Reprocessing-Solutions',
 tfx='https://www.medtechdive.com/news/teleflex-sale-oem-acute-care-interventional-urology/807504/',
 vmd='https://www.hmenews.com/article/in-brief-molina-pauses-adapthealth-lowers-viemed-grows-cms-finalizes',
 cb='https://aahomecare.org/post/CMS-Releases-DMEPOS-Home-Health-Proposed-Final-Rule-with-Provisions-to-Restart-CB-Program',
 itgr='https://www.medicaldesignandoutsourcing.com/?p=280019',
 masi='https://pulse2.com/danaher-to-acquire-masimo-for-9-9-billion/',
 numo='https://www.hmenews.com/article/hanger-numotion-to-merge',
 # pharmacy
 iqvm='https://www.iqvia.com/insights/the-iqvia-institute/reports/us-medicine-use-trends-2026',
 ncpa='https://ncpa.org/newsroom/news-releases/2025/10/19/ncpa-releases-2025-digest-report',
 ncpas='https://www.drugtopics.com/view/ncpa-advocates-for-medicare-drug-price-negotiation-program-overhaul-due-to-pharmacy-cash-flow',
 grdn='https://www.sec.gov/Archives/edgar/data/0001802255/000119312526338032/d160709dex991.htm',
 grdnc='https://www.nasdaq.com/articles/guardian-pharmacy-services-q2-earnings-call-highlights',
 grdnn='https://finviz.com/news/387762/guardian-pharmacy-services-acquires-assets-of-tennessee-based-nautilus-pharmacy',
 btsg='https://www.sec.gov/Archives/edgar/data/0001865782/000119312526326654/btsg-ex99_1.htm',
 btsgc='https://www.marketbeat.com/instant-alerts/brightspring-health-services-q2-earnings-call-highlights-2026-07-31/',
 omni='https://www.cvshealth.com/news/company-news/omnicare-receives-court-approval-for-sale-of-business-to-genierx.html',
 omnib='https://www.beckershospitalreview.com/pharmacy/cvs-to-sell-its-troubled-long-term-care-pharmacy/',
 opch='https://www.sec.gov/Archives/edgar/data/0001014739/000101473926000021/exhibit991-q22026.htm',
 opchc='https://www.marketbeat.com/instant-alerts/option-care-health-q2-earnings-call-highlights-2026-07-29/',
 nhia='https://rxtoolkit.com/inside-2026-nhia-conference-home-infusion-updates/',
 pbm='https://www.sidley.com/en/insights/newsupdates/2026/02/congress-passes-significant-federal-pharmacy-benefit-manager-reform-impacting-pharmaceutical-market',
 ftcins='https://truveris.com/ftc-settlements-with-esi-cvs-and-optum-rx/',
 mintz='https://www.mintz.com/insights-center/viewpoints/2146/2026-07-07-state-regulation-pbms-subject-robust-legal-challenges',
 cor='https://www.sec.gov/Archives/edgar/data/0001140859/000114085926000032/exhibit991-q32026.htm',
 sol='https://www.mdm.com/news/operations/earnings/cardinal-health-reports-flat-4q-revenue-higher-profit-and-a-1-9b-acquisition/',
 sia='https://www.staffingindustry.com/editorial/healthcare-staffing-report/healthcare-staffing-rebounds-as-demand-strengthens-in-the-second-and-third-quarters',
 amn='https://www.sec.gov/Archives/edgar/data/0001142750/000114275026000008/amn-ex991x20260630xearning.htm',
 aya='https://www.staffingindustry.com/news/global-daily-news/aya-healthcare-terminates-merger-agreement-with-cross-country-healthcare',
 knox='https://www.staffingindustry.com/editorial/healthcare-staffing-report/private-equity-firm-knox-lane-completes-acquisition-of-cross-country-names-new-ceo',
 knoxf='https://www.fiercehealthcare.com/finance/staffing-firm-cross-country-healthcare-be-acquired-knox-lane-437m',
 jolts='https://www.bls.gov/news.release/jolts.t01.htm',
 strata='https://stocks.observer-reporter.com/observerreporter/article/gnwcq-2026-4-30-strata-acquires-ohio-valley-perfusion-associates',
 jll='https://www.joplinglobe.com/region/national_business/life-couriers-announces-completion-of-acquisition-by-jll-partners/article_8bf5ef6e-794d-56cc-9f48-d026baeb5497.html',
 velo='https://www.staffingindustry.com/editorial/healthcare-staffing-report/locum-tenens-provider-velosource-acquires-two-firms',
 snap='https://www.staffingindustry.com/editorial/healthcare-staffing-report/snapcare-announces-merger-with-connectrn',
 idr='https://www.staffingindustry.com/editorial/healthcare-staffing-report/care-career-buys-idr-healthcare-its-sixth-acquisition-in-18-months',
 focus='https://www.staffingindustry.com/editorial/healthcare-staffing-report/elite365-announces-deal-for-healthcare-staffing-firm-focus-staff',
)
BI='https://www.benchmarkintl.com/insights/'
T = dict(
 precise=BI+'benchmark-international-successfully-facilitated-the-transaction-between-precise-bioscience-llc-and-new-horizon-medical-solutions/',
 form=BI+'completed-transactions/benchmark-international-successfully-facilitated-the-transaction-between-formulation-technology-incorporated-and-aavin-private-equity/',
 frost=BI+'completed-transactions/benchmark-international-successfully-facilitated-the-transaction-between-fast-response-onsite-testing-inc-and-relentless-health-inc/',
 cepro=BI+'completed-transactions/benchmark-international-successfully-facilitated-the-transaction-between-critical-environments-professionals-and-scientific-safety-alliance/',
 dental=BI+'completed-transactions/benchmark-international-facilitated-the-transaction-of-dental-holdings-llc-and-solmetex-llc/',
 foster=BI+'benchmark-international-successfully-facilitated-the-transaction-between-fosterbridge-inc-and-amvie/',
 medtemps=BI+'benchmark-international-successfully-facilitated-the-transaction-between-medical-temps-inc-and-health-advocates-network/',
 brooks=BI+'completed-transactions/benchmark-international-successfully-facilitated-the-transaction-between-the-brooks-group-and-private-investors/',
)

# ---------- building blocks ----------
def P(t, extra=''): return f'<p style="margin: 0; text-align: justify{extra}">{t}</p>'
def PC(t): return f'<p style="margin: 0 0 14px">{t}</p>'
def EYE(t): return f'<div style="font-weight: 700; font-size: 10.5px; line-height: 16px; letter-spacing: 2.6px; text-transform: uppercase">{t}</div>'
def H2(t, m='0'): return f'<h2 style="margin: {m}; {SERIF}; font-weight: 600; font-size: 21px; line-height: 27px; letter-spacing: 0; color: #B68757; text-wrap: balance">{t}</h2>'
def table(cols, head, rows, pad=5, fs=12):
    g=f'display: grid; grid-template-columns: {cols}; column-gap: 14px'
    o=[f'<div style="font-size: {fs}px; line-height: 17px; letter-spacing: 0.2px">',
       f'<div style="{g}; padding: 0 0 7px; border-bottom: 2px solid #B68757; font-weight: 700; font-size: 9.5px; line-height: 14px; letter-spacing: 1.6px; text-transform: uppercase; align-items: end">'+''.join(f'<div>{h}</div>' for h in head)+'</div>']
    for r in rows:
        o.append(f'<div style="{g}; padding: {pad}px 0; border-bottom: 1px solid #D9D3CA">'+''.join((f'<div style="font-weight: 700">{c}</div>' if i==0 else f'<div>{c}</div>') for i,c in enumerate(r))+'</div>')
    o.append('</div>'); return '\n'.join(o)
def band(stats, icon, alt):
    cells=''.join(f'<div style="display: flex; flex-direction: column; gap: 4px"><div style="{SERIF}; font-weight: 600; font-size: 30px; line-height: 34px; letter-spacing: 0; color: #B68757">{a}</div><div style="font-size: 11px; line-height: 15px; letter-spacing: 0.3px">{b}</div></div>' for a,b in stats)
    return f'<div style="margin: 4px 0; display: flex; align-items: center; background: #2E2E2E; color: #FFFFFF"><div style="flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 18px; padding: 0 8px 0 20px">{cells}</div><img src="{ICON[icon]}" alt="{alt}" style="display: block; width: 236px; height: 112px"></div>'
def quote(q, who):
    return f'<div style="break-inside: avoid; display: flex; flex-direction: column; margin: 6px 0 20px; padding: 16px 0 14px; border-top: 1px solid #B68757; border-bottom: 1px solid #B68757; text-align: left"><div style="{SERIF}; font-style: italic; font-weight: 500; font-size: 15.5px; line-height: 24px; letter-spacing: 0; color: #333333">&ldquo;{q}&rdquo;</div><div style="margin-top: 6px; font-size: 10.5px; line-height: 15px; letter-spacing: 0.3px">{who}</div></div>'
def XREF(pid, pre, webpre, anchor, label, cap=False):
    return f'{webpre} <a href="#{anchor}">{label}</a>' if WEB else f'{pre} @@PG:{pid}@@'
def cols2(inner): return f'<div style="column-count: 2; column-gap: 32px; text-align: justify">{inner}</div>'

pages=[]  # (file, title, body_html, kind)
def page(fn, title, inner, n, h=890):
    body=f'''<img src="{KNOT}" alt="" style="position: absolute; left: 310px; top: 600px; width: 506px; height: 718px; opacity: 0.3">
<div style="position: absolute; left: 0; top: 40px; width: 432px; height: 1px; background: #6D7681"></div>
<div style="position: absolute; right: 48px; top: 30px; {CINZEL}; font-size: 12px; line-height: 20px; letter-spacing: 0.8px; color: #6D7681">{RUN}</div>
<div data-fit="{h}" style="position: absolute; left: 48px; top: 76px; width: 720px; height: {h}px; display: flex; flex-direction: column; gap: 14px">
{inner}
</div>
<div style="position: absolute; left: 0; bottom: 38px; width: 816px; text-align: center; font-weight: 700; font-size: 8.5px; line-height: 12px; letter-spacing: 3.6px">BENCHMARKINTL.COM</div>
<div style="position: absolute; right: 48px; bottom: 38px; font-weight: 700; font-size: 8.5px; line-height: 12px; letter-spacing: 2px">@@PN@@</div>'''
    pages.append((fn,title,body))

# ---------- 01 cover ----------
exec(open(os.path.join(ROOT,'extra.py')).read())
if WEB: exec(open(os.path.join(ROOT,'webhelpers.py')).read())
def fig(a,b): return f'<div style="display: flex; flex-direction: column; gap: 4px"><div style="{SERIF}; font-weight: 600; font-size: 30px; line-height: 34px; letter-spacing: 0; color: #B68757">{a}</div><div style="font-size: 11px; line-height: 15px; letter-spacing: 0.3px">{b}</div></div>'
BRIEF='Healthcare enters the fourth quarter of 2026 with health systems, distributors and public strategic buyers setting the pace, and with private equity completing fewer and more carefully underwritten transactions. Private equity closed roughly 337 healthcare services deals in the first half, a pace that would make 2026 the slowest year since 2017, while medtech deal value reached $36.5 billion over the same six months and pharma and life sciences recorded its strongest quarter since 2020. Demand underneath the deal market is steady, with national health spending running 6.8% above last year in July and projected to reach nearly $9.0 trillion by 2034.'
FIGS=[('6.8%', 'Growth in national health spending in the year to July 2026'), ('337', 'Private equity healthcare services deals in the first half, the slowest pace since 2017'), ('$36.5B', 'Medtech deal value in the first half of 2026'), ('13.6x', 'Median EBITDA multiple private equity paid for healthcare services companies in 2025, weighted toward larger platforms')]
cover=f'''<img src="{KNOT}" alt="" style="position: absolute; left: 310px; top: 600px; width: 506px; height: 718px; opacity: 0.3">
<img src="{COVER}" alt="Four line illustrations: a clinic, laboratory glassware, a patient monitor and a pharmacy bottle with a capsule" style="position: absolute; left: 0; top: 0; width: 816px; height: 590px">
<img src="{LOGO}" alt="Benchmark International" style="position: absolute; left: 293px; top: 42px; width: 230px; height: 108px">
<div style="position: absolute; left: 48px; top: 334px; width: 720px; display: grid; grid-template-columns: repeat(4, 1fr); text-align: center; color: #FFFFFF; font-weight: 700; font-size: 8px; line-height: 14px; letter-spacing: 2px; text-transform: uppercase">
<div>Provider<br>Services</div><div>Life Sciences<br>&amp; Diagnostics</div><div>Medical Products<br>&amp; Distribution</div><div>Pharmacy &amp;<br>Healthcare Services</div>
</div>
<div style="position: absolute; left: 48px; top: 400px; width: 720px; display: flex; flex-direction: column; color: #FFFFFF">
<h1 style="margin: 0; {CINZEL}; font-weight: 400; font-size: 46px; line-height: 54px; letter-spacing: 2px">HEALTHCARE</h1>
<div style="height: 1px; background: #B68757; margin: 13px 0 11px"></div>
<div style="{SERIF}; font-style: italic; font-weight: 600; font-size: 24px; line-height: 31px; letter-spacing: 0">Q4 2026 M&amp;A Sector Report</div>
</div>
<div data-fit="392" style="position: absolute; left: 48px; top: 606px; width: 720px; height: 392px; display: flex; flex-direction: column; gap: 10px">
<div style="font-weight: 700; font-size: 9.5px; line-height: 14px; letter-spacing: 2px; text-transform: uppercase">October 2026 - Jared Hardin | Managing Director | Benchmark International</div>
<h2 style="margin: 0; {SERIF}; font-weight: 600; font-size: 21px; line-height: 27px; letter-spacing: 0; color: #B68757">The quarter in brief</h2>
<p style="margin: 0; text-align: justify">{BRIEF}</p>
<div style="display: grid; grid-template-columns: repeat(4, 1fr); column-gap: 22px; padding: 13px 0 14px; border-top: 1px solid #B68757; border-bottom: 1px solid #B68757">
{''.join(fig(a,b) for a,b in FIGS)}
</div>
<div style="font-size: 10px; line-height: 14px; letter-spacing: 0.2px">Information as of October 5, 2026. Public-company and larger-platform multiples are reference points, and a private company&#39;s price depends on the business itself.</div>
</div>
<div style="position: absolute; left: 0; bottom: 38px; width: 816px; text-align: center; font-weight: 700; font-size: 8.5px; line-height: 12px; letter-spacing: 3.6px">BENCHMARKINTL.COM</div>'''
pages.append(('Main.dc.html','Cover',cover))

# ---------- 02 four focus areas ----------
c4='118px 1fr 1fr 124px'
p2=EYE('The four focus areas at the start of the quarter')+table(c4,['Focus area','Where the market stands','Who is buying','Benchmark International: closed in the trailing 24 months, and live'],[
 ['Provider Services','The United States has 14,655 urgent care centers and the 100 largest operators hold 41% of them; Medicare has proposed lowering the physician conversion factor by 1.2% to 1.7% for 2027','HCA Healthcare with 70 urgent care centers acquired in 2026, MyEyeDr., U.S. Physical Therapy, Addus HomeCare and Concentra','2 closed, 19 live'],
 ['Life Sciences & Diagnostics','Research outsourcing demand is recovering, with IQVIA booking $1.22 of new work for each dollar of revenue; Medicare laboratory fee cuts of up to 15% a year are scheduled to resume in 2027','Labcorp and Quest for laboratories, Thermo Fisher, Danaher and Merck KGaA for tools and reagents, sponsor-backed clinical research site networks','4 closed, 4 live'],
 ['Medical Products & Distribution','Stryker grew 9.0% organically and Steris grew healthcare consumables 9%; tariff costs and refunds are moving earnings in both directions, and 41% of health systems plan to cut capital spending','KKR, Danaher, Mitsui Chemicals, Cardinal Health, Aspen Surgical and Platinum Equity','1 closed, 8 live'],
 ['Pharmacy & Healthcare Services','Net medicine spending reached $606 billion in 2025; negotiated Medicare prices are compressing long-term care pharmacy revenue; healthcare staffing is forecast to grow 1% to $39.0 billion','Guardian Pharmacy, Cencora, Cardinal Health and McKesson, Knox Lane in staffing, Strata Critical Medical in perfusion','5 closed, 8 live'],
],pad=7)+H2('Deal market: strategic buyers are active while private equity completes fewer deals','10px 0 0')+P(f'Private equity healthcare services deal value was $17.8 billion in the first half of 2026, 7.3% below the prior year, and the roughly 337 transactions in the period annualize to 674 against an average of 903 a year between 2018 and 2024 ({L("PitchBook, Q2 2026 Healthcare Services Report",U["pb"])}; {L("Fierce Healthcare, August 2026",U["pbf"])}). Physician practice management accounts for most of the decline, with 71 deals in the second quarter against 111 a year earlier, while ancillary and outsourced services such as surgery centers, staffing and laboratories are tracking only 4.9% below 2025 ({L("Becker&#39;s ASC Review",U["pbasc"])}). PwC counted 300 health services transactions in the first quarter and about $28 billion of value through May 31 ({L("PwC via Fierce Healthcare, June 17, 2026",U["pwchs"])}).')
page('P02.dc.html','The four focus areas',p2,2)

# ---------- 03 deal market ----------
c3='190px 1fr 86px 150px'
p3=P(f'Deal activity in the rest of healthcare has been stronger than in provider services, and pharma and life sciences deal value exceeded $65 billion in the first quarter, with 16 transactions of $1 billion or more, the strongest quarter since 2020 ({L("PwC via Fierce Biotech",U["pwcph"])}). Medtech followed a decade-high 2025 with $36.5 billion of deal value in the first half ({L("PwC via MedTech Dive",U["pwcmt"])}), and hospitals and health systems announced 18 transactions in the second quarter, including three mega-mergers ({L("Kaufman Hall, July 13, 2026",U["kh"])}).')+table(c3,['Healthcare deal indicator','Latest reading','Period','Source'],[
 ['All healthcare transactions','549 deals, level with both the prior quarter and the prior year; private equity was the buyer in 181','Q1 2026',L('LevinPro data via Becker&#39;s ASC Review',U['levin'])],
 ['Physician group share of health services deals','46%, up from 37% a year earlier','Q1 2026',L('PwC via Fierce Healthcare',U['pwchs'])],
 ['Median private equity entry multiple, healthcare services','13.6x EBITDA, with median net debt of 5.2x EBITDA','2025',L('PitchBook via Becker&#39;s ASC Review',U['pbasc'])],
 ['Projected private equity healthcare services exits','Down 26.5% by count and 30.9% by value','2026',L('PitchBook',U['pb'])],
 ['Average purchase price, completed middle-market transactions in all industries','7.0x trailing adjusted EBITDA, with senior debt priced at 7.8%','Q2 2026',L('GF Data via ACG',U['gf'])],
 ['Median multiple, transactions of $5 million to $50 million in all industries','5.8x, the highest since early 2022','Q2 2026',L('IBBA and M&A Source Market Pulse',U['ibba'])],
])+P(f'Financing became more expensive during the third quarter, when the Federal Reserve raised its target range by a quarter point to 3.75% to 4.00% on September 16 ({L("Federal Reserve",U["fed"])}), the 10-year Treasury yielded 5.24% on October 1 ({L("US Treasury",U["tsy"])}), and direct lenders widened buyout loan spreads to an average of 509 basis points over the benchmark rate in the second quarter from 474 in the first ({L("PitchBook, Q2 2026 US PE Breakdown",U["pbpe"])}).')+quote('Financial sponsors still have near-record levels of &lsquo;dry powder,&rsquo; but they are becoming increasingly more selective with the assets they choose to invest in.', f'Houlihan Lokey, {L("Summer 2026 Payor Technology Deep Dive",U["hl"])}')+H2('Demand: spending and employment continue to grow','4px 0 0')+P(f'National health spending grew 6.8% in the year to July 2026, after a revised 7.1% in June, and represented 18.4% of GDP ({L("Altarum Health Sector Economic Indicators, September 28, 2026",U["alt2"])}). CMS projects nearly $9.0 trillion of spending in 2034, or 20.6% of GDP, on average annual growth of 5.4% ({L("CMS National Health Expenditure fact sheet",U["nhefs"])}). Healthcare employers added 17,000 jobs in September against a twelve-month average of 33,000 ({L("Bureau of Labor Statistics, October 2, 2026",U["bls"])}). Spending growth supports demand across the sector, and a particular business captures it through its payer rates, labor costs and collections.')
page('P03.dc.html','Deal market and demand',p3,3)

# ---------- 04 policy ----------
c4b='176px 1fr 150px'
p4=EYE('Reimbursement, policy and deal regulation')+H2('Medicare rates for 2027 are proposed and the Medicaid changes begin in January')+table(c4b,['Item','Status in October 2026','Source'],[
['Medicare Physician Fee Schedule, 2027','Proposed conversion factors of $33.17 for qualifying participants in advanced alternative payment models and $32.84 for other clinicians, reductions of 1.19% and 1.68%, as the one-year 2.5% increase for 2026 expires; final rule pending',L('CMS proposed rule',U['pfsf'])],
 ['Hospital outpatient and surgery center rates, 2027','Proposed increase of 2.4% for both; 637 procedures would leave the inpatient-only list and about 618 would be added to the surgery center list',L('CMS rule register',U['oppsr'])],
 ['Home health, 2027','Proposed aggregate increase of 2.4%, or $420 million',L('CMS fact sheet',U['hh'])],
 ['Medicare Advantage, 2027','Final rate increase of 2.48%, more than $13 billion',L('CMS final rate notice',U['maf'])],
 ['Medicare telehealth','Specified Medicare flexibilities extended through December 31, 2027',L('HHS policy updates',U['teleh'])],
 ['Medicaid','Work requirements and six-month eligibility reviews for applicable expansion adults begin in 2027; provider-tax thresholds in most expansion states phase down from October 2027',L('Medicaid.gov',U['mcaid'])+'; '+L('CMS provider-tax proposal',U['ptax'])],
 ['Marketplace coverage','Enhanced premium tax credits expired after 2025; enrollment fell from 22.1 million to 19.2 million',L('KFF, June 29, 2026',U['kff'])],
 ['Pharmaceutical tariffs','100% default rate on covered patented products, effective July 31 for the companies named in Annex III and September 29 for others; country and company exceptions apply and generics are excluded',L('White House proclamation',U['whp'])],
],pad=3,fs=11.5)+H2('State review of healthcare transactions now reaches private equity and management companies','2px 0 0')+P(f'California\'s AB 1415 took effect on January 1, 2026 and brings private equity groups, hedge funds and management services organizations into the state\'s transaction notice requirements ({L("Nixon Peabody",U["ca1415"])}). Oregon\'s SB 951 bars management services organizations from majority ownership or control of medical practices, with existing arrangements required to comply by January 1, 2029 ({L("Reed Smith",U["or951"])}). Massachusetts, Indiana, New Mexico, Rhode Island and Washington have enacted notice or approval requirements, and Maine\'s 180-day notice and approval regime begins January 1, 2027 ({L("BakerHostetler",U["state"])}).')+P(f'Restrictive covenants for clinicians are also narrowing, and Virginia\'s ban on noncompetes for healthcare professionals, effective July 1, 2026, retains an exception for the sale of a business ({L("DLA Piper",U["va"])}). Federal tax law keeps a top long-term capital gains rate of 20% and an estate and gift exemption of $15 million per person ({L("Tax Foundation",U["taxf"])}; {L("HBK CPAs & Consultants",U["hbk"])}). A seller\'s proceeds also depend on entity and deal structure, the portion of the price taxed as ordinary income, the net investment income tax and state tax, and on the ownership and review requirements of each state involved.')
page('P04.dc.html','Reimbursement, policy and deal regulation',p4,4)
add_policy()

# ---------- subsector helper ----------
ct='70px 196px 170px 1fr'
def txpage(fn,title,eye,h,intro,rows,after,n):
    page(fn,title,EYE(eye)+H2(h)+intro+table(ct,['Date','Target (linked)','Buyer','Terms disclosed'],rows)+after,n)

# ---------- 05/06 provider ----------
p5=EYE('Provider Services')+H2('Health systems are buying access points and sponsors are trading platforms')+band([('14,655','Urgent care centers in the United States in April 2026'),('70','Urgent care centers HCA Healthcare acquired in three 2026 transactions'),('42.2%','Share of physicians working in physician-owned practices, down from 60.1% in 2012')],'clinic','Line illustration of a clinic building with a heartbeat line')+cols2(
PC(f'Patient volumes are growing in the outpatient settings that founder-owned providers occupy, and HCA reported emergency room visits up 3.6% and equivalent admissions up 2.7% on a same-facility basis in the second quarter ({L("HCA Healthcare",U["hca"])}). Concentra saw 2.6% more visits a day at 4.6% more revenue per visit ({L("Concentra",U["con"])}), and U.S. Physical Therapy averaged 33.5 visits per clinic per day at a net rate of $107.59, although therapist salaries rose to 57.9% of revenue from 56.6% ({L("U.S. Physical Therapy",U["usph"])}).')+
PC(f'Urgent care is consolidating toward hospital ownership, with the 100 largest operators holding 6,056 of the country\'s 14,655 centers and 55.9% of those locations affiliated with a hospital ({L("Journal of Urgent Care Medicine, May 29, 2026",U["jucm"])}). HCA bought 13 CommunityMed centers in North Texas in February, 17 Urgent Care Group clinics in the Carolinas in June and the 40-center Texas MedClinic in August ({L("Becker&#39;s ASC Review",U["hcauc"])}; {L("Healthcare Dive",U["hcatx"])}). Scale without hospital backing has been harder to sustain, and venture-backed Carbon Health filed for Chapter 11 in February with 96 clinics and more than $100 million of debt ({L("Secured Finance Network",U["carbon"])}).')+
PC(f'In eye care, EyeCare Partners agreed on September 28 to sell its optometry business of more than 300 offices to MyEyeDr., with the proceeds going to debt reduction ({L("EyeCare Partners",U["ecp"])}). Independent practice continues to shrink, and 42.2% of physicians worked in physician-owned practices in the AMA\'s latest survey against 60.1% in 2012 ({L("AMA survey via Medical Economics",U["amap"])}).')+
quote('The convergence of demographic demand, patient preference, technological innovation, and supportive policy is transforming home-based care from a niche offering into a core component of healthcare systems.', f'William Blair, {L("The Home as the Future of Senior Care",U["wb"])}, September 29, 2026')+
PC(f'Care in the home drew the largest provider transactions of the year, with Kinderhook agreeing to take Enhabit private at an enterprise value of about $1.1 billion ({L("HLTH",U["enh"])}), and Addus HomeCare agreeing to pay about $275 million for AccentCare\'s personal care division, which generates about $280 million of annual revenue in ten states ({L("Addus HomeCare",U["addus"])}). Addus grew personal care revenue 6.8% on a same-store basis with rate increases of 9.9% in Texas and 3.9% in Illinois ({L("Addus second-quarter results",U["addq"])}).')+
PC(f'Dialysis and emergency medical services are growing more slowly. DaVita reported normalized non-acquired treatment growth of 0.3% ({L("DaVita",U["dva"])}), and Fresenius Medical Care reported US same-market treatments down 0.9% after exiting about 100 clinics ({L("Fresenius Medical Care",U["fme"])}). Global Medical Response raised $478.7 million in its May initial public offering at a valuation of about $3.35 billion ({L("JEMS",U["gmr"])}), and Congress extended the Medicare ambulance add-on payments through December 31, 2027 ({L("EMS1",U["amb"])}).'))
page('P05.dc.html','Provider Services',p5,5)

txpage('P06.dc.html','Provider Services transactions','Provider Services: selected acquisitions and financings','Disclosed prices are read alongside the ownership interest acquired',
P(f'U.S. Physical Therapy paid $37.6 million for interests of 50% to 70% in three businesses with about $27.0 million of combined annual revenue. Those are prices for partial interests, so a comparison with a whole-company sale has to account for the share acquired, debt, the economics the founders retain and EBITDA ({L("U.S. Physical Therapy",U["usph"])}; {L("investor presentation, May 2026",U["usphd"])}).'),[
 ['Sep 2026',L('EyeCare Partners optometry business',U['ecp']),'MyEyeDr.','More than 300 offices; price undisclosed; closing expected in the fourth quarter'],
 ['Sep 2026',L('AccentCare personal care division',U['addus']),'Addus HomeCare','About $275 million for about $280 million of annual revenue'],
 ['Aug 2026',L('Texas MedClinic',U['hcatx']),'HCA Healthcare','40 urgent care centers in San Antonio, Austin and Houston; undisclosed'],
 ['Jul 2026',L('12-clinic physical therapy practice',U['usph']),'U.S. Physical Therapy','$16.4 million for a 67% interest; $12.0 million of annual revenue'],
 ['Jun 2026',L('Urgent Care Group',U['hcauc']),'HCA Healthcare','17 clinics in the Carolinas; undisclosed'],
 ['May 2026',L('Global Medical Response',U['gmr']),'Initial public offering','$478.7 million raised at a valuation of about $3.35 billion'],
 ['Apr 2026',L('Haven Health Management',U['haven']),'MKH Capital Partners','22 addiction and psychiatric locations; reported as a nine-figure price'],
 ['Mar 2026',L('Talkspace',U['brew']),'Universal Health Services','About $835 million'],
 ['Feb 2026',L('Enhabit',U['enh']),'Kinderhook','Enterprise value of about $1.1 billion; 249 home health and 117 hospice locations'],
 ['Jan 2026',L('Eight-clinic physical therapy practice',U['usph']),'U.S. Physical Therapy','$6.2 million for a 50% interest; $8.0 million of annual revenue'],
 ['Jan 2026',L('PatientCare EMS Solutions',U['pcems']),'Grant Avenue Capital','Ground ambulance provider, Tyler, Texas; undisclosed'],
 ['Jan 2026',L('Ally Pediatric Therapy',U['pespj']),'ACES, backed by General Atlantic','Pediatric and autism therapy, Phoenix; undisclosed'],
],
P(f'The reimbursement calendar bears on price in each of these trades, and Medicare\'s proposed 2027 dialysis rule would raise total payments 1.1% ({L("CMS",U["esrd"])}), and Acadia Healthcare, whose adjusted EBITDA fell to $149.2 million from $201.8 million, has named Medicaid work requirements and labor costs as risks to behavioral health volumes ({L("Acadia Healthcare",U["achc"])}). Buyers are paying most readily for in-network commercial revenue, dense local footprints and clinicians who stay after closing.'),6)

# ---------- 07/08 life sciences ----------
add_prov_impl()
p7=EYE('Life Sciences & Diagnostics')+H2('Research spending has turned up and laboratories are selling to the national networks')+band([('1.22x','IQVIA net new business relative to revenue in the second quarter'),('$9.1B','Biotech venture funding in the first half, the most since early 2022'),('15%','Annual Medicare laboratory fee cut that could resume in 2027')],'lab','Line illustration of a laboratory flask and a test tube')+cols2(
PC(f'Clinical laboratories are consolidating into Labcorp and Quest through hospital outreach purchases and sales by independent owners. Quest grew revenue 10.2% in the second quarter on 13.1% more requisitions ({L("Quest Diagnostics",U["dgx"])}). Labcorp spent $528.6 million on acquisitions in the first half, recording $250.0 million of acquired assets for Empire City Laboratories and $165.0 million for the Parkview Health outreach laboratory ({L("Labcorp Form 10-Q",U["lh10q"])}), after paying about $194 million for Community Health Systems\' outreach laboratories ({L("Labcorp, December 2, 2025",U["lhchs"])}). Independent laboratories number 7,824 of the 301,284 CLIA-certified sites in the country ({L("CMS, September 2026",U["clia"])}).')+
PC(f'Medicare payment is the open question for laboratory owners, because fee cuts under the Protecting Access to Medicare Act have been delayed through 2026, and reductions of up to 15% a year could resume in 2027 unless Congress passes the RESULTS Act ({L("Association for Diagnostics & Laboratory Medicine",U["pama"])}).')+
PC(f'Outsourced research has recovered from two slow years, with IQVIA\'s net bookings up 19% ({L("IQVIA",U["iqv"])}), ICON reporting a 22% sequential rise in requests for proposal ({L("ICON",U["icon"])}), Medpace growing revenue 17.2% ({L("Medpace",U["medp"])}) and Charles River posting its best organic growth since 2023 ({L("Charles River Laboratories",U["crl"])}). Biotech venture funding reached at least $9.1 billion in the first half ({L("BioPharma Dive",U["bio"])}), and Thermo Fisher described the US academic and government market as stabilizing ({L("Thermo Fisher call summary",U["tmo"])}). Congress has kept the 15% cap on NIH indirect costs blocked, although the fiscal 2027 budget request proposes it again ({L("Congressional Research Service",U["nih"])}).')+
quote('Biopharma spending and activity are picking up thanks to increasing specialty therapeutics demand, greater funding, and more drug approvals.', f'Harris Williams, {L("Outsourced Pharma Services",U["hwph"])}, September 24, 2026')+
PC(f'Private equity sponsors continue to lead the consolidation of clinical research sites. Headlands Research, owned by THL, bought the two-site Clinical Trials Research in California in June ({L("Headlands Research",U["head"])}), and Summit Clinical Research added Dallas Research Institute to its Pinnacle network in September ({L("Summit Clinical Research",U["summit"])}).')+
PC(f'Trade policy changes manufacturing economics by product, origin and company agreement, and buyers verify tariff eligibility, pass-through and change-of-control terms ({L("White House proclamation",U["whp"])}; detail {XREF('X-policy','on page','under','policy','Policy and price')}). The BIOSECURE Act became law in December 2025 ({L("Akin",U["biosec"])}), and Medicare moved skin substitutes to a flat rate of about $127 per square centimeter in 2026, a change CMS expects to reduce spending by $19.6 billion ({L("Polsinelli",U["skin"])}).'))
page('P07.dc.html','Life Sciences & Diagnostics',p7,7)

txpage('P08.dc.html','Life Sciences & Diagnostics transactions','Life Sciences & Diagnostics: announced transactions','Strategic buyers paid for consumables, data and laboratory volume',
P(f'The largest buyers of 2026 were operating companies adding recurring product lines. Danaher\'s Leica Biosystems bought StatLab, a pathology consumables maker that Audax and Linden had built through nine add-on acquisitions in five years, and Merck KGaA agreed to buy Bio-Techne at an enterprise value of $11.3 billion, a 36% premium.'),[
 ['Sep 2026',L('StatLab',U['statlab']),'Danaher (Leica Biosystems)','Anatomic pathology consumables; about $250 million of 2025 revenue; undisclosed'],
 ['Sep 2026',L('Dallas Research Institute',U['summit']),'Summit Clinical Research, backed by LongueVue Capital','Metabolic disease research site; undisclosed'],
 ['Sep 2026',L('Worldwide Clinical Trials early-phase unit',U['ftre']),'Fortrea','$45 million for a 200-bed clinical pharmacology unit and laboratory in Texas'],
 ['Jun 2026',L('Bio-Techne',U['tech']),'Merck KGaA','Enterprise value of $11.3 billion; signed, closing expected by early 2027'],
 ['Jun 2026',L('Clinical Trials Research',U['head']),'Headlands Research, owned by THL','Two physician-led sites in California; undisclosed'],
 ['Jun 2026',L('Biocare Medical',U['mt10']),'Agilent','$950 million'],
 ['Mar 2026',L('Clario',U['clario']),'Thermo Fisher Scientific','$8.875 billion in cash plus deferred and contingent payments'],
 ['Feb 2026',L('Empire City Laboratories',U['lhec']),'Labcorp','Founder-owned clinical laboratory, select assets; $250.0 million of assets recorded'],
 ['Jan 2026',L('Catalyst Clinical Research',U['cat']),'Worldwide Clinical Trials','Oncology-focused research organization; about $500 million'],
 ['Jan 2026',L('Resolution Medical',U['mpo']),'Resonetics','Device design and manufacturing; undisclosed'],
 ['Dec 2025',L('Community Health Systems outreach laboratories',U['lhchs']),'Labcorp','About $194 million in cash for assets in 13 states'],
],
P(f'Contract development and manufacturing saw its own large trades, including Samsung Biologics\' $1.8 billion agreement for peptide manufacturer PolyPeptide and Lone Star Funds\' purchase of Lonza\'s capsules business, alongside new US capacity from Cambrex, PCI and Vetter ({L("DCAT Value Chain Insights",U["dcat"])}). Device design firms sold to manufacturers that want engineering in house, as the Resonetics and Currier purchases show, and NAMSA bought Labcorp\'s US medical device testing business in January ({L("Medical Product Outsourcing",U["mpo"])}).'),8)

# ---------- 09/10 med products ----------
add_ls_impl()
p9=EYE('Medical Products & Distribution')+H2('Procedure demand is firm and consumables are outgrowing capital equipment')+band([('9.0%','Stryker organic sales growth in the second quarter'),('$36.5B','Medtech deal value in the first half, after a decade-high 2025'),('41%','Health system executives who plan to cut capital spending in 2026')],'device','Line illustration of a patient monitor')+cols2(
PC(f'Device makers are reporting steady procedure volumes, with Stryker growing 9.0% organically in the second quarter ({L("Stryker",U["syk"])}), Medtronic raising its organic growth guidance to between 7.25% and 7.75% ({L("Medtronic",U["mdt"])}) and Zimmer Biomet growing 4.0% ({L("Zimmer Biomet",U["zbh"])}). Hospitals are spending more readily on consumables than on installed equipment, and Steris grew healthcare service revenue 10% and consumables 9% while capital equipment grew 1% ({L("Steris",U["ste"])}), and 41% of health system executives plan to cut capital spending ({L("HFMA",U["hfma"])}).')+
PC(f'The same preference for consumables shows in instrument reprocessing, where Aspen Surgical bought Ruhof Healthcare, a maker of instrument-cleaning detergents with about $50 million of revenue, in January ({L("Aspen Surgical",U["ruhof"])}).')+
quote('A wide variety of healthcare products and services create strong investor appeal due to their nondeferrable and recurring demand.', f'Harris Williams, {L("Outlook 2026: Healthcare & Life Sciences",U["hw"])}')+
PC(f'Dental results diverged between distributors and manufacturers, as Henry Schein grew dental merchandise distribution 9.7% ({L("Henry Schein",U["hsic"])}) and Envista grew 5% ({L("Envista via Pulse 2.0",U["nvst"])}), while Dentsply Sirona\'s sales fell 4.1% with the Americas down 10.7% ({L("Dentsply Sirona",U["xray"])}). Mitsui Chemicals agreed to buy Ultradent Products for $900 million ({L("Becker&#39;s Dental Review",U["ultra"])}).')+
PC(f'Several of the largest distribution businesses changed ownership in the past year. Medline raised $6.26 billion in its December initial public offering and grew net sales 11.6% in the second quarter ({L("Fierce Healthcare",U["mdlnipo"])}; {L("Medline",U["mdln"])}). Owens & Minor received $375 million in cash, a retained equity stake and a preferred return for its products and healthcare services segment ({L("Owens & Minor",U["omipr"])}), McKesson sold 13% of its medical-surgical unit for $1.25 billion ({L("McKesson",U["mck"])}) and Cardinal Health spent $360 million on two home supply businesses ({L("HME News",U["cahhme"])}).')+
PC(f'In respiratory and home equipment, Teleflex sold its acute care and urology businesses to Intersurgical for $530 million and its component unit to Montagu and Kohlberg for $1.5 billion ({L("MedTech Dive",U["tfx"])}), Viemed grew revenue 23.9% on home ventilation ({L("HME News",U["vmd"])}) and Medicare is restarting competitive bidding for home medical equipment with contracts from 2027 ({L("AAHomecare",U["cb"])}).')+
PC(f'Tariffs have moved earnings up as well as down. The Supreme Court struck down the emergency-powers tariffs in February and importers began receiving refunds in April ({L("Barnes Dennig",U["ieepa"])}), after which Medline booked a net benefit of $243 million and Stryker reversed $158 million of charges. The Section 232 investigation into medical devices remained open in September with no tariff imposed ({L("iData Research",U["dev232"])}), and the FDA\'s Quality Management System Regulation took effect on February 2 ({L("Ropes & Gray",U["qmsr"])}).'))
page('P09.dc.html','Medical Products & Distribution',p9,9)

txpage('P10.dc.html','Medical Products & Distribution transactions','Medical Products & Distribution: selected acquisitions and financings','Sponsors bought manufacturing platforms and strategics bought product lines',
P(f'KKR\'s agreement to take contract manufacturer Integer Holdings private values the company at $5.7 billion, a 51.8% premium, and Danaher paid about 18 times estimated 2027 EBITDA for Masimo. Divestitures supplied much of the remaining activity, and Bain & Company counts them as 34% of strategic medtech deal value in 2025 ({L("Bain & Company via Fierce Biotech","https://www.fiercebiotech.com/medtech/medtech-ma-rebounded-2025-softer-valuations-drive-competition-report")}).'),[
 ['Sep 2026',L('Numotion',U['numo']),'Hanger, owned by Patient Square Capital','Complex rehabilitation equipment; undisclosed; closing expected in the fourth quarter'],
 ['Aug 2026',L('Integer Holdings',U['itgr']),'KKR','Enterprise value of $5.7 billion; $127 a share'],
 ['Jul 2026',L('AdaptHealth diabetes business and Strive Medical',U['cahhme']),'Cardinal Health','$360 million combined'],
 ['Jun 2026',L('Ultradent Products',U['ultra']),'Mitsui Chemicals','Dental consumables; $900 million'],
 ['Jun 2026',L('Masimo',U['masi']),'Danaher','Enterprise value of about $9.9 billion; 18x estimated 2027 EBITDA'],
 ['Jun 2026',L('McKesson Medical-Surgical, 13% interest',U['mck']),'Apollo','$1.25 billion'],
 ['May 2026',L('Amplitude Vascular Systems',U['mt10']),'Stryker','$435 million plus up to $400 million in milestones'],
 ['Mar 2026',L('Apex Dental Laboratory Group',U['apex']),'Private equity investors','16 dental laboratories in 12 states; undisclosed'],
 ['Jan 2026',L('Ruhof Healthcare',U['ruhof']),'Aspen Surgical','Instrument reprocessing chemistries; about $50 million of revenue; undisclosed'],
 ['Dec 2025',L('Medline',U['mdlnipo']),'Initial public offering','$6.26 billion raised at a valuation above $38 billion'],
 ['Dec 2025',L('Owens & Minor Products & Healthcare Services',U['omi']),'Platinum Equity','$375 million in cash, a 5% retained equity interest and a preferred return'],
 ['Dec 2025',L('Teleflex acute care and urology; component unit',U['tfx']),'Intersurgical; Montagu and Kohlberg','$530 million; $1.5 billion'],
],
P(f'Owens & Minor\'s announced terms combined $375 million of cash with a 5% retained equity interest and a preferred return, and the company also kept specified tax assets, so the cash figure alone understates what the seller received ({L("Owens & Minor",U["omipr"])}). Comparing distribution with manufacturing valuations requires the full consideration, the scope acquired and comparable earnings. Buyers of product companies will examine clearances, quality records, customer qualification and the exposure of the bill of materials to tariffs.'),10)

# ---------- 11/12 pharmacy ----------
add_mp_impl()
p11=EYE('Pharmacy & Healthcare Services')+H2('Drug pricing reform is reshaping pharmacy while staffing returns to growth')+band([('$606B','US net medicine spending in 2025, up 10.6%'),('$39.0B','Forecast US healthcare staffing revenue in 2026'),('$250M','Sale price of Omnicare, which CVS bought for about $13 billion in 2015')],'pharmacy','Line illustration of a medicine bottle and a capsule')+cols2(
PC(f'Medicine spending is growing quickly while pharmacy margins shrink. Net spending reached $606 billion in 2025, up 10.6%, with GLP-1 and obesity drugs adding $14 billion ({L("IQVIA Institute",U["iqvm"])}). Independent pharmacies numbered 18,960 in mid-2025 and reported their lowest gross profit in ten years ({L("NCPA Digest",U["ncpa"])}), and 67% of owners surveyed report waiting 22 days or more for manufacturer refunds on drugs with negotiated Medicare prices ({L("Drug Topics",U["ncpas"])}).')+
PC(f'Negotiated Medicare prices have cut deepest in long-term care pharmacy, where Guardian Pharmacy Services grew revenue 2% while serving 8% more residents, and its chief executive said first-half revenue would have grown at a low double-digit rate without the price reductions ({L("Guardian Pharmacy Services",U["grdn"])}; {L("call summary",U["grdnc"])}). BrightSpring attributed about $50 million of second-quarter pressure in its home and community pharmacy unit to the same cause ({L("BrightSpring call summary",U["btsgc"])}), and a bankruptcy court approved the sale of Omnicare to GenieRx for $250 million in cash ({L("CVS Health",U["omni"])}; {L("Becker&#39;s Hospital Review",U["omnib"])}).')+
PC(f'Specialty pharmacy and infusion are growing fastest. BrightSpring\'s specialty and infusion revenue rose 30% to $2.9 billion ({L("BrightSpring",U["btsg"])}), and Option Care Health reported high-single-digit growth in acute therapies and named tuck-in acquisitions as a priority ({L("Option Care Health",U["opch"])}; {L("call summary",U["opchc"])}). Neither of the bills to create a full Medicare home infusion benefit has been enacted ({L("RxToolKit",U["nhia"])}).')+
PC(f'Congress enacted pharmacy benefit manager reform in February, under which Part D compensation must be delinked from list prices from 2028 and rebates passed through in full to employer plans from 2029 ({L("Sidley Austin",U["pbm"])}), and all three large managers have settled the FTC\'s insulin case on terms that include cost-plus pharmacy reimbursement ({L("Truveris",U["ftcins"])}). State laws barring managers from owning pharmacies remain in litigation ({L("Mintz",U["mintz"])}).')+
PC(f'Drug distributors continue to buy physician practice management organizations. Cencora completed its purchase of OneOncology in February ({L("Cencora",U["cor"])}), and The Specialty Alliance, which Cardinal Health controls, acquired Solaris Health for about $1.9 billion in cash in November 2025, leaving Cardinal with about 76% of the alliance after closing ({L("Cardinal Health Form 10-K",U["cah10k"])}). McKesson grew oncology and multispecialty revenue 33% ({L("McKesson",U["mck"])}).')+
PC(f'Healthcare staffing is growing again after three years of contraction, and Staffing Industry Analysts forecasts 1% growth to $39.0 billion in 2026 and 3% in 2027, led by locum tenens at 4% ({L("Staffing Industry Analysts",U["sia"])}). AMN Healthcare grew nurse and allied revenue 11% ({L("AMN Healthcare",U["amn"])}), and health care and social assistance had 1,359,000 open positions in August ({L("Bureau of Labor Statistics JOLTS",U["jolts"])}).'))
page('P11.dc.html','Pharmacy & Healthcare Services',p11,11)

txpage('P12.dc.html','Pharmacy & Healthcare Services transactions','Pharmacy & Healthcare Services: announced transactions','Scale mergers met resistance and buyers turned to specialist tuck-ins',
P(f'Aya Healthcare ended its agreement to buy Cross Country Healthcare in December 2025 after an extended FTC review ({L("Staffing Industry Analysts",U["aya"])}), and Knox Lane completed a $437 million purchase of the company in July at $13.25 a share against the $18.61 Aya had offered ({L("Fierce Healthcare",U["knoxf"])}). Purchases of smaller specialist firms in pharmacy, infusion, perfusion and locum tenens closed throughout the year.'),[
 ['Sep 2026',L('Nautilus Pharmacy',U['grdnn']),'Guardian Pharmacy Services','Tennessee pharmacy assets serving 14 states; undisclosed'],
 ['Aug 2026',L('Life Couriers',U['jll']),'JLL Partners','Radiopharmaceutical and time-critical healthcare logistics; undisclosed'],
 ['Jul 2026',L('Cross Country Healthcare',U['knox']),'Knox Lane','$437 million; nurse, allied and locum tenens staffing'],
 ['Jul 2026',L('Wellness Concepts',U['grdn']),'Guardian Pharmacy Services','Long-term care pharmacy, Virginia; undisclosed'],
 ['Jun 2026',L('Quest Locum Tenens and Syncx',U['velo']),'VeloSource, backed by Interlock Equity','Locum tenens staffing and workforce software; undisclosed'],
 ['Jun 2026',L('BluHaven Management and Realo Specialty Care Pharmacy',U['pespjn']),'Soleo Health','Infusion and specialty pharmacy; undisclosed'],
 ['May 2026',L('Omnicare',U['omni']),'GenieRx Holdings','$250 million in cash through a bankruptcy sale; long-term care pharmacy in 47 states'],
 ['Apr 2026',L('Ohio Valley Perfusion Associates',U['strata']),'Strata Critical Medical','About $1 million; a mid-single-digit EBITDA multiple'],
 ['Feb 2026',L('OneOncology',U['cor']),'Cencora','Oncology practice management; completed'],
 ['Feb 2026',L('IDR Healthcare',U['idr']),'Care Career','Travel nurse, allied and school staffing; the buyer\'s sixth purchase in 18 months'],
 ['Jan 2026',L('Focus Staff',U['focus']),'Elite365','Travel nurse and allied staffing, Dallas; undisclosed'],
],
P(f'Buyers in this focus area say they pay for contracted, recurring revenue and for spare capacity they can fill. Strata Critical Medical cited recurring revenue, multi-year contracts and high customer retention in perfusion services, and Guardian describes pharmacy acquisitions as a way to use the capacity of its existing pharmacies. Staffing Industry Analysts counted 23 healthcare staffing transactions in 2025 against 17 in 2019, with buyers favoring diversified workforce platforms ({L("Staffing Industry Analysts",U["snap"])}). Travel nurse gross margin of 19.9% in 2025 remains below the roughly 25% earned before the pandemic ({L("Staffing Industry Analysts",U["sia"])}).'),12)

add_ph_impl()
# ---------- 13 valuation ----------
SA='https://stockanalysis.com/stocks/%s/statistics/'
grp=[('Provider Services',[('HCA Healthcare','hca',9.07),('Tenet Healthcare','thc',6.59),('U.S. Physical Therapy','usph',15.77),('DaVita','dva',8.53),('Addus HomeCare','adus',12.65),('Pennant Group','pntg',25.44),('Acadia Healthcare','achc',9.40),('LifeStance Health','lfst',36.12),('Privia Health','prva',38.68),('Concentra','con',14.06),('Ensign Group','ensg',20.35)]),
 ('Life Sciences & Diagnostics',[('Labcorp','lh',13.65),('Quest Diagnostics','dgx',13.81),('Thermo Fisher','tmo',24.27),('Danaher','dhr',21.67),('Bio-Techne','tech',34.05),('IQVIA','iqv',18.71),('Medpace','medp',27.48),('ICON','iclr',28.85),('Charles River','crl',19.66)]),
 ('Medical Products & Distribution',[('Stryker','syk',16.31),('Steris','ste',13.35),('Teleflex','tfx',19.49),('Henry Schein','hsic',12.14),('Dentsply Sirona','xray',7.53),('Envista','nvst',10.41),('Zimmer Biomet','zbh',9.50),('Integer Holdings','itgr',16.23),('Solventum','solv',17.42),('Viemed Healthcare','vmd',6.25)]),
 ('Pharmacy & Healthcare Services',[('Option Care Health','opch',11.02),('BrightSpring','btsg',22.96),('Guardian Pharmacy','grdn',23.09),('McKesson','mck',15.82),('Cencora','cor',12.73),('Cardinal Health','cah',13.67),('CVS Health','cvs',10.41),('AMN Healthcare','amn',5.74)])]
X0=200; PX=12.5
ch=[f'<div style="position: relative; width: 720px; height: 292px; font-size: 11.5px; line-height: 16px; letter-spacing: 0.2px">']
for v in (0,10,20,30,40):
    x=X0+v*PX
    ch.append(f'<div style="position: absolute; left: {x:.0f}px; top: 44px; width: 1px; height: 220px; background: #E3DED6"></div><div style="position: absolute; left: {x-20:.0f}px; top: 270px; width: 40px; text-align: center">{v}x</div>')
xm=X0+7.0*PX
ch.append(f'<div style="position: absolute; left: {xm:.0f}px; top: 26px; width: 0; height: 238px; border-left: 1px dashed #6D7681"></div><div style="position: absolute; left: {xm-10:.0f}px; top: 4px; width: 300px; font-weight: 600">Private mid-market average, all industries, 7.0x</div>')
MED={}
for i,(name,cs) in enumerate(grp):
    y=70+i*52; vals=[c[2] for c in cs]; med=statistics.median(vals); MED[name]=(med,min(vals),max(vals),len(vals))
    ch.append(f'<div style="position: absolute; left: 0; top: {y}px; width: 190px; font-weight: 600">{name}</div>')
    ch.append(f'<div style="position: absolute; left: {X0+min(vals)*PX:.0f}px; top: {y+7}px; width: {(max(vals)-min(vals))*PX:.0f}px; height: 2px; background: #D2CDC4"></div>')
    for v in vals: ch.append(f'<div style="position: absolute; left: {X0+v*PX-5:.0f}px; top: {y+3}px; width: 10px; height: 10px; border-radius: 50%; background: #9B958B"></div>')
    xm2=X0+med*PX
    ch.append(f'<div style="position: absolute; left: {xm2-2:.0f}px; top: {y-5}px; width: 4px; height: 26px; background: #B68757"></div><div style="position: absolute; left: {xm2-30:.0f}px; top: {y-23}px; width: 60px; text-align: center; font-weight: 700">{med:.1f}x</div>')
ch.append('</div>')
if WEB: ch=['@@CHART@@']
m=MED
lst=''.join(f'<div style="break-inside: avoid; margin: 0 0 7px"><span style="font-weight: 700">{name}:</span> '+'; '.join(f'{L(c[0],SA%c[1])} {c[2]:.1f}x' for c in cs)+'</div>' for name,cs in grp)
p13=EYE('Public-market valuation reference')+H2('Public multiples show relative standing, and private prices are set business by business')+f'<figure style="margin: 0; display: flex; flex-direction: column; gap: 6px"><div style="font-size: 11px; line-height: 15px; letter-spacing: 0.3px">Enterprise value to trailing twelve-month EBITDA, listed companies by focus area; each dot is one company and the gold bar marks the median</div>{"".join(ch)}</figure>'+P(f'These are enterprise values of public companies relative to reported trailing EBITDA. Differences in sub-sector, size, growth, earnings adjustments and business mix mean the chart cannot be discounted directly to a founder-owned company. The 13.6x median that private equity paid for healthcare services companies in 2025 ({L("PitchBook via Becker&#39;s ASC Review",U["pbasc"])}), the 7.0x all-industry average for the second quarter of 2026 ({L("GF Data via ACG",U["gf"])}) and the 5.8x median for transactions of $5 million to $50 million ({L("IBBA and M&A Source Market Pulse",U["ibba"])}) each describe a different sample and period, so they serve as separate reference points. {XREF('X-bridge','Page','The','valuation','valuation bridge',cap=True)} sets out how public trading, strategic control transactions, sponsor platforms and private add-ons relate to the value of a private company.')+f'<div style="column-count: 2; column-gap: 32px; font-size: 11.5px; line-height: 17px; letter-spacing: 0.2px">{lst}</div>'+f'<div style="font-size: 10.5px; line-height: 15px; letter-spacing: 0.2px">Multiples are enterprise value to trailing EBITDA as published by StockAnalysis and retrieved on October 5, 2026; they use reported EBITDA, which is lower than the adjusted EBITDA companies present, and an unusually low EBITDA can inflate a ratio. Select Medical, Cross Country Healthcare and NeoGenomics are excluded because the first two were acquired during 2026 and the third has minimal trailing EBITDA.</div>'
page('P13.dc.html','Public-market valuation',p13,13)
add_bridge()

# ---------- 14 benchmark ----------
cb='170px 150px 1fr 128px'
p14=H2('Benchmark International\'s activity in these focus areas')+P('Benchmark International has closed 12 transactions in these four focus areas over the trailing 24 months and is working on 39 further engagements as of October 1, 2026. Pharmacy and healthcare services is the largest group among the closed transactions, with five, followed by life sciences and diagnostics with four. Provider services leads the live engagements with 19, of which ten are in preparation for market. Across all four, 20 engagements are on the market, 13 are in preparation, four are in legal documentation and two are in discussion with a buyer.')+P('Among the nine announced transactions listed below, six went to operating companies, one to a private equity firm and one to a group of private investors, and in one the buyer is undisclosed.')+table(cb,['Seller (linked)','Buyer as announced','What the seller does','Focus area'],[
 [L('Precise Bioscience',T['precise']),'New Horizon Medical Solutions','Amniotic membrane allografts for wound care and sports medicine, Durham, North Carolina','Life Sciences & Diagnostics'],
 [L('Formulation Technology',T['form']),'AAVIN Private Equity','Contract manufacturer of nutritional supplements, Oakdale, California','Life Sciences & Diagnostics'],
 [L('Fast Response On-Site Testing',T['frost']),'Relentless Health','Mobile occupational health testing, Santa Cruz, California','Life Sciences & Diagnostics'],
 [L('Critical Environments Professionals, certification division',T['cepro']),'Scientific Safety Alliance','Certification testing for pharmacy compounding spaces, laboratories and bio-containment facilities','Life Sciences & Diagnostics'],
 [L('Dental Holdings',T['dental']),'Solmetex','Patent holder and brand owner of ReLeaf hands-free dental suction devices','Medical Products & Distribution'],
 [L('FosterBridge',T['foster']),'Amivie','In-home care for Ohio Medicaid waiver participants','Provider Services'],
 [L('Medical Temps',T['medtemps']),'Health Advocates Network','Nurse staffing for healthcare facilities in northern Louisiana','Pharmacy & Healthcare Services'],
 [L('The Brooks Group and Associates',T['brooks']),'A group of private investors','Training, research and instructional design for pharmaceutical, biotech and device companies, West Chester, Pennsylvania','Pharmacy & Healthcare Services'],
 ['Fitzgerald Enterprises','An undisclosed buyer','Healthcare executive and clinical placement','Pharmacy & Healthcare Services'],
])
page('P14.dc.html','Benchmark International activity',p14,14)

# ---------- 15 buyers ----------
p15=H2('What buyers reward and what they discount')+P('Across the four focus areas, acquirers pay the most for revenue that recurs under contract or clinical necessity and that is paid by a balanced mix of payers, and they discount revenue that depends on one reimbursement rate, one referral source or the owner personally. The specifics differ by focus area, and an owner or advisor can test a business against them well before a sale.')+table('124px 1fr 1fr',['Focus area','Buyers reward','Buyers discount'],[
 ['Provider Services','In-network commercial revenue and a balanced payer mix; dense local footprints; clinicians who stay, often with retained equity; clean billing and coding records; capacity to open new sites','Heavy dependence on one Medicaid program or one fee schedule; referral concentration; restrictive covenants that state law no longer enforces; structures that need restructuring under new state ownership rules'],
 ['Life Sciences & Diagnostics','Recurring consumables and reagents; accreditation and certification scope; hospital and physician relationships that route test volume; sponsor and research organization repeat business; US manufacturing capacity','Revenue tied to one Medicare payment code; dependence on one grant-funded customer group; a single sponsor or study; capacity that needs reinvestment'],
 ['Medical Products & Distribution','Patents and regulatory clearances; consumables sold on a recurring basis; clinical relationships and brand preference; quality system records ready for inspection','Tariff-exposed supply chains without alternatives; commodity distribution without exclusive lines; pricing set by one purchasing group; capital equipment sold into shrinking hospital budgets'],
 ['Pharmacy & Healthcare Services','Specialty and infusion therapies with limited distribution access; multi-year facility contracts; high customer retention; credentialed clinicians in specialist roles such as perfusion and locum tenens','Brand drug volume subject to negotiated prices; legal exposure in billing practices; commodity per diem staffing; revenue that depends on strike or crisis demand'],
],pad=7)+f'<div style="margin-top: 10px; display: flex; gap: 32px"><div style="width: 408px; display: flex; flex-direction: column; gap: 14px; text-align: justify">'+P(f'In the second quarter of 2026, 87% of surveyed transactions above $5 million received at least three offers, and lower-middle-market sales took about 11 to 12 months to close ({L("IBBA and M&A Source Market Pulse",U["ibbar"])}). That survey covers all industries, and a healthcare sale can also require state notices or approvals, payer consents, enrollment actions and a billing and coding review, depending on structure and jurisdiction. Owners who prepare financial, concentration, license, accreditation and management evidence before approaching buyers shorten that path.')+f'</div><div style="width: 280px; position: relative"><img src="{CHECK}" alt="Line illustration of a checklist on a clipboard under a magnifying glass" style="position: absolute; left: 0; top: 4px; width: 280px; height: calc(100% - 22px); object-fit: cover"><div style="position: absolute; left: 0; bottom: 0; width: 280px; height: 18px; background: #B68757"></div></div></div>'
page('P15.dc.html','What buyers reward and discount',p15,15)
add_ready()

# ---------- sources (auto-collected) ----------
def links(html):
    seen=[]; out=[]
    for u,t in re.findall(r'<a href="([^"]+)">(.*?)</a>', html):
        if u not in seen: seen.append(u); out.append((t,u))
    return out
bodies={fn:b for fn,_,b in pages}
def srcblock(title, fns, skip=('stockanalysis.com','benchmarkintl.com')):
    ls=[]; seen=set()
    for fn in fns:
        for t,u in links(bodies[fn]):
            if any(s in u for s in skip) or u in seen: continue
            seen.add(u); ls.append(L(t,u))
    if WEB: return f'<h4>{title}</h4><ul>'+''.join(f'<li>{x}</li>' for x in ls)+'</ul>'
    return f'<div style="margin: 0 0 6px; font-weight: 700; font-size: 9.5px; line-height: 14px; letter-spacing: 1.6px; text-transform: uppercase; break-after: avoid">{title}</div><p style="margin: 0 0 14px">'+'; '.join(ls)+'</p>'
SS='column-count: 2; column-gap: 32px; font-size: 10.5px; line-height: 15px; letter-spacing: 0.15px; text-align: left'
s1=H2('Sources')+f'<div style="{SS}">'+srcblock('Deal market, demand, policy and regulation',['P02.dc.html','P03.dc.html','P04.dc.html','X-policy'])+srcblock('Provider Services',['P05.dc.html','P06.dc.html','X-prov'])+'</div>'

s2=srcblock('Life Sciences & Diagnostics',['P07.dc.html','P08.dc.html','X-ls'])+srcblock('Medical Products & Distribution',['P09.dc.html','P10.dc.html','X-mp'])+srcblock('Pharmacy & Healthcare Services',['P11.dc.html','P12.dc.html','X-ph'])+srcblock('Valuation and seller preparation',['P13.dc.html','P15.dc.html'])+f'<div style="margin: 0 0 6px; font-weight: 700; font-size: 9.5px; line-height: 14px; letter-spacing: 1.6px; text-transform: uppercase; break-after: avoid">Benchmark International</div><p style="margin: 0 0 14px">Transaction records and the engagement portfolio as of October 1, 2026; announced transactions as published at '+L('benchmarkintl.com/insights','https://www.benchmarkintl.com/insights/completed-transactions/')+' and linked in the table '+XREF('P14.dc.html','on page','under','benchmark','Benchmark International activity')+'; listed-company multiples from '+L('StockAnalysis','https://stockanalysis.com/')+', each linked '+XREF('P13.dc.html','on page','under','valuation','Valuation')+'</p></div>'
s1=s1[:-6]+s2
SRC=s1

# ---------- 18 paywall + back ----------
pw=[('PitchBook','Deal-level multiples and sponsor holdings by healthcare sub-sector; the full Healthcare Services Report data','https://pitchbook.com'),
('LevinPro HC (Levin Associates)','Quarterly healthcare deal counts with prices by sector, including physician groups, home health and laboratories','https://healthcare.levinassociates.com'),
('GF Data','Middle-market multiples and leverage by size tier, with a healthcare services cut','https://gfdata.com'),
('S&P Capital IQ, Mergermarket, LSEG and Dealogic','Transaction records, comparable company data and league tables','https://www.spglobal.com/marketintelligence'),
('Bain Global Healthcare Private Equity Report (full)','Multiples and sector charts behind the 2025 totals','https://www.bain.com'),
('KPMG Healthcare and Life Sciences Investment Outlook 2026','Investor survey and sub-sector outlooks (registration required)','https://kpmg.com/kpmg-us/content/dam/kpmg/pdf/gated/2026/hcls-investment-outlook-2026.pdf'),
('Health Affairs','Year-by-year tables for the CMS national health expenditure projections','https://www.healthaffairs.org'),
('Axios Pro, PE Hub, Modern Healthcare, STAT+ and Bloomberg','Sale-process reporting, sponsor pricing and financing detail','https://www.axios.com/pro'),
('GenomeWeb, 360Dx, Laboratory Economics, The Dark Report and G2 Intelligence','Laboratory transaction pricing and Medicare laboratory payment coverage','https://www.360dx.com'),
('Evaluate and IQVIA commercial data','Drug pipeline, sales and prescription data; the IQVIA Institute reports are free with registration','https://www.evaluate.com'),
('Staffing Industry Analysts research','Healthcare staffing segment sizes, bill rates and the largest-firm rankings','https://www.staffingindustry.com'),
('NHIA Infusion Industry Trends 2026','Home and alternate-site infusion market size, patients and providers by therapy','https://nhia.org/nhia-releases-infusion-industry-trends-report/'),
('Drug Channels Institute','Annual pharmacy and pharmacy benefit manager report, including specialty share and pharmacy rankings','https://www.drugchannels.net'),
('ORTHOWORLD, Vision Monday and HME News data partners','Orthopedic deal data, optometry consolidation surveys and home medical equipment deal counts','https://www.orthoworld.com'),
('Earnings call transcripts (AlphaSense, Seeking Alpha)','Management commentary on acquisition criteria and pipelines','https://www.alpha-sense.com')]
pwl=''.join(f'<p style="margin: 0 0 6px; break-inside: avoid"><span style="font-weight: 700">{L(a,u)}:</span> {b}</p>' for a,b,u in pw)
back=f'''<img src="{KNOT}" alt="" style="position: absolute; left: 310px; top: 600px; width: 506px; height: 718px; opacity: 0.3">
<div style="position: absolute; left: 0; top: 40px; width: 432px; height: 1px; background: #6D7681"></div>
<div style="position: absolute; right: 48px; top: 30px; {CINZEL}; font-size: 12px; line-height: 20px; letter-spacing: 0.8px; color: #6D7681">{RUN}</div>
<div data-fit="560" style="position: absolute; left: 48px; top: 230px; width: 720px; display: flex; flex-direction: column; gap: 22px">
{EYE('Benchmark International Mid-Market')}
{H2('Considering a transaction in healthcare?')}
{P('Our first step is always a confidential conversation exploring your goals, your company and your options.')}
<div style="margin-top: 10px; display: flex; gap: 32px; align-items: center">
<div style="width: 344px; display: flex; flex-direction: column">
<img src="{SIGN}" alt="Line illustration of a signed agreement with a pen and a seal" style="display: block; width: 344px; height: 178px">
<div style="height: 18px; background: #B68757"></div>
</div>
<div style="width: 344px; display: flex; align-items: center; gap: 20px">
<img src="{HEAD}" alt="Jared Hardin" style="display: block; width: 84px; height: 84px; border-radius: 50%">
<div style="display: flex; flex-direction: column; gap: 2px">
<div style="font-weight: 700; font-size: 12px; line-height: 20px; letter-spacing: 2.6px">JARED HARDIN</div>
<div>Managing Director</div>
<div>Benchmark International</div>
<div>813-771-6675</div>
<div>j.hardin@benchmarkintl.com</div>
</div>
</div>
</div>
</div>
<div style="position: absolute; left: 0; top: 839px; width: 816px; height: 217px; background: #303030; color: #FFFFFF">
<div style="position: absolute; left: 0; top: 26px; width: 816px; text-align: center; font-weight: 700; font-size: 10px; line-height: 14px; letter-spacing: 4px; color: #B68757">HEADQUARTERS</div>
<div style="position: absolute; left: 48px; top: 52px; width: 720px; height: 1px; background: #B68757"></div>
<div style="position: absolute; left: 48px; top: 70px; width: 720px; display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 24px; text-align: center; font-size: 9.5px; line-height: 16px; letter-spacing: 0.5px">
<div style="display: flex; flex-direction: column; align-items: center"><div style="{CINZEL}; font-size: 23px; line-height: 34px; letter-spacing: 4px; margin-bottom: 6px">AMERICAS</div><div>4030 West Boy Scout Blvd.</div><div>Suite 500, Tampa, FL 33607</div><div>+1 813 898 2350</div><a href="mailto:US@BENCHMARKINTL.COM" style="margin-top: 4px; color: #C99A68; font-weight: 700; font-size: 8.5px; letter-spacing: 2px">US@BENCHMARKINTL.COM</a></div>
<div style="display: flex; flex-direction: column; align-items: center"><div style="{CINZEL}; font-size: 23px; line-height: 34px; letter-spacing: 4px; margin-bottom: 6px">EUROPE</div><div>One New Bailey, 4 Stanley St.</div><div>Manchester, M3 5JL</div><div>+44 (0) 161 359 4400</div><a href="mailto:UK@BENCHMARKINTL.COM" style="margin-top: 4px; color: #C99A68; font-weight: 700; font-size: 8.5px; letter-spacing: 2px">UK@BENCHMARKINTL.COM</a></div>
<div style="display: flex; flex-direction: column; align-items: center"><div style="{CINZEL}; font-size: 23px; line-height: 34px; letter-spacing: 4px; margin-bottom: 6px">AFRICA</div><div>Airport Office Park, Freight Rd., Ground Floor</div><div>Runway 01, Cape Town Airport, 7525</div><div>+27 (0) 21 300 2055</div><a href="mailto:AFRICA@BENCHMARKINTL.COM" style="margin-top: 4px; color: #C99A68; font-weight: 700; font-size: 8.5px; letter-spacing: 2px">AFRICA@BENCHMARKINTL.COM</a></div>
</div>
</div>'''
pages.append(('P16.dc.html','Contact',back))
PN={fn:i+1 for i,(fn,_,_) in enumerate(pages)}
prim=('<h4>Primary references</h4><ul>'+''.join(f'<li>{L(t,U[k])}</li>' for t,k in PRIMARY)+'</ul>') if WEB else '<div style="margin: 0 0 6px; font-weight: 700; font-size: 9.5px; line-height: 14px; letter-spacing: 1.6px; text-transform: uppercase; break-after: avoid">Primary references</div><p style="margin: 0 0 14px">'+'; '.join(L(t,U[k]) for t,k in PRIMARY)+'</p>'
SRC=SRC[:-6]+prim+'</div>'
page('P17.dc.html','Sources',SRC,17)

ONEP='''<div data-fit="738" style="position: absolute; left: 48px; top: 76px; width: 720px; height: 738px; display: flex; flex-direction: column; gap: 12px">
{H2('Subscription and gated sources for further research')}
{P('The sources below sit behind a subscription, a membership or a registration form and were not used for any figure in this report. Each would add depth on the points noted.',extra='; font-size: 11.5px; line-height: 17px')}
<div style="column-count: 2; column-gap: 32px; font-size: 11px; line-height: 16px; letter-spacing: 0.15px">{pwl}</div>
'''
# ---------- emit ----------
# web.py runs everything above this line with WEB set and stops here.
FONT='<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500&amp;family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,500;1,6..72,600&amp;family=Quicksand:wght@400;500;600;700&amp;display=swap" rel="stylesheet">'
CSS='body{margin:0}\na{color:#8C6239;text-decoration-thickness:.5px;text-underline-offset:2px}a:hover{color:#5E4126}'
ROOTSTYLE="position: relative; width: 816px; height: 1056px; box-sizing: border-box; overflow: hidden; background: #FFFFFF; font-family: 'Quicksand', 'Avenir Next', 'Segoe UI', sans-serif; font-size: 12.5px; line-height: 21px; letter-spacing: 0.4px; color: #333333"
boards={}; order=[]; prev=[]
PN={fn:i+1 for i,(fn,_,_) in enumerate(pages)}
for i,(fid,title,body) in enumerate(pages):
    fn='Main.dc.html' if i==0 else f'P{i+1:02d}.dc.html'
    body=body.replace('@@PN@@',f'{i+1:02d}')
    body=re.sub(r'@@PG:([\w.-]+)@@',lambda m:str(PN[m.group(1)]),body)
    body=esc(body)
    doc=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Healthcare Q4 2026: {esc(title)}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONT}
<style>
{CSS}
</style>
</helmet>
<div style="{ROOTSTYLE}">
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":816,"height":1056}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''
    open(os.path.join(OUT,fn),'w').write(doc)
    boards[fn]={"x":(i%6)*896,"y":(i//6)*1176,"w":816,"h":1056,"title":f"{i+1:02d} {title}"}; order.append(fn)
    prev.append(f'<div class="pg" data-fn="{fn}" style="{ROOTSTYLE}; page-break-after: always">{body}</div>')
idx={"v":3,"createdOnFiles":{"v":1,"at":"2026-10-05T20:40:00Z"},"title":"Healthcare Q4 2026 M&A Sector Report","launch":{"view":"canvas"},"pages":[],"boards":boards,"order":order,"notes":{},"designSystems":[]}
json.dump(idx,open(os.path.join(OUT,'canvas.json'),'w'),indent=1)
loc={COVER:'art/cover.svg',ICON['clinic']:'art/clinic.svg',ICON['lab']:'art/lab.svg',ICON['device']:'art/device.svg',ICON['pharmacy']:'art/pharmacy.svg'}
h='\n'.join(prev)
for k,v in loc.items(): h=h.replace(k,v)
open(os.path.join(ROOT,'preview.html'),'w').write(f'<!doctype html><html><head><meta charset="utf-8">{FONT.replace("&amp;","&")}<style>{CSS}@page{{size:8.5in 11in;margin:0}}</style></head><body>{h}</body></html>')
print(len(pages),'pages', {k:round(v[0],2) for k,v in MED.items()})

# ---------- separate one-pager ----------
K2='/_blob/bd5fc1f3255afc83b150bac424fabe40'
one=eval('f"""'+ONEP.replace('data-fit="738"','data-fit="890"').replace('height: 738px','height: 890px')+'</div>"""')
one=one.replace('were not used for any figure in this report','were not used for any figure in the Healthcare Q4 2026 M&A Sector Report')
body=f'''<img src="{K2}" alt="" style="position: absolute; left: 310px; top: 600px; width: 506px; height: 718px; opacity: 0.3">
<div style="position: absolute; left: 0; top: 40px; width: 432px; height: 1px; background: #6D7681"></div>
<div style="position: absolute; right: 48px; top: 30px; {CINZEL}; font-size: 12px; line-height: 20px; letter-spacing: 0.8px; color: #6D7681">{RUN}</div>
{one}
<div style="position: absolute; left: 0; bottom: 38px; width: 816px; text-align: center; font-weight: 700; font-size: 8.5px; line-height: 12px; letter-spacing: 3.6px">BENCHMARKINTL.COM</div>'''
body=esc(body)
O2=os.path.join(ROOT,'root2','project'); os.makedirs(O2,exist_ok=True)
doc=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Healthcare Q4 2026: Subscription and gated sources</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONT}
<style>
{CSS}
</style>
</helmet>
<div style="{ROOTSTYLE}">
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":816,"height":1056}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''
open(os.path.join(O2,'Main.dc.html'),'w').write(doc)
json.dump({"v":3,"createdOnFiles":{"v":1,"at":"2026-10-05T21:05:00Z"},"title":"Healthcare Q4 2026 Subscription Sources","launch":{"view":"focused","file":"Main.dc.html"},"pages":[],"boards":{"Main.dc.html":{"x":0,"y":0,"w":816,"h":1056,"title":"Subscription and gated sources"}},"order":["Main.dc.html"],"notes":{},"designSystems":[]},open(os.path.join(O2,'canvas.json'),'w'),indent=1)
open(os.path.join(ROOT,'preview.html'),'a').write(f'<div class="pg" data-fn="ONEPAGER" style="{ROOTSTYLE}">{body}</div>')
