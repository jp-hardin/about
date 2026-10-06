from lib import *
from pages_a import *

TXCOLS = '64px 190px 170px 1fr'
TXHEAD = ['Date', 'Target (linked)', 'Buyer', 'Detail and terms disclosed']


# ============ MANAGED IT & CLOUD ============
def p05():
    section('Managed IT & Cloud Services')
    b = band([('9.6%', 'Revenue growth at managed service providers in 2025, with adjusted EBITDA up 17.1%'),
              ('64', 'Managed service provider acquisitions announced worldwide in the first quarter of 2026'),
              ('19%+', 'Adjusted EBITDA margin at best-in-class IT solution providers for a sixth consecutive year')],
             'cloud', 'Line illustration of a cloud connected to two servers')
    parts = [
        colp("Managed service providers came into 2026 with their strongest operating results in several years. Revenue grew 9.6% in 2025 against 7.1% in 2024 and adjusted EBITDA grew 17.1%, the best-in-class providers earned adjusted EBITDA margins above 19% for a sixth consecutive year, and the enterprise value of the average IT solution provider rose about 15% ([[ConnectWise Service Leadership Index, June 23, 2026|" + SLI + "]])."),
        colp("Growth is harder to find at the level of the individual provider. In Kaseya's survey of more than 1,000 providers, 71% named winning new customers as their main challenge, 24% reported clients cutting IT budgets, and 16% reported difficulty hiring technicians against 9% a year earlier. Almost half ranked artificial intelligence and automation as their clients' leading need, yet 13% earn meaningful revenue from it ([[Kaseya 2026 State of the MSP Report|" + KASEYA + "]])."),
        colp("Cloud demand continues to widen the work available. Cloud infrastructure services revenue rose 43% in the second quarter ([[Synergy Research Group|" + SYNERGY + "]]) and Microsoft reported more than 30 million paid seats of Microsoft 365 Copilot ([[Microsoft|" + MSFT + "]]). Vendor licensing changes are also moving customers, and 11:11 Systems bought Ntirety as Broadcom's changes to its VMware partner program reshape how providers operate ([[ChannelE2E|https://www.channele2e.com/brief/1111-systems-acquires-ntirety-as-vmware-consolidation-continues/]])."),
        quote('A shift in valuations is visible, as providers with higher shares of managed services achieve superior multiples compared to traditional value-added resellers (VARs).',
              'Houlihan Lokey, [[December 2025 IT Services Market Update|' + HL_IT + ']]'),
        colp("Acquirers announced 64 managed service provider transactions worldwide in the first quarter of 2026 against 169 in all of 2025, and outside investors led 80% of them. Evergreen Services Group alone completed 47 acquisitions in 2025 ([[Omdia|" + OMDIA_MA + "]]). The 20 MSP of Plano, Texas reached its 49th acquisition in July 2026 ([[ChannelE2E|https://www.channele2e.com/brief/the-20-msp-acquires-sundance-networks-reaches-49-acquisitions]]) and buys providers with $1 million to $5 million of revenue using operating cash flow and bank debt ([[Omdia|" + OMDIA_20 + "]])."),
        colp("Sponsors are also trading the platforms themselves. AEA Investors bought a majority of Magna5 from NewSpring Holdings in February 2026 ([[PrivSource|https://www.privsource.com/acquisitions/deal/aea-investors-majority-invests-in-magna5-mwSNWX]]), Berkshire Partners invested in Thrive alongside Court Square in January 2025 ([[PrivSource|https://www.privsource.com/acquisitions/deal/vXSaDv]]), and Park Place Technologies completed its merger with Service Express to form a data center services business with $1.2 billion of annual revenue ([[Park Place Technologies|https://www.parkplacetechnologies.com/press-release/park-place-technologies-completes-merger-with-service-express/]])."),
        colp("Public companies are buying as well. Cognizant completed its purchase of Astreya in June 2026 and ePlus bought the assets of Daymark Solutions in August ([[Cognizant|https://news.cognizant.com/2026-06-22-Cognizant-Completes-Acquisition-of-Astreya,-Expanding-AI-Infrastructure-and-Managed-Services-Capabilities?asPDF=1]]; [[Channel Insider|https://www.channelinsider.com/channel-business/mergers-and-acquisitions/eplus-acquires-daymark-solutions-assets/]])."),
    ]
    body = '\n'.join([kicker('Managed IT & Cloud Services'),
                      h2('Consolidators are buying recurring revenue and the strongest providers are earning record margins'), b, columns(parts, 3)])
    return page('Technology Q4 2026: Managed IT & Cloud Services', 5, body)


def p06():
    section('Managed IT & Cloud Services: announced transactions')
    intro = ("Prices for managed service providers are almost never published, so the pattern of who is buying is the most useful public evidence. The transactions below show three kinds of acquirer at work: sponsor-backed platforms adding regional providers, sponsors buying the platforms from one another, and public companies buying capacity in cloud and artificial intelligence infrastructure operations.")
    rows = [
        ('Aug 2026', '[[Daymark Solutions (assets)|https://www.channelinsider.com/channel-business/mergers-and-acquisitions/eplus-acquires-daymark-solutions-assets/]]', 'ePlus', 'Microsoft cloud solution provider in New England; undisclosed'),
        ('Jul 2026', '[[Sundance Networks|https://www.channele2e.com/brief/the-20-msp-acquires-sundance-networks-reaches-49-acquisitions]]', 'The 20 MSP', 'Managed IT and security for customers in New Mexico, Philadelphia and New York; the buyer\'s 49th acquisition'),
        ('Jun 2026', '[[Astreya|https://news.cognizant.com/2026-06-22-Cognizant-Completes-Acquisition-of-Astreya,-Expanding-AI-Infrastructure-and-Managed-Services-Capabilities?asPDF=1]]', 'Cognizant', 'Managed IT services with about 2,600 employees; reported at approximately $600 million ([[Coverager|https://coverager.com/cognizant-to-acquire-astreya/]])'),
        ('Mar 2026', '[[phoenixNAP Phoenix data center and colocation business|https://www.privsource.com/acquisitions/deal/radiusdc-to-acquire-phoenixnap-phoenix-data-center-and-colocation-business-x7SWXO]]', 'RadiusDC', 'Colocation facility and campus development rights; announced, closing expected in the second quarter'),
        ('Feb 2026', '[[OnPar Technologies|https://rcpmag.com/blogs/rcp-channel-briefing/2026/02/net-at-work-acquires-onpar-technologies.aspx]]', 'Net at Work', 'Managed service provider; undisclosed'),
        ('Feb 2026', '[[Magna5|https://www.privsource.com/acquisitions/deal/aea-investors-majority-invests-in-magna5-mwSNWX]]', 'AEA Investors', 'Majority investment in a Pennsylvania managed IT and security platform; seller NewSpring Holdings'),
        ('Feb 2026', '[[Verinext|https://www.channelinsider.com/channel-business/mergers-and-acquisitions/arctiq-verinext-services-deal/]]', 'Arctiq, backed by Gallant Capital Partners', 'Managed services, hybrid infrastructure, networking and security; undisclosed'),
        ('Jan 2026', '[[Ntirety|https://www.channele2e.com/brief/1111-systems-acquires-ntirety-as-vmware-consolidation-continues/]]', '11:11 Systems', 'VMware-focused managed and professional services; undisclosed'),
        ('Jan 2026', '[[Service Express|https://www.parkplacetechnologies.com/press-release/park-place-technologies-completes-merger-with-service-express/]]', 'Park Place Technologies', 'Merger forming a data center services business with $1.2 billion of annual revenue'),
        ('Jul 2025', '[[Baroan Technologies|https://www.streetinsider.com/Press+Releases/Thrive+Acquires+Managed+IT+Provider+Baroan+Technologies/25084665.html]]', 'Thrive, backed by Berkshire Partners and Court Square', 'Managed service provider in northern New Jersey; undisclosed'),
        ('Jun 2025', '[[TechMD and 1nteger Security|https://www.streetinsider.com/PRNewswire/Integris+Amplifies+Position+as+a+Leading+Future-Ready+MSP+with+Strategic+Acquisition/24939729.html]]', 'Integris, backed by OMERS Private Equity', 'Northeast managed service provider founded in 1986; undisclosed'),
        ('Mar 2025', '[[Element Technologies|https://www.privsource.com/acquisitions/deal/rJSVwN]]', 'New Charter Technologies, backed by Oval Partners', 'Cybersecurity, automation and document management for the legal sector; undisclosed'),
    ]
    close = ("The published benchmarks point in one direction. Best-in-class providers reached record valuations in 2025 according to the Service Leadership Index ([[ConnectWise|" + SLI + "]]), and acquirers in this focus area pay the most for a high share of revenue under managed service agreements, security services attached to those agreements, low customer concentration and a service desk that runs without the owner.")
    body = '\n'.join([kicker('Managed IT & Cloud Services: announced transactions'),
                      h2('Platforms, sponsors and public companies are all buying'), p(intro),
                      table(TXCOLS, TXHEAD, rows, pad=4), p(close)])
    return page('Technology Q4 2026: Managed IT & Cloud Services transactions', 6, body)


# ============ CYBERSECURITY ============
def p07():
    section('Cybersecurity')
    IC3 = 'https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf'
    DBIR = 'https://www.techrepublic.com/article/news-verizon-dbir-vulnerability-exploitation-2026/'
    IBM = 'https://www.esecurityplanet.com/cybersecurity/ibm-2026-cost-of-a-data-breach-report-key-findings/'
    GSEC = 'https://www.gartner.com/en/newsroom/press-releases/2025-07-29-gartner-forecasts-worldwide-end-user-spending-on-information-security-to-total-213-billion-us-dollars-in-2025'
    b = band([('$20.9B', 'Cybercrime losses reported to the FBI in 2025, up 26% on 2024'),
              ('$240B', 'Forecast worldwide information security spending in 2026, up 12.5%'),
              ('48%', 'Share of breaches that involved a third party, up from 30% a year earlier')],
             'shield', 'Line illustration of a shield with a padlock')
    parts = [
        colp("Spending on security is growing faster than IT services as a whole. Gartner forecasts worldwide information security spending of $240 billion in 2026, 12.5% above 2025 ([[Gartner|" + GSEC + "]]), against 5.3% growth for IT services ([[Gartner|" + GARTNER + "]])."),
        colp("The loss data explain the budgets. The FBI received more than one million complaints in 2025 with reported losses of $20.9 billion, 26% more than in 2024 ([[FBI Internet Crime Complaint Center|" + IC3 + "]]). Verizon found ransomware present in 48% of breaches and a third party involved in 48%, up from 30% ([[Verizon 2026 DBIR via TechRepublic|" + DBIR + "]]), and IBM put the average cost of a breach in the United States at $11.5 million ([[IBM via eSecurity Planet|" + IBM + "]])."),
        colp("Staffing shortages push that spending toward outside providers. In the ISC2 workforce study, 59% of respondents described the skills gaps on their teams as critical or significant, against 44% a year earlier ([[ISC2 via SecurityInfoWatch|https://www.securityinfowatch.com/cybersecurity/article/55338497/cybersecurity-skills-gaps-now-outpace-headcount-shortages-isc2-workforce-study-finds]]). Acquisitions of managed security providers rose to 22% of all managed service provider transactions in the first quarter ([[Omdia|" + OMDIA_MA + "]])."),
        quote('After a Q1 marked by moderating deal value and no transactions over $1 billion, Q2 saw a clear return of megadeals on both the M&A and financing sides of the market.',
              'Houlihan Lokey, [[Q2 2026 Cybersecurity Quarterly Update|' + HL_CYBER + ']]'),
        colp("Ransomware remains the costliest event for smaller organizations. Sophos found a median ransom payment of $769,000 and an average recovery cost of $1.7 million among organizations hit in the past year ([[Sophos State of Ransomware 2026|https://www.sophos.com/blog/sophos-state-of-ransomware-2026]]), and the insurer Coalition reported that business email compromise and funds transfer fraud together made up 58% of the incidents in its 2025 claims ([[Coalition via Insurance-Canada|https://insurance-canada.ca/?p=85044]])."),
        colp("Regulation is a less dependable driver than it appeared a year ago. The Department of War suspended the third-party certification phase of CMMC on July 13, 2026, leaving self-assessment against NIST 800-171 in force while a task force reviews the program ([[DoD Chief Information Officer|" + CMMC + "]]). The final update to the HIPAA Security Rule has moved to 2027 at the earliest ([[Paubox|https://www.paubox.com/blog/hhs-pushes-final-hipaa-security-rule-update-to-2027]]), and CISA has yet to publish its final incident reporting rule for critical infrastructure ([[CISA|https://www.cisa.gov/topics/cyber-threats-and-advisories/information-sharing/cyber-incident-reporting-critical-infrastructure-act-2022-circia]])."),
        colp("Consolidation among service providers continued through the third quarter. LevelBlue, whose investors include SoftBank and Liberty Strategic Capital, completed its purchases of Trustwave and Cybereason in 2025 ([[LevelBlue|https://www.levelblue.com/newsroom/press-releases/levelblue-completes-acquisition-of-cybereason-expanding-global-leadership-in-managed-detection-and-response-xdr-and-incident-response]]), CyberMaxx acquired Avertium in September 2026 ([[MSSP Alert|https://www.msspalert.com/brief/cybermaxx-acquires-avertium-to-expand-managed-security-services]]), and Accenture agreed in June to buy a majority of the industrial security firm Dragos and all of two smaller companies for a combined $4.175 billion ([[SecurityWeek|https://www.securityweek.com/cybersecurity-ma-roundup-37-deals-announced-in-june-2026/]])."),
    ]
    body = '\n'.join([kicker('Cybersecurity'),
                      h2('Losses and staffing shortages are moving security budgets to outside providers'), b, columns(parts, 4)])
    return page('Technology Q4 2026: Cybersecurity', 7, body)


def p08():
    section('Cybersecurity: announced transactions')
    JUN = 'https://www.securityweek.com/cybersecurity-ma-roundup-37-deals-announced-in-june-2026/'
    JUL = 'https://www.securityweek.com/cybersecurity-ma-roundup-21-deals-announced-in-july-2026/'
    AUG = 'https://www.securityweek.com/cybersecurity-ma-roundup-33-deals-announced-in-august-2026/'
    intro = ("Software sets the headline prices in cybersecurity. The largest transactions in the table below were purchases of security software companies by Google, Palo Alto Networks and ServiceNow, while most of the managed security, consulting and compliance firms listed changed hands at undisclosed prices. SecurityWeek counted 33 cybersecurity transactions in August 2026 alone ([[SecurityWeek|" + AUG + "]]).")
    rows = [
        ('Sep 2026', '[[Avertium|https://www.msspalert.com/brief/cybermaxx-acquires-avertium-to-expand-managed-security-services]]', 'CyberMaxx', 'Managed security, Microsoft security services and compliance advisory; undisclosed'),
        ('Sep 2026', '[[AssurePoint|https://www.msspalert.com/brief/a-lign-acquires-assurepoint-to-expand-irap-services-in-australia]]', 'A-LIGN', 'Cloud security assessments in Australia; undisclosed'),
        ('Aug 2026', '[[At-Bay|' + AUG + ']]', 'Munich Re', 'Cyber insurer with managed detection services; $575 million'),
        ('Aug 2026', '[[CyberCatch|' + AUG + ']]', 'Datavault AI', 'Continuous compliance software; $94.5 million'),
        ('Jul 2026', '[[MDSec Consulting|' + JUL + ']]', 'Bank of America', 'UK information security consultancy with about 65 professionals; undisclosed'),
        ('Jul 2026', '[[Evo Security|' + JUL + ']]', 'Barracuda Networks', 'Identity and access software for managed service providers; undisclosed'),
        ('Jun 2026', '[[Dragos (majority), with runZero and NetRise|' + JUN + ']]', 'Accenture', 'Industrial and asset security; $4.175 billion combined'),
        ('Apr 2026', '[[Armis|https://itbrief.com.au/story/servicenow-completes-usd-7-75-billion-armis-acquisition]]', 'ServiceNow', 'Asset visibility and exposure management software; $7.75 billion in cash'),
        ('Mar 2026', '[[Wiz|https://itdaily.com/news/business/google-acquires-wiz/]]', 'Google', 'Cloud security software; $32 billion'),
        ('Feb 2026', '[[CyberArk|https://www.crnasia.com/news-network/2026/palo-alto-networks-completes-25b-acquisition-of-cyberark-for-identity-security-push]]', 'Palo Alto Networks', 'Identity security software; $25 billion in cash and stock'),
        ('Dec 2025', '[[Hornetsecurity|https://www.securityweek.com/proofpoint-completes-1-8-billion-acquisition-of-hornetsecurity/]]', 'Proofpoint', 'Microsoft 365 security sold through more than 12,000 managed service providers; $1.8 billion'),
        ('Nov 2025', '[[Cybereason|https://www.levelblue.com/newsroom/press-releases/levelblue-completes-acquisition-of-cybereason-expanding-global-leadership-in-managed-detection-and-response-xdr-and-incident-response]]', 'LevelBlue', 'Managed detection and incident response; undisclosed'),
        ('Aug 2025', '[[Trustwave|https://www.businesswire.com/news/home/20250819451116/en/LevelBlue-Completes-Acquisition-of-Trustwave-to-Form-the-Worlds-Largest-Managed-Security-Services-Provider]]', 'LevelBlue', 'Managed security services; undisclosed'),
        ('Feb 2025', '[[Secureworks|https://www.nasdaq.com/press-release/sophos-completes-secureworks-acquisition-2025-02-03]]', 'Sophos, backed by Thoma Bravo', 'Managed detection and response; about $859 million, or $8.50 a share'),
    ]
    close = ("One disclosed price is directly relevant to providers that sell through the channel. Proofpoint paid $1.8 billion for Hornetsecurity, whose annual recurring revenue was nearly $200 million and growing 20%, a price of about nine times recurring revenue by our calculation ([[SecurityWeek|https://www.securityweek.com/proofpoint-completes-1-8-billion-acquisition-of-hornetsecurity/]]). Services firms trade on EBITDA and at lower prices than software, and buyers pay most for monitoring and response revenue under multi-year contracts, cleared and certified staff, and a customer base in regulated industries.")
    body = '\n'.join([kicker('Cybersecurity: announced transactions'),
                      h2('Software commands the largest prices while services firms trade most often'), p(intro),
                      table(TXCOLS, TXHEAD, rows, pad=3), p(close)])
    return page('Technology Q4 2026: Cybersecurity transactions', 8, body)


# ============ TELECOM & UCAAS ============
RNG = 'https://www.sec.gov/Archives/edgar/data/0001384905/000138490526000043/rng-20260630x8kxex991.htm'
ZM = 'https://investors.zoom.us/news-releases/news-release-details/zoom-communications-reports-financial-results-second-quarter-0'
EGHT = 'https://www.investors.8x8.com/news-releases/news-release-details/8x8-inc-reports-record-revenue-first-quarter-fiscal-year-2027'
TSD = 'https://omdia.tech.informa.com/blogs/2026/jan/key-insights-from-the-16point6bn-dollars-technology-services-distribution-tsd-market'
SANDLER = 'https://www.channeldive.com/news/sandler-partners-independent-roots-private-equity/809263/'
ATT_LUMEN = 'https://www.fierce-network.com/broadband/atts-575b-lumen-deal-now-complete'
CABLEONE = 'https://broadbandbreakfast.com/cable-one-to-combine-fiber-jv-with-point-broadband-acquire-vyve/'


def p09():
    section('Telecom & UCaaS')
    b = band([('5.9%', 'Revenue growth at RingCentral in the second quarter of 2026'),
              ('26M', 'Microsoft Teams Phone users with public network calling, up 30% in 20 months'),
              ('$16.6B', 'Billings through technology services distributors in 2024, up 14.5%')],
             'tower', 'Line illustration of a transmission tower with signal arcs')
    parts = [
        colp("Cloud voice has become a steady, mid-single-digit growth business. RingCentral grew revenue 5.9% to $657 million in the second quarter ([[RingCentral|" + RNG + "]]), Zoom grew 4.9% with enterprise revenue up 7.8% ([[Zoom|" + ZM + "]]), and 8x8 grew 5% ([[8x8|" + EGHT + "]]). Microsoft's Teams Phone passed 26 million users with public network calling in late 2025 ([[UC Today|https://www.uctoday.com/microsoft-teams-phone-pstn-users-surges-to-26-million-up-30-in-20-months]])."),
        colp("Growth for the vendors now comes from artificial intelligence features sold to existing customers. RingCentral reported that 13% of its recurring revenue comes from customers using a paid AI product, double the share a year earlier ([[RingCentral|" + RNG + "]]). For resellers and regional providers the consequence is that customer relationships and support quality carry the value, since the underlying platforms are increasingly alike."),
        colp("Most business communications services reach customers through advisors. Billings through technology services distributors reached $16.6 billion in 2024, up 14.5%, and the six largest distributors hold 72.3% of the channel ([[Omdia|" + TSD + "]]). The four largest have each taken institutional investment, and Avant announced a recapitalization with Pamlico Capital and Court Square in late 2025 ([[Channel Dive|" + SANDLER + "]])."),
        quote('Consolidation is accelerating as sponsors pursue scale benefits, network densification, and operational synergies amid heightened investor focus on return thresholds and free cash flow generation.',
              'Houlihan Lokey, [[Q1 2026 Digital Infrastructure Industry Update|' + HL_DI + ']], on fiber broadband'),
        colp("The retirement of copper lines is creating replacement demand. The FCC voted unanimously in March 2026 to remove filing requirements from the copper retirement process ([[Telecompetitor|" + FCC_IP + "]]), and AT&T, which plans to retire most of its copper outside California by the end of 2029, received approval to discontinue service across more than 30% of that footprint ([[Broadband Breakfast|" + ATT_COPPER + "]]). Every analog line that carries an alarm panel, elevator phone or fax machine needs a replacement service."),
        colp("Fiber has drawn the largest sums. Verizon completed its roughly $20 billion purchase of Frontier in January 2026 ([[Converge Digest|https://convergedigest.com/verizon-completes-frontier-acquisition-expands-fiber-reach-to-30m-passings/]]), AT&T paid $5.75 billion for Lumen's consumer fiber business ([[Fierce Network|" + ATT_LUMEN + "]]), and Charter closed its $34.5 billion purchase of Cox in August ([[Light Reading|https://www.lightreading.com/cable-technology/charter-cox-deal-is-a-wrap-with-spectrum-brand-to-take-over-within-a-year]]). With all 50 state plans under the federal BEAD program approved, rural construction funding is moving from planning to building ([[Broadband Breakfast|" + BEAD + "]])."),
    ]
    body = '\n'.join([kicker('Telecom & UCaaS'),
                      h2('Infrastructure investors are buying fiber while cloud voice grows about 5% a year'), b, columns(parts, 3)])
    return page('Technology Q4 2026: Telecom & UCaaS', 9, body)


def p10():
    section('Telecom & UCaaS: announced transactions')
    intro = ("Regional fiber and broadband providers are being bought by platforms backed by infrastructure and private equity funds, and the national carriers have completed several large network purchases. Among business communications providers, the buyers are distributors and platforms adding service capability.")
    ROUND = 'https://bbcmag.com/september-2026-isp-roundup/'
    rows = [
        ('Oct 2026', '[[Fastwyre Broadband, Nebraska business|https://www.telecompetitor.com/rightfiber-completes-acquisition-of-fastwyre-broadbands-nebraska-business/]]', 'Rightfiber, a Grain Management company', 'Broadband in 26 communities; undisclosed'),
        ('Oct 2026', '[[MontanaSky|https://www.telecompetitor.com/vero-fiber-and-montanasky-complete-merger/]]', 'Vero Fiber (merger)', 'Internet provider in northwest Montana founded in 1993; undisclosed'),
        ('Sep 2026', '[[Granite State Communications|' + ROUND + ']]', 'TDS Telecom', 'Fiber and voice provider in New Hampshire with 11,000 service addresses; undisclosed'),
        ('Sep 2026', '[[CCI Network Services|https://www.channeldive.com/news/appdirect-adds-ai-avatars-to-its-technology-commerce-platform/831694/]]', 'AppDirect', 'Telecom provider forming a unified communications and customer experience practice; undisclosed'),
        ('Aug 2026', '[[Cox Communications|https://www.lightreading.com/cable-technology/charter-cox-deal-is-a-wrap-with-spectrum-brand-to-take-over-within-a-year]]', 'Charter Communications', '$34.5 billion'),
        ('May 2026', '[[Crown Castle fiber and small cell businesses|https://investor.crowncastle.com/node/29086]]', 'Zayo and Arium Networks, an EQT company', 'Fiber to Zayo and small cells to Arium; $8.5 billion combined'),
        ('Mar 2026', '[[GFiber and Astound (merger)|https://www.fierce-network.com/broadband/gfiber-merge-astound-after-alphabet-sells-majority-stake-private-equity]]', 'Stonepeak, with Alphabet retaining a minority', '7.1 million combined locations; announced, closing expected in the fourth quarter'),
        ('Feb 2026', '[[Lumen consumer fiber business|' + ATT_LUMEN + ']]', 'AT&T', '$5.75 billion for more than 4 million fiber locations and more than 1 million subscribers'),
        ('Jan 2026', '[[Frontier Communications|https://convergedigest.com/verizon-completes-frontier-acquisition-expands-fiber-reach-to-30m-passings/]]', 'Verizon', 'About $20 billion including assumed debt'),
        ('Jan 2026', '[[Mega Broadband Investments, remaining 55%|https://ir.cableone.net/news-events/investor-news/news-details/2026/Cable-One-to-Acquire-Full-Ownership-of-Mega-Broadband/default.aspx]]', 'Cable One', '$475 million to $495 million; about 675,000 locations passed; closing expected in October 2026'),
        ('Jan 2026', '[[Clearwave Fiber|' + CABLEONE + ']]', 'Point Broadband, backed by GTCR and Berkshire Partners', 'Combination passing more than 500,000 locations in 12 states; announced'),
        ('Sep 2025', '[[Tachus Fiber Internet|https://www.telecompetitor.com/ezee-fiber-announces-close-of-acquisition-of-tachus-fiber-internet/]]', 'Ezee Fiber, backed by I Squared Capital', 'Fiber provider in greater Houston; undisclosed'),
        ('Jul 2025', '[[Metronet|https://pulse2.com/kkr-metronet-acquisition-finalized-forming-jv-with-t-mobile-to-boost-fiber-expansion/amp/]]', 'KKR and T-Mobile joint venture', 'Fiber to 2.6 million homes and businesses in 19 states; undisclosed'),
    ]
    close = ("Fiber networks are priced on the locations they pass and the share of those locations that subscribe. AT&T's purchase from Lumen works out to roughly $1,400 for each location passed, on a network where about one location in four takes service, a calculation from the figures in the announcement ([[Fierce Network|" + ATT_LUMEN + "]]). A regional provider with higher take rates, long-term contracts with schools, hospitals and businesses, and a funded construction plan will be valued on those merits.")
    body = '\n'.join([kicker('Telecom & UCaaS: announced transactions'),
                      h2('National carriers closed large network purchases and funds are assembling regional platforms'), p(intro),
                      table(TXCOLS, TXHEAD, rows, pad=3), p(close)])
    return page('Technology Q4 2026: Telecom & UCaaS transactions', 10, body)


# ============ SYSTEMS INTEGRATION ============
AVIXA = 'https://www.commercialintegrator.com/news/avixa-releases-latest-insights-from-iota-report/143231/'
AVNET = 'https://www.avnetwork.com/news/avixa-forecast-will-pro-av-revenue-grow-through-2030'
CCONNECT = 'https://news.constructconnect.com/august-2026-data-center-report-construction-starts-total-22.3-billion-second-highest-on-record'
CENSUS = 'https://www.census.gov/construction/c30/pdf/release.pdf'
SIA_IDX = 'https://www.securityindustry.org/2026/06/24/new-security-industry-association-research-shows-80-of-professionals-see-positive-conditions-in-the-security-industry/'
AVISPL = 'https://ravepubs.com/26north-acquires-avi-spl/'
MYRIAD = 'https://www.channelinsider.com/channel-business/mergers-and-acquisitions/muriad360-advisex-ai-infrastructure/'
CI_AUG = 'https://www.channelinsider.com/channel-business/mergers-and-acquisitions/august-2026-ma-recap/'
CI_APR = 'https://www.channelinsider.com/channel-business/mergers-and-acquisitions/april-2026-ma-recap/'
CI_JAN = 'https://www.channelinsider.com/channel-business/mergers-and-acquisitions/january-2026-mergers-acquisitions/'


def p11():
    section('Systems Integration')
    b = band([('62.5%', 'Forecast growth in worldwide data center systems spending in 2026'),
              ('$81.5B', 'US data center construction starts in the first half of 2026, above all of 2025'),
              ('$402B', 'Forecast professional audiovisual revenue in 2030, from $332 billion in 2025')],
             'integrate', 'Line illustration of a monitor showing a connected network above three equipment racks')
    parts = [
        colp("Data center construction is the fastest-growing source of work for integrators. Gartner expects spending on data center systems to rise 62.5% to $822 billion in 2026 ([[Gartner|" + GARTNER + "]]), and Dell'Oro Group has raised its outlook for worldwide data center capital spending above $1 trillion ([[Dell'Oro Group|" + DELLORO + "]]). In the United States, data center construction starts totaled $81.5 billion in the first six months of the year against $72.5 billion in all of 2025 ([[ConstructConnect|" + CCONNECT + "]])."),
        colp("That work reaches cabling, low-voltage, security and network integrators as well as electrical contractors. Census figures show office construction, the category that includes data centers, running 24.6% above a year earlier in August while total construction spending was 1.7% lower ([[US Census Bureau|" + CENSUS + "]])."),
        colp("Outsourcing contracts show the same pull. Infrastructure-as-a-service contract value in the Americas rose 86% in the second quarter while traditional managed services contract value fell 12% ([[ISG Index|" + ISG + "]])."),
        colp("Audiovisual integration is growing more slowly. AVIXA forecasts professional audiovisual revenue of $402 billion in 2030 against $332 billion in 2025 ([[AVIXA via Commercial Integrator|" + AVIXA + "]]), a 3.9% annual rate that it lowered from 5.3% on tariffs and high interest rates ([[AV Network|" + AVNET + "]]). 26North agreed in June 2025 to buy control of AVI-SPL, a global integrator with about 4,400 employees, from Marlin Equity Partners ([[rAVe|" + AVISPL + "]])."),
        quote('Buyers prioritized platforms offering recurring, contract-backed service revenue and geographically dense technician networks, which effectively insulate platforms from macroeconomic headwinds and wage inflation.',
              'Houlihan Lokey, [[Q2 2026 Security and Safety Solutions Market Update|' + HL_SEC + ']]'),
        colp("Security integration is the most active part of the focus area. In the Security Industry Association's June survey, 80% of professionals rated business conditions good or excellent ([[Security Industry Association|" + SIA_IDX + "]]). Pavion, backed by Wind Point Partners, bought Communication Company in September 2026 ([[Pavion|https://www.webull.com/news/15543005417877504]]), Knox Lane took a majority of SAGE Integration ([[SDM Magazine|https://www.sdmmag.com/articles/105855-knox-lane-partners-with-sage-integration]]), and Everon acquired Scarsdale Security Systems ([[SDM Magazine|https://www.sdmmag.com/articles/105686-everon-expands-national-account-presence-with-acquisition-of-scarsdale-security-systems]])."),
        colp("Among IT integrators, buyers are assembling scale in infrastructure and adding certified practices in enterprise software. Myriad360 bought Advizex to form a business with more than $900 million of run-rate gross revenue ([[Channel Insider|" + MYRIAD + "]]), and recent purchases have targeted partners for Workday, ServiceNow and Sage Intacct ([[Channel Insider, April 2026|" + CI_APR + "]]; [[January 2026|" + CI_JAN + "]])."),
    ]
    body = '\n'.join([kicker('Systems Integration'),
                      h2('Data center construction and security upgrades are filling integrator backlogs'), b, columns(parts, 4)])
    return page('Technology Q4 2026: Systems Integration', 11, body)


def p12():
    section('Systems Integration: announced transactions')
    intro = ("Security and life-safety integrators account for most of the transactions below, and their buyers include private equity firms and the platforms they own. Houlihan Lokey counted 83 completed safety and security transactions worth nearly $6.0 billion in the second quarter of 2026, up from 72 worth $2.9 billion in the first ([[Houlihan Lokey|" + HL_SEC + "]]).")
    rows = [
        ('Oct 2026', '[[Sonitrol of El Paso|https://www.sdmmag.com/articles/105864-sonitrol-el-paso-is-now-part-of-securitas-technology]]', 'Securitas Technology', 'Regional electronic security firm; undisclosed'),
        ('Sep 2026', '[[SAGE Integration|https://www.sdmmag.com/articles/105855-knox-lane-partners-with-sage-integration]]', 'Knox Lane', 'Majority investment in a national security systems integrator; undisclosed'),
        ('Sep 2026', '[[Communication Company|https://www.webull.com/news/15543005417877504]]', 'Pavion, backed by Wind Point Partners', 'Midwest life safety, security, audiovisual and communications integrator founded in 1976; undisclosed'),
        ('Aug 2026', '[[Scarsdale Security Systems|https://www.sdmmag.com/articles/105686-everon-expands-national-account-presence-with-acquisition-of-scarsdale-security-systems]]', 'Everon', 'Commercial security and fire, Scarsdale, New York; about 100 employees; undisclosed'),
        ('Aug 2026', '[[Bangert|' + CI_AUG + ']]', 'Sage', 'Implementation partner for Sage Intacct Construction; undisclosed'),
        ('Apr 2026', '[[Intecrowd|' + CI_APR + ']]', 'UST', 'Workday implementation partner; undisclosed'),
        ('Feb 2026', '[[Advizex Technologies|' + MYRIAD + ']]', 'Myriad360', 'Enterprise infrastructure and managed services; combined run-rate gross revenue above $900 million'),
        ('Dec 2025', '[[Coastal Cloud|https://www.privsource.com/acquisitions/activity/buyout/it-services/2025]]', 'Tata Consultancy Services', 'Salesforce consultancy sold by Sverica Capital and its founders; $700 million; agreed'),
        ('Jun 2025', '[[AVI-SPL (controlling interest)|' + AVISPL + ']]', '26North Partners', 'Audiovisual and collaboration integrator with more than 4,400 employees; Marlin Equity Partners keeps a minority stake; undisclosed'),
        ('May 2025', '[[Fiber Solutions|https://www.sdmmag.com/articles/104310-convergint-acquires-fiber-solutions]]', 'Convergint', 'Fiber, structured cabling, security and audiovisual integrator, Fort Myers, Florida; undisclosed'),
        ('Feb 2025', '[[Fire Security & Sound Systems|https://www.sdmmag.com/articles/103996-sciens-acquires-fire-security-and-sound-systems-in-ny]]', 'Sciens Building Solutions', 'Fire alarm, security, nurse call and sound systems, Latham, New York; undisclosed'),
        ('Jan 2025', '[[AVCON|https://www.businesswire.com/news/home/20250106537109/en/AVI-Systems-Signs-Agreement-to-Acquire-North-Carolina-based-AVCON]]', 'AVI Systems', 'Audiovisual integrator, Cary, North Carolina, founded in 1997; undisclosed'),
    ]
    close = ("None of these announcements states a price against earnings, which is typical for integrators. The consistent point in buyer commentary is the mix of revenue: service agreements, monitoring and managed services are valued well above installation work, and buyers also weigh technician density in a region, manufacturer certifications and the share of work won from repeat customers.")
    body = '\n'.join([kicker('Systems Integration: announced transactions'),
                      h2('Sponsor-backed platforms are the most frequent buyers of integrators'), p(intro),
                      table(TXCOLS, TXHEAD, rows, pad=3), p(close)])
    return page('Technology Q4 2026: Systems Integration transactions', 12, body)
