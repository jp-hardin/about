import lib
from lib import *

# ---------------- shared source URLs ----------------
GARTNER = 'https://www.gartner.com/en/newsroom/press-releases/2026-07-27-gartner-forecasts-worldwide-it-spending-to-grow-14-point-2-percent-in-2026-totaling-6-point-37-trillion'
OMDIA_MA = 'https://omdia.tech.informa.com/om145542/global-msp-ma-1q26'
CHDIVE_MA = 'https://www.channeldive.com/news/channel-acquistions-consolidation-managed-services-omdia/828297/'
GFDATA = 'https://www.acg.org/news-trends/news/gf-data-reports-show-steady-middle-market-deal-flow-amid-more-selective'
IBBA = 'https://www.ibba.org/wp-content/uploads/2026/08/mp-highlights-q2-2026.pdf'
IBBA_PR = 'https://www.webull.com/news/15462423712777216'
PITCHBOOK = 'https://pitchbook.brightspotcdn.com/40/42/bbeb88094080abaea3d7c87530b8/q2-2026-us-pe-breakdown.pdf'
FED = 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm'
TREASURY = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202610'
REUTERS_Q3 = 'https://www.globalbankingandfinance.com/global-m-deal-rush-fades-third-quarter-rising-borrowing/'
REUTERS_H1 = 'https://wdez.com/?p=962887'
SYNERGY = 'https://www.srgresearch.com/articles/q2-cloud-market-passes-143-billion-highest-growth-rate-in-eight-years'
AMZN = 'https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Second-Quarter-Results'
MSFT = 'https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast'
ISG = 'https://www.businesswire.com/news/home/20260714306199/en/Driven-by-AI-Americas-Tech-Services-Demand-Accelerates-in-Q2-to-New-High-ISG-Index'
DELLORO = 'https://www.delloro.com/news/ai-infrastructure-buildouts-and-memory-cost-inflation-drove-data-center-capex-higher-in-1q-2026/'
PLATFORMONOMICS = 'https://platformonomics.com/2026/07/follow-the-capex-q2-2026-scoreboard/'
SLI = 'https://www.connectwise.com/company/press/releases/service-leadership-report-reveals-historic-growth-for-it-solution-providers-and-the-operational-factors-defining-this-economic-shift'
KASEYA = 'https://www.kaseya.com/wp-content/uploads/dlm_uploads/2026/04/Kaseya_2026-State-of-the-MSP_report_2026.pdf'
OMDIA_20 = 'https://omdia.tech.informa.com/blogs/2026/sep/msp-spotlight-the-20-msp-a-founder-led-roll-up-with-pre-aligned-acquisition-engine'
HL_IT = 'https://cdn.hl.com/pdf/2025/it-services-december-2025-market-update.pdf'
HL_CYBER = 'https://cdn.hl.com/pdf/2026/hl-cybersecurity-quarterly-update-q2-2026.pdf'
HL_DI = 'https://cdn.hl.com/pdf/2026/tech-digital-infra-q1-26.pdf'
HL_SEC = 'https://cdn.hl.com/pdf/2026/security-and-safety-solutions-q2-2026-market-update.pdf'
LINCOLN_EMS = 'https://www.lincolninternational.com/wp-content/uploads/2026-Q2_EMS-Quarterly-Review_vF2.pdf'
LINCOLN_GOV = 'https://lincolninternational.com/wp-content/uploads/Q3_2026-Defense-Technology-and-Government-Services-Market-Update.pdf'
RJ_GOV = 'https://www.raymondjames.com/-/media/rj/dotcom/files/corporations-and-institutions/investment-banking/industry-insight/government-technology-solutions-quarterly.pdf'
BAIRD_AI4 = 'https://www.rwbaird.com/corporations-and-institutions/investment-banking/insights/2026/08/ai4-2026-recap-the-handoff-economy/'
WILEY = 'https://www.wiley.law/alert-New-Forced-Labor-Tariffs-Imposed-on-60-US-Trading-Partners'
SNELL = 'https://www.swlaw.com/publication/the-continued-utilization-of-tariffs-to-control-the-semiconductor-industry/'
CMMC = 'https://dodcio.defense.gov/CMMC/About/'
MCGUIRE = 'https://www.passwordprotectedlaw.com/2026/07/dow-suspends-cmmc-phase-ii-requirements-launches-60-day-review/'
SPACEPOLICY = 'https://spacepolicyonline.com/news/house-clears-fy2027-cr-now-to-the-president/'
FEDSCOOP = 'https://fedscoop.com/radio/trump-admin-sets-75-7b-topline-civilian-it-budget-for-2027/'
FR_8A = 'https://www.federalregister.gov/documents/2026/08/11/2026-16370/reforms-to-13-cfr-124103-to-remove-sbas-8a-programs-rebuttable-presumption-of-social-disadvantage'
FR_GSAR = 'https://www.federalregister.gov/documents/2026/09/22/2026-19331/general-services-administration-acquisition-regulation-gsar-implementation-of-executive-order-14275'
FR_RECERT = 'https://www.federalregister.gov/documents/2024/12/17/2024-29393/hubzone-program-updates-and-clarifications-and-clarifications-to-other-small-business-programs'
FCC_IP = 'https://www.telecompetitor.com/fcc-reaches-deregulation-compromise-to-hasten-ip-transition/'
ATT_COPPER = 'https://broadbandbreakfast.com/at-t-approved-to-discontinue-service-at-more-than-30-of-copper-footprint-this-year/'
BEAD = 'https://broadbandbreakfast.com/bead-enters-cleanup-phase-with-more-broadband-gaps-to-fill/'
NTIA = 'https://broadbandusa.ntia.gov/funding-programs/broadband-equity-access-and-deployment-bead-program'
TAXF = 'https://taxfoundation.org/data/all/federal/2026-tax-brackets/'
IRS_NIIT = 'https://www.irs.gov/individuals/net-investment-income-tax'
COOLEY_QSBS = 'https://www.cooley.com/news/insight/2025/2025-07-11-the-one-big-beautiful-bill-act-expands-qsbs-benefits'
ALSTON = 'https://www.alston.com/en/insights/publications/2025/07/tax-provisions-one-big-beautiful-bill-act'
EMS_AUG = 'https://www.electronics.org/news-release/north-american-ems-orders-outpace-shipments-august-bookings-rise-535-year-over-year'
BM = 'https://www.benchmarkintl.com/insights/completed-transactions/'


# The opening paragraph and the four headline figures, used by the cover and by the site page.
BRIEF = ("Technology services enter the fourth quarter of 2026 with demand set by the build-out of artificial intelligence infrastructure and with acquirers paying most readily for contracted, recurring revenue. "
         "Gartner expects worldwide IT spending to reach $6.37 trillion this year, 14.2% above 2025, with data center systems up 62.5% and IT services up 5.3% ([[Gartner, July 27, 2026|" + GARTNER + "]]). "
         "Buyers announced 64 acquisitions of managed service providers in the first quarter, 73% more than a year earlier, and outside investors led four of every five ([[Omdia|" + OMDIA_MA + "]]). "
         "Financing became more expensive after the Federal Reserve raised its target range in September, which favors sellers whose earnings are documented and whose customers are under contract.")
FIGS = [('$6.37T', 'Forecast worldwide IT spending in 2026, up 14.2% on 2025'),
         ('64', 'Managed service provider acquisitions announced in the first quarter, up 73%'),
         ('1.39', 'North American EMS book-to-bill ratio, three months to August'),
         ('7.0x', 'Average EBITDA multiple in completed middle-market transactions, Q2 2026')]


def cover():
    section('Cover')
    art = ('<img src="%s" alt="Server racks in a data center with streaks of light" style="position: absolute; left: 0; top: 0; width: 816px; height: 590px; object-fit: cover">'
           '<div style="position: absolute; left: 0; top: 0; width: 816px; height: 590px; background: linear-gradient(180deg, rgba(35,31,32,0.78) 0%%, rgba(35,31,32,0.6) 45%%, rgba(35,31,32,0.78) 100%%)"></div>\n') % COVER_PHOTO
    labels = ['Managed IT<br>&amp; Cloud Services', 'Cybersecurity', 'Telecom<br>&amp; UCaaS', 'Systems<br>Integration', 'Electronics<br>&amp; Hardware', 'Government<br>Technology']
    brief, stats = BRIEF, FIGS
    body = (HEAD % {'title': 'Technology Q4 2026: Cover', 'wm': WATERMARK} + art +
            '<img src="%s" alt="Benchmark International" style="position: absolute; left: 293px; top: 42px; width: 230px; height: 108px">\n' % LOGO +
            '<div style="position: absolute; left: 0; top: 334px; width: 816px; display: grid; grid-template-columns: repeat(6, 1fr); text-align: center; color: #FFFFFF; font-weight: 700; font-size: 8px; line-height: 14px; letter-spacing: 1.6px; text-transform: uppercase">' +
            ''.join('<div>%s</div>' % l for l in labels) + '</div>\n'
            '<div style="position: absolute; left: 48px; top: 400px; width: 720px; display: flex; flex-direction: column; color: #FFFFFF">'
            '<h1 style="margin: 0; font-family: ' + CINZEL + '; font-weight: 400; font-size: 46px; line-height: 54px; letter-spacing: 2px">TECHNOLOGY</h1>'
            '<div style="height: 1px; background: ' + GOLD + '; margin: 13px 0 11px"></div>'
            '<div style="font-family: ' + SERIF + '; font-style: italic; font-weight: 600; font-size: 24px; line-height: 31px; letter-spacing: 0">Q4 2026 M&amp;A Sector Report</div></div>\n'
            '<div data-fit="350" style="position: absolute; left: 48px; top: 618px; width: 720px; height: 350px; display: flex; flex-direction: column; gap: 13px">'
            '<div style="font-weight: 700; font-size: 9.5px; line-height: 14px; letter-spacing: 2px; text-transform: uppercase">October 2026 - Jared Hardin | Managing Director | Benchmark International</div>'
            '<h2 style="margin: 0; font-family: ' + SERIF + '; font-weight: 600; font-size: 21px; line-height: 27px; letter-spacing: 0; color: ' + GOLD + '">The quarter in brief</h2>' +
            p(brief) +
            '<div style="display: grid; grid-template-columns: repeat(4, 1fr); column-gap: 22px; padding: 13px 0 14px; border-top: 1px solid ' + GOLD + '; border-bottom: 1px solid ' + GOLD + '">' +
            ''.join(stat(a, b) for a, b in stats) + '</div></div>\n' + FOOT + TAIL)
    return body


def p02():
    section('The six focus areas and the deal market')
    cols = '104px 1fr 1fr 106px'
    rows = [
        ('Managed IT & Cloud Services',
         'Managed service providers grew revenue 9.6% and adjusted EBITDA 17.1% in 2025; cloud infrastructure spending rose 43% in the second quarter of 2026',
         'Evergreen Services Group, The 20 MSP, Integris, Thrive, CompassMSP and Magna5 among consolidators; ePlus and Cognizant among public buyers',
         '1 closed, 11 live'),
        ('Cybersecurity',
         'Reported cybercrime losses reached $20.9 billion in 2025; the Department of War suspended the third-party certification phase of CMMC in July 2026',
         'LevelBlue, CyberMaxx, A-LIGN and Accenture in services; Palo Alto Networks, Google and ServiceNow in software',
         'None closed, 3 live'),
        ('Telecom & UCaaS',
         'RingCentral, Zoom and 8x8 are each growing revenue about 5%; AT&T plans to retire most of its copper outside California by the end of 2029; all 50 state broadband plans are approved',
         'Verizon, AT&T and T-Mobile with KKR and EQT in fiber; Point Broadband, Ezee Fiber, Vero Fiber, Rightfiber and TDS Telecom regionally; AppDirect in the channel',
         '1 closed, 3 live'),
        ('Systems Integration',
         'Data center systems spending is forecast to rise 62.5% in 2026; professional audiovisual revenue is forecast to grow from $332 billion in 2025 to $402 billion in 2030',
         'Pavion, Convergint, Everon, Securitas Technology and Knox Lane in security; 26North in audiovisual; Myriad360, ePlus and Net at Work in IT',
         '4 closed, 11 live'),
        ('Electronics & Hardware',
         'North American EMS bookings rose 53.5% in August while shipments rose 1.0%; Section 301 duties replaced the expired 10% import surcharge on July 24',
         'Jabil, Sanmina and Flex among public manufacturers; Transom Capital, Tide Rock, Align Capital Partners and Arcline among sponsors',
         '5 closed, 6 live'),
        ('Government Technology',
         'The fiscal 2027 budget requests $75.7 billion for civilian IT against $67.9 billion in 2026; a continuing resolution funds the government through December 11',
         'Leidos, Booz Allen, Parsons and SAIC; sponsor-backed ERT, Xpect Solutions, B&A and Detroit Defense',
         '2 closed, 4 live'),
    ]
    t = table(cols, ['Focus area', 'Where the market stands', 'Who is buying', 'Benchmark International, trailing 24 months'], rows, pad=6)
    para = ("Global mergers and acquisitions reached $3.9 trillion in the first nine months of 2026, 28% above the same period of 2025 and the highest nine-month total since 2001, while the number of transactions fell 8% "
            "([[LSEG data reported by Reuters|" + REUTERS_Q3 + "]]). Technology was the largest sector in the first half at $649 billion ([[Reuters, July 1, 2026|" + REUTERS_H1 + "]]). "
            "The third quarter was the slowest of the year at $993 billion, 41% below the second quarter, as borrowing costs rose. "
            "Add-on acquisitions by sponsor-backed platforms made up roughly three-quarters of all US buyouts in the second quarter ([[PitchBook, Q2 2026 US PE Breakdown|" + PITCHBOOK + "]]), and those smaller purchases are the transactions in which most founder-owned technology companies take part.")
    body = '\n'.join([kicker('The six focus areas at the start of the quarter'), t,
                      h2('Deal market: value is concentrated in large transactions and add-ons carry the volume', mt=6), p(para)])
    return page('Technology Q4 2026: The six focus areas', 2, body)


def p03():
    section('Deal market, financing and demand')
    rows = [
        ('US private equity deal activity', '2,384 transactions worth $177.3 billion, with value 37.5% below the prior quarter', 'Q2 2026', '[[PitchBook|' + PITCHBOOK + ']]'),
        ('Companies held by US private equity', '13,509, with a median holding period of 4.2 years for companies sold in 2026', 'Q2 2026', '[[PitchBook|' + PITCHBOOK + ']]'),
        ('Managed service provider acquisitions', '64 worldwide, up 73%, with outside investors leading 80% of them; 37 in North America, up 28%', 'Q1 2026', '[[Omdia|' + OMDIA_MA + ']]; [[Channel Dive|' + CHDIVE_MA + ']]'),
        ('Cybersecurity transactions announced', '37 in June, 21 in July and 33 in August',
         'Jun to Aug 2026', '[[SecurityWeek|https://www.securityweek.com/cybersecurity-ma-roundup-33-deals-announced-in-august-2026/]]'),
        ('Average purchase price, completed middle-market transactions in all industries', '7.0x trailing adjusted EBITDA against 7.3x in the first quarter, with senior debt priced at 7.8%', 'Q2 2026', '[[GF Data via ACG|' + GFDATA + ']]'),
        ('Multiple paid in transactions of $5 million to $50 million in all industries', '5.8x EBITDA, the highest since the first quarter of 2022; 87% of sales above $5 million drew three or more offers', 'Q2 2026', '[[IBBA and M&A Source Market Pulse|' + IBBA + ']]; [[release|' + IBBA_PR + ']]'),
    ]
    t = table('190px 1fr 86px 150px', ['Deal indicator', 'Latest reading', 'Period', 'Source'], rows)
    fin = ("Financing became more expensive during the third quarter. The Federal Reserve raised its target range by a quarter point to 3.75% to 4.00% on September 16 ([[Federal Reserve|" + FED + "]]), "
           "the 10-year Treasury yielded 5.24% on October 1 ([[US Treasury|" + TREASURY + "]]), and a small sample of recent buyout loans from direct lenders priced at an average of 509 basis points over the benchmark rate, against 474 in the first quarter ([[PitchBook|" + PITCHBOOK + "]]). "
           "Lenders also reduced leverage, and total debt on platform acquisitions in the GF Data sample fell to 2.9x EBITDA from 3.4x ([[GF Data via ACG|" + GFDATA + "]]). "
           "Buyers respond to dearer debt by favoring companies whose cash flow is contracted.")
    q = quote('M&A activity stayed robust, driven by sector consolidation and continued strong interest from financial investors.',
              'Houlihan Lokey, [[December 2025 IT Services Market Update|' + HL_IT + ']]')
    dem = ("Gartner's July forecast puts worldwide IT spending at $6.37 trillion in 2026, with data center systems rising 62.5% to $822 billion, software rising 15.5% and IT services rising 5.3% to $1.57 trillion ([[Gartner|" + GARTNER + "]]). "
           "Cloud infrastructure services revenue reached $143.4 billion in the second quarter, 43% above the prior year ([[Synergy Research Group|" + SYNERGY + "]]), with Amazon Web Services growing 37% ([[Amazon|" + AMZN + "]]) and Microsoft Azure growing 43% ([[Microsoft|" + MSFT + "]]). "
           "Amazon, Alphabet, Meta and Microsoft have guided to a combined $735 billion to $750 billion of capital spending this year ([[Platformonomics compilation of company guidance|" + PLATFORMONOMICS + "]]). "
           "Traditional outsourcing is moving the other way: managed services contract value in the Americas fell 12% in the second quarter while infrastructure-as-a-service contract value rose 86% ([[ISG Index|" + ISG + "]]).")
    body = '\n'.join([kicker('Deal market, financing and demand'), t, p(fin), q,
                      h2('Demand: artificial intelligence infrastructure is setting the pace', mt=0), p(dem)])
    return page('Technology Q4 2026: Deal market, financing and demand', 3, body)


def p04():
    section('Policy, trade and tax')
    rows = [
        ('Import tariffs', 'Section 301 duties took effect on July 24, 2026 in place of the expired 10% Section 122 surcharge, at 10% for Canada, Mexico, the United Kingdom and India and 12.5% for China and Vietnam; certain semiconductor manufacturing equipment is exempt', '[[Wiley Rein, July 27, 2026|' + WILEY + ']]'),
        ('Semiconductor tariffs', 'A 25% Section 232 tariff has applied to specified advanced computing chips since January 2026, with exemptions that include chips destined for US data centers', '[[Snell & Wilmer|' + SNELL + ']]'),
        ('CMMC for defense suppliers', 'Phase 1 self-assessments have applied since November 10, 2025; the Department of War suspended Phase II, the move to third-party certification, on July 13, 2026 and set up a reform task force', '[[DoD Chief Information Officer|' + CMMC + ']]; [[McGuireWoods|' + MCGUIRE + ']]'),
        ('Federal funding', 'A continuing resolution signed on September 2 funds the government through December 11, 2026; the fiscal 2027 request holds $75.7 billion for civilian IT', '[[SpacePolicyOnline|' + SPACEPOLICY + ']]; [[FedScoop|' + FEDSCOOP + ']]'),
        ('SBA 8(a) program', 'A final rule effective September 10, 2026 removes the presumption of social disadvantage for individually owned applicants; firms owned by tribes and Alaska Native corporations are exempt', '[[Federal Register|' + FR_8A + ']]'),
        ('Copper retirement', 'The FCC streamlined its copper retirement rules in March 2026; AT&T plans to retire most of its copper outside California by the end of 2029', '[[Telecompetitor|' + FCC_IP + ']]; [[Broadband Breakfast|' + ATT_COPPER + ']]'),
        ('Rural broadband funding', 'All 50 state plans under the $42.45 billion BEAD program are approved and the program is moving into construction', '[[Broadband Breakfast|' + BEAD + ']]; [[NTIA|' + NTIA + ']]'),
    ]
    t = table('150px 1fr 150px', ['Item', 'Status in October 2026', 'Source'], rows, pad=4)
    tax = ("Federal tax law is settled for an owner planning a closing in late 2026 or 2027. The top rate on long-term capital gains remains 20% ([[Tax Foundation|" + TAXF + "]]), with the 3.8% net investment income tax applying above $250,000 of income for joint filers ([[IRS|" + IRS_NIIT + "]]), "
           "and the estate and gift exemption stands at $15 million per person. The 2025 tax act also made 100% bonus depreciation permanent and restored immediate deduction of domestic research costs ([[Alston & Bird|" + ALSTON + "]]), both of which raise after-tax cash flow for electronics manufacturers and software-heavy service firms. "
           "For C corporation stock issued after July 4, 2025, the qualified small business stock exclusion now phases in at 50% after three years, 75% after four and 100% after five, with the cap raised to $15 million and the gross asset limit to $75 million ([[Cooley|" + COOLEY_QSBS + "]]).")
    trade = ("Trade policy bears most directly on hardware. Manufacturers and integrators that import components should expect buyers to ask for landed cost by country of origin and for the contract terms that pass duty changes through to customers.")
    body = '\n'.join([kicker('Policy, trade and tax'),
                      h2('Tariffs moved to a new legal footing in July and the defense cybersecurity mandate is paused'), t,
                      h2('Tax: rates are unchanged and several provisions favor sellers', mt=2), p(tax), p(trade)])
    return page('Technology Q4 2026: Policy, trade and tax', 4, body)
