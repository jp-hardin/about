#!/usr/bin/env python3
"""Static site generator for the Benchmark International Middle Market site.

Edit content in this file (sectors, team, stories) or in tombstones.json, then run:

    python3 mid-market-practice/_build/build.py

Pages are written to mid-market-practice/. No dependencies beyond the Python standard library.
"""
import json
import os
import re
from urllib.parse import urlparse
from html import escape, unescape

import pagecopy

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

PHONE = "813-771-6675"
PHONE_HREF = "tel:8137716675"
EMAIL = "mmt@benchmarkintl.com"
def _asset_version(rel):
    import hashlib
    with open(os.path.join(SITE, rel), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


HUBSPOT = {"region": "na1", "portalId": "4039078", "formId": "902fb6ab-81fb-42c4-abf8-5355537a8abb"}
AS_OF = "October 2026"

# Search and AI discovery. SITE_URL is the one place to change when the site moves (for example to HubSpot);
# canonical links, sitemap.xml, robots.txt, llms.txt, social previews and structured data all build from it.
# The sandbox (github.io) builds with its own address; the live preview and the live copy build with
# MMT_SITE_URL=https://mmt.benchmarkintl.com/ (set by the Stage live preview workflow).
SITE_URL = os.environ.get("MMT_SITE_URL", "https://jp-hardin.github.io/about/mid-market-practice/")
SITE_UPDATED = "2026-10-21"   # date stamp for sitemap.xml; update when content changes
ORG_NAME = "Benchmark International Middle Market"
PARENT_ORG = {"@type": "Organization", "@id": "https://www.benchmarkintl.com/#organization", "name": "Benchmark International",
              "url": "https://www.benchmarkintl.com/", "numberOfEmployees": {"@type": "QuantitativeValue", "minValue": 300},
              "address": {"@type": "PostalAddress", "streetAddress": "4030 W Boy Scout Blvd, Suite 500", "addressLocality": "Tampa",
                          "addressRegion": "FL", "postalCode": "33607", "addressCountry": "US"}}
REPORT_DATE = "2026-10"       # publication month of the current industry reports (ISO 8601)

# Report downloads: every "Download" button opens a short form (name, email, two opt-ins, agreement to the report
# terms). Each submission is added as a row to the "MMT Report Downloads" Google Sheet by the Apps Script web app in
# _build/forms/report-signups.gs. REPORT_FORM_URL is that web app's /exec address; while it is empty the form still
# gates the download but records nothing. REPORT_TERMS_VERSION is written into each row's Notes, so change it when
# the wording of report-terms.html or of the form's consent lines changes.
REPORT_FORM_URL = "https://script.google.com/macros/s/AKfycbyWqNQfWuW0IGHqsuDyAKeQBP2RSgcuWHhgJAxsFVR2Wg-y16KaXDYSQyenhe7isEJV/exec"
REPORT_TERMS_VERSION = "2026-10-28"

# Important Disclosures: shown on disclosures.html and printed as the last page of every industry report PDF
# (_build/reports/disclosures.py). Adapted from a peer firm's report disclosures; have Compliance confirm any
# change, and add Benchmark International's own regulatory status here if Compliance wants it stated.
DISCLOSURES = [
    "\u201cBenchmark International\u201d refers to the Benchmark International group of companies, which provide merger and acquisition advisory services to business owners through offices around the world. The Middle Market team is part of Benchmark International. Any reference to Benchmark International in this material includes its affiliated companies, as the context requires.",
    "Benchmark International and its affiliates may have had, may currently have, or may in the future have business relationships with companies named in this material, with potential parties to a transaction and their related persons, or with their competitors, customers, or suppliers. When Benchmark International is engaged to provide advisory services in a transaction, it acts only for its client in connection with that transaction.",
    "The distribution of this material in certain jurisdictions may be restricted by law, and accordingly, recipients of this material represent that they are able to receive it without contravention of any registration requirement or other legal restrictions in the jurisdictions in which they reside or in which they conduct business.",
    "This material does not contain all the information needed to assess any transaction. You must conduct your own investigations and analyses. Benchmark International does not provide valuations, appraisals, or fairness opinions, and does not provide accounting, tax, investment, regulatory, or legal advice to anyone. This material is for discussion and informational purposes only and is not a recommendation, offer, or solicitation for the purchase or sale of any security or an invitation or inducement to engage in any transaction or investment activity. Benchmark International obtained the information in this material from public filings, company announcements, published reports, and other third-party sources, together with its own transaction experience. Benchmark International has not independently verified such information, the information is current only as of the date stated, and no obligation is undertaken to provide updated or additional information. Transaction values, multiples, and other figures are as publicly reported, and the value of any private company depends on its own circumstances. No representation or warranty, expressed or implied, is made in relation to the fairness, accuracy, correctness, or completeness of the information, opinions, or conclusions expressed herein. All forward-looking statements herein involve assumptions and elements of subjective judgment and analysis and are not facts. Past transactions are not indicative of future results, and nothing in this material guarantees future results or performance.",
    "Company names, logos, and trademarks referenced in this material are the property of their respective owners and are used for identification only. Their use does not imply any affiliation with or endorsement by those owners.",
    "This material is only being distributed to, and only made available to, and directed at: (a) persons who are outside the United Kingdom; (b) persons in the United Kingdom who have professional experience in matters relating to investments falling within Article 19(5) of the UK Financial Services and Markets Act 2000 (Financial Promotion) Order 2005, as amended (the \u201cOrder\u201d); (c) high net worth entities and other persons to whom it may otherwise lawfully be communicated falling within Article 49(2)(a) to (d) of the Order; or (d) any other person to whom this material may otherwise lawfully be communicated or caused to be communicated (all such persons in (b) to (d) together being referred to as \u201cRelevant Persons\u201d). This material must not be acted on or relied on by persons in the United Kingdom who are not Relevant Persons. In the United Kingdom, any investment or investment activity to which this material relates is only available to, and will be engaged with, Relevant Persons.",
]




# Services offered on every sector page
SERVICES = [
    ("Sell-Side Mergers & Acquisitions", "Comprehensive advisory services for the sale of privately held businesses, including valuation analysis, transaction preparation, investment positioning, confidential buyer outreach, competitive bid management, negotiation, and transaction execution."),
    ("Controlling Ownership Transactions", "Advisory services for qualifying majority and other controlling ownership transfers to strategic acquirers, private equity firms, and family offices."),
    ("Strategic Buyer Identification & Engagement", "Identification, qualification, and engagement of strategic and financial acquirers pursuing qualifying business acquisitions."),
    ("Exit Readiness & Transaction Planning", "Comprehensive assessment of transaction readiness, valuation drivers, quality of earnings, financial reporting, management infrastructure, and potential diligence considerations."),
]

# Old 12-industry URLs → current industry page (redirect stubs keep any shared links working)
LEGACY = {
    "architecture-engineering": "business-services",
    "financial-services": "business-services",
    "construction": "industrial",
    "energy-utilities": "industrial",
    "environmental-recycling": "industrial",
    "transportation": "industrial",
    "consumer-food-retail": "consumer",
    "software": "technology",
}

# ─────────────────────────────────────────────────────────────────────────────
# Sectors
# `count` = completed transactions tagged to the matching industries on
# benchmarkintl.com/about/our-success (≈1,000 most recent closings, as of AS_OF):
#   Industrial = Industrial + Construction + Energy + Environmental + Transportation
#   Business Services = Business Products & Services + Architecture & Engineering + Financial
#   Consumer = Consumer, Food & Retail;  Healthcare = Healthcare;  Technology = Software + Technology
# ─────────────────────────────────────────────────────────────────────────────
SECTORS = [
    {
        "slug": "industrial",
        "name": "Industrials",
        "prose": "industrial markets",           # running-prose name ("valuation in industrial markets")
        "title_in": "Industrial Markets",        # Title Case heading form ("What We're Seeing in Industrial Markets")
        "adj": "industrial",                     # adjective before "transactions"
        "count": 290,
        "tagline": "Advising founder-led manufacturers, distributors, and industrial services businesses on strategic sales, mergers, and qualifying change-of-control transactions designed to maximize enterprise value and achieve shareholder objectives.",
        "short": "Manufacturing, industrial distribution, building products, energy and environmental services, and transportation.",
        "overview": [
            "Reshoring, automation, infrastructure investment, and the push for supply-chain resilience have put middle-market industrial companies at the top of many buyers' lists. Strategic acquirers want capabilities and capacity they can't build quickly. Private equity platforms want founder-built businesses with engineering know-how, sticky customers, and room to grow through add-ons.",
            "Our Industrial group advises owners of manufacturers, fabricators, distributors, and industrial service providers across five sectors. We translate machine capability, certifications, installed base, and customer relationships into the terms buyers use to value them, then run a competitive process that puts those qualities in front of the right strategic and financial partners.",
        ],
        "segments": [
            ("Manufacturing & Industrial Technology", "Engineered products and precision manufacturing where proprietary processes, certifications, and approved-vendor status create durable advantages.",
             ["Precision machining & fabrication", "Aerospace & defense components", "Electronics & microelectronics", "Plastics & molding", "Coatings & metal finishing", "Pumps, vacuum & flow control"]),
            ("Industrial Distribution & Services", "Value-added distributors and field-service providers with recurring maintenance revenue and dense local relationships.",
             ["Gases & specialty supplies", "Hydraulics & fluid power", "MRO & parts distribution", "Fire & life safety", "Industrial maintenance & turnarounds", "Material handling"]),
            ("Building Products & Construction Services", "Specialty trades, infrastructure contractors, and building-products businesses benefiting from infrastructure spending and non-residential construction.",
             ["Mechanical, electrical & plumbing", "Roofing & exteriors", "Infrastructure & marine construction", "Crane & equipment services", "Building products distribution", "Testing & inspection"]),
            ("Energy, Power & Environmental Services", "Businesses serving power generation, water, energy transition, and regulated environmental markets with non-discretionary demand.",
             ["Power generation & backup power", "Energy consulting", "Water treatment & chemicals", "Environmental & emergency response", "Recycling & waste services"]),
            ("Transportation & Logistics", "Carriers, 3PLs, and specialized logistics providers with diversified shippers and capabilities buyers cannot easily replicate.",
             ["Dedicated & intermodal trucking", "3PL & customs brokerage", "Export crating & rigging", "Pallets & packaging logistics", "Marine & subsea"]),
        ],
        "themes": [
            ("Reshoring and supply-chain resilience", "Customers are qualifying domestic suppliers and dual sources, which raises the value of certified capacity and long-standing OEM relationships."),
            ("Platform building by private equity", "Sponsors keep assembling industrial platforms through add-on acquisitions, creating competitive tension for well-run founder-owned businesses."),
            ("Infrastructure and electrification", "Spending on infrastructure, grid modernization, and water is lifting demand for specialty contractors, power services, and environmental providers."),
            ("Service and aftermarket revenue", "Buyers pay a premium for recurring maintenance, repair, and aftermarket revenue that smooths project and capital-spending cycles."),
        ],
        "value": [
            ("Engineering know-how", "Proprietary processes, certifications such as AS9100 and ISO, and engineered-to-order capabilities."),
            ("Customer stickiness", "Approved-vendor status, long OEM relationships, and recurring service agreements."),
            ("Capacity & equipment", "Modern equipment, documented maintenance, and room for a buyer to add volume."),
        ],
    },
    {
        "slug": "business-services",
        "name": "Business Services",
        "prose": "business services",
        "title_in": "Business Services",
        "adj": "business services",
        "count": 230,
        "tagline": "Advising owners of commercial, professional, and tech-enabled service businesses with recurring revenue and loyal clients.",
        "short": "Commercial and facility services, marketing and tech-enabled services, engineering and consulting, financial and insurance services, and staffing and human capital.",
        "overview": [
            "Business services is one of the most active and diverse areas of middle-market M&A. Buyers look for recurring or repeat revenue, a diversified client base, scalable delivery, and a management team that can support growth. Those qualities attract strategic consolidators and private equity firms building platforms through acquisition.",
            "Our Business Services group represents commercial and facility services providers, marketing and tech-enabled service firms, engineering and consulting practices, financial and insurance services businesses, and staffing and human capital firms. We frame contracts, retention, utilization, and margin profile the way buyers evaluate them, and we know which consolidators and sponsors are active in each niche.",
        ],
        "segments": [
            ("Commercial & Facility Services", "Route-based, compliance-driven, and contracted services where recurring revenue and density create value.",
             ["Fire protection & life safety", "Managed print & document services", "Testing, inspection & certification", "Security services", "Painting & property maintenance"]),
            ("Marketing, Sales & Technology-Enabled Services", "Agencies, outsourced sales, and technology consultancies that help clients grow, often with long relationships and embedded workflows.",
             ["Outsourced sales & brokerage", "Promotional products", "Digital strategy & consulting", "Education technology consulting", "Display & signage"]),
            ("Engineering, Architecture & Consulting", "Licensed professional-services firms whose talent, backlog, and public-sector relationships attract national platforms.",
             ["Civil & transportation engineering", "Architecture", "Surveying & geospatial", "Forensic engineering", "BIM & reality capture"]),
            ("Financial & Insurance Services", "Fee-based financial businesses with recurring commissions, renewals, and high client retention.",
             ["Insurance brokerage & MGAs", "Claims adjusting", "Appraisal management", "Wealth & financial planning", "Trading technology"]),
            ("Staffing & Human Capital", "Staffing, search, and workforce solutions firms with repeat client relationships, deep candidate networks, and recurring placement revenue.",
             ["Commercial & light industrial staffing", "Professional & technical staffing", "Executive search", "Recruitment process outsourcing", "Talent development & HR consulting"]),
        ],
        "themes": [
            ("Consolidation by sponsor-backed platforms", "National platforms in fire and life safety, engineering, insurance, and facility services continue to acquire founder-owned firms to add density and capabilities."),
            ("Premium for recurring revenue", "Contracted, subscription, and inspection-driven revenue earns higher multiples than project work, so how revenue is presented matters."),
            ("Talent as a strategic asset", "In professional services, licensed people and their client relationships drive value, which puts retention planning and deal structure at the center of the process."),
            ("Tech enablement", "Firms that use technology to deliver services more efficiently, or to give clients better data, stand out to buyers seeking scalable models."),
        ],
        "value": [
            ("Recurring revenue", "Contracted, subscription, inspection, or renewal revenue with demonstrated retention."),
            ("Client diversification", "Long-tenured relationships without outsized concentration."),
            ("Scalable operations", "Systems, KPIs, and leadership that can support add-on acquisitions."),
        ],
    },
    {
        "slug": "consumer",
        "name": "Consumer",
        "prose": "consumer markets",
        "title_in": "Consumer Markets",
        "adj": "consumer",
        "count": 80,
        "tagline": "Advising founders of food, restaurant, consumer brand, foodservice, and consumer services businesses.",
        "short": "Food and beverage (including restaurants), consumer brands and products, foodservice and distribution, and consumer services.",
        "overview": [
            "Buyers of consumer businesses look for brands with pricing power, loyal customers, channel diversity, and room to grow distribution. Strategic acquirers use acquisitions to add brands, categories, and capabilities. Consumer-focused private equity firms and family offices back founders who have built a differentiated product and want a partner to scale it.",
            "Our Consumer group represents food and beverage producers, restaurant groups, consumer brand owners, foodservice suppliers and distributors, and multi-site consumer services businesses. We present the brand's story, unit economics, and growth runway in the way buyers underwrite them.",
        ],
        "segments": [
            ("Food & Beverage", "Food and beverage producers and distributors with quality certifications and loyal wholesale and retail customers, and multi-unit restaurant and catering groups.",
             ["Bakery & specialty foods", "Dairy & ingredients distribution", "Seafood import & processing", "Nutritional supplements", "Confectionery", "Restaurants & catering"]),
            ("Consumer Brands & Products", "Branded products with recognized names, enthusiast followings, and multi-channel distribution.",
             ["Outdoor & recreation", "Beauty & wellness", "Sporting goods & accessories", "Flags & specialty manufacturing", "Containers & storage"]),
            ("Foodservice & Distribution", "Restaurant equipment, parts, supplies, and service providers, and the distributors that keep restaurants, hospitality, and retail operating.",
             ["Restaurant equipment & supplies", "Commercial coffee equipment", "Outdoor kitchen appliances", "CPG sales agencies", "Dealer distribution"]),
            ("Consumer Services & Retail", "Multi-site and route-based consumer services with recurring local demand.",
             ["Car wash & auto care", "Collision repair", "Equipment rental & storage", "Home services"]),
        ],
        "themes": [
            ("Brands with pricing power", "Buyers favor brands that have held price and volume through inflation, and that can show it in their data."),
            ("Omnichannel growth", "Businesses balanced across wholesale, retail, foodservice, and e-commerce are less exposed to any single channel and easier to scale."),
            ("Strategic portfolio building", "Strategic acquirers buy niche brands and distribution businesses to fill category gaps faster than they could build them."),
            ("Multi-site consolidation", "Consumer services categories such as car wash, collision repair, and home services keep consolidating under sponsor-backed platforms."),
        ],
        "value": [
            ("Brand equity", "Recognized brands, loyal customers, and demonstrable pricing power."),
            ("Channel diversity", "Balanced exposure across retail, foodservice, e-commerce, and wholesale."),
            ("Margin & capacity", "Gross-margin resilience and production or distribution capacity a buyer can fill."),
        ],
    },
    {
        "slug": "healthcare",
        "name": "Healthcare",
        "prose": "healthcare",
        "title_in": "Healthcare",
        "adj": "healthcare",
        "count": 55,
        "tagline": "Advising healthcare providers, life sciences and medical products companies, and pharmacy and healthcare services businesses.",
        "short": "Provider services, life sciences and diagnostics, medical products and distribution, and pharmacy and healthcare services.",
        "overview": [
            "Healthcare remains one of the most resilient and actively consolidated industries in the middle market. Demand is steady and growing, and health systems, public strategics, and private equity platforms continue to acquire providers and suppliers to extend their reach.",
            "Our Healthcare group represents physician and therapy practices, urgent care operators, laboratories, medical device and product companies, and pharmacy and healthcare services businesses. We show buyers the clinical quality, payer mix, and growth behind each business while managing the regulatory and diligence complexity these transactions bring.",
        ],
        "segments": [
            ("Provider Services", "Clinics, practices, and care providers with strong referral relationships and clinical reputations.",
             ["Urgent care", "Optometry & eye care", "Pediatric & physical therapy", "Multi-specialty medical groups", "Emergency medical services", "Renal care"]),
            ("Life Sciences & Diagnostics", "Laboratories, research sites, and product-development firms serving pharma, biotech, and device companies.",
             ["Clinical & pathology labs", "Biologics & reagents", "Clinical research sites", "Human-factors & device design"]),
            ("Medical Products & Distribution", "Manufacturers and distributors of medical devices, consumables, and equipment.",
             ["Surgical instrument reprocessing", "Emergency medical supplies", "Respiratory & anesthesia products", "Dental devices", "Orthopedic products"]),
            ("Pharmacy & Healthcare Services", "Pharmacy, infusion, staffing, and logistics businesses supporting providers and patients.",
             ["Specialty & mail-order pharmacy", "Home infusion", "Pharmaceutical delivery", "Clinical staffing"]),
        ],
        "themes": [
            ("Health system consolidation", "Hospital systems and national operators keep adding outpatient and urgent care sites to capture patients closer to home."),
            ("Outsourcing and specialization", "Providers and pharma companies increasingly outsource labs, research, staffing, and logistics to specialists."),
            ("Strategic interest in med-tech niches", "Public strategics acquire focused device and product companies to add patented technology and clinical relationships."),
            ("Care moving to the home", "Home infusion, home care, and delivery services benefit as care shifts away from inpatient settings."),
        ],
        "value": [
            ("Payer & revenue quality", "A balanced payer mix and clean revenue-cycle performance."),
            ("Clinical reputation", "Quality outcomes, referral relationships, and regulatory standing."),
            ("Platform scalability", "Systems and leadership ready for new sites and add-on acquisitions."),
        ],
    },
    {
        "slug": "technology",
        "name": "Technology",
        "prose": "technology",
        "title_in": "Technology",
        "adj": "technology",
        "count": 105,
        "tagline": "Advising founders of software, IT services, and technology businesses with recurring revenue and mission-critical products.",
        "short": "Vertical software, enterprise and infrastructure software, IT and managed services, and communications and hardware.",
        "overview": [
            "Vertical software and mission-critical technology businesses command some of the strongest buyer interest in the market. Software consolidators, strategic acquirers, and private equity firms compete for products that are deeply embedded in customer workflows, with recurring revenue and high switching costs.",
            "Our Technology group has represented pharmacy software, field-service, lending, CAD/CAM, and IT management platforms, as well as managed service providers and technology consultancies. We know how to present ARR, retention, unit economics, and the product roadmap, and we bring buyers ranging from software holding companies to large-cap private equity.",
        ],
        "segments": [
            ("Vertical Software", "Industry-specific software that runs critical workflows for its customers.",
             ["Pharmacy & healthcare software", "Field service management", "Lending & financial software", "CAD/CAM & manufacturing software", "Marketing analytics"]),
            ("Enterprise & Infrastructure Software", "Horizontal software for IT, data, and communications teams.",
             ["Endpoint & desktop management", "Database performance", "Email & communications governance"] ),
            ("IT & Managed Services", "IT providers and software development firms with contracted and recurring revenue.",
             ["Managed IT for education", "Microsoft-stack consulting", "Custom software development", "Data conversion & migration", "Government training & simulation"]),
            ("Communications & Hardware", "Telecom, electronics, and specialized technology talent businesses.",
             ["Cloud communications", "Telecom services", "Optical inspection systems", "Cybersecurity & IT staffing"]),
        ],
        "themes": [
            ("Software consolidators", "Serial acquirers of vertical software are active buyers of founder-led companies with loyal niche customer bases."),
            ("Sponsor appetite for recurring revenue", "Private equity continues to favor ARR, high net revenue retention, and low churn."),
            ("AI and data", "Buyers are looking for proprietary data and workflows that position a product to benefit from AI rather than be displaced by it."),
            ("Managed services and security", "Demand for managed IT and cybersecurity keeps pulling platforms toward MSPs with contracted revenue and certified talent."),
        ],
        "value": [
            ("Recurring revenue", "ARR growth, net revenue retention, and low churn."),
            ("Mission-critical product", "Deep workflow integration and high switching costs."),
            ("Scalable unit economics", "Efficient customer acquisition and a credible product roadmap."),
        ],
    },
]
SECTOR_BY_SLUG = {s["slug"]: s for s in SECTORS}

# Industry reports are kept off the site until the final versions are ready. While this is False the build writes
# no Insights page, report pages, PDFs or old report addresses, removes any already in the site folder, and drops
# every link, button, sitemap entry and llms.txt line that points to them. Set True and rebuild the reports to publish.
# The github.io preview always shows the reports. The live copy (the Publish MMT site workflow) builds with
# MMT_REPORTS=off until the reports are released there, which hides them as described in CLAUDE.md.
REPORTS_LIVE = os.environ.get("MMT_REPORTS", "on") != "off"

# ─────────────────────────────────────────────────────────────────────────────
# Insights: quarterly industry reports. Add a new entry each quarter; the newest
# report per industry becomes "Current" and older ones move to the archive.
# Report pages and PDFs are generated by _build/reports/<folder>/ into insights/.
# `legacy` is the report's old reports/ filename, kept as a redirect.
# ─────────────────────────────────────────────────────────────────────────────
INSIGHTS = [
    {"sector": "industrial", "quarter": 4, "year": 2026, "slug": "industrial-industry-report-q4-2026", "legacy": "industrial-q4-2026",
     "title": "Industrials Q4 2026 M&A Industry Report",
     "summary": "Manufacturing and industrial technology; distribution and services; building products and construction services; energy, power and environmental services; and transportation and logistics: the order books, the deal market, and what acquirers are paying for."},
    {"sector": "business-services", "quarter": 4, "year": 2026, "slug": "business-services-industry-report-q4-2026", "legacy": "business-services-q4-2026",
     "title": "Business Services Q4 2026 M&A Industry Report",
     "summary": "Commercial and facility services; marketing, sales and tech-enabled services; engineering, architecture and consulting; financial and insurance services; and staffing and human capital: the deal market, public-market valuations, and what buyers are paying for."},
    {"sector": "consumer", "quarter": 4, "year": 2026, "slug": "consumer-industry-report-q4-2026", "legacy": "consumer-q4-2026",
     "title": "Consumer Q4 2026 M&A Industry Report",
     "summary": "Food and beverage (including restaurants), consumer brands and products, foodservice and distribution, and consumer services and retail: who is buying, what they are paying for, and what an owner can prepare."},
    {"sector": "healthcare", "quarter": 4, "year": 2026, "slug": "healthcare-industry-report-q4-2026", "legacy": "healthcare-q4-2026",
     "title": "Healthcare Q4 2026 M&A Industry Report",
     "summary": "Provider services, life sciences and diagnostics, medical products and distribution, and pharmacy and healthcare services: the deal market, the policy calendar, and what buyers are paying for."},
    {"sector": "technology", "quarter": 4, "year": 2026, "slug": "technology-industry-report-q4-2026", "legacy": "technology-q4-2026",
     "title": "Technology Q4 2026 M&A Industry Report",
     "summary": "Managed IT and cloud services, cybersecurity, telecom and UCaaS, systems integration, electronics and hardware, and government technology: the deal market, the policy calendar, and what buyers are paying for."},
]
for _i in INSIGHTS:
    # A report built from a PowerPoint industry report deck (reports/<folder>/brief.pptx) is summarized by its cover sentence.
    _brief = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", f"{_i['sector']}-q{_i['quarter']}-{_i['year']}", "brief.json")
    if os.path.exists(_brief):
        _i["summary"] = json.load(open(_brief, encoding="utf-8"))["lead"]
    _i["period"] = f"Q{_i['quarter']} {_i['year']}"
    _i["url"] = f"insights/{_i['slug']}.html"
    _i["pdf"] = f"insights/{_i['slug']}.pdf"


def current_report(slug):
    reports = [i for i in INSIGHTS if i["sector"] == slug]
    return max(reports, key=lambda i: (i["year"], i["quarter"])) if reports else None


PUBLISHED_REPORTS = INSIGHTS if REPORTS_LIVE else []

for _s in SECTORS:
    _cur = current_report(_s["slug"])
    if _cur and REPORTS_LIVE:
        _s["report"] = (f"{_cur['period']} Industry Report", _cur["url"])

# ─────────────────────────────────────────────────────────────────────────────
# Team
# ─────────────────────────────────────────────────────────────────────────────
TEAM_LEAD = [
    ("Jordan Houtz", "Managing Director | Head of Middle Market", "jordan-houtz",
     ["As Managing Director and Head of Middle Market, Jordan represents clients with total enterprise values (TEV) ranging from $50 million to $500 million across the United States. He is a seasoned investment banker with more than 15 years of experience originating and executing complex domestic and cross-border M&A transactions for corporate and private equity clients.",
      "His deep experience on both the buy and sell sides of M&A transactions gives his clients a unique advantage in understanding deal dynamics and achieving their objectives. By leading full-cycle processes from idea and thesis generation through valuation, diligence, and negotiation, he stays closely involved in every stage of his clients’ transactions. Jordan builds lasting client relationships and stays focused on the outcomes that matter to them."]),
    ("Jared Hardin", "Managing Director", "jared-hardin",
     ["As Managing Director, Jared is the first team member an owner works with. He walks owners through their options as they consider and plan their next step.",
      "Jared spent more than 20 years as a C-suite executive and business owner, leading sales, marketing, technology, operations, and finance. He has also worked with hundreds of owners of industrial, healthcare, business services, consumer, and technology companies. That background uniquely positions him to understand the challenges owners face and show them how buyers evaluate a business, the range buyers would likely pay, and the paths open to them."]),
    ("Alex Zykov", "Transaction Director", "alex-zykov",
     ["As a Transaction Director, Alex leads the execution of our clients’ transactions from onboarding through signing and closing. He oversees every aspect of the process for middle-market clients across the industrial, consumer, business services, healthcare, and technology industries. He makes sure clients understand each step and feel confident along the way, supporting them and our team through due diligence, evaluating competing offers, and leading negotiations through to the finish line.",
      "Alex’s career spans corporate development, executing transactions on Wall Street, and cofounding and running boutique advisory firms serving small and mid-sized businesses. Each step was deliberate: building the breadth of knowledge and experience needed to give his clients the best possible advice and help them achieve their goals. He discovered his passion for corporate finance at MIT, where he earned dual degrees in Economics and Management Science, and later earned his MBA from the University of Virginia’s Darden School of Business."]),
    ("Shannon Hess", "Client Engagement Director", "shannon-hess",
     ["Shannon grew up in a military family, living on Army bases until she was nine years old. She enjoyed living in Germany and Hawaii and traveling to many wonderful places. Growing up in a military family meant a disciplined way of life, with importance placed on punctuality, respect, and loyalty.",
      "Shannon works with our Field Directors and with owners who are considering working with us. She is an additional point of contact for clients who want another perspective or someone to talk through their concerns. She has been with Benchmark International long enough to see many deals through from start to finish, and she draws on that experience to answer any questions clients have."]),
]
# Team contact details (phone, email); use None for a missing value. Anything missing shows the team line or team email.
TEAM_CONTACT = {
    "jordan-houtz": ("813-771-6675", "jhoutz@benchmarkintl.com"),
    "jared-hardin": ("210-241-7990", "j.hardin@benchmarkintl.com"),
    "alex-zykov": ("813-898-2372", "azykov@benchmarkintl.com"),
    "shannon-hess": ("813-898-2397", "hess@benchmarkintl.com"),
    "sunny-garten": ("813-898-2357", "garten@benchmarkintl.com"),
    "michael-wynn": ("813-384-4972", "mwynn@benchmarkintl.com"),
    "jason-lisiak": (None, "jlisiak@benchmarkintl.com"),
    "alexandra-barr": ("813-387-6046", "abarr@benchmarkintl.com"),
    "josiah-warren": ("813-898-2398", "jwarren@benchmarkintl.com"),
    "luke-ernst": ("813-771-6318", "lernst@benchmarkintl.com"),
}
# Personal LinkedIn profile URLs, keyed like TEAM_CONTACT. Anyone not listed has no LinkedIn row.
TEAM_LINKEDIN = {
    "jordan-houtz": "https://www.linkedin.com/in/jordanhoutz",
    "jared-hardin": "https://www.linkedin.com/in/jared-p-hardin",
    "alex-zykov": "https://www.linkedin.com/in/alex-zykov-787646b",
    "shannon-hess": "https://www.linkedin.com/in/shannon-l-hess",
    "sunny-garten": "https://www.linkedin.com/in/sunny-yang-garten-28a11010",
    "michael-wynn": "https://www.linkedin.com/in/michael-wynn-009",
    "jason-lisiak": "https://www.linkedin.com/in/jplisiak",
    "alexandra-barr": "https://www.linkedin.com/in/alexandra-barr-400531104",
    "josiah-warren": "https://www.linkedin.com/in/josiah-warren",
    "luke-ernst": "https://www.linkedin.com/in/lukesernst",
}
PHONE_PLACEHOLDER = "XXX-XXX-XXXX"
LINKEDIN_PLACEHOLDER = "linkedin.com/in/your-profile"
EMAIL_PLACEHOLDER = "name@benchmarkintl.com"

# Team filter groups, in display order
TEAM_GROUPS = [("leadership", "Leadership"), ("deal-team", "Deal Team"), ("transaction-support", "Transaction Support")]
TEAM_GROUP_OF = {"alexandra-barr": "transaction-support", "josiah-warren": "transaction-support"}

TEAM_SUPPORT = [
    ("Sunny Garten", "Senior Deal Associate", "sunny-garten"),
    ("Michael Wynn", "Senior Deal Associate", "michael-wynn"),
    ("Jason Lisiak, CFA", "Research Associate", "jason-lisiak"),
    ("Alexandra Barr", "Transaction Support Associate", "alexandra-barr"),
    ("Josiah Warren", "Transaction Support Associate", "josiah-warren"),
    ("Luke Ernst", "Deal Analyst", "luke-ernst"),
]

# Profile window bios for the support team, keyed by image slug.
TEAM_SUPPORT_BIO = {
    "sunny-garten": ["Sunny runs the daily work of a client\u2019s sale alongside the Transaction Director, from market launch through closing. She is the person owners call with questions; she also prepares management meetings with buyers and keeps offers and due diligence on schedule. A native of Beijing, she holds a BA in Business Administration from the University of International Relations and an MS from the Illinois Institute of Technology, and brings experience in financial analysis, negotiation, and cross-border investment."],
    "michael-wynn": ["As a Senior Deal Associate, Michael partners with business owners from market launch through a signed purchase agreement, guiding buyer conversations and competing offers through due diligence and final negotiations. He has worked on more than 220 transactions in corporate M&A at Alliant, a top five insurance brokerage with over $6 billion in revenue, and at PCF Insurance Services, an HGGC portfolio company that exited on the strength of its unprecedented growth through M&A. Michael also has experience in quality of earnings (QofE) and post-close integration, and holds a B.S. in Accounting from Florida State University."],
    "jason-lisiak": ["Jason is responsible for research across the firm\u2019s M&A practice and brings extensive institutional investment experience to each engagement. He previously served as a Senior Research Analyst and co-portfolio manager of the real estate and small-cap funds at a $20 billion institutional asset manager. He applies that buy-side perspective on behalf of sellers, analyzing industry dynamics, competitive landscapes, and strategic positioning to help clients realize the full value of their businesses. A CFA charterholder and member of CFA Society Tampa Bay, Jason holds a B.S. from SUNY Geneseo. He also coaches founders at the University of Tampa\u2019s Lowth Entrepreneurship Center."],
    "alexandra-barr": ["As a Transaction Support Associate, Alexandra helps business owners prepare their companies for market. She analyzes financial statements and operating data, develops buyer materials, and works with clients and their finance teams to address questions that may arise during due diligence. Her work helps buyers understand a company’s performance, operations, and growth opportunities.",
                       "Before joining Benchmark, Alexandra worked in finance at Volkswagen Group of America, evaluating profitability across multiple vehicle programs in domestic and international markets. Her experience spans pricing strategy, investment analysis, and developing business cases to inform executive decisions. She holds a B.S. in Industrial Engineering from West Virginia University."],
    "josiah-warren": ["As an associate on the Middle Market team, Josiah conducts the financial and operational review that precedes a client\u2019s launch to market, analyzing historical performance, building financial models, and evaluating key business metrics. He has spent more than five years at Benchmark International, starting as a transaction support analyst before moving to central operations as the senior quality control specialist. Before Benchmark, Josiah worked at iTValuations, where he gained buy-side, sell-side, and valuation experience. He earned a bachelor\u2019s degree in Enterprise Risk Management, with minors in International Business and Spanish, from The Pennsylvania State University."],
    "luke-ernst": ["Luke supports the deal team on every transaction in process. He contacts prospective buyers, manages confidentiality agreements, maintains the data room, and prepares the offer comparisons and status tracking that keep several buyers on the same schedule through closing. Before Benchmark, he worked in strategic finance at a single-family office and in investment banking at CEA Group. He earned a BS in Finance and Economics from the University of Tampa in three years and holds the FMVA\u00ae certification."],
}

# Client video stories (Vimeo IDs) → sector
STORIES = [
    ("158933030", "Software", "technology", "How pharmacy software leader Rx30 secured a strategic investment from PE giant GTCR to accelerate growth and innovation"),
    ("254578384", "Financial Services", "business-services", "The strategic acquisition of Silexx by industry leader CBOE to deliver advanced analytics and execution tools globally"),
    ("696225328", "Energy & Power", "industrial", "Why business executive Tim Wood decided to sell to explore new opportunities"),
    ("766180085", "Engineering", "business-services", "Joe Maynard shares how he was able to transition into the legacy and lifestyle he envisioned"),
    ("736906177", "Healthcare", "healthcare", "How leading provider of medical equipment O'Flynn Group scaled market presence to new heights"),
]

TESTIMONIALS = [
    ("Family Business", "We chose Benchmark International as our advisor in this process to ensure that we received best and highest value. The Benchmark International team played a pivotal role in terms of both deal structure, as well as guiding all parties through to a successful closing.", "Gina Gruenwald", "CEO of Blue Wave", "technology"),
    ("Perfect Fit", "The Benchmark International team did a great job finding and matching us up with a perfect fit in a partner for an acquisition. We look forward to a great future thanks to their efforts in finding a partner that fits us very well and offers unlimited potential for our company and team going forward, and we couldn’t have asked for a better result!", "Greg Galante", "CEO of ACS", None),
    ("New Heights", "From our initial conversation through the final closing, Benchmark International was thoughtful, responsive, and clearly had our best interests top of mind. Thanks to them, we were able to find the perfect buyer for this next phase of our growth.", "Meighan Newhouse", "Co-Founder and CEO, Inspirant Group", "business-services"),
    ("Efficient M&A", "My thanks to the Benchmark International team. The process was far more complex than I ever thought it could be. They were right there every step of the way not only handling the issues but also walking me through the key points so that I could make the best decision for my employees, family, and customers.", "Luke Reinstetle", "Founder and CEO of Morgan Wood", "industrial"),
]

LIBRARY = [
    ("kp0gV6Dj0_0", "Sell-Side Process", "Before the Sale: What a Sell-Side M&A Process Really Looks Like", "Jordan Houtz, Managing Director and Head of Middle Market, walks through what a successful sell-side process looks like, how buyers evaluate a business, what drives a premium valuation, and what owners should do before going to market."),
    ("X8a04-Ok6j4", "Growth & Exit Strategy", "Taking Control of Your Growth and Exit Strategy", "Managing Director Jared Hardin discusses taking control of your growth and exit strategy, including the key considerations and the right time to go to market."),
    ("8giQ5YAiCIA", "Webinar", "Selling for Maximum Value", "An M&A expert\u2019s guide to preparation and process: how owners can position their company to achieve the highest value in a sale."),
]

# Closing Remarks, the Benchmark International podcast hosted by Dara Shareef.
# A short, hand-picked set of episodes shown beneath the CEO Library videos:
# (YouTube id, label, title, description).
PODCAST = [
    ("08LRm0acEhs", "Owner Story", "Thomas Frey on Selling a Business", "The founder of Silexx Financial Systems describes building his trading software company and selling it to Cboe Global Markets with Benchmark International, and how he decided what he wanted from life after the sale."),
    ("W92GtOXmD90", "Owner Story", "Keith Marshall on Opportunity and M&A", "The founder of Solution Matrix traces the company from a home-based start to a manufacturing business, the role his family played along the way, and the sale through Benchmark International to a buyer who could carry it forward."),
    ("JgZd56mMlmQ", "Deal Terms", "Doug Starcher on Simplifying M&A Legal Terms", "A managing partner at Nelson Mullins with more than 35 years in M&A explains the terms every owner will meet in a sale, including letters of intent, representations and warranties, indemnification, and working capital."),
]
# Publish dates, lengths and thumbnails for the video structured data on the home page, from Vimeo and the
# YouTube channel feed: id -> (upload date, seconds or None, thumbnail). Videos without a known publish date
# are left out of the structured data (Google requires one); add the date here to include them.
VIDEO_META = {
    "158933030": ("2016-03-14", 278, "https://i.vimeocdn.com/video/1779468038-e74874803dca2e4d662a6c8c3cc2ba2df0d91cdec7f13cdef664a57c5ec41643-d_1280x720"),
    "254578384": ("2018-02-06", 336, "https://i.vimeocdn.com/video/1779468455-52833ecf156d84bb56c9a95e614c6042b0115521d446977671b5309e3b452a7b-d_1280x720"),
    "696225328": ("2022-04-05", 273, "https://i.vimeocdn.com/video/1779460963-61b4433ae2550784bac866e2fd3eca6853d78670781ddcf470096ecffd64b5e2-d_1280x720"),
    "766180085": ("2022-11-01", 521, "https://i.vimeocdn.com/video/1779543341-6ae8f38987238880dcf8845aaf3dd9650b28e94cdefa87f6dcc0e944299b30a6-d_1280x720"),
    "736906177": ("2022-08-05", 216, "https://i.vimeocdn.com/video/1779465411-5d28fd45412a975cc54e0500d3026d7bb79805da1cba4ed4ecb5cc04c1423e30-d_1280x720"),
    "08LRm0acEhs": ("2026-09-02", None, "https://i.ytimg.com/vi/08LRm0acEhs/hqdefault.jpg"),
    "W92GtOXmD90": ("2026-10-07", None, "https://i.ytimg.com/vi/W92GtOXmD90/hqdefault.jpg"),
    "JgZd56mMlmQ": ("2026-08-12", None, "https://i.ytimg.com/vi/JgZd56mMlmQ/hqdefault.jpg"),
}


def video_schema():
    """VideoObject entries for the client stories, CEO Library and podcast videos shown on the home page."""
    vids = [(v, t, t, f"https://player.vimeo.com/video/{v}", f"https://vimeo.com/{v}") for v, _, _, t in STORIES[:4]]
    vids += [(v, t, d, f"https://www.youtube.com/embed/{v}", f"https://www.youtube.com/watch?v={v}") for v, _, t, d in LIBRARY + PODCAST]
    out = []
    for vid, name, desc, embed, url in vids:
        if vid not in VIDEO_META:
            continue
        date, secs, thumb = VIDEO_META[vid]
        o = {"@type": "VideoObject", "name": name, "description": desc, "uploadDate": date, "thumbnailUrl": thumb,
             "embedUrl": embed, "url": url, "publisher": {"@id": SITE_URL + "#org"}}
        if secs:
            o["duration"] = f"PT{secs // 60}M{secs % 60}S"
        out.append(o)
    return out


PODCAST_LINKS = [
    ("Spotify", "https://open.spotify.com/show/4tH5twLR8zllxpeQqS9vgR"),
    ("Apple Podcasts", "https://podcasts.apple.com/us/podcast/closing-remarks/id1896060877"),
    ("YouTube", "https://www.youtube.com/playlist?list=PLY23_cDjMExKHyUNVI5rD8B24wzgK5RnC"),
]

# Award badges on the home page (assets/img/awards/award-<n>.png): (alt text, award name, awarded by).
AWARDS = [
    ("The M&A Advisor: Investment Banking Firm of the Year", "Investment Banking Firm of the Year", "The M&A Advisor"),
    ("PitchBook: #1 Sell-Side Exclusive M&A Advisor in the World", "#1 Sell-Side Exclusive M&A Advisor in the World", "PitchBook"),
    ("LSEG: #1 Privately-Held M&A Advisor Worldwide", "#1 Privately-Held M&A Advisor Worldwide", "LSEG"),
    ("DealMakers: First in Mergers & Acquisitions (Unlisted Deals), Investment Advisers by Deal Flow",
     "First in Mergers & Acquisitions (Unlisted Deals), Investment Advisers by Deal Flow", "DealMakers"),
]

TOMBSTONES = json.load(open(os.path.join(HERE, "tombstones.json"), encoding="utf-8"))
for t in TOMBSTONES:
    t["sector_name"] = SECTOR_BY_SLUG[t["sector"]]["name"]


# ─────────────────────────────────────────────────────────────────────────────
# Partials
# ─────────────────────────────────────────────────────────────────────────────
def meta_desc(text, n=160):
    """Shortens a meta description to about n characters, ending at a sentence or word."""
    if len(text) <= n:
        return text
    cut = text[:n]
    end = cut.rfind(". ")
    return cut[:end + 1] if end > n * 0.6 else cut[:cut.rfind(" ")].rstrip(",;:") + "…"


def e(s):
    return escape(s, quote=True)


def number_word(k):
    """Spells out small counts in running prose ("five sectors")."""
    words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    return words[k] if 0 <= k < len(words) else str(k)


FONTS = "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap"


def head(title, desc, root, canonical=""):
    desc = meta_desc(desc, 160)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#231f20">
<script>document.documentElement.classList.add('js')</script>
<link rel="icon" href="{root}assets/img/brand/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{FONTS}">
<link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<link rel="stylesheet" href="{root}assets/css/style.css?v={_asset_version('assets/css/style.css')}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(root, current=""):
    def cur(k):
        return ' aria-current="page"' if k == current else ""
    insights_link = f'      <a href="{root}insights/index.html"{cur("insights")}>Insights</a>\n' if REPORTS_LIVE else ""
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{root}index.html" aria-label="Benchmark International Middle Market home">
      <img src="{root}assets/img/brand/benchmark-logo-white.png" alt="Benchmark International" width="138" height="26">
      <span class="brand-tag">Middle Market</span>
    </a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Primary">
      <a href="{root}industries/index.html"{cur('industries')}>Industries</a>
      <a href="{root}transactions.html"{cur('transactions')}>Transactions</a>
      <a href="{root}index.html#team"{cur('team')}>Team</a>
{insights_link}      <a href="{root}index.html#library"{cur('library')}>CEO Library</a>
      <a class="nav-phone" href="{PHONE_HREF}">{PHONE}</a>
      <a class="btn" href="{root}index.html#form">Start the Conversation</a>
    </nav>
  </div>
</header>
<main id="main">
"""


SOCIAL = {
    "LinkedIn": ("https://www.linkedin.com/company/benchmark-international/", '<path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.4c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9V21H9z"/>'),
    "Instagram": ("https://www.instagram.com/benchmarkinternational/", '<path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4zM17.3 5.5a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM12 2c-2.7 0-3.1 0-4.1.1C3.6 2.3 2.3 3.6 2.1 7.9 2 8.9 2 9.3 2 12s0 3.1.1 4.1c.2 4.3 1.5 5.6 5.8 5.8 1 .1 1.4.1 4.1.1s3.1 0 4.1-.1c4.3-.2 5.6-1.5 5.8-5.8.1-1 .1-1.4.1-4.1s0-3.1-.1-4.1c-.2-4.3-1.5-5.6-5.8-5.8C15.1 2 14.7 2 12 2z"/>'),
    "YouTube": ("https://www.youtube.com/@benchmarkinternational8905", '<path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8zM9.7 15V9l5.8 3z"/>'),
    "Email": (f"mailto:{EMAIL}", '<path d="M2 5h20v14H2zm2 2v.5l8 5 8-5V7zm16 2.8-8 5-8-5V17h16z"/>'),
}



def report_gate(root):
    """The short form in front of every report PDF. The download links carry data-gate (the PDF) and data-report
    (its title); assets/js/main.js opens this dialog, sends the form to REPORT_FORM_URL and then starts the download."""
    return f"""<dialog class="gate" id="report-gate" aria-labelledby="gate-title" data-endpoint="{e(REPORT_FORM_URL)}" data-terms="{REPORT_TERMS_VERSION}">
  <button class="gate-close" type="button" aria-label="Close">&times;</button>
  <form class="gate-form" novalidate>
    <p class="eyebrow">Free download</p>
    <h2 id="gate-title">Get the full report</h2>
    <p class="gate-report"></p>
    <div class="gate-row">
      <label>First name<input name="first_name" autocomplete="given-name" required maxlength="80"></label>
      <label>Last name<input name="last_name" autocomplete="family-name" required maxlength="80"></label>
    </div>
    <label>Work email<input name="email" type="email" autocomplete="email" required maxlength="160"></label>
    <label class="gate-hp" aria-hidden="true">Company website<input name="company_website" tabindex="-1" autocomplete="off"></label>
    <label class="gate-check"><input type="checkbox" name="reports" value="yes"><span>Email me new Middle Market industry reports when they are published.</span></label>
    <label class="gate-check"><input type="checkbox" name="newsletter" value="yes"><span>Send me the Benchmark International Middle Market newsletter.</span></label>
    <label class="gate-check gate-terms"><input type="checkbox" name="terms" value="yes" required><span>I agree to the <a href="{root}report-terms.html" target="_blank">Report Terms and Conditions</a>, including the Important Disclosures and the Privacy Notice.</span></label>
    <p class="gate-error" role="alert" hidden></p>
    <button class="btn gate-submit" type="submit">Download the report</button>
    <p class="gate-fine">The two email boxes are optional, and you can unsubscribe at any time from any email or on our <a href="{root}email-preferences.html" target="_blank">email preferences</a> page. Your details stay with the Middle Market team.</p>
  </form>
  <div class="gate-done" hidden>
    <p class="eyebrow">Thank you</p>
    <h2>Your download is starting</h2>
    <p>If it does not start, use the button below.</p>
    <a class="btn gate-file" href="#" download>Download the PDF</a>
  </div>
</dialog>"""


def gated(root, pdf, title, cls, label):
    """A download link that goes through the report form. Without JavaScript it opens the report terms page."""
    return (f'<a class="{cls}" href="{root}report-terms.html#download" data-gate="{root}{pdf}" data-report="{e(title)}">{label}</a>')

def footer(root):
    ext = ' target="_blank" rel="noopener"'
    social = "".join(
        f'<a href="{href}" aria-label="{name}"{"" if name == "Email" else ext}><svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">{path}</svg></a>'
        for name, (href, path) in SOCIAL.items())
    sectors = "".join(f'<li><a href="{root}industries/{s["slug"]}.html">{e(s["name"])}</a></li>' for s in SECTORS)
    sectors += f'<li><a href="{root}industries/index.html">All Industries</a></li>'
    pages = (f'<li><a href="{root}about.html">About</a></li><li><a href="{root}transactions.html">Transactions</a></li><li><a href="{root}index.html#team">Team</a></li>'
             + (f'<li><a href="{root}insights/index.html">Insights</a></li>' if REPORTS_LIVE else "") + f'<li><a href="{root}index.html#library">CEO Library</a></li><li><a href="{root}index.html#form">Contact</a></li>')
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{root}assets/img/brand/benchmark-logo-white.png" alt="Benchmark International" width="138" height="26">
        <p>Benchmark International’s Middle Market team represents premier privately held companies across the United States in sell-side M&amp;A, offering white-glove, high-touch service to the firm’s largest clients.</p>
        <p><a href="{PHONE_HREF}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <div class="social">{social}</div>
      </div>
      <div><h4>Industries</h4><ul>{sectors}</ul></div>
      <div><h4>Middle Market</h4><ul>{pages}</ul></div>
      <div><h4>Benchmark International</h4><ul>
        <li><a href="https://www.benchmarkintl.com/about/">About</a></li>
        <li><a href="https://www.benchmarkintl.com/about/our-success/">Our Success</a></li>
        <li><a href="https://www.benchmarkintl.com/about/global-team/">Global Team</a></li>
        <li><a href="https://www.benchmarkintl.com/about/awards/">Awards</a></li>
        <li><a href="https://www.benchmarkintl.com/about/process/">Process</a></li>
        <li><a href="https://www.benchmarkintl.com/about/the-numbers/">The Numbers</a></li>
        <li><a href="https://www.benchmarkintl.com/sellers/">Seller Resources</a></li>
        <li><a href="https://blog.benchmarkcorporate.com/">Blog</a></li>
        <li><a href="https://www.benchmarkintl.com/contact/">Contact</a></li>
      </ul></div>
    </div>
    <div class="footer-base">
      <span>&copy; 2026 Benchmark International. All rights reserved. Information as of <time datetime="{SITE_UPDATED}">{AS_OF}</time>.</span>
      <span><a href="{root}disclosures.html">Important Disclosures</a> &nbsp;/&nbsp; <a href="https://www.benchmarkintl.com/terms/">Terms</a> &nbsp;/&nbsp; <a href="https://www.benchmarkintl.com/privacy-policy/">Privacy Policy</a>{f' &nbsp;/&nbsp; <a href="{root}report-terms.html">Report Terms</a> &nbsp;/&nbsp; <a href="{root}email-preferences.html">Email Preferences</a>' if REPORTS_LIVE else ""}</span>
    </div>
  </div>
</footer>
{report_gate(root) if REPORTS_LIVE else ""}
<script src="{root}assets/js/main.js?v={_asset_version('assets/js/main.js')}" defer></script>
</body>
</html>
"""


def cta(root, title="It All Starts With a Conversation", form=False, sub="", paras=None):
    if not form:
        body = (f'<p class="lead"><strong>{e(sub)}</strong></p>' if sub else "") + "".join(f'<p class="lead">{e(x)}</p>' for x in paras) if paras else \
            '<p class="lead">Our first step is always a confidential conversation exploring your goals, your company, and your options.</p>'
        return f"""<section class="section section--knot cta" id="contact">
  <div class="wrap center reveal">
    <p class="eyebrow">Confidential. No pressure. No commitments.</p>
    <h2 class="display">{e(title)}</h2>
    {body}
    <div class="btn-row"><a class="btn" href="{root}index.html#form">Start the Conversation</a><a class="btn btn--light" href="{PHONE_HREF}">Call {PHONE}</a></div>
    <p class="contact-line">Call to speak with an M&amp;A expert at <a href="{PHONE_HREF}">{PHONE}</a></p>
  </div>
</section>
"""
    steps = [
        ("Share a few details", "Tell us about your company and what you are considering. Everything you share is held in strict confidence."),
        ("Talk with a Managing Director", "A senior member of the Middle Market team will set up a private conversation at a time that suits you."),
        ("See your options clearly", "Understand the paths available, from a strategic sale to a merger or change-of-control transaction, and what each could mean for you."),
    ]
    step_html = "".join(f'<li><span class="contact-step-num">{k + 1:02d}</span><div><h3>{e(h)}</h3><p>{e(p)}</p></div></li>'
                        for k, (h, p) in enumerate(steps))
    icon_phone = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
    icon_mail = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>'
    icon_lock = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>'
    return f"""<section class="section section--knot section--photo section--photo-soft contact" id="contact">
  <div class="section-media" aria-hidden="true"><img src="{root}assets/img/site/contact-bg.jpg" alt="" loading="lazy" width="1920" height="1100"></div>
  <div class="wrap contact-grid">
    <div class="contact-info reveal">
      <p class="eyebrow">Confidential. No pressure. No commitments.</p>
      <h2 class="display">{e(title)}</h2>
      <p class="lead">Our first step is always a confidential conversation exploring your goals, your company, and your options.</p>
      <ol class="contact-steps">{step_html}</ol>
      <div class="contact-direct">
        <a href="{PHONE_HREF}">{icon_phone}<span><small>Speak with an M&amp;A expert</small>{PHONE}</span></a>
        <a href="mailto:{EMAIL}">{icon_mail}<span><small>Email the team</small>{EMAIL}</span></a>
      </div>
    </div>
    <div class="contact-card reveal" id="form">
      <p class="eyebrow">Start the Conversation</p>
      <h3 class="contact-card-title">Tell Us About Your Business</h3>
      <p class="contact-card-sub">A member of our team will follow up with you personally.</p>
      <div id="hs-form" class="hs-form-host">
        <noscript><p>Call <a href="{PHONE_HREF}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a> to start the conversation.</p></noscript>
      </div>
      <script charset="utf-8" src="https://js.hsforms.net/forms/embed/v2.js"></script>
      <script>
        (function () {{
          var host = document.getElementById('hs-form');
          // a copy of each enquiry for the General Form tab of the report downloads sheet (REPORT_FORM_URL)
          function logContact($form) {{
            var endpoint = "{e(REPORT_FORM_URL)}", form = $form && ($form[0] || $form);
            if (!endpoint || !form || !form.querySelectorAll) return;
            var data = new URLSearchParams({{ action: 'contact', page: location.pathname }}), extra = [];
            form.querySelectorAll('input, select, textarea').forEach(function (el) {{
              if (!el.name || el.type === 'hidden' || el.type === 'submit' || ((el.type === 'checkbox' || el.type === 'radio') && !el.checked)) return;
              var v = String(el.value || '').trim();
              if (!v) return;
              if (el.name === 'firstname') data.set('first_name', v);
              else if (el.name === 'lastname') data.set('last_name', v);
              else if (el.name === 'email') data.set('email', v);
              else extra.push((el.closest('.hs-form-field') && el.closest('.hs-form-field').querySelector('label') ? el.closest('.hs-form-field').querySelector('label').textContent.replace(/\*/g, '').trim() : el.name) + ': ' + v);
            }});
            data.set('details', extra.join('; '));
            if (navigator.sendBeacon) navigator.sendBeacon(endpoint, data);
            else fetch(endpoint, {{ method: 'POST', mode: 'no-cors', body: data }});
          }}
          function fallback() {{ host.innerHTML = '<p class="hs-fallback">Call <a href="{PHONE_HREF}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a> to start the conversation.</p>'; }}
          if (window.hbspt) {{
            hbspt.forms.create({{ region: "{HUBSPOT['region']}", portalId: "{HUBSPOT['portalId']}", formId: "{HUBSPOT['formId']}", target: "#hs-form", css: "", submitButtonClass: "btn hs-submit", submitText: "Start the Conversation", onFormSubmit: logContact }});
          }} else {{ fallback(); }}
        }})();
      </script>
      <p class="contact-privacy">{icon_lock}<span>Your information is kept strictly confidential.</span></p>
    </div>
  </div>
</section>
"""


_SIZES = {}


def img_size(rel):
    """width="…" height="…" for an image in the site folder, so the page keeps its layout while images load."""
    if rel not in _SIZES:
        try:
            from PIL import Image
            with Image.open(os.path.join(SITE, rel)) as im:
                _SIZES[rel] = f'width="{im.width}" height="{im.height}"'
        except Exception:
            _SIZES[rel] = ""
    return _SIZES[rel]


def tombstone(t, root, show_sector=False):
    text = e(f"{t['seller']} {t['buyer']} {t['sector_name']} {t.get('segment', '')} {t.get('desc', '')}".lower())
    if t.get("image"):
        face = f'<div class="tomb-face tomb-face--img"><img src="{root}{t["image"]}" alt="{e(t["seller"])} {e(t["verb"].lower())} {e(t["buyer"])}" loading="lazy" width="200" height="200"></div>'
    else:
        face = (f'<div class="tomb-face"><img src="{root}{t["seller_logo"]}" alt="{e(t["seller"])}" loading="lazy" {img_size(t["seller_logo"])}>'
                f'<span class="tomb-verb">{e(t["verb"])}</span>'
                f'<img src="{root}{t["buyer_logo"]}" alt="{e(t["buyer"])}" loading="lazy" {img_size(t["buyer_logo"])}></div>')
    badge = '<span class="tomb-badge">Featured</span>' if t.get("featured") else ""
    desc = f'<p class="tomb-desc">{e(t["desc"])}</p>' if t.get("desc") else ""
    names = [t["sector_name"]] + [SECTOR_BY_SLUG[x["sector"]]["name"] for x in t.get("also", [])]
    meta = f'<span class="tomb-sector">{e(" · ".join(names) if show_sector else t.get("segment", ""))}</span>'
    cap = f'<div class="tomb-cap"><strong>{e(t["seller"])}</strong><span>{e(t["verb"].lower())} {e(t["buyer"])}</span>{desc}{meta}</div>'
    sectors = " ".join([t["sector"]] + [x["sector"] for x in t.get("also", [])])
    attrs = f'data-sector="{sectors}" data-segment="{e(t.get("segment", ""))}" data-text="{text}"'
    if t.get("link"):
        return f'<a class="tomb" href="{e(t["link"])}" target="_blank" rel="noopener" {attrs}>{badge}{face}{cap}</a>'
    return f'<div class="tomb" {attrs}>{badge}{face}{cap}</div>'


def vimeo(vid, title):
    return (f'<iframe src="https://player.vimeo.com/video/{vid}?badge=0&amp;autopause=0&amp;dnt=1" loading="lazy" '
            f'allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="{e(title)}"></iframe>')


def yt(vid, title):
    return (f'<button class="yt" data-id="{vid}" aria-label="Play: {e(title)}" '
            f'style="background-image:url(https://i.ytimg.com/vi/{vid}/hqdefault.jpg)"></button>')


def deals_in(slug):
    """Deals for one industry. A deal listed under `also` appears in that industry
    too, shown with the segment it has there."""
    out = []
    for t in TOMBSTONES:
        if t["sector"] == slug:
            out.append(t)
        for extra in t.get("also", []):
            if extra["sector"] == slug:
                out.append(dict(t, sector=slug, segment=extra["segment"], sector_name=SECTOR_BY_SLUG[slug]["name"], cross=True))
    return out


def photo(slug, name, root):
    """Path to an industry photo from the approved image library (assets/img/industries/<slug>/)."""
    return f"{root}assets/img/industries/{slug}/{name}.jpg"


def photo_hero(slug, root):
    """Opening tag of a page hero backed by the industry's hero photo."""
    return f'<section class="hero hero--page hero--photo"><div class="hero-media" aria-hidden="true"><img src="{photo(slug, "hero", root)}" alt="" width="1920" height="1000" fetchpriority="high"></div>'


def photo_strip(slug, root, n=4):
    imgs = "".join(f'<figure class="photo-strip-item"><img src="{photo(slug, f"g{k}", root)}" alt="" loading="lazy" width="900" height="675"></figure>' for k in range(1, n + 1))
    return f'<div class="photo-strip reveal" aria-hidden="true">{imgs}</div>'


def report_extras(page, slug, root, extra=None, faqs=None):
    """Finishes an industry report page: the industry photo hero, photo breaks after report sections 2 and 5,
    and the Important Disclosures link at the end of the report."""
    page = page.replace('<section class="hero hero--page">', photo_hero(slug, root), 1)
    page = page.replace('assets/css/report.css">', f'assets/css/report.css?v={_asset_version("assets/css/report.css")}">', 1)
    sep = '\n<section class="rsec'
    parts = page.split(sep)
    for k, g in ((2, (1, 2)), (5, (3, 4))):
        if len(parts) > k + 1:
            imgs = "".join(f'<img src="{photo(slug, f"g{x}", root)}" alt="" loading="lazy" width="900" height="675">' for x in g)
            parts[k] += f'\n<figure class="rphoto reveal" aria-hidden="true">{imgs}</figure>'
    page = sep.join(parts)
    note = (f'<aside class="rdisclosure"><p class="eyebrow">Important Disclosures</p><p>This report is for informational purposes only and is not advice '
            f'or an offer or solicitation. Information is as of the date stated and has not been independently verified. '
            f'<a class="link-arrow" href="{root}disclosures.html">Read the Important Disclosures</a></p></aside>\n  </article>')
    assert page.count("</article>") == 1, "report page should have one <article>"
    page = page.replace("</article>", note, 1)
    rpt, sec = current_report(slug), SECTOR_BY_SLUG[slug]
    author = next(({"@type": "Person", "@id": person_id(i), "name": n, "jobTitle": r, "worksFor": {"@id": SITE_URL + "#org"}} for n, r, i, _ in TEAM_LEAD if i == "jared-hardin"), None)
    article = {"@type": "Report", "headline": rpt["title"], "name": rpt["title"], "description": rpt["summary"],
               "datePublished": REPORT_DATE, "dateModified": REPORT_DATE, "inLanguage": "en-US", "url": abs_url(rpt["url"]),
               "author": author, "publisher": {"@id": SITE_URL + "#org"}, "about": f"{sec['name']} mergers and acquisitions",
               "image": SITE_URL + f"assets/img/social/{slug}-report.jpg"}
    article.update(extra or {})
    return finalize(page, rpt["url"], crumbs=[("Middle Market", ""), ("Insights", "insights/index.html"), (rpt["title"], rpt["url"])],
                    schema=[article] + ([faq_schema(faqs)] if faqs else []), image=f"assets/img/social/{slug}-report.jpg")


def industry_card(s, root):
    tags = "".join(f"<li>{e(seg[0])}</li>" for seg in s["segments"])
    return f"""<a class="ind-card ind-card--photo" href="{root}industries/{s['slug']}.html">
  <div class="ind-photo"><img src="{photo(s['slug'], 'card', root)}" alt="" loading="lazy" width="900" height="560"></div>
  <h3>{e(s['name'])}</h3>
  <p>{e(s['short'])}</p>
  <ul class="ind-tags">{tags}</ul>
  <div class="ind-meta"><span class="ind-count">{s['count']}+ completed transactions</span><span class="ind-go">Explore</span></div>
</a>"""


def cta_card(root):
    return f"""<a class="ind-card ind-card--cta" href="{root}index.html#form">
  <p class="eyebrow">Not sure where you fit?</p>
  <h3>Let's talk about your business.</h3>
  <p>Every company is different. Start with a confidential conversation about your goals and options.</p>
  <div class="ind-meta"><span class="ind-count">{PHONE}</span><span class="ind-go">Start the Conversation</span></div>
</a>"""


def team_members(lead_only=False):
    """All team members as dicts, leadership first."""
    people = [dict(name=n, role=r, img=i, bio=b, group="leadership") for n, r, i, b in TEAM_LEAD]
    if not lead_only:
        people += [dict(name=n, role=r, img=i, bio=TEAM_SUPPORT_BIO.get(i, []), group=TEAM_GROUP_OF.get(i, "deal-team")) for n, r, i in TEAM_SUPPORT]
    return people


def team_dialog(m, root):
    """Profile window for one team member (opened by clicking their card)."""
    did = f"tm-{m['img']}"
    phone, email = TEAM_CONTACT.get(m["img"], (None, None))
    # Only real details are shown; anyone without them shows the team's main line instead of a placeholder.
    phone_html = f'<a href="tel:{phone.replace("-", "")}">{e(phone)}</a>' if phone else f'<a href="{PHONE_HREF}">{e(PHONE)}</a>'
    email_html = f'<a href="mailto:{email}">{e(email)}</a>' if email else f'<a href="mailto:{EMAIL}">{e(EMAIL)}</a>'
    li = TEAM_LINKEDIN.get(m["img"])
    li_row = f'<li><small>LinkedIn</small><a href="{e(li)}" target="_blank" rel="noopener">Connect on LinkedIn</a></li>' if li else ""
    bio = "".join(f"<p>{e(x)}</p>" for x in m["bio"]) or f'<p>{e(m["name"].split()[0])} is part of the Benchmark International Middle Market team.</p>'
    return f"""<dialog class="team-dialog" id="{did}" aria-labelledby="{did}-name">
  <button type="button" class="team-close" aria-label="Close"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <div class="team-dialog-head"><h3 id="{did}-name">{e(m['name'])}</h3><p class="team-title">{e(m['role'])}</p></div>
  <div class="team-dialog-body">
    <div class="team-dialog-left">
      <img src="{root}assets/img/team/{m['img']}.jpg" alt="{e(member_alt(m))}" loading="lazy" width="480" height="480">
      <ul class="team-contact">
        <li><small>{"Phone" if phone else "Team Phone"}</small>{phone_html}</li>
        <li><small>{"Email" if email else "Team Email"}</small>{email_html}</li>
        {li_row}
      </ul>
    </div>
    <div class="team-dialog-right">{bio}</div>
  </div>
</dialog>"""


def member_alt(m):
    return f"{m['name']}, {m['role'].replace(' | ', ', ')}, Benchmark International"


def team_html(root, lead_only=False):
    """Leadership cards and the support-team row; clicking anyone opens their profile window."""
    people = team_members(lead_only)
    lead = "".join(f"""<button type="button" class="member member-open reveal" data-dialog="tm-{m['img']}" aria-haspopup="dialog">
  <img src="{root}assets/img/team/{m['img']}.jpg" alt="{e(member_alt(m))}" loading="lazy" width="480" height="480">
  <span class="member-body"><span class="member-name">{e(m['name'])}</span><span class="role">{e(m['role'])}</span><span class="member-link">View Profile</span></span>
</button>""" for m in people if m["group"] == "leadership")
    support = "".join(f"""<button type="button" class="member member-open" data-dialog="tm-{m['img']}" aria-haspopup="dialog">
  <img src="{root}assets/img/team/{m['img']}.jpg" alt="{e(member_alt(m))}" loading="lazy" width="120" height="120">
  <span class="member-body"><span class="member-name">{e(m['name'])}</span><span class="role">{e(m['role'])}</span></span>
</button>""" for m in people if m["group"] != "leadership")
    dialogs = "".join(team_dialog(m, root) for m in people)
    return f'<div class="team-lead">{lead}</div>' + (f'<div class="team-support">{support}</div>' if support else "") + dialogs


def team_section(root):
    """The leadership team module used on the industry pages and the online industry reports."""
    return f"""<section class="section">
  <div class="wrap">
    <div class="section-head center reveal"><p class="eyebrow">Your Deal Team</p><h2 class="h2">Leadership Team</h2></div>
    {team_html(root, lead_only=True)}
    <div class="center" style="margin-top:36px"><a class="link-arrow" href="{root}index.html#team">Meet the full team</a></div>
  </div>
</section>"""


def abs_url(rel):
    """Absolute URL for a site-relative path ("" or "index.html" is the home page)."""
    rel = "" if rel in ("", "index.html") else rel
    return SITE_URL + rel


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"


def org_schema():
    return {
        "@type": ["Organization", "ProfessionalService"], "@id": SITE_URL + "#org", "name": ORG_NAME,
        "alternateName": ["Benchmark International Middle Market team", "Middle Market team"],
        "url": SITE_URL, "logo": SITE_URL + "assets/img/brand/benchmark-logo-black.svg",
        "description": "Benchmark International's Middle Market team represents privately held companies across the United States "
                       "with $50M–$500M in total enterprise value (TEV) on strategic sales, mergers, and qualifying change-of-control transactions.",
        "parentOrganization": PARENT_ORG, "telephone": "+1-" + PHONE, "email": EMAIL, "address": PARENT_ORG["address"],
        "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": "+1-" + PHONE, "email": EMAIL, "areaServed": "US", "availableLanguage": "English"},
        "slogan": "Your Legacy Is Built. Your Next Chapter Awaits.",
        "award": ["#1 global M&A advisor for privately owned businesses (PitchBook Q2 2026 Global League Tables)"] + [f"{n} ({by})" for _, n, by in AWARDS],
        "areaServed": {"@type": "Country", "name": "United States"},
        "knowsAbout": ["Sell-side M&A", "Mergers and acquisitions advisory", "Controlling ownership transactions", "Exit readiness and transaction planning"] + [x["name"] for x in SECTORS],
        "sameAs": [v[0] for k, v in SOCIAL.items() if k != "Email"] + [PARENT_ORG["url"]],
        "member": [{"@id": person_id(m["img"])} for m in team_members()],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Sell-side M&A advisory services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d}} for n, d in SERVICES]},
    }


def person_id(img):
    return SITE_URL + "#" + img


def breadcrumb_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "name": name, "item": abs_url(rel)} for n, (name, rel) in enumerate(crumbs)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def linkify(text):
    """Escapes an answer and links the team email and phone number."""
    html = e(text).replace(EMAIL, f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    return html.replace(PHONE, f'<a href="{PHONE_HREF}">{PHONE}</a>')


def faq_html(faqs, title="Frequently Asked Questions", eyebrow="Questions Owners Ask"):
    items = "".join(f'<details class="faq-item"><summary><h3>{e(q)}</h3></summary><p>{linkify(a)}</p></details>' for q, a in faqs)
    return f"""<section class="section section--paper" id="faq">
  <div class="wrap faq-wrap">
    <div class="section-head reveal"><p class="eyebrow">{e(eyebrow)}</p><h2 class="h2">{e(title)}</h2></div>
    <div class="faq">{items}</div>
  </div>
</section>
"""


def home_faqs():
    return [
        ("What does Benchmark International's Middle Market team do?",
         "Benchmark International's Middle Market team represents premier privately held companies across the United States in sell-side M&A, "
         "offering white-glove, high-touch service to the firm's largest clients."),
        ("What size companies does the Middle Market team advise?",
         "Our Middle Market team advises privately held businesses, typically with enterprise values of $50 million to $500 million, "
         "that meet applicable M&A broker exemption requirements, including companies with less than $25 million in annual EBITDA "
         "or less than $250 million in annual revenue."),
        ("Which industries does the Middle Market team focus on?",
         "Five industries: " + ", ".join(x["name"] for x in SECTORS[:-1]) + ", and " + SECTORS[-1]["name"] + "."),
        ("What services does the Middle Market team provide?",
         "Our Middle Market team provides comprehensive sell-side M&A advisory services, specializing in business sales, mergers, "
         "controlling ownership transfers, strategic acquisitions, and exit planning for privately held companies. Our services span "
         "transaction preparation, valuation analysis, buyer identification, deal structuring, negotiation, and execution, subject to "
         "applicable regulatory requirements."),
        next((q, " ".join(ans)) for q, ans in pagecopy.load("about")["faq"] if "FINRA" in q),
        ("How does working with Benchmark International start?",
         "The first step is always a confidential conversation about your goals, your company, and your options. A senior member of the "
         "Middle Market team sets up a private conversation, then walks you through the paths available, from a strategic sale to a merger or change-of-control transaction."),
        ("How large is Benchmark International?",
         "Headquartered in Tampa, FL, Benchmark International has over 300 employees across 15 global offices in the Americas, Europe, and Africa "
         "and is proudly ranked the #1 global M&A advisor for privately owned businesses (based on PitchBook's Q2 2026 Global League Tables)."),
        ("How do I contact the Middle Market team?", f"Call {PHONE} or email {EMAIL}."),
    ]


def semi_list(items):
    """Joins list items that contain their own commas or "and": "A; B; and C"."""
    items = list(items)
    if len(items) < 2:
        return "".join(items)
    if len(items) == 2:
        return items[0] + " and " + items[1]
    return "; ".join(items[:-1]) + "; and " + items[-1]


def sector_faqs(s, buyers):
    n = s["name"]
    segs = [x[0] for x in s["segments"]]
    faqs = [
        (f"What types of {s['adj']} companies does Benchmark International advise?",
         f"The Middle Market team advises {s['adj']} companies across {number_word(len(segs))} sectors: " + semi_list(segs) + "."),
        (f"What do buyers value in {s['adj']} companies?",
         " ".join(f"{h}: {d}" for h, d in s["value"])),
        (f"How many {s['adj']} transactions has Benchmark International completed?",
         f"Benchmark International lists {s['count']}+ completed {s['adj']} transactions on benchmarkintl.com, as of {AS_OF}."),
    ]
    if buyers:
        faqs.append((f"Who is acquiring {s['adj']} companies?",
                     f"Acquirers and investors in Benchmark International's selected {s['adj']} transactions include " + semi_list(buyers[:8]) + "."))
    if s.get("report"):
        faqs.append((f"Is there a current {s['adj']} M&A market report?",
                     f"Yes. The {current_report(s['slug'])['title']} covers deal activity, valuations, and what buyers are paying for, and is free to read online or download as a PDF."))
    return faqs


def person_schema(m, root_abs=SITE_URL):
    phone, email = TEAM_CONTACT.get(m["img"], (None, None))
    p = {"@type": "Person", "@id": person_id(m["img"]), "name": m["name"], "jobTitle": m["role"].replace(" | ", ", "),
         "worksFor": {"@id": SITE_URL + "#org"}, "url": SITE_URL + "#team", "image": f"{SITE_URL}assets/img/team/{m['img']}.jpg"}
    if m["bio"]:
        p["description"] = m["bio"][0].split(". ")[0].rstrip(".") + "."
    if phone:
        p["telephone"] = "+1-" + phone
    if email:
        p["email"] = email
    if TEAM_LINKEDIN.get(m["img"]):
        p["sameAs"] = [TEAM_LINKEDIN[m["img"]]]
    return p


def finalize(html, rel, crumbs=None, schema=None, image="assets/img/social/default.jpg"):
    """Adds the canonical link, social preview tags and JSON-LD structured data to a finished page."""
    url = abs_url(rel)
    title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)"', html).group(1)
    page = {"@type": "WebPage", "@id": url, "url": url, "name": unescape(title), "description": unescape(desc),
            "isPartOf": {"@type": "WebSite", "@id": SITE_URL + "#website", "name": ORG_NAME, "url": SITE_URL, "publisher": {"@id": SITE_URL + "#org"}},
            "about": {"@id": SITE_URL + "#org"}, "publisher": {"@id": SITE_URL + "#org"}, "inLanguage": "en-US",
            "dateModified": SITE_UPDATED, "primaryImageOfPage": SITE_URL + image,
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".lead", ".faq-item"]}}
    graph = [org_schema(), page]
    if crumbs:
        graph.append(breadcrumb_schema(crumbs))
    graph += schema or []
    tags = (f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n'
            f'<meta property="og:site_name" content="{ORG_NAME}">\n'
            f'<meta property="og:image" content="{SITE_URL}{image}">\n<meta property="og:image:width" content="1200">\n'
            f'<meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{title}">\n<meta name="twitter:description" content="{desc}">\n'
            f'<meta name="twitter:image" content="{SITE_URL}{image}">\n'
            + jsonld({"@context": "https://schema.org", "@graph": graph}) + "\n</head>")
    assert html.count("</head>") == 1
    return html.replace("</head>", tags, 1)


SITEMAP = []   # (rel, priority) of every indexable page written this build
PAGE_FAQS = {}  # rel -> [(question, answer)] from each page's FAQPage schema, for llms-full.txt


def write(rel, html, crumbs=None, schema=None, image="assets/img/social/default.jpg", index=True):
    if index:
        for x in schema or []:
            if x.get("@type") == "FAQPage":
                PAGE_FAQS[rel] = [(q["name"], q["acceptedAnswer"]["text"]) for q in x["mainEntity"]]
        html = finalize(html, rel, crumbs, schema, image)
        SITEMAP.append(rel)
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", rel)


# ─────────────────────────────────────────────────────────────────────────────
# Pages
# ─────────────────────────────────────────────────────────────────────────────
def page_home():
    root = ""
    featured = [t for t in TOMBSTONES if t.get("featured")]
    marquee_items = "".join(
        f'<a href="{e(t["link"])}" target="_blank" rel="noopener" title="{e(t["seller"])} / {e(t["buyer"])}"><img src="{t["image"]}" alt="{e(t["seller"])} {e(t["verb"].lower())} {e(t["buyer"])}" loading="lazy" width="170" height="170"></a>'
        if t.get("link") else
        f'<a href="transactions.html" title="{e(t["seller"])} / {e(t["buyer"])}"><img src="{t["image"]}" alt="{e(t["seller"])} {e(t["verb"].lower())} {e(t["buyer"])}" loading="lazy" width="170" height="170"></a>'
        for t in featured)
    stories = "".join(f"""<article class="story reveal">
  <div class="story-media">{vimeo(vid, title)}</div>
  <div class="story-body"><p class="eyebrow"><a href="industries/{slug}.html" style="text-decoration:none">{e(label)}</a></p><p>{e(title)}</p></div>
</article>""" for vid, label, slug, title in STORIES[:4])
    testimonials = "".join(f"""<figure class="testimonial reveal">
  <p class="eyebrow">{e(k)}</p>
  <blockquote>“{e(q)}”</blockquote>
  <figcaption><cite>{e(n)}<span>{e(r)}</span></cite></figcaption>
</figure>""" for k, q, n, r, _ in TESTIMONIALS)
    library = "".join(f"""<article class="story reveal">
  <div class="story-media">{yt(vid, title)}</div>
  <div class="story-body"><p class="eyebrow">{e(label)}</p><h3>{e(title)}</h3><p>{e(desc)}</p></div>
</article>""" for vid, label, title, desc in LIBRARY)
    podcast = "".join(f"""<article class="story reveal">
  <div class="story-media">{yt(vid, title)}</div>
  <div class="story-body"><p class="eyebrow">{e(label)}</p><h3>{e(title)}</h3><p>{e(desc)}</p></div>
</article>""" for vid, label, title, desc in PODCAST)
    podcast_links = "".join(f'<a href="{url}" target="_blank" rel="noopener">{e(name)}</a>' for name, url in PODCAST_LINKS)
    cards = "".join(industry_card(s, root) for s in SECTORS) + cta_card(root)
    awards = "".join(f'<img src="assets/img/awards/award-{i}.png" alt="{e(a[0])}" loading="lazy" width="520" height="300">' for i, a in enumerate(AWARDS, 1))

    html = head("Middle Market M&A Advisory | Benchmark International",
                "Sell-side M&A advisory for owners of privately held companies with $50M–$500M in enterprise value: strategic sales, mergers, and change-of-control transactions.", root)
    html += header(root)
    html += f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Benchmark International · <span class="nowrap">Middle Market</span></p>
    <h1 class="display">Your Legacy Is Built. <em>Your Next Chapter Awaits.</em></h1>
    <p class="lead">Maximize your company's value and achieve your goals with the world's #1 privately owned sell-side M&amp;A advisor.</p>
    <div class="btn-row">
      <a class="btn" href="#form">Start the Conversation</a>
      <a class="btn btn--light" href="industries/index.html">Explore Our Industries</a>
    </div>
  </div>
</section>

<section class="section--dark section--tight section--photo section--photo-soft">
  <div class="section-media" aria-hidden="true"><img src="assets/img/site/stats-bg.jpg" alt="" width="1920" height="900"></div>
  <div class="wrap">
    <div class="stats">
      <div class="stat"><div class="stat-num">#1</div><div class="stat-label">Privately owned sell-side M&amp;A advisor worldwide<sup>*</sup></div></div>
      <div class="stat"><div class="stat-num">$50M–$500M</div><div class="stat-label">Total Enterprise Value (TEV) range we serve</div></div>
      <div class="stat"><div class="stat-num">5</div><div class="stat-label">Focused industries with dedicated deal expertise</div></div>
      <div class="stat"><div class="stat-num">15</div><div class="stat-label">Global offices across the Americas, Europe &amp; Africa</div></div>
    </div>
    <p class="note">* Based on PitchBook’s Q2 2026 Global League Tables.</p>
  </div>
</section>

<section class="section section--tight awards-band" id="recognition">
  <div class="wrap"><div class="awards reveal">{awards}</div></div>
</section>

<section class="section section--paper" id="industries">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Industry Expertise</p>
        <h2 class="h2">Five Industries. Deep Expertise.</h2>
        <p class="lead">We focus on five industries where we know the buyers, the valuation drivers, and the questions that will come up in diligence.</p>
      </div>
      <a class="link-arrow" href="industries/index.html">View all industries</a>
    </div>
    <div class="ind-grid reveal">{cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">You Built an Extraordinary Company</p>
      <h2 class="h2">Let's Talk About What's Next.</h2>
      <hr class="rule">
      <p>Most owners sell a business once in a lifetime. The stakes couldn’t be higher. Yet many don’t realize that an exit can take many forms: a full sale, a merger, or a qualifying change-of-control transaction. Each option comes with different implications for your wealth, your family, and your company’s future.</p>
      <p>Benchmark International helps you explore these options with clarity, discretion, and a global network of qualified buyers.</p>
      <p>Whether you’re planning a sale, exploring a merger, or simply preparing for the future, the right strategy helps you maximize value and protect your legacy.</p>
    </div>
    <div class="quote-card reveal">
      It all starts with a conversation.
      <a class="phone" href="{PHONE_HREF}">{PHONE}</a>
      <a class="btn" href="#form">Start the Conversation</a>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">Peace of Mind for Business Owners</p>
      <h2 class="h2">Your Benchmark Journey</h2>
      <p class="lead">We serve presidents, CEOs, founders, and owners of privately held companies in our five industries. As they consider the next step, most want three things:</p>
    </div>
    <div class="pillars">
      <div class="pillar pillar--photo reveal"><div class="pillar-photo"><img src="assets/img/site/journey-1.jpg" alt="" loading="lazy" width="900" height="600"></div><div class="pillar-num">01</div><h3 class="h3">Understand Every Option</h3><p>We'll walk you through every path, from a full sale to a merger or change-of-control transaction, with buyers from across the country and around the world.</p></div>
      <div class="pillar pillar--photo reveal"><div class="pillar-photo"><img src="assets/img/site/journey-2.jpg" alt="" loading="lazy" width="900" height="600"></div><div class="pillar-num">02</div><h3 class="h3">Be Positioned for Maximum Value</h3><p>We'll help you see your company the way buyers do, so you can address gaps and highlight strengths before going to market.</p></div>
      <div class="pillar pillar--photo reveal"><div class="pillar-photo"><img src="assets/img/site/journey-3.jpg" alt="" loading="lazy" width="900" height="600"></div><div class="pillar-num">03</div><h3 class="h3">Execute with Confidence</h3><p>While you weigh your options, our experienced team works as your partner, running a discreet process to secure the right deal on your terms.</p></div>
    </div>
  </div>
</section>

<section class="section section--dark" id="who-we-help">
  <div class="wrap fit-split">
    <figure class="fit-photo reveal" aria-hidden="true"><img src="assets/img/site/who-we-help.jpg" alt="" loading="lazy" width="900" height="1100"></figure>
    <div>
    <div class="section-head reveal">
      <p class="eyebrow">Who We Help</p>
      <h2 class="h2" style="color:#fff">Perfect for You If You Are</h2>
    </div>
    <div class="fit">
      <div class="fit-item reveal"><h3>Looking to retire</h3><p>Ready to sell so you can retire or move on to what's next.</p></div>
      <div class="fit-item reveal"><h3>Approached by a buyer</h3><p>Weighing an unsolicited offer and want to know if it's fair.</p></div>
      <div class="fit-item reveal"><h3>Exploring a merger</h3><p>Weighing a merger or change of control to take your business to its next stage.</p></div>
      <div class="fit-item reveal"><h3>Ready to learn more</h3><p>Curious what buyers would likely pay for your company so you can plan for the future.</p></div>
    </div>
    </div>
  </div>
</section>

<section class="section section--cream" id="clients">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">In Their Words</p>
      <h2 class="h2">Working With Clients Around the World</h2>
    </div>
    <div class="testimonials">{testimonials}</div>
  </div>
</section>

<section class="section section--paper" id="transactions">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Businesses We've Served</p>
        <h2 class="h2">Selected Transactions</h2>
      </div>
      <a class="link-arrow" href="transactions.html">View all transactions by industry</a>
    </div>
  </div>
  <div class="marquee reveal"><div class="marquee-track">{marquee_items}{marquee_items.replace('<a ', '<a aria-hidden="true" tabindex="-1" ')}</div></div>
</section>

<section class="section" id="team">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">Middle Market</p>
      <h2 class="h2">Meet Your Team</h2>
    </div>
    {team_html(root)}
    <div class="center" style="margin-top:48px"><a class="btn" href="#form">Start the Conversation</a></div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">Client Stories</p>
      <h2 class="h2" style="color:#fff">Hear From Our Clients</h2>
    </div>
    <div class="stories">{stories}</div>
  </div>
</section>

<section class="section" id="library">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">CEO Library</p>
      <h2 class="h2">Insight for Owners Considering What's Next</h2>
    </div>
    <div class="library">{library}</div>
    <div class="podcast-head reveal">
      <p class="eyebrow">Closing Remarks Podcast</p>
      <h3>Owners and Advisors on Selling a Business and What Comes After</h3>
      <p>Closing Remarks is the Benchmark International podcast hosted by Dara Shareef. Each episode is a plain-language conversation with an owner who has sold a company or an advisor who works on these transactions.</p>
    </div>
    <div class="library">{podcast}</div>
    <p class="podcast-links reveal"><span>Listen to every episode on</span>{podcast_links}</p>
  </div>
</section>

"""
    faqs = home_faqs()
    html += faq_html(faqs)
    html += cta(root, form=True)
    html += footer(root)
    team = [person_schema(m) for m in team_members()]
    write("index.html", html, crumbs=[("Middle Market", "")], schema=[faq_schema(faqs)] + team + video_schema())


def page_industries():
    root = "../"
    total = sum(s["count"] for s in SECTORS)
    rows = ""
    for i, s in enumerate(SECTORS):
        deals = deals_in(s["slug"])
        deals = [t for t in deals if not t.get("cross")] + [t for t in deals if t.get("cross")]
        picks = [t for t in deals if t.get("featured") and not t.get("cross")][:3]
        picks += [t for t in deals if t not in picks and t.get("desc")][:3 - len(picks)]
        minis = "".join(tombstone(t, root) for t in picks)
        segs = "".join(f'<li><a href="{s["slug"]}.html#seg-{k + 1}">{e(seg[0])}</a></li>' for k, seg in enumerate(s["segments"]))
        rows += f"""<article class="ind-row reveal" id="{s['slug']}">
  <div class="ind-row-main">
    <p class="eyebrow">{s['count']}+ completed transactions<sup>†</sup></p>
    <h2 class="h2">{e(s['name'])}</h2>
    <p class="lead">{e(s['tagline'])}</p>
    <p>{e(s['overview'][0])}</p>
    <h3 class="h3">Sectors</h3>
    <ul class="seg-links">{segs}</ul>
    <div class="btn-row"><a class="btn" href="{s['slug']}.html">Explore {e(s['name'])}</a><a class="btn btn--ghost" href="{root}transactions.html#{s['slug']}">{len(deals)} Selected Transactions</a></div>
  </div>
  <div class="ind-row-side">
    <a class="ind-row-photo" href="{s['slug']}.html" tabindex="-1" aria-hidden="true"><img src="{photo(s['slug'], 'card', root)}" alt="" loading="lazy" width="900" height="560"></a>
    <div class="ind-row-deals tomb-grid tomb-grid--compact">{minis}</div>
  </div>
</article>"""
    html = head("Industries We Advise | Benchmark International Middle Market",
                "Benchmark International's Middle Market team focuses on five industries: Industrials, Business Services, Consumer, Healthcare, and Technology.", root)
    html += header(root, "industries")
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Middle Market</a> / Industries</div>
    <p class="eyebrow">Industry Expertise</p>
    <h1 class="display">Five Industries. Deep Expertise.</h1>
    <p class="lead">We focus on five industries where we have deep transaction experience and long relationships with the most active strategic and financial buyers. Industry focus means we know what drives value, who is buying, and how to run a process that gets you the best outcome.</p>
    <nav class="jump" aria-label="Industries">{''.join(f'<a href="#{s["slug"]}">{e(s["name"])}</a>' for s in SECTORS)}</nav>
  </div>
</section>

<section class="section--dark section--tight">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><div class="stat-num">5</div><div class="stat-label">Focused Industries</div></div>
      <div class="stat"><div class="stat-num">{total}+</div><div class="stat-label">Completed Transactions<sup>†</sup></div></div>
      <div class="stat"><div class="stat-num">{len(TOMBSTONES)}</div><div class="stat-label">Featured Transactions</div></div>
      <div class="stat"><div class="stat-num">#1</div><div class="stat-label">Global M&amp;A Advisor to Privately Held Companies<sup>*</sup></div></div>
    </div>
    <p class="note">† Completed transactions tagged to these industries on benchmarkintl.com/about/our-success, as of {AS_OF}. * PitchBook Q2 2026 Global League Tables.</p>
  </div>
</section>

<section class="section">
  <div class="wrap ind-rows">{rows}</div>
  <div class="wrap"><p class="note">† Completed transactions tagged to each industry on benchmarkintl.com/about/our-success, as of {AS_OF}.</p></div>
</section>
"""
    html += cta(root)
    html += footer(root)
    items = {"@type": "ItemList", "name": "Middle Market industries", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": x["name"], "url": abs_url(f"industries/{x['slug']}.html")} for k, x in enumerate(SECTORS)]}
    write("industries/index.html", html, crumbs=[("Middle Market", ""), ("Industries", "industries/index.html")], schema=[items])


def paras_html(ps):
    return "".join(f"<p>{e(x)}</p>" for x in ps)


# Search-result descriptions for the industry pages (about 160 characters, so Google shows them whole).
SECTOR_META_DESC = {
    "industrial": "Industrials M&A advisory for owners of $50M–$500M companies in manufacturing, distribution, building products, energy services, and transportation.",
    "business-services": "Business Services M&A advisory for owners of $50M–$500M companies in facility, marketing, engineering, financial, and staffing services.",
    "consumer": "Consumer M&A advisory for owners of $50M–$500M food and beverage, restaurant, consumer brand, foodservice, and consumer services companies.",
    "healthcare": "Healthcare M&A advisory for owners of $50M–$500M provider, life sciences, medical products, and pharmacy and healthcare services companies.",
    "technology": "Technology M&A advisory for owners of $50M–$500M software, IT and managed services, communications, and hardware companies.",
}


def page_sector(i, s):
    root = "../"
    cp = pagecopy.load(s["slug"], [x[0] for x in s["segments"]])
    deals = deals_in(s["slug"])
    deals.sort(key=lambda t: (bool(t.get("cross")), not t.get("featured"), not t.get("desc"), -int(t.get("year") or 0)))
    tombs = "".join(tombstone(t, root) for t in deals)
    seg_counts = {seg[0]: sum(1 for t in deals if t.get("segment") == seg[0]) for seg in s["segments"]}
    chips = '<button class="chip" data-filter="all" aria-pressed="true">All Sectors</button>' + "".join(
        f'<button class="chip" data-filter="{e(seg[0])}" aria-pressed="false">{e(seg[0])} <span>{seg_counts[seg[0]]}</span></button>'
        for seg in s["segments"])
    segments = "".join(f"""<article class="segment reveal" id="seg-{k + 1}">
  <div class="segment-num">{k + 1:02d}</div>
  <div class="segment-body">
    <h3>{e(name)}</h3>
    {paras_html(cp.get('segments', {}).get(name) or [desc])}
    <p class="eyebrow" style="margin:16px 0 8px">Subsector Expertise</p>
    <ul class="ind-tags">{''.join(f'<li>{e(x)}</li>' for x in subs)}</ul>
    <button class="link-arrow seg-jump" data-segment="{e(name)}">{seg_counts[name]} selected transactions</button>
  </div>
</article>""" for k, (name, desc, subs) in enumerate(s["segments"]))
    glance = "".join(f'<li><a href="#seg-{k + 1}">{e(seg[0])}</a><span>{seg_counts[seg[0]]}</span></li>' for k, seg in enumerate(s["segments"]))
    theme_items = cp["themes"]["items"] if cp.get("themes") else [(h, [p]) for h, p in s["themes"]]
    themes_title = (cp.get("themes") or {}).get("title") or f"What We're Seeing in {s['title_in']}"
    themes = "".join(f'<article class="theme reveal"><span class="theme-num">{k + 1:02d}</span><h3>{e(h)}</h3>{paras_html(ps)}</article>'
                     for k, (h, ps) in enumerate(theme_items))
    value_items = cp["value"]["items"] if cp.get("value") else [(h, [p]) for h, p in s["value"]]
    value_title = cp["value"]["title"] if cp.get("value") else "Seeing Your Company Through a Buyer's Eyes"
    value = "".join(f'<li><span class="vnum">{k + 1:02d}</span><div><h4>{e(h)}</h4>{paras_html(ps)}</div></li>' for k, (h, ps) in enumerate(value_items))
    if cp.get("statement"):
        value_lead = f'<p class="lead"><strong>{e(cp["statement"]["title"])}</strong></p>' + paras_html(cp["statement"]["paras"])
    elif cp.get("value"):
        value_lead = ""
    else:
        value_lead = f'<p class="lead">We build the story around the factors that drive valuation in {e(s["prose"])}, so qualified buyers compete on your terms.</p>'
    seen, buyers = set(), []
    for t in deals:
        b = t["buyer"].strip()
        if b.lower() in seen or any(w in b.lower() for w in ("individual", "undisclosed", "trust")):
            continue
        seen.add(b.lower())
        buyers.append(b)
    buyer_list = "".join(f"<li>{e(b)}</li>" for b in buyers[:18])
    if cp.get("services"):
        services = "".join(f'<article class="service reveal"><h3>{e(h)}</h3>{paras_html(ps)}</article>' for h, ps in cp["services"]["items"])
        services_head = f'<h2 class="h2">{e(cp["services"]["title"])}</h2>' + "".join(f'<p class="lead">{e(x)}</p>' for x in cp["services"]["intro"])
    else:
        services = "".join(f'<article class="service reveal"><h3>{e(h)}</h3><p>{e(p)}</p></article>' for h, p in SERVICES)
        services_head = (f'<h2 class="h2">Advisory Built Around Your Goals</h2>'
                         f'<p class="lead">An exit can take many forms. We help owners of {e(s["adj"])} companies choose the path that fits their wealth, family, and company goals.</p>')
    hero = cp.get("hero") or {}
    hero_lead = f'<p class="lead">{e(hero["sub"])}</p>' + "".join(f'<p class="hero-text">{e(x)}</p>' for x in hero["paras"]) if hero.get("sub") else f'<p class="lead">{e(s["tagline"])}</p>'
    if cp.get("overview"):
        overview = f'<h2 class="h2">{e(cp["overview"]["title"])}</h2>\n      <hr class="rule">\n      ' + paras_html(cp["overview"]["paras"])
    else:
        overview = (f'<h2 class="h2">{e(s["name"])} M&amp;A Advisory</h2>\n      <hr class="rule">\n      ' + paras_html(s["overview"])
                    + "<p>Every engagement is led by the Middle Market team and backed by Benchmark International's global network of strategic acquirers, private equity groups, family offices, and independent sponsors.</p>")
    acq = cp.get("acquirers")
    acq_html = (f'<h3 class="h3">{e(acq["title"])}</h3>' + paras_html(acq["paras"])
                + f'<h4 class="buyer-head">Acquirers and Investors in Our Selected {e(s["name"])} Transactions</h4>') if acq else \
               f'<h3 class="h3">Acquirers and Investors in Our Selected {e(s["name"])} Transactions</h3>'
    story = next((x for x in STORIES if x[2] == s["slug"]), None)
    quote = next((x for x in TESTIMONIALS if x[4] == s["slug"]), None)
    feature = ""
    if story or quote:
        left = right = ""
        if story:
            left = f'<article class="story reveal"><div class="story-media">{vimeo(story[0], story[3])}</div><div class="story-body"><p class="eyebrow">Client Story</p><p>{e(story[3])}</p></div></article>'
        if quote:
            right = f'<figure class="testimonial reveal"><p class="eyebrow">{e(quote[0])}</p><blockquote>“{e(quote[1])}”</blockquote><figcaption><cite>{e(quote[2])}<span>{e(quote[3])}</span></cite></figcaption></figure>'
        feature = f"""<section class="section section--cream">
  <div class="wrap">
    <div class="section-head center reveal"><p class="eyebrow">In Their Words</p><h2 class="h2">Client Perspective</h2></div>
    <div class="stories">{left}{right}</div>
  </div>
</section>"""
    prev_s = SECTORS[i - 1]
    next_s = SECTORS[(i + 1) % len(SECTORS)]
    team_cards = team_section(root)
    cur = ' aria-current="page"'
    tabs = "".join(f'<a href="{x["slug"]}.html"{cur if x is s else ""}>{e(x["name"])}</a>' for x in SECTORS)

    report_btn = f'<a class="btn btn--light" href="{root}{s["report"][1]}">{e(s["report"][0])}</a>' if s.get("report") else ""
    html = head(f"{s['name']} M&A Advisory | Benchmark International", SECTOR_META_DESC[s["slug"]], root)
    html += header(root, "industries")
    html += f"""
{photo_hero(s['slug'], root)}
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Middle Market</a> / <a href="index.html">Industries</a> / {e(s['name'])}</div>
    <h1 class="display">{e(s['name'])}</h1>
    {hero_lead}
    <div class="btn-row"><a class="btn" href="#deals">Selected Transactions</a><a class="btn btn--light" href="{root}index.html#form">Discuss Your Business</a>{report_btn}</div>
  </div>
</section>
<nav class="sector-tabs" aria-label="Industries"><div class="wrap">{tabs}</div></nav>

<section class="section--dark section--tight">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><div class="stat-num">{s['count']}+</div><div class="stat-label">Completed transactions<sup>†</sup></div></div>
      <div class="stat"><div class="stat-num">{len(s['segments'])}</div><div class="stat-label">Sectors</div></div>
      <div class="stat"><div class="stat-num">{len(deals)}</div><div class="stat-label">Selected transactions below</div></div>
      <div class="stat"><div class="stat-num">{len(buyers)}</div><div class="stat-label">Distinct acquirers in those deals</div></div>
    </div>
    <p class="note">† Completed transactions tagged to the categories that make up our {e(s['name'])} group on benchmarkintl.com/about/our-success, as of {AS_OF}.</p>
  </div>
</section>

<section class="section">
  <div class="wrap split split--top">
    <div class="reveal">
      <p class="eyebrow">Overview</p>
      {overview}
    </div>
    <aside class="glance reveal">
      <p class="eyebrow">At a Glance</p>
      <h3>Sectors We Cover</h3>
      <ul>{glance}</ul>
      <a class="btn" href="#deals">View Transactions</a>
    </aside>
  </div>
</section>

{photo_strip(s['slug'], root)}

<section class="section section--paper">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Sector Expertise</p>
      <h2 class="h2">Where We Focus</h2>
      <p class="lead">We advise {e(s['adj'])} companies in {number_word(len(s['segments']))} sectors, including these subsectors:</p>
    </div>
    <div class="segments">{segments}</div>
  </div>
</section>

<section class="section" id="deals">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Selected Transactions</p>
        <h2 class="h2">Recent {e(s['name'])} Engagements</h2>
      </div>
      <a class="link-arrow" href="{root}transactions.html#{s['slug']}">All transactions</a>
    </div>
    <div class="filter-bar" role="group" aria-label="Filter by sector">{chips}</div>
    <p class="result-count" aria-live="polite"></p>
    <div class="tomb-grid tomb-grid--detail" data-tomb-filter data-filter-key="segment" data-limit="12">{tombs}</div>
    <div class="center"><button class="btn btn--ghost show-more" hidden>Show All Transactions</button></div>
  </div>
</section>

<section class="section section--dark section--photo">
  <div class="section-media" aria-hidden="true"><img src="{photo(s['slug'], 'hero', root)}" alt="" loading="lazy" width="1920" height="1000"></div>
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Market Perspective</p>
      <h2 class="h2" style="color:#fff">{e(themes_title)}</h2>
    </div>
    <div class="themes{' themes--3' if len(theme_items) in (5, 6) else ''}">{themes}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--top">
    <div class="reveal">
      <p class="eyebrow">What Buyers Value</p>
      <h2 class="h2">{e(value_title)}</h2>
      {value_lead}
      <ul class="value-list">{value}</ul>
    </div>
    <div class="reveal">
      <p class="eyebrow">Who Is Buying</p>
      {acq_html}
      <ul class="buyer-list">{buyer_list}</ul>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">How We Help</p>
      {services_head}
    </div>
    <div class="services">{services}</div>
  </div>
</section>

{feature}

{{SECTOR_FAQ}}
{team_cards}

<section class="section section--tight section--paper">
  <div class="wrap sector-nav">
    <a href="{prev_s['slug']}.html"><small>← Previous industry</small><strong>{e(prev_s['name'])}</strong></a>
    <a href="{next_s['slug']}.html" style="text-align:right"><small>Next industry →</small><strong>{e(next_s['name'])}</strong></a>
  </div>
</section>
"""
    faqs = [(q, " ".join(a)) for q, a in cp["faq"]] if cp.get("faq") else sector_faqs(s, buyers)
    html = html.replace("{SECTOR_FAQ}", faq_html(faqs, f"{s['name']} M&A: Common Questions"))
    if cp.get("cta"):
        html += cta(root, cp["cta"]["title"], sub=cp["cta"]["sub"], paras=cp["cta"]["paras"])
    else:
        html += cta(root, f"Considering a Transaction in {s['title_in']}?")
    html += footer(root)
    service = {"@type": "Service", "name": f"{s['name']} M&A advisory", "serviceType": "Sell-side M&A advisory",
               "provider": {"@id": SITE_URL + "#org"}, "areaServed": {"@type": "Country", "name": "United States"},
               "description": s["tagline"], "employee": [{"@id": person_id(m["img"])} for m in team_members(lead_only=True)]}
    write(f"industries/{s['slug']}.html", html,
          crumbs=[("Middle Market", ""), ("Industries", "industries/index.html"), (s["name"], f"industries/{s['slug']}.html")],
          schema=[faq_schema(faqs), service] + [person_schema(m) for m in team_members(lead_only=True)], image=f"assets/img/social/{s['slug']}.jpg")


def page_legacy(old, new, folder="industries"):
    """Redirect stub at <folder>/<old>.html to the industry page industries/<new>.html (or the industries index)."""
    target = "index" if new == "index" else new
    label = "Industries" if new == "index" else SECTOR_BY_SLUG[new]["name"]
    back = "" if folder == "industries" else "../industries/"
    write(f"{folder}/{old}.html", index=False, html=f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Redirecting…</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{abs_url(f'industries/{target}.html')}">
<meta http-equiv="refresh" content="0; url={back}{target}.html">
</head><body><p>This page has moved to <a href="{back}{target}.html">{e(label)}</a>.</p></body></html>
""")


def page_transactions():
    root = ""
    chips = '<button class="chip" data-filter="all" aria-pressed="true">All Industries</button>' + "".join(
        f'<button class="chip" data-filter="{s["slug"]}" aria-pressed="false">{e(s["name"])} <span>{len(deals_in(s["slug"]))}</span></button>' for s in SECTORS)
    order = {s["slug"]: k for k, s in enumerate(SECTORS)}
    items = sorted(TOMBSTONES, key=lambda t: (order[t["sector"]], not t.get("featured"), -int(t.get("year") or 0)))
    tombs = "".join(tombstone(t, root, show_sector=True) for t in items)
    html = head("Completed M&A Transactions | Benchmark International",
                "Selected completed sell-side M&A transactions advised by Benchmark International across Industrials, Business Services, Consumer, Healthcare, and Technology.", root)
    html += header(root, "transactions")
    html += f"""
<section class="hero hero--page hero--photo"><div class="hero-media" aria-hidden="true"><img src="assets/img/site/transactions-hero.jpg" alt="" width="1920" height="1000" fetchpriority="high"></div>
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Middle Market</a> / Transactions</div>
    <p class="eyebrow">Our Success</p>
    <h1 class="display">Selected Transactions</h1>
    <p class="lead">A curated selection of completed transactions across our five industries. Tombstones marked <strong style="color:var(--gold)">Featured</strong> are signature Middle Market transactions.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="filter-bar" role="group" aria-label="Filter by industry">{chips}</div>
    <input class="search" type="search" placeholder="Search by company, acquirer, or sector" aria-label="Search transactions">
    <p class="result-count" aria-live="polite"></p>
    <div class="tomb-grid tomb-grid--detail" data-tomb-filter data-filter-key="sector">{tombs}</div>
    <p class="note">Source: Benchmark International transaction announcements and benchmarkintl.com/about/our-success, as of {AS_OF}. Selected transactions shown.</p>
  </div>
</section>
"""
    html += cta(root)
    html += footer(root)
    deals = {"@type": "ItemList", "name": "Selected completed transactions", "numberOfItems": len(items), "itemListElement": [
        dict({"@type": "ListItem", "position": n + 1, "name": f"{t['seller']} {t['verb'].lower()} {t['buyer']}",
              "description": " ".join(x for x in (t.get("desc", ""), f"{t['sector_name']}." + (f" {t['year']}." if t.get("year") else "")) if x)},
             **({"url": t["link"]} if t.get("link") else {})) for n, t in enumerate(items)]}
    write("transactions.html", html, crumbs=[("Middle Market", ""), ("Transactions", "transactions.html")], schema=[deals])


def insight_card(i, root, current):
    sec = SECTOR_BY_SLUG[i["sector"]]
    text = e(f'{i["title"]} {sec["name"]} {i["period"]} {i["summary"]}'.lower())
    badge = '<span class="insight-badge">Current</span>' if current else '<span class="insight-badge insight-badge--archive">Archive</span>'
    return f"""<article class="insight-card{' insight-card--current' if current else ''}" data-sector="{i['sector']}" data-text="{text}">
  <a class="insight-cover" href="{root}{i['url']}" aria-label="{e(i['title'])}" style="background-image:url('{photo(i['sector'], 'card', root)}')">
    <span class="insight-cover-period">{e(i['period'])}</span>
    <span class="insight-cover-sector">{e(sec['name'])}</span>
  </a>
  <div class="insight-body">
    <p class="insight-meta"><span>Industry Report</span><span aria-hidden="true">·</span><span>{e(sec['name'])}</span>{badge}</p>
    <h3><a href="{root}{i['url']}">{e(i['title'])}</a></h3>
    <p class="insight-summary">{e(i['summary'])}</p>
    <div class="insight-actions">
      <a class="btn" href="{root}{i['url']}">Read the Report</a>
      {gated(root, i['pdf'], i['title'], "link-arrow", "Download PDF")}
    </div>
  </div>
</article>"""


def page_insights():
    root = "../"
    order = {s["slug"]: k for k, s in enumerate(SECTORS)}
    current = [current_report(s["slug"]) for s in SECTORS if current_report(s["slug"])]
    archive = sorted([i for i in INSIGHTS if i not in current],
                     key=lambda i: (-i["year"], -i["quarter"], order[i["sector"]]))
    chips = '<button class="chip" data-filter="all" aria-pressed="true">All Industries</button>' + "".join(
        f'<button class="chip" data-filter="{s["slug"]}" aria-pressed="false">{e(s["name"])}</button>' for s in SECTORS)
    cards = "".join(insight_card(i, root, True) for i in current)
    if archive:
        rows = "".join(f"""<li class="archive-row" data-sector="{i['sector']}" data-text="{e((i['title'] + ' ' + i['period']).lower())}">
  <span class="archive-period">{e(i['period'])}</span>
  <a class="archive-title" href="{root}{i['url']}">{e(i['title'])}</a>
  <span class="archive-sector">{e(SECTOR_BY_SLUG[i['sector']]['name'])}</span>
  {gated(root, i['pdf'], i['title'], "link-arrow", "PDF")}
</li>""" for i in archive)
        archive_html = f'<ul class="archive-list">{rows}</ul>'
    else:
        archive_html = '<p class="archive-empty">Earlier editions will be archived here as each new quarterly report is published.</p>'
    latest = max(current, key=lambda i: (i["year"], i["quarter"]))["period"] if current else ""
    html = head("Middle Market M&A Industry Reports | Benchmark International",
                "Quarterly middle market M&A reports on deal activity, valuation metrics, and buyer demand in Industrials, Business Services, Consumer, Healthcare, and Technology.", root)
    html += header(root, "insights")
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Middle Market</a> / Insights</div>
    <p class="eyebrow">Insights</p>
    <h1 class="display">Unique Perspectives on the Middle Market</h1>
    <p class="lead">Quarterly industry reports from the Middle Market team on deal activity, valuations, and what buyers are paying for across our five industries.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Current Reports</p>
        <h2 class="h2">{e(latest)} Industry Reports</h2>
      </div>
    </div>
    <div class="filter-bar" role="group" aria-label="Filter by industry">{chips}</div>
    <div data-tomb-filter data-filter-key="sector">
      <div class="insight-grid">{cards}</div>
      <div class="archive reveal">
        <div class="archive-head"><p class="eyebrow">Report Archive</p><h2 class="h2">Previous Editions</h2></div>
        {archive_html}
      </div>
    </div>
  </div>
</section>
"""
    html += cta(root, "Curious What This Means for Your Business?")
    html += footer(root)
    reports = {"@type": "ItemList", "name": "Middle Market industry reports", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": i["title"], "url": abs_url(i["url"])} for k, i in enumerate(INSIGHTS)]}
    write("insights/index.html", html, crumbs=[("Middle Market", ""), ("Insights", "insights/index.html")], schema=[reports])



# Report Terms and Conditions: agreed to on the download form. A working draft for Compliance and counsel to confirm
# before the site goes live; change REPORT_TERMS_VERSION and TERMS_UPDATED whenever the wording changes.
TERMS_UPDATED = "October 28, 2026"
POSTAL_ADDRESS = "Benchmark International, 4030 W Boy Scout Blvd, Suite 500, Tampa, FL 33607, United States"
REPORT_TERMS = [
    ("About these terms", [
        "These terms apply when you request or download a Middle Market industry report (a “Report”) from this website. By checking the box on the download form and downloading a Report, you agree to them. If you do not agree, please do not download the Report. The online version of each Report remains available on this website.",
        f"The Reports are published by the Middle Market team of Benchmark International, {POSTAL_ADDRESS.split(', ', 1)[1]}. You can reach us at {EMAIL}."]),
    ("How you may use a Report", [
        "You may read, download, and print a Report for your own information and for internal use within your business. You may quote brief passages with attribution to Benchmark International and a link to this website.",
        "You may not sell, republish, redistribute, or make a Report available to others in whole or in substantial part, remove or alter any notice in it, or use it to build a database or a competing product, without our written permission. Requests can be sent to " + EMAIL + "."]),
    ("No advice and no offer", [
        "The Reports are general market commentary for information only. They are not a recommendation, an offer, or a solicitation to buy or sell any security or business, and they are not investment, legal, tax, accounting, or valuation advice. Benchmark International does not provide valuations, appraisals, or fairness opinions. Please consult your own advisers before making any decision."]),
    ("Information and sources", [
        "Reports draw on public filings, company announcements, published research, and other third-party sources, together with our own transaction experience. We have not independently verified third-party information. Figures are current only as of the date stated in each Report, and we are under no obligation to update them. Forward-looking statements are opinions, not facts, and past transactions do not predict future results."]),
    ("Ownership", [
        "The Reports and their contents are owned by Benchmark International and protected by copyright and other laws. Company names, logos, and trademarks mentioned in a Report belong to their owners, are used for identification only, and do not imply any affiliation or endorsement."]),
    ("Limitation of liability", [
        "Reports are provided “as is” without any warranty. To the fullest extent permitted by law, Benchmark International and its affiliates, officers, and employees are not liable for any loss or damage arising from the use of, or reliance on, a Report or this website."]),
    ("Privacy notice", [
        "When you download a Report we collect your first name, last name, and email address, which Report you requested, the date, your agreement to these terms, and your choices about the two optional emails. We use this information to provide the Report, to keep a record of your agreement and your choices, and, only if you opted in, to send you new industry reports or the Middle Market newsletter. We may also use it to respond to you if you contact us.",
        "We do not sell your information or share it for targeted advertising. It is stored with service providers that process it on our behalf, such as our cloud document and email providers, and it may be disclosed if the law requires. We keep it for as long as you remain subscribed or we have a business need for it, and we keep a record of any unsubscribe request so that we can continue to honor it.",
        "Depending on where you live, you may have the right to ask for access to, correction of, or deletion of your information, to withdraw your consent at any time, and to object to its use, and visitors in the European Economic Area and the United Kingdom may complain to their data protection authority. To make a request, email " + EMAIL + ". We will not treat you differently for exercising these rights. Your information may be stored and processed in the United States. These Reports are intended for business owners and professionals and are not directed to anyone under 18.",
        "For more on how Benchmark International handles personal information, see the Benchmark International Privacy Policy."]),
    ("Emails and unsubscribing", [
        "Checking a box on the download form is optional and is never a condition of receiving a Report. We send industry reports or the Middle Market newsletter only to people who opt in. Every such email identifies Benchmark International, includes our postal address, and has a working unsubscribe link. You can also unsubscribe on our email preferences page or by emailing " + EMAIL + ". We act on unsubscribe requests promptly, and in any case within 10 business days.",
        "Postal address: " + POSTAL_ADDRESS + "."]),
    ("Changes and governing law", [
        "We may update these terms from time to time; the date below shows the latest version, and the version you agreed to is recorded with your download. These terms are governed by the laws of the State of Florida, United States, without regard to conflict-of-laws rules, except where the law of your country of residence gives you rights that cannot be waived."]),
]


def page_report_terms():
    root = ""
    html = head("Report Terms and Conditions | Benchmark International",
                "Terms for downloading Benchmark International Middle Market industry reports, with the Important Disclosures and the privacy notice.", root)
    html += header(root)
    toc = "".join(f'<li><a href="#t{k}">{e(t)}</a></li>' for k, (t, _) in enumerate(REPORT_TERMS, 1)) + '<li><a href="#disclosures">Important Disclosures</a></li>'
    body = "".join(f'<h2 class="legal-h" id="t{k}">{e(t)}</h2>' + "".join(f"<p>{e(x)}</p>" for x in ps) for k, (t, ps) in enumerate(REPORT_TERMS, 1))
    body = body.replace(e("Benchmark International Privacy Policy."), '<a href="https://www.benchmarkintl.com/privacy-policy/">Benchmark International Privacy Policy</a>.')
    body = body.replace(e("email preferences page"), f'<a href="{root}email-preferences.html">email preferences page</a>')
    body += '<h2 class="legal-h" id="disclosures">Important Disclosures</h2>' + "".join(f"<p>{e(p)}</p>" for p in DISCLOSURES)
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Middle Market</a> / Report Terms and Conditions</div>
    <p class="eyebrow">Legal</p>
    <h1 class="display">Report Terms and Conditions</h1>
    <p class="lead">The terms for downloading our industry reports, including the Important Disclosures and how we handle your information.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <article class="legal" id="download">
      <p class="legal-updated">Last updated {TERMS_UPDATED}.</p>
      <ol class="legal-toc">{toc}</ol>
      {body}
      <p class="legal-links"><a class="link-arrow" href="{root}insights/index.html">Back to Insights</a></p>
    </article>
  </div>
</section>
"""
    html += footer(root)
    write("report-terms.html", html, crumbs=[("Middle Market", ""), ("Report Terms and Conditions", "report-terms.html")])


def page_email_preferences():
    """Unsubscribe from the industry report emails or the newsletter; recorded in the report downloads sheet."""
    root = ""
    html = head("Email Preferences | Benchmark International", "Unsubscribe from Benchmark International Middle Market emails.", root)
    html = html.replace("</head>", '<meta name="robots" content="noindex">\n</head>')
    html += header(root)
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Middle Market</a> / Email Preferences</div>
    <p class="eyebrow">Email preferences</p>
    <h1 class="display">Unsubscribe</h1>
    <p class="lead">Enter the email address you used and choose what to stop receiving. We act on every request promptly, and in any case within 10 business days.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <form class="prefs-form legal" data-endpoint="{e(REPORT_FORM_URL)}" novalidate>
      <label>Email address<input name="email" type="email" autocomplete="email" required maxlength="160"></label>
      <label class="gate-hp" aria-hidden="true">Company website<input name="company_website" tabindex="-1" autocomplete="off"></label>
      <label class="gate-check"><input type="checkbox" name="reports" value="yes" checked><span>Stop sending me Middle Market industry reports.</span></label>
      <label class="gate-check"><input type="checkbox" name="newsletter" value="yes" checked><span>Stop sending me the Middle Market newsletter.</span></label>
      <p class="gate-error" role="alert" hidden></p>
      <button class="btn" type="submit">Update my preferences</button>
      <p class="prefs-done" hidden>Thank you. Your request has been recorded. You can also email <a href="mailto:{EMAIL}">{EMAIL}</a> at any time.</p>
      <p class="gate-fine">See the <a href="{root}report-terms.html">Report Terms and Conditions</a> for how we handle your information.</p>
    </form>
  </div>
</section>
"""
    html += footer(root)
    write("email-preferences.html", html, index=False)

def page_disclosures():
    root = ""
    html = head("Important Disclosures | Benchmark International",
                "Important disclosures for Benchmark International's Middle Market " + ("industry reports and website." if REPORTS_LIVE else "website."), root)
    html += header(root)
    paras = "".join(f"<p>{e(p)}</p>" for p in DISCLOSURES)
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Middle Market</a> / Important Disclosures</div>
    <p class="eyebrow">Legal</p>
    <h1 class="display">Important Disclosures</h1>
    <p class="lead">{"These disclosures apply to the Middle Market industry reports and to the content of this website." if REPORTS_LIVE else "These disclosures apply to the content of this website."}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <article class="legal">{paras}
      <p class="legal-links">{f'<a class="link-arrow" href="{root}insights/index.html">Back to Insights</a>' if REPORTS_LIVE else f'<a class="link-arrow" href="{root}index.html">Back to Home</a>'}</p>
    </article>
  </div>
</section>
"""
    html += footer(root)
    write("disclosures.html", html, crumbs=[("Middle Market", ""), ("Important Disclosures", "disclosures.html")])


def about_facts():
    """The About page's Key Facts table, also used in llms-full.txt."""
    lead = ", ".join(f"{n} ({r})" for n, r, _, _ in TEAM_LEAD)
    support = ", ".join(f"{n} ({r})" for n, r, _ in TEAM_SUPPORT)
    rows = [
        ("Who we are", "The Middle Market team of Benchmark International, serving owners of companies with $50M–$500M in total enterprise value (TEV)."),
        ("What we do", "Specialized sell-side M&A advisory services to owners of privately held businesses, focused on qualifying mergers, business sales, and controlling ownership transitions."),
        ("Company size served", "$50 million to $500 million in total enterprise value (TEV)."),
        ("Industries", ", ".join(x["name"] for x in SECTORS) + "."),
        ("Services", ", ".join(n for n, _ in SERVICES) + "."),
        ("Firm", "Headquartered in Tampa, FL, with over 300 employees across 15 global offices in the Americas, Europe, and Africa; ranked the #1 global M&A advisor for privately owned businesses (PitchBook Q2 2026 Global League Tables)."),
        ("Leadership", lead + "."),
        ("Deal team", support + "."),
        ("Research", "Quarterly M&A reports for each of our five industries, published on the Insights page."),
        ("Contact", f"{PHONE} | {EMAIL}"),
    ]
    return rows if REPORTS_LIVE else [r for r in rows if r[0] != "Research"]


def page_about():
    """The About page: Jordan's practice overview, then a plain fact sheet AI assistants and search engines can cite."""
    root = ""
    cp = pagecopy.load("about")
    sec = {x["title"].split(".")[0]: x for x in cp.get("sections", [])}
    facts = about_facts()
    rows = "".join(f"<tr><th scope=\"row\">{e(k)}</th><td>{e(v)}</td></tr>" for k, v in facts)
    report_links = "".join(f'<li><a href="{i["url"]}">{e(i["title"])}</a></li>' for i in INSIGHTS)
    hero, stmt = cp["hero"], cp.get("statement")
    slug_of = {"Industrials": "industrial"}
    slug_of.update({x["name"]: x["slug"] for x in SECTORS})

    def prose(key, eyebrow, extra="", cls="section"):
        x = sec[key]
        return f"""<section class="{cls}">
  <div class="wrap about-wrap reveal">
    <p class="eyebrow">{eyebrow}</p>
    <h2 class="h2">{e(x["title"])}</h2>
    <hr class="rule">
    {paras_html([q for q in x["paras"] if not q.startswith("**")])}{extra}
  </div>
</section>
"""

    def cards(key, eyebrow, link=False):
        x = sec[key]
        intro = []
        for ln in x["lines"]:
            if pagecopy._is_item_head(ln):
                break
            if ln.strip():
                intro.append(ln.strip())
        items = "".join(
            f'<article class="service reveal"><h3>'
            + (f'<a href="industries/{slug_of[h]}.html">{e(h)}</a>' if link and h in slug_of else e(h))
            + f'</h3>{paras_html(ps)}</article>' for h, ps in x["items"])
        return f"""<section class="section section--paper">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">{eyebrow}</p>
      <h2 class="h2">{e(x["title"])}</h2>
      {"".join(f'<p class="lead">{e(i)}</p>' for i in intro)}
    </div>
    <div class="services{' services--5' if len(x['items']) == 5 else ''}">{items}</div>
  </div>
</section>
"""

    faqs = [(q, " ".join(ans)) for q, ans in cp["faq"]]
    html = head("About the Middle Market Team | Benchmark International",
                "Benchmark International's Middle Market team: sell-side M&A advisory for privately held companies with $50M–$500M in enterprise value across five industries.", root)
    html += header(root)
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Middle Market</a> / About</div>
    <p class="eyebrow">About</p>
    <h1 class="display">{e(hero["title"])}</h1>
    <p class="lead">{e(hero["sub"])}</p>
    {"".join(f'<p class="hero-text">{e(x)}</p>' for x in hero["paras"])}
  </div>
</section>
"""
    if stmt:
        html += f"""<section class="section--dark section--tight">
  <div class="wrap center reveal">
    <h2 class="h2" style="color:#fff">{e(stmt["title"])}</h2>
    {"".join(f'<p class="lead">{e(x)}</p>' for x in stmt["paras"])}
  </div>
</section>
"""
    html += prose("Built for the Middle Market", "Our Practice")
    html += cards("A Disciplined Approach to Maximizing Shareholder Value", "Our Approach")
    html += cards("Specialized Industry Coverage", "Industries", link=True)
    html += prose("Experienced Professionals", "Our Team", f'<p><a class="link-arrow" href="{root}index.html#team">Meet the team</a></p>')
    html += prose("Global Reach", "Global Platform", cls="section section--paper")
    html += prose("Research-Driven Advisory", "Research",
                  f'<div class="btn-row"><a class="btn" href="{root}insights/index.html">Explore Our Industry Research</a></div>' if REPORTS_LIVE else "")
    html += f"""
<section class="section section--paper">
  <div class="wrap about-wrap">
    <h2 class="h2">Key Facts</h2>
    <table class="facts">{rows}</table>
    {f'<h2 class="h2">Current Industry Reports</h2>{chr(10)}    <ul class="about-list">{report_links}</ul>' if REPORTS_LIVE else ""}
    <p class="note">Information as of {AS_OF}. See the <a href="disclosures.html">Important Disclosures</a>.</p>
  </div>
</section>
"""
    html += faq_html(faqs)
    c = cp["cta"]
    html += cta(root, c["title"], sub=c["sub"], paras=c["paras"])
    html += footer(root)
    write("about.html", html, crumbs=[("Middle Market", ""), ("About", "about.html")],
          schema=[faq_schema(faqs)] + [person_schema(m) for m in team_members()])


AI_BOTS = ("GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User",
           "Google-Extended", "Googlebot", "Applebot", "Applebot-Extended", "Bingbot", "Meta-ExternalAgent", "Meta-ExternalFetcher",
           "Amazonbot", "DuckAssistBot", "MistralAI-User", "CCBot", "cohere-ai")


def write_discovery_files():
    """sitemap.xml, robots.txt and llms.txt for search engines and AI assistants (absolute URLs from SITE_URL)."""
    pages = list(dict.fromkeys(SITEMAP + [i["url"] for i in PUBLISHED_REPORTS]))
    prio = lambda r: "1.0" if r == "index.html" else "0.8" if r.startswith(("industries/", "insights/")) or r == "about.html" else "0.6"
    urls = "".join(f"  <url><loc>{abs_url(r)}</loc><lastmod>{SITE_UPDATED}</lastmod><priority>{prio(r)}</priority></url>\n" for r in pages)
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
    base = urlparse(SITE_URL).path
    pdfs = f"Disallow: {base}insights/*.pdf\n" if REPORTS_LIVE else ""   # the PDFs are behind the download form; the report pages are open
    robots = ("# Search engines and AI assistants are welcome to read and cite this site.\n"
              "User-agent: *\nAllow: /\nDisallow: " + base + "_build/\n" + pdfs + "\n"
              + "".join(f"User-agent: {b}\nAllow: /\n{pdfs}\n" for b in AI_BOTS)
              + f"Sitemap: {SITE_URL}sitemap.xml\n")
    sec = "\n".join(f"- [{x['name']}]({abs_url('industries/' + x['slug'] + '.html')}): {x['short']}" for x in SECTORS)
    def md_link(i):
        md = i['url'][:-5] + '.md'
        return f" ([Markdown]({abs_url(md)}))" if os.path.exists(os.path.join(SITE, md)) else ""
    rep = "\n".join(f"- [{i['title']}]({abs_url(i['url'])}){md_link(i)}: {i['summary']}" for i in PUBLISHED_REPORTS)
    faqs = "\n".join(f"- **{q}** {a}" for q, a in home_faqs())
    llms = f"""# {ORG_NAME}

> Benchmark International's Middle Market team represents privately held companies across the United States with $50M–$500M in total enterprise value (TEV) on strategic sales, mergers, and qualifying change-of-control transactions, across five industries: {", ".join(x["name"] for x in SECTORS)}.

Information as of {AS_OF}. Contact: {PHONE}, {EMAIL}. Parent firm: Benchmark International (https://www.benchmarkintl.com/).

## Key pages
- [Home]({SITE_URL}): overview, team, client stories, and contact form
- [About]({abs_url('about.html')}): key facts about the Middle Market team
- [Industries]({abs_url('industries/index.html')}): the five industries
- [Transactions]({abs_url('transactions.html')}): selected completed transactions
{f"- [Insights]({abs_url('insights/index.html')}): quarterly M&A industry reports" + chr(10) if REPORTS_LIVE else ""}- [Important Disclosures]({abs_url('disclosures.html')})
- [Full text for AI assistants]({abs_url('llms-full.txt')}): every page's key facts, services, team, industries, and FAQs in one file

## Industries
{sec}

{"## Industry reports" + chr(10) + rep + chr(10) + chr(10) if REPORTS_LIVE else ""}## Common questions
{faqs}
"""
    for name, body in (("sitemap.xml", sitemap), ("robots.txt", robots), ("llms.txt", llms), ("llms-full.txt", llms_full())):
        with open(os.path.join(SITE, name), "w", encoding="utf-8") as f:
            f.write(body)
        print("wrote", name)


def llms_full():
    """The whole site as one plain Markdown file, so an AI assistant can answer from it without crawling every page."""
    out = [f"# {ORG_NAME}", "",
           "> Benchmark International's Middle Market team represents privately held companies across the United States with $50M–$500M "
           "in total enterprise value (TEV) on strategic sales, mergers, and qualifying change-of-control transactions.", "",
           f"Information as of {AS_OF} (updated {SITE_UPDATED}). Source: {SITE_URL}", "", "## Key facts", ""]
    out += [f"- **{k}:** {v}" for k, v in about_facts()]
    out += ["", "## Services", ""] + [f"### {n}\n\n{d}\n" for n, d in SERVICES]
    out += ["## Team", ""]
    for m in team_members():
        phone, email = TEAM_CONTACT.get(m["img"], (None, None))
        contact = " | ".join(x for x in (phone, email) if x)
        out += [f"### {m['name']}, {m['role'].replace(' | ', ', ')}", ""] + ([contact, ""] if contact else []) + [p + "\n" for p in m["bio"]]
    out += ["## Industries", ""]
    for s in SECTORS:
        rel = f"industries/{s['slug']}.html"
        cp = pagecopy.load(s["slug"], [x[0] for x in s["segments"]])
        out += [f"### {s['name']}", "", f"Page: {abs_url(rel)}", "", s["tagline"], "", f"Completed transactions: {s['count']}+ (as of {AS_OF}).", "", "Sectors:", ""]
        out += [f"- **{seg[0]}:** " + " ".join(cp.get("segments", {}).get(seg[0]) or [seg[1]]) for seg in s["segments"]]
        if s.get("report"):
            r = current_report(s["slug"])
            out += ["", f"Current report: [{r['title']}]({abs_url(r['url'])}). {r['summary']}"]
            fq = os.path.join(HERE, "reports", f"{s['slug']}-q{r['quarter']}-{r['year']}", "faq.json")
            if os.path.exists(fq):
                out += ["", f"#### From the {r['title']}", ""] + [f"**{q}**\n{a}\n" for q, a in json.load(open(fq, encoding="utf-8"))["faqs"]]
        faqs = PAGE_FAQS.get(rel, [])
        if faqs:
            out += ["", f"#### {s['name']} M&A: common questions", ""] + [f"**{q}**\n{a}\n" for q, a in faqs]
        out.append("")
    if REPORTS_LIVE:
        out += ["## Industry reports", ""] + [f"- [{i['title']}]({abs_url(i['url'])}): {i['summary']}" for i in PUBLISHED_REPORTS]
    out += ["", "## Selected completed transactions", "", f"Publicly announced transactions advised by Benchmark International. Full list: {abs_url('transactions.html')}", ""]
    for t in TOMBSTONES:
        bits = [t["sector_name"], t.get("segment", ""), t.get("year", "")]
        line = f"- {t['seller']} {t['verb'].lower()} {t['buyer']} ({', '.join(b for b in bits if b)})"
        if t.get("desc"):
            line += f": {t['desc']}"
        if t.get("link"):
            line += f" [Announcement]({t['link']})"
        out.append(line)
    out += ["", "## Common questions", ""]
    seen = set()
    for rel in ("index.html", "about.html"):
        for q, a in PAGE_FAQS.get(rel, []):
            if q not in seen:
                seen.add(q)
                out.append(f"**{q}**\n{a}\n")
    out += ["## Important disclosures", "", f"Benchmark International does not provide valuations, appraisals, or fairness opinions. "
            f"Full disclosures: {abs_url('disclosures.html')}", ""]
    return "\n".join(out)


def remove_unpublished_reports():
    """While REPORTS_LIVE is False: deletes the Insights page, report pages, PDFs, Markdown copies and old report
    addresses from the site folder, so nothing links to or serves them. Rebuild the reports to bring them back."""
    targets = [os.path.join(SITE, "insights"), os.path.join(SITE, "reports")]
    for rel in ("report-terms.html", "email-preferences.html"):
        if os.path.exists(os.path.join(SITE, rel)):
            os.remove(os.path.join(SITE, rel))
            print("removed", rel)
    shots = os.path.join(SITE, "assets", "img", "reports")
    if os.path.isdir(shots):
        import shutil
        shutil.rmtree(shots)
        print("removed assets/img/reports")
    for d in targets:
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if f.endswith((".html", ".pdf", ".md")):
                os.remove(os.path.join(d, f))
                print("removed", os.path.relpath(os.path.join(d, f), SITE))


def page_report_redirects():
    for i in INSIGHTS:
        if not i.get("legacy"):
            continue
        target = f"../{i['url']}"
        write(f"reports/{i['legacy']}.html", index=False, html=f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Redirecting…</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{abs_url(i['url'])}">
<meta http-equiv="refresh" content="0; url={target}">
</head><body><p>This report has moved to <a href="{target}">{e(i['title'])}</a>.</p></body></html>
""")
        # Reports were also published as insights/<industry>-sector-report-...; that address redirects here.
        old = i["slug"].replace("-industry-report-", "-sector-report-")
        if old != i["slug"]:
            write(f"insights/{old}.html", index=False, html=f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Redirecting…</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{abs_url(i['url'])}">
<meta http-equiv="refresh" content="0; url={i['slug']}.html">
</head><body><p>This report has moved to <a href="{i['slug']}.html">{e(i['title'])}</a>.</p></body></html>
""")


if __name__ == "__main__":
    page_home()
    page_industries()
    for i, s in enumerate(SECTORS):
        page_sector(i, s)
    for old, new in LEGACY.items():
        page_legacy(old, new)
    # The industry pages were for a time published under sectors/; keep those addresses working.
    page_legacy("index", "index", "sectors")
    for s in SECTORS:
        page_legacy(s["slug"], s["slug"], "sectors")
    page_transactions()
    if REPORTS_LIVE:
        page_insights()
        page_report_redirects()
    else:
        remove_unpublished_reports()
    page_disclosures()
    if REPORTS_LIVE:
        page_report_terms()
        page_email_preferences()
    page_about()
    write_discovery_files()
