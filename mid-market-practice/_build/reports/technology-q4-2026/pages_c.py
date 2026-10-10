import statistics
import lib
from lib import *
from pages_a import *
from pages_b import TXCOLS, TXHEAD

# ============ ELECTRONICS & HARDWARE ============
EMS_JUL = 'https://www.electronics.org/news-release/north-american-ems-orders-surge-july-book-bill-stands-129'
EMS_JAN = 'https://www.electronics.org/news-release/north-american-ems-market-opens-2026-soft-note-momentum-cools'
PCB_JUL = 'https://www.electronics.org/news-release/north-american-pcb-demand-strengthens-july-bookings-surge-62'
JABIL = 'https://www.sec.gov/Archives/edgar/data/0000898293/000162828026063890/jbl-20260930ex991.htm'
CELESTICA = 'https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000043/cls-20260630prcondensedfs.htm'
SANMINA = 'https://s201.q4cdn.com/209924174/files/doc_news/Sanmina-Reports-Third-Quarter-Fiscal-2026-Financial-Results-2026.pdf'
SIA_SEMI = 'https://www.semiconductors.org/global-semiconductor-sales-increase-35-1-from-q1-2026-to-q2-2026/'
SIGMATRON = 'https://www.barchart.com/story/news/32505546/transom-capital-and-sigmatron-international-announce-entry-into-merger-agreement'
QUALITEL = 'https://circuitsassembly.com/ca/editorial/menu-news/43626-qualitel-corporation-acquires-fusion-ems.html'
STENTECH = 'https://www.businesswire.com/news/home/20260421837617/en/StenTech-Acquires-Pentagon-EMS-to-Further-Enhance-Tooling-Capabilities'
PRIV_MFG = 'https://www.privsource.com/acquisitions/activity/add-on/manufacturing/2026'
NAVITAS = 'https://circuitsassembly.com/ca/editorial/menu-news/43633-navitas-to-acquire-claros.html'
SILVUS = 'https://www.govconwire.com/articles/motorola-solutions-silvus-technologies-acquisition'
DFEND = 'https://www.govconwire.com/articles/motorola-solutions-d-fend-counter-drone-acquisition'
AACB = 'https://www.aacb.com/trade-tariff-news/section-122-is-out-section-301-is-in'


def p13():
    section('Electronics & Hardware')
    b = band([('1.39', 'Orders booked for each dollar shipped by North American EMS firms in the three months to August 2026'),
              ('53.5%', 'Growth in North American EMS bookings in August against a year earlier'),
              ('1.46', 'Orders booked for each dollar shipped by North American circuit board makers in July')],
             'chip', 'Close view of a printed circuit board')
    parts = [
        colp("Orders at North American electronics manufacturers are running well ahead of shipments. Bookings at electronics manufacturing services (EMS) firms were 53.5% above the prior year in August while shipments were 1.0% higher, and the three-month book-to-bill ratio stands at 1.39 ([[Global Electronics Association, October 1, 2026|" + EMS_AUG + "]]). Printed circuit board makers reported bookings up 62.0% and shipments up 14.5% in July, a ratio of 1.46 ([[Global Electronics Association|" + PCB_JUL + "]])."),
        colp("Artificial intelligence infrastructure accounts for much of the order growth at the largest contract manufacturers. Jabil grew revenue 21% to $36.0 billion in its fiscal 2026 and guided to $44.5 billion for fiscal 2027 ([[Jabil|" + JABIL + "]]). Celestica grew second-quarter revenue 62% and raised its 2026 outlook to $20.5 billion ([[Celestica|" + CELESTICA + "]]), and Sanmina grew revenue about 70% in its June quarter ([[Sanmina|" + SANMINA + "]]). Worldwide semiconductor sales reached $403.3 billion in the second quarter ([[Semiconductor Industry Association|" + SIA_SEMI + "]])."),
        colp("Shipments across the wider North American EMS industry were 1.0% above the prior year in August, well below the growth of the largest firms ([[Global Electronics Association|" + EMS_AUG + "]]). A full order book is valuable to an acquirer when it converts to shipments, so buyers examine component availability, labor and capacity closely."),
        quote('Buyers continued to prioritize localized manufacturing capacity and exposure to resilient, specification-driven end markets.',
              'Lincoln International, [[Q2 2026 EMS Quarterly Review|' + LINCOLN_EMS + ']]'),
        colp("Acquirers have been buying domestic capacity and specialized capability. Transom Capital agreed to take SigmaTron International private at an enterprise value of about $83 million, a 134% premium to the prior share price ([[Transom Capital and SigmaTron|" + SIGMATRON + "]]). Qualitel bought Fusion EMS of Oregon to add to its plants in Washington and Mexicali ([[Circuits Assembly|" + QUALITEL + "]]), and StenTech, backed by Align Capital Partners, made its fifth add-on with Pentagon EMS ([[StenTech|" + STENTECH + "]])."),
        colp("Defense and public safety electronics have drawn the highest prices. Motorola Solutions paid $4.4 billion for the communications technology firm Silvus Technologies in 2025 ([[GovCon Wire|" + SILVUS + "]]) and $1.5 billion for the counter-drone firm D-Fend Solutions in 2026 ([[GovCon Wire|" + DFEND + "]])."),
        colp("Tariffs remain the main planning variable. The Section 301 duties that replaced the import surcharge on July 24 ([[Wiley Rein|" + WILEY + "]]) exempt semiconductors and treat finished electronics more narrowly than the surcharge did ([[A&A Customs Brokers|" + AACB + "]])."),
    ]
    body = '\n'.join([kicker('Electronics & Hardware'),
                      h2('Order books are filling faster than factories can ship'), b, columns(parts, 3)])
    return page('Technology Q4 2026: Electronics & Hardware', 13, body)


def p14():
    section('Electronics & Hardware: announced transactions and indicators')
    intro = ("Sales of contract manufacturers slowed in the second quarter. Lincoln International recorded three EMS transactions in the second quarter against eight in the first ([[Lincoln International|" + LINCOLN_EMS + "]]). The buyers that are active want domestic or near-shore capacity, certifications for aerospace, defense and medical work, and engineering content that customers specify by name.")
    rows = [
        ('Sep 2026', '[[Fusion EMS|' + QUALITEL + ']]', 'Qualitel', 'EMS provider in Hillsboro, Oregon; undisclosed'),
        ('Aug 2026', '[[D-Fend Solutions|' + DFEND + ']]', 'Motorola Solutions', 'Counter-drone radio frequency technology; $1.5 billion'),
        ('Aug 2026', '[[Claros|' + NAVITAS + ']]', 'Navitas Semiconductor', 'Power delivery technology for AI data centers; up to about $232.8 million; announced'),
        ('Apr 2026', '[[Pentagon EMS|' + STENTECH + ']]', 'StenTech, backed by Align Capital Partners', 'Precision tooling and machining for electronics, aerospace and defense, near Portland, Oregon; undisclosed'),
        ('2026', '[[Analog Technologies|' + PRIV_MFG + ']]', 'Tide Rock', 'EMS provider with aerospace and defense certifications; undisclosed'),
        ('2026', '[[Plasma Ruggedized Solutions|' + PRIV_MFG + ']]', 'Novaria Group, backed by Arcline', 'Coatings and encapsulation for defense, medical and industrial electronics; undisclosed'),
        ('Aug 2025', '[[Silvus Technologies|' + SILVUS + ']]', 'Motorola Solutions', 'Mobile network communications technology for defense and public safety; $4.4 billion'),
        ('May 2025', '[[SigmaTron International|' + SIGMATRON + ']]', 'Transom Capital', 'Listed EMS provider; $3.02 a share, about $83 million of enterprise value; announced'),
    ]
    ind = [
        ('EMS bookings', '-3.3%', '+44.3%', '+53.5%'),
        ('EMS shipments', '+0.1%', '-0.3%', '+1.0%'),
        ('EMS book-to-bill ratio, three-month', '1.25', '1.29', '1.39'),
    ]
    indt = table('1fr 120px 120px 120px', ['North American EMS, change on prior year', 'January 2026', 'July 2026', 'August 2026'], ind, pad=4)
    src = note(
        "Source: Global Electronics Association monthly releases for [[January|" + EMS_JAN + "]], [[July|" + EMS_JUL + "]] and [[August|" + EMS_AUG + "]] 2026. The book-to-bill ratio divides orders booked by shipments billed over three months.")
    close = ("The order data bear on the timing of a sale. Bookings turned from a 3.3% decline in January to growth above 40% in July and August, and a manufacturer that can show that backlog converting to shipments at steady margins presents buyers with visible growth. Buyers discount backlog that depends on one program or one customer, and they look closely at how tariff costs are passed through in customer contracts.")
    body = '\n'.join([kicker('Electronics & Hardware: announced transactions and indicators'),
                      h2('Buyers want domestic capacity, certifications and specified engineering content'), p(intro),
                      table(TXCOLS, TXHEAD, rows, pad=4), indt, src, p(close)])
    return page('Technology Q4 2026: Electronics & Hardware transactions', 14, body)


# ============ GOVERNMENT TECHNOLOGY ============
WASHTECH = 'https://washingtontechnology.com/opinion/2026/06/15-trillion-defense-budget-it-programs-contractors-should-be-watching/414438/'
AKIN = 'https://www.akingump.com/print/v2/content/1134675/washingtons-new-deadline-a-longer-road-for-the-same-can.pdf'
BAH = 'https://www.govconwire.com/articles/booz-allen-2-8b-q1-fy2027-revenue-financial-results'
LDOS = 'https://www.govconwire.com/articles/leidos-q2-2026-earnings-results'
CACI_R = 'https://www.govconwire.com/articles/caci-q4-full-fy2026-revenues-contract-awards'
SAIC_R = 'https://www.govconwire.com/articles/saic-q2-fy2027-revenue-guidance-raised'
NASCIO = 'https://statescoop.com/state-cios-anticipate-a-more-turbulent-technology-landscape-nascios-annual-survey-finds/'
ULTRA = 'https://www.govconwire.com/articles/booz-allen-720m-ultra-ic-mission-solutions-close'
ALTAMIRA = 'https://www.govconwire.com/articles/parsons-acquires-altamira-defense-intelligence'
KUDU = 'https://www.govconwire.com/articles/leidos-cyber-firm-kudu-dynamics'
SILVEREDGE = 'https://www.govconwire.com/articles/saic-silveredge-acquire-godspeed-robert-miller'
SEV1 = 'https://www.executivebiz.com/articles/ert-sev1tech-acquisition'
AMIVERO = 'https://www.govconwire.com/articles/xpect-solutions-acquires-amivero-national-security'
IWAVES = 'https://www.govconwire.com/articles/ba-intelligent-waves-defense-cyber-acquisition'
ATHENIX = 'https://www.govconwire.com/articles/detroit-defense-athenix-solutions-group'
CAPGOV = 'https://www.govconwire.com/articles/itc-federal-acquires-capgemini-government-solutions'
APRIVA = 'https://www.govconwire.com/articles/itc-federal-acquires-apriva-iss-fbi-classified-comms'
EXPANSIA = 'https://www.executivebiz.com/articles/expansia-jhna-ctsi-merger-defense-tech-platform'


def p15():
    section('Government Technology')
    b = band([('$75.7B', 'Civilian agency IT in the fiscal 2027 budget request, up from $67.9 billion'),
              ('$20.5B', 'Cyberspace activities in the fiscal 2027 defense budget request'),
              ('98%', 'States with an enterprise AI policy in 2026, up from 76% a year earlier')],
             'gov', 'A satellite dish antenna')
    parts = [
        colp("Federal technology budgets are rising. The fiscal 2027 request holds $75.7 billion for civilian agency IT against $67.9 billion in fiscal 2026, led by Veterans Affairs at $12.2 billion and Homeland Security at $11.7 billion ([[FedScoop|" + FEDSCOOP + "]]). The defense request totals $1.5 trillion, of which $350 billion is mandatory funding, and includes $20.5 billion for cyberspace activities and $58.5 billion for artificial intelligence ([[Washington Technology|" + WASHTECH + "]])."),
        colp("The timing of that money is less certain. The government is operating under a continuing resolution through December 11 ([[SpacePolicyOnline|" + SPACEPOLICY + "]]), and the Senate Appropriations Committee had reported none of the twelve fiscal 2027 bills when the resolution passed ([[Akin|" + AKIN + "]]). New program starts wait for full-year appropriations, which delays awards for contractors of every size."),
        colp("Results at the large contractors show the effect. Leidos grew revenue 7% in the second quarter and raised the lower end of its guidance ([[GovCon Wire|" + LDOS + "]]) and CACI grew 10.9% in its fiscal 2026 ([[GovCon Wire|" + CACI_R + "]]). Booz Allen's revenue fell 4.2% in its June quarter even as it booked $1.50 of new work for each dollar of revenue ([[GovCon Wire|" + BAH + "]]), and SAIC attributed a book-to-bill ratio of 0.6 to a large recompete that slipped on procurement delays ([[GovCon Wire|" + SAIC_R + "]])."),
        quote('Defense tech firms have corrected from the valuation highs of Q1, while investors continue to be cautious about the potential AI impact on traditional government services business models, resulting in multiple compression despite healthy earnings and improving forecasts.',
              'Lincoln International, [[Q3 2026 Defense Technology & Government Services Report|' + LINCOLN_GOV + ']]'),
        colp("Procurement rules are changing at the same time. GSA proposed on September 22 to move schedule ordering procedures out of the Federal Acquisition Regulation as part of a wider rewrite ([[Federal Register|" + FR_GSAR + "]]), and a final rule effective September 10 removed the presumption of social disadvantage for individually owned 8(a) applicants ([[Federal Register|" + FR_8A + "]]). A contractor that no longer qualifies as small after a sale cannot receive new set-aside orders under multiple-award contracts ([[Federal Register|" + FR_RECERT + "]]), so the buyer's size affects how much revenue carries forward."),
        colp("State and local governments are a growing second market. Among state chief information officers, 98% now report an enterprise AI policy and 64% expect agentic AI to be the most impactful emerging technology of the next two to three years, while 55% have dedicated funding for citizen digital services ([[NASCIO survey via StateScoop|" + NASCIO + "]])."),
    ]
    body = '\n'.join([kicker('Government Technology'),
                      h2('Budgets for cyber, AI and mission software are rising while award timing and procurement rules shift'), b, columns(parts, 3)])
    return page('Technology Q4 2026: Government Technology', 15, body)


def p16():
    section('Government Technology: announced transactions')
    intro = ("The large contractors are buying software, cyber and signals capability at disclosed prices, and sponsor-backed platforms are buying founder-owned firms with positions at defense, intelligence and homeland security agencies. Transaction volume has slowed: Raymond James reported that government technology transaction volume fell 68% from the first quarter to the second, with strategic volume 61% below the second quarter of 2025 ([[Raymond James, Q2 2026 Market Update|" + RJ_GOV + "]]).")
    rows = [
        ('Sep 2026', '[[Athenix Solutions Group|' + ATHENIX + ']]', 'Detroit Defense, backed by Proteus Enterprises and Gladstone Investment', 'Mission software and engineering for defense and intelligence customers; undisclosed'),
        ('Sep 2026', '[[Intelligent Waves|' + IWAVES + ']]', 'B&A, backed by DFW Capital Partners', 'Cyber, secure communications and tactical edge services; undisclosed'),
        ('Sep 2026', '[[Capgemini Government Solutions|' + CAPGOV + ']]', 'ITC Federal', 'Data, AI and digital modernization for federal agencies; undisclosed'),
        ('Sep 2026', '[[Amivero|' + AMIVERO + ']]', 'Xpect Solutions, backed by NewSpring Holdings', 'AI and data science for Homeland Security; undisclosed'),
        ('Aug 2026', '[[Ultra I&C Mission Solutions|' + ULTRA + ']]', 'Booz Allen', 'Defense software, encryption and edge computing; $720 million'),
        ('Feb 2026', '[[Sev1Tech|' + SEV1 + ']]', 'ERT, backed by Macquarie Capital', 'IT modernization, cyber and cloud for defense, intelligence and civilian agencies; undisclosed'),
        ('Jan 2026', '[[Altamira Technologies|' + ALTAMIRA + ']]', 'Parsons', 'Signals intelligence, missile warning and cyber; $375 million including a $45 million earnout'),
        ('Jan 2026', '[[EXPANSIA, JHNA and CTSi|' + EXPANSIA + ']]', 'Falfurrias Management Partners', 'Three firms merged into a defense technology platform of more than 525 people; undisclosed'),
        ('Oct 2025', '[[SilverEdge Government Solutions|' + SILVEREDGE + ']]', 'SAIC', 'Cyber and software; $205 million in cash; seller Godspeed Capital'),
        ('May 2025', '[[Kudu Dynamics|' + KUDU + ']]', 'Leidos', 'Founder-led cyber and vulnerability research firm; about $300 million in cash'),
    ]
    close = ("Parsons expects Altamira to produce more than $200 million of revenue in 2026, which places its price at about 1.9 times revenue including the earnout and about 1.65 times on the $330 million paid at closing, a calculation from the figures in the announcement ([[GovCon Wire|" + ALTAMIRA + "]]). EBITDA multiples were not disclosed in any of these transactions. Buyers pay the most for prime positions on contracts awarded in full and open competition, cleared staff, and software or data rights the company owns, and they discount revenue that depends on a set-aside status the buyer cannot keep.")
    body = '\n'.join([kicker('Government Technology: announced transactions'),
                      h2('Prime contractors disclose prices and sponsor-backed platforms are the most frequent buyers of founder-owned firms'), p(intro),
                      table(TXCOLS, TXHEAD, rows, pad=4), p(close)])
    return page('Technology Q4 2026: Government Technology transactions', 16, body)


# ============ VALUATION ============
COMPS = {
 'Managed IT & Cloud Services': [('CDW','cdw',11.30),('Insight Enterprises','nsit',9.72),('ePlus','plus',11.08),('PC Connection','cnxn',14.28),('Kyndryl','kd',4.08),('DXC Technology','dxc',2.87),('Accenture','acn',8.30),('Cognizant','ctsh',6.79),('EPAM Systems','epam',6.46)],
 'Cybersecurity': [('Fortinet','ftnt',50.58),('Qualys','qlys',23.67),('Check Point','chkp',13.05)],
 'Telecom & UCaaS': [('RingCentral','rng',18.57),('8x8','eght',13.57),('Zoom','zm',15.12),('Five9','fivn',18.89),('Ooma','ooma',24.78),('Crexendo','cxdo',19.26),('Shenandoah Telecommunications','shen',11.52),('Telephone and Data Systems','tds',9.71)],
 'Systems Integration': [('Wesco','wcc',15.43),('ScanSource','scsc',9.39),('Climb Global Solutions','clmb',14.92),('Comfort Systems USA','fix',29.31),('EMCOR','eme',17.24),('IES Holdings','iesc',23.96),('ADT','adt',4.74)],
 'Electronics & Hardware': [('Jabil','jbl',13.58),('Flex','flex',21.93),('Celestica','cls',28.78),('Sanmina','sanm',14.86),('Plexus','plxs',23.75),('Benchmark Electronics','bhe',21.07),('Kimball Electronics','ke',7.70),('TTM Technologies','ttmi',30.67),('Keysight','keys',38.66)],
 'Government Technology': [('Booz Allen Hamilton','bah',9.49),('CACI','caci',16.05),('SAIC','saic',10.50),('Leidos','ldos',8.72),('Parsons','psn',12.68),('ICF','icfi',10.29),('Tyler Technologies','tyl',30.15)],
}
MED = {k: statistics.median([v for _, _, v in rows]) for k, rows in COMPS.items()}


def fmt(v):
    return ('%.1fx' % v)


def web_chart():
    """The valuation chart for the site page, drawn with the shared .mchart styles in report.css."""
    MAXV = 60.0  # the same scale as the print chart; multiples above 60x are left out of COMPS
    pc = lambda v: '%.2f%%' % (v / MAXV * 100)
    rows = []
    for name, cs in COMPS.items():
        vals = [v for _, _, v in cs]
        med = MED[name]
        dots = ''.join('<i class="dot" style="left:%s" title="%s %s"></i>' % (pc(v), html.escape(n), fmt(v)) for n, _, v in cs)
        rows.append('<div class="mrow"><div class="mlabel">%s</div><div class="mtrack"><i class="mavg" style="left:%s"></i>'
                    '<i class="mrange" style="left:%s;width:%s"></i>%s<i class="mmed" style="left:%s"><b>%s</b></i></div></div>' % (
                        html.escape(name), pc(7.0), pc(min(vals)), pc(max(vals) - min(vals)), dots, pc(med), fmt(med)))
    axis = ''.join('<span style="left:%s">%dx</span>' % (pc(v), v) for v in (0, 10, 20, 30, 40, 50, 60))
    return ('<div class="mchart" role="img" aria-label="Enterprise value to trailing EBITDA for listed companies in each focus area, with the median marked">'
            + ''.join(rows) + '<div class="mrow mrow--axis"><div class="mlabel"></div><div class="mtrack maxis">' + axis + '</div></div>'
            '<p class="mkey"><span><i class="dot"></i> One listed company</span><span><i class="kmed"></i> Median</span>'
            '<span><i class="kavg"></i> Private mid-market average, all industries, 7.0x</span></p></div>')


def p17():
    section('Public-market valuation')
    X0, W, MAXV = 200, 500, 60.0
    def x(v):
        return X0 + v * W / MAXV
    H = 44 + 40 * len(COMPS) + 4
    c = []
    for t in (0, 10, 20, 30, 40, 50, 60):
        c.append('<div style="position: absolute; left: %dpx; top: 44px; width: 1px; height: %dpx; background: #E3DED6"></div>' % (x(t), H - 44))
        c.append('<div style="position: absolute; left: %dpx; top: %dpx; width: 40px; text-align: center">%dx</div>' % (x(t) - 20, H + 6, t))
    c.append('<div style="position: absolute; left: %dpx; top: 26px; width: 0; height: %dpx; border-left: 1px dashed #6D7681"></div>' % (x(7.0), H - 26))
    c.append('<div style="position: absolute; left: %dpx; top: 4px; width: 330px; font-weight: 600">Private mid-market average, all industries, 7.0x</div>' % (x(7.0) - 10))
    for i, (name, rows) in enumerate(COMPS.items()):
        y = 62 + 40 * i
        vals = [v for _, _, v in rows]
        c.append('<div style="position: absolute; left: 0; top: %dpx; width: 196px; font-weight: 600">%s</div>' % (y, html.escape(name)))
        c.append('<div style="position: absolute; left: %dpx; top: %dpx; width: %dpx; height: 2px; background: #D2CDC4"></div>' % (x(min(vals)), y + 7, x(max(vals)) - x(min(vals))))
        for v in vals:
            c.append('<div style="position: absolute; left: %dpx; top: %dpx; width: 10px; height: 10px; border-radius: 50%%; background: #9B958B"></div>' % (x(v) - 5, y + 3))
        m = MED[name]
        c.append('<div style="position: absolute; left: %dpx; top: %dpx; width: 4px; height: 26px; background: %s"></div>' % (x(m) - 2, y - 5, GOLD))
        c.append('<div style="position: absolute; left: %dpx; top: %dpx; width: 60px; text-align: center; font-weight: 700">%s</div>' % (x(m) - 30, y - 22, fmt(m)))
    fig = ('<figure style="margin: 0; display: flex; flex-direction: column; gap: 6px"><div style="font-size: 11px; line-height: 15px; letter-spacing: 0.3px">Enterprise value to trailing twelve-month EBITDA, listed companies by focus area; each dot is one company and the gold bar marks the median</div>'
           '<div style="position: relative; width: 720px; height: %dpx; font-size: 11.5px; line-height: 16px; letter-spacing: 0.2px">%s</div></figure>') % (H + 26, ''.join(c))
    txt = ("Public multiples describe companies many times larger than a founder-owned business and are best read as an indication of relative standing among the six focus areas. Electronics manufacturers carry a median of " + fmt(MED['Electronics & Hardware']) + " on the strength of data center demand, communications and integration companies sit between " + fmt(MED['Systems Integration']) + " and " + fmt(MED['Telecom & UCaaS']) + ", and government contractors and IT services companies have the lowest medians at " + fmt(MED['Government Technology']) + " and " + fmt(MED['Managed IT & Cloud Services']) + ". "
           "The low readings for large IT services firms come as investors weigh how artificial intelligence will change labor-based pricing. Private benchmarks sit below most of these figures. The median US buyout was priced at 12.5x EBITDA in 2025 ([[PitchBook|" + PITCHBOOK + "]]), completed middle-market transactions in all industries averaged 7.0x in the second quarter of 2026 ([[GF Data via ACG|" + GFDATA + "]]), and transactions of $5 million to $50 million were priced at 5.8x ([[IBBA and M&A Source Market Pulse|" + IBBA + "]]).")
    if lib.WEB:
        fig = ('<figure><div class="fine">Enterprise value to trailing twelve-month EBITDA, listed companies by focus area; each dot is one company and the gold bar marks the median</div>' + web_chart() + '</figure>')
    lists = []
    for name, rows in COMPS.items():
        items = '; '.join('[[%s|https://stockanalysis.com/stocks/%s/statistics/]] %s' % (n, t, fmt(v)) for n, t, v in rows)
        if lib.WEB:
            lists.append('<div><strong>%s:</strong> %s</div>' % (html.escape(name), md(items)))
        else:
            lists.append('<div style="break-inside: avoid; margin: 0 0 6px"><span style="font-weight: 700">%s:</span> %s</div>' % (html.escape(name), md(items)))
    comp = '<div class="fine cols">' + ''.join(lists) + '</div>' if lib.WEB else '<div style="column-count: 2; column-gap: 32px; font-size: 11px; line-height: 16px; letter-spacing: 0.2px">' + ''.join(lists) + '</div>'
    foot = note(
        "Multiples are enterprise value to trailing EBITDA as published by [[StockAnalysis|https://stockanalysis.com/]] and retrieved on October 5, 2026; they use reported EBITDA, which is lower than the adjusted EBITDA companies present. "
        "Multiples above 60x are omitted as not meaningful, which removes CrowdStrike, Palo Alto Networks, Zscaler, Okta, Tenable and Bandwidth and leaves three security software companies; those three are a guide to software and say little about the price of a security services firm.")
    body = '\n'.join([kicker('Public-market valuation reference'),
                      h2('Listed medians run from ' + fmt(MED['Managed IT & Cloud Services']) + ' EBITDA for IT services to ' + fmt(MED['Electronics & Hardware']) + ' for electronics manufacturers, with security software higher still'),
                      fig, p(txt), comp, foot])
    return page('Technology Q4 2026: Public-market valuation', 17, body, gap=12)


# ============ BENCHMARK ============
def p18():
    section('Benchmark International')
    intro = ("Benchmark International has closed 13 transactions in these six focus areas over the trailing 24 months and is working on 38 further engagements as of October 1, 2026. Electronics and hardware is the largest group among the closed transactions, with five, followed by systems integration with four. "
             "Managed IT and cloud services and systems integration lead the live engagements with 11 each. Across all six, 19 engagements are on the market, eight are in preparation, eight are in legal documentation and three are in discussion with a buyer.")
    buyers = ("Operating companies were the buyers in most of the announced transactions. Of the eleven listed below, seven were sold to a company in the seller's own or an adjacent field, including one owned by a private equity firm, and four were sold to investment firms that back founder-owned companies. "
              "Benchmark International is ranked the leading privately owned sell-side M&A advisor in the world in PitchBook's Q2 2026 Global League Tables ([[Benchmark International|https://www.benchmarkintl.com/about/our-success/]]).")
    def u(slug):
        return BM + slug + '/'
    rows = [
        ('[[MartianCraft|' + u('benchmark-international-successfully-facilitated-the-transaction-between-martiancraft-llc-and-walnut-capital-partners') + ']]', 'Walnut Capital Partners', 'Software design and development for mobile, Mac and backend systems, Fairfax, Virginia', 'Managed IT & Cloud Services'),
        ('[[EM3 Networks|' + u('benchmark-international-facilitated-the-transaction-of-em3-networks-llc-and-capcon-networks') + ']]', 'Capcon Networks', 'Dedicated leased lit fiber for schools, hospitals and libraries nationwide', 'Telecom & UCaaS'),
        ('[[Clearline Networks|' + u('benchmark-international-successfully-facilitated-the-transaction-between-clearline-networks-llc-and-zeus-fire-and-security') + ']]', 'Zeus Fire and Security', 'Voice and data cabling, audiovisual and security systems in Tennessee and nearby states', 'Systems Integration'),
        ('[[High Tech Solutions - Systems Group|' + u('benchmark-international-successfully-facilitated-the-transaction-between-high-tech-solutions-systems-group-inc-and-ai-fire') + ']]', 'AI Fire', 'Fire alarm, security, access control and video surveillance systems in Montana and northern Wyoming', 'Systems Integration'),
        ('[[Sheffield Scientific|' + u('benchmark-international-successfully-facilitated-the-transaction-between-sheffield-scientific-and-trm') + ']]', 'TRM, a portfolio company of 424 Capital', 'Asset management consulting, IT upgrades and risk software for power generators', 'Systems Integration'),
        ('[[Paragon Manufacturing|' + u('benchmark-international-successfully-facilitated-the-transaction-between-paragon-manufacturing-corp-and-bluerock-global-private-equity') + ']]', 'BlueRock Global Private Equity', 'Build-to-print custom cables, harnesses, electro-mechanical assemblies and box builds', 'Electronics & Hardware'),
        ('[[Boostr|' + u('benchmark-international-successfully-facilitated-the-transaction-between-of-boostr-llc-and-balius-partners') + ']]', 'Balius Partners', 'Indoor and outdoor display assemblies for school and university sports programs', 'Electronics & Hardware'),
        ('[[A.T. Parker (Solar Electronics Company)|' + u('benchmark-international-successfully-facilitated-the-transaction-between-at-parker-inc-and-assessimus-group-gmbh') + ']]', 'Assessimus Group', 'Test equipment for electromagnetic compatibility laboratories, North Hollywood, California', 'Electronics & Hardware'),
        ('[[Laser Lens Tek (American Photonics)|' + u('benchmark-international-successfully-facilitated-the-transaction-between-laser-lens-tek-inc-and-bluerock-global-private-equity') + ']]', 'BlueRock Global Private Equity', 'Precision optical components and coatings for laser systems, Sarasota, Florida', 'Electronics & Hardware'),
        ('[[Complete Control Services|' + u('benchmark-international-successfully-facilitated-the-transaction-between-complete-control-services-inc-and-amtech-drives-inc') + ']]', 'Amtech Drives', 'Instrumentation, calibration and controls integration in southern New Jersey', 'Electronics & Hardware'),
        ('[[Invocon|' + u('benchmark-international-successfully-facilitated-the-transaction-of-invocon-inc-and-cemtrex-inc') + ']]', 'Cemtrex', 'Instrumentation and wireless sensing for satellites, launch vehicles and missile defense', 'Government Technology'),
    ]
    t = table('170px 140px 1fr 118px', ['Seller (linked)', 'Buyer as announced', 'What the seller does', 'Focus area'], rows, pad=4)
    body = '\n'.join([h2("Benchmark International's activity in these focus areas"), p(intro), p(buyers), t])
    return page('Technology Q4 2026: Benchmark International activity', 18, body)


# ============ REWARD / DISCOUNT ============
def p19():
    section('What buyers reward and discount')
    intro = ("Across the six focus areas, acquirers pay the most for revenue that recurs under contract and for capability that customers or regulators require, and they discount revenue that depends on one project, one customer or the owner personally. The specifics differ by focus area, and an owner or advisor can test a business against them well before a sale.")
    rows = [
        ('Managed IT & Cloud Services', 'A high share of revenue under managed service agreements; security services attached to them; low customer concentration; documented service desk processes', 'Hardware resale and project revenue; month-to-month agreements; a service desk that depends on the owner; one vendor or one large client'),
        ('Cybersecurity', 'Monitoring and response revenue under multi-year contracts; certified and cleared staff; customers in regulated industries; proprietary tools or methods', 'One-time assessments; resale of licenses at thin margins; dependence on one compliance mandate whose timing can change'),
        ('Telecom & UCaaS', 'Owned fiber or long-term network contracts; high take rates; low churn among business and institutional customers; a funded construction plan', 'Legacy copper and premises-based systems; commission revenue without contract ownership; subsidy-dependent construction without committed customers'),
        ('Systems Integration', 'Service, monitoring and managed revenue; technician density in a region; manufacturer certifications; repeat customers', 'Installation revenue tied to new construction cycles; one general contractor or one manufacturer; fixed-price backlog with thin margins'),
        ('Electronics & Hardware', 'Domestic or near-shore capacity; aerospace, defense and medical certifications; engineering content specified by customers; backlog that converts to shipments', 'One program or one customer; tariff costs that cannot be passed through; aging equipment; commodity assembly work'),
        ('Government Technology', 'Prime positions won in full and open competition; cleared staff; owned software and data rights; funded backlog with years remaining', 'Revenue under a set-aside status the buyer cannot keep; recompetes due within a year; subcontract positions controlled by another prime'),
    ]
    t = table('112px 1fr 1fr', ['Focus area', 'Buyers reward', 'Buyers discount'], rows, pad=4)
    prep = ("Sellers who prepare early capture more of the competition that the survey data describe. In the second quarter of 2026, 87% of transactions above $5 million attracted three or more offers, and sales in the lower middle market took 11 to 12 months to close ([[IBBA and M&A Source Market Pulse|" + IBBA_PR + "]]). "
            "A technology sale also carries steps that other industries do not have, because buyers will test contract assignability, software and data ownership, security practices and, for government work, the effect of a change in size status. An owner who expects to sell within three years should therefore have reviewed financial statements, a schedule of recurring revenue by contract and renewal date, and a second layer of management in place before the first buyer conversation.")
    lower = ('<div style="margin-top: 6px; display: flex; gap: 32px"><div style="width: 448px; display: flex; flex-direction: column; gap: 14px; text-align: justify">' + p(prep) + '</div>'
             '<div style="width: 240px; position: relative"><img src="' + PREP_PHOTO + '" alt="A technician working inside a laptop" style="position: absolute; left: 0; top: 4px; width: 240px; height: calc(100% - 22px); object-fit: cover"><div style="position: absolute; left: 0; bottom: 0; width: 240px; height: 18px; background: ' + GOLD + '"></div></div></div>')
    if lib.WEB:
        lower = p(prep)
    body = '\n'.join([h2('What buyers reward and what they discount'), p(intro), t, lower])
    return page('Technology Q4 2026: What buyers reward and discount', 19, body)


# ============ CONTACT ============
def p20():
    def office(name, l1, l2, tel, mail):
        return ('<div style="display: flex; flex-direction: column; align-items: center"><div style="font-family: ' + CINZEL + '; font-size: 23px; line-height: 34px; letter-spacing: 4px; margin-bottom: 6px">' + name + '</div>'
                '<div>' + l1 + '</div><div>' + l2 + '</div><div>' + tel + '</div>'
                '<a href="mailto:' + mail + '" style="margin-top: 4px; color: #C99A68; font-weight: 700; font-size: 8.5px; letter-spacing: 2px">' + mail + '</a></div>')
    body = (HEAD % {'title': 'Technology Q4 2026: Contact', 'wm': WATERMARK} + RUN +
            '<div data-fit="560" style="position: absolute; left: 48px; top: 230px; width: 720px; display: flex; flex-direction: column; gap: 22px">\n'
            '<div style="font-weight: 700; font-size: 10.5px; line-height: 16px; letter-spacing: 2.6px; text-transform: uppercase">Benchmark International Middle Market</div>\n' +
            h2('Considering a transaction in technology?') + '\n' +
            p('Our first step is always a confidential conversation exploring your goals, your company and your options.') + '\n'
            '<div style="margin-top: 10px; display: flex; gap: 32px; align-items: center">\n'
            '<div style="width: 344px; display: flex; flex-direction: column">\n'
            '<img src="' + CONTACT_PHOTO + '" alt="A team working together at laptops around a table" style="display: block; width: 344px; height: 178px; object-fit: cover">\n'
            '<div style="height: 18px; background: ' + GOLD + '"></div>\n</div>\n'
            '<div style="width: 344px; display: flex; align-items: center; gap: 20px">\n'
            '<img src="' + HEADSHOT + '" alt="Jared Hardin" style="display: block; width: 84px; height: 84px; border-radius: 50%">\n'
            '<div style="display: flex; flex-direction: column; gap: 2px">\n'
            '<div style="font-weight: 700; font-size: 12px; line-height: 20px; letter-spacing: 2.6px">JARED HARDIN</div>\n'
            '<div>Managing Director</div>\n<div>Benchmark International</div>\n<div>813-771-6675</div>\n<div>j.hardin@benchmarkintl.com</div>\n'
            '</div>\n</div>\n</div>\n</div>\n'
            '<div style="position: absolute; left: 0; top: 839px; width: 816px; height: 217px; background: #303030; color: #FFFFFF">\n'
            '<div style="position: absolute; left: 0; top: 26px; width: 816px; text-align: center; font-weight: 700; font-size: 10px; line-height: 14px; letter-spacing: 4px; color: ' + GOLD + '">HEADQUARTERS</div>\n'
            '<div style="position: absolute; left: 48px; top: 52px; width: 720px; height: 1px; background: ' + GOLD + '"></div>\n'
            '<div style="position: absolute; left: 48px; top: 70px; width: 720px; display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 24px; text-align: center; font-size: 9.5px; line-height: 16px; letter-spacing: 0.5px">\n' +
            office('AMERICAS', '4030 West Boy Scout Blvd.', 'Suite 500, Tampa, FL 33607', '+1 813 898 2350', 'US@BENCHMARKINTL.COM') +
            office('EUROPE', 'One New Bailey, 4 Stanley St.', 'Manchester, M3 5JL', '+44 (0) 161 359 4400', 'UK@BENCHMARKINTL.COM') +
            office('AFRICA', 'Airport Office Park, Freight Rd., Ground Floor', 'Runway 01, Cape Town Airport, 7525', '+27 (0) 21 300 2055', 'AFRICA@BENCHMARKINTL.COM') +
            '\n</div>\n</div>\n' + TAIL)
    return body


# ============ SOURCES ============
def sources_pages(start_no, groups, per_page_groups):
    """groups: ordered list of (heading, [(label,url),...]). per_page_groups: list of lists of headings."""
    if lib.WEB:
        out = ['<p>Every figure in this report is linked where it appears. The same sources are listed here by section, with the link text used in the report.</p>', '<div class="fine">']
        for hname, items in groups:
            out.append('<h4>%s</h4><ul>%s</ul>' % (html.escape(hname, quote=False), ''.join(
                '<li><a target="_blank" rel="noopener" href="%s">%s</a></li>' % (html.escape(u, quote=True), html.escape(l, quote=False)) for l, u in items)))
        out.append('<h4>Benchmark International</h4><ul><li>Transaction records and the engagement portfolio as of October 1, 2026</li>'
                   '<li>Announced transactions as published at <a target="_blank" rel="noopener" href="https://www.benchmarkintl.com/insights/completed-transactions/">benchmarkintl.com/insights</a>, each linked in the table of Benchmark International transactions</li>'
                   '<li>Listed-company multiples from <a target="_blank" rel="noopener" href="https://stockanalysis.com/">StockAnalysis</a>, each linked in the valuation section</li></ul></div>')
        return ['\n'.join(out)]
    pages = []
    for i, heads in enumerate(per_page_groups):
        blocks = []
        for hname in heads:
            items = dict(groups)[hname]
            links = '; '.join('<a href="%s">%s</a>' % (html.escape(u, quote=True), html.escape(l, quote=False)) for l, u in items)
            blocks.append('<div style="margin: 0 0 5px; font-weight: 700; font-size: 9.5px; line-height: 14px; letter-spacing: 1.6px; text-transform: uppercase; break-after: avoid">%s</div><p style="margin: 0 0 12px">%s</p>' % (html.escape(hname, quote=False), links))
        if i == len(per_page_groups) - 1:
            blocks.append('<div style="margin: 0 0 5px; font-weight: 700; font-size: 9.5px; line-height: 14px; letter-spacing: 1.6px; text-transform: uppercase; break-after: avoid">Benchmark International</div>'
                          '<p style="margin: 0 0 12px">Transaction records and the engagement portfolio as of October 1, 2026; announced transactions as published at <a href="https://www.benchmarkintl.com/insights/completed-transactions/">benchmarkintl.com/insights</a> and linked in the table on page 18; listed-company multiples from <a href="https://stockanalysis.com/">StockAnalysis</a>, each linked on page 17</p>')
        head = h2('Sources' if i == 0 else 'Sources, continued')
        lead = '<p style="margin: 0; text-align: justify; font-size: 11.5px; line-height: 17px">Every figure in this report is linked where it appears. The same sources are listed here by section, with the link text used in the report.</p>' if i == 0 else ''
        cols = '<div style="column-count: 2; column-gap: 32px; font-size: 10.5px; line-height: 15px; letter-spacing: 0.15px; text-align: left">' + ''.join(blocks) + '</div>'
        pages.append(page('Technology Q4 2026: Sources' + ('' if i == 0 else ', continued'), start_no + i, '\n'.join(x for x in [head, lead, cols] if x)))
    return pages
