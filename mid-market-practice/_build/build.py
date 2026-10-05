#!/usr/bin/env python3
"""Static site generator for the Benchmark International Mid-Market site.

Edit content in this file (sectors, team, stories) or in tombstones.json, then run:

    python3 mid-market-practice/_build/build.py

Pages are written to mid-market-practice/. No dependencies beyond the Python standard library.
"""
import json
import os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

PHONE = "813-771-6675"
PHONE_HREF = "tel:8137716675"
EMAIL = "Tampa@Benchmarkintl.com"
HUBSPOT = {"region": "na1", "portalId": "4039078", "formId": "902fb6ab-81fb-42c4-abf8-5355537a8abb"}
AS_OF = "October 2026"

# ─────────────────────────────────────────────────────────────────────────────
# Icons (24x24, stroke = currentColor)
# ─────────────────────────────────────────────────────────────────────────────
ICONS = {
    "industrial": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
    "business-services": '<rect x="3" y="7" width="18" height="13" rx="1"/><path d="M8 7V5a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2M3 13h18"/>',
    "consumer": '<path d="M4 7h16l-1.5 12.5a1 1 0 0 1-1 .5h-11a1 1 0 0 1-1-.5L4 7zM9 7V5a3 3 0 0 1 6 0v2"/>',
    "healthcare": '<path d="M12 21s-7.5-4.6-9.3-9.5C1.5 8.2 3.6 4.5 7.2 4.5c2 0 3.5 1 4.8 2.7 1.3-1.7 2.8-2.7 4.8-2.7 3.6 0 5.7 3.7 4.5 7-1.8 4.9-9.3 9.5-9.3 9.5zM8 12h2.5l1-2 2 4 1-2H16"/>',
    "technology": '<rect x="5" y="5" width="14" height="14" rx="1"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
}


def icon(slug):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[slug] + "</svg>")


# Services offered on every sector page
SERVICES = [
    ("Sell-Side M&A", "A full sale to the right strategic acquirer or financial sponsor, run as a confidential, competitive process from positioning through closing."),
    ("Recapitalizations & Partial Sales", "Take chips off the table while keeping a stake in the upside, through majority or minority recapitalizations with private equity and family offices."),
    ("Strategic Partnerships & Growth Capital", "Find a partner that brings capital, capabilities or market access to accelerate the next phase of growth."),
    ("Exit Planning & Valuation", "Understand what your company is worth today, what drives value in your sector, and the steps that will maximize it before you go to market."),
]

# Old 12-sector URLs → new sector (redirect stubs keep any shared links working)
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
        "name": "Industrial",
        "count": 290,
        "tagline": "Advising founder-led manufacturers, distributors and industrial service companies on sales, recapitalizations and partnerships.",
        "short": "Manufacturing, industrial distribution, building products, energy and environmental services, and transportation.",
        "overview": [
            "Reshoring, automation, infrastructure investment and the push for supply-chain resilience have put middle-market industrial companies at the top of many buyers' lists. Strategic acquirers want capabilities and capacity they can't build quickly. Private equity platforms want founder-built businesses with engineering know-how, sticky customers and room to grow through add-ons.",
            "Our Industrial group advises owners of manufacturers, fabricators, distributors and industrial service providers across five segments. We translate machine capability, certifications, installed base and customer relationships into the terms buyers use to value them, then run a competitive process that puts those qualities in front of the right strategic and financial partners.",
        ],
        "segments": [
            ("Manufacturing & Industrial Technology", "Engineered products and precision manufacturing where proprietary processes, certifications and approved-vendor status create durable advantages.",
             ["Precision machining & fabrication", "Aerospace & defense components", "Electronics & microelectronics", "Plastics & molding", "Coatings & metal finishing", "Pumps, vacuum & flow control"]),
            ("Industrial Distribution & Services", "Value-added distributors and field-service providers with recurring maintenance revenue and dense local relationships.",
             ["Gases & specialty supplies", "Hydraulics & fluid power", "MRO & parts distribution", "Fire & life safety", "Industrial maintenance & turnarounds", "Material handling"]),
            ("Building Products & Construction Services", "Specialty trades, infrastructure contractors and building-products businesses benefiting from infrastructure spending and residential demand.",
             ["Mechanical, electrical & plumbing", "Roofing & exteriors", "Infrastructure & marine construction", "Crane & equipment services", "Building products distribution", "Testing & inspection"]),
            ("Energy, Power & Environmental Services", "Businesses serving power generation, water, energy transition and regulated environmental markets with non-discretionary demand.",
             ["Power generation & backup power", "Energy consulting", "Water treatment & chemicals", "Environmental & emergency response", "Recycling & waste services"]),
            ("Transportation & Logistics", "Carriers, 3PLs and specialized logistics providers with diversified shippers and capabilities buyers can't easily replicate.",
             ["Dedicated & intermodal trucking", "3PL & customs brokerage", "Export crating & rigging", "Pallets & packaging logistics", "Marine & subsea"]),
        ],
        "themes": [
            ("Reshoring and supply-chain resilience", "Customers are qualifying domestic suppliers and dual sources, which raises the value of certified capacity and long-standing OEM relationships."),
            ("Platform building by private equity", "Sponsors keep assembling industrial platforms through add-on acquisitions, creating competitive tension for well-run founder-owned businesses."),
            ("Infrastructure and electrification", "Spending on infrastructure, grid modernization and water is lifting demand for specialty contractors, power services and environmental providers."),
            ("Service and aftermarket revenue", "Buyers pay a premium for recurring maintenance, repair and aftermarket revenue that smooths project and capital-spending cycles."),
        ],
        "value": [
            ("Engineering know-how", "Proprietary processes, certifications such as AS9100 and ISO, and engineered-to-order capabilities."),
            ("Customer stickiness", "Approved-vendor status, long OEM relationships and recurring service agreements."),
            ("Capacity & equipment", "Modern equipment, documented maintenance and room for a buyer to add volume."),
        ],
    },
    {
        "slug": "business-services",
        "name": "Business Services",
        "count": 230,
        "tagline": "Advising owners of commercial, professional and tech-enabled service businesses with recurring revenue and loyal clients.",
        "short": "Commercial and facility services, marketing and tech-enabled services, engineering and consulting, financial and insurance services, and staffing and human capital.",
        "overview": [
            "Business services is one of the most active and diverse areas of middle-market M&A. Buyers look for recurring or repeat revenue, a diversified client base, scalable delivery and a management team that can support growth. Those qualities attract strategic consolidators and private equity firms building platforms through acquisition.",
            "Our Business Services group represents commercial and facility services providers, marketing and tech-enabled service firms, engineering and consulting practices, financial and insurance services businesses, and staffing and human capital firms. We frame contracts, retention, utilization and margin profile the way buyers evaluate them, and we know which consolidators and sponsors are active in each niche.",
        ],
        "segments": [
            ("Commercial & Facility Services", "Route-based, compliance-driven and contracted services where recurring revenue and density create value.",
             ["Fire protection & life safety", "Managed print & document services", "Testing, inspection & certification", "Security services", "Painting & property maintenance"]),
            ("Marketing, Sales & Tech-Enabled Services", "Agencies, outsourced sales and technology consultancies that help clients grow, often with long relationships and embedded workflows.",
             ["Outsourced sales & brokerage", "Promotional products", "Digital strategy & consulting", "Education technology consulting", "Display & signage"]),
            ("Engineering, Architecture & Consulting", "Licensed professional-services firms whose talent, backlog and public-sector relationships attract national platforms.",
             ["Civil & transportation engineering", "Architecture", "Surveying & geospatial", "Forensic engineering", "BIM & reality capture"]),
            ("Financial & Insurance Services", "Fee-based financial businesses with recurring commissions, renewals and high client retention.",
             ["Insurance brokerage & MGAs", "Claims adjusting", "Appraisal management", "Wealth & financial planning", "Trading technology"]),
            ("Staffing & Human Capital", "Staffing, search and workforce solutions firms with repeat client relationships, deep candidate networks and recurring placement revenue.",
             ["Commercial & light industrial staffing", "Professional & technical staffing", "Executive search", "Recruitment process outsourcing", "Talent development & HR consulting"]),
        ],
        "themes": [
            ("Consolidation by sponsor-backed platforms", "National platforms in fire and life safety, engineering, insurance and facility services continue to acquire founder-owned firms to add density and capabilities."),
            ("Premium for recurring revenue", "Contracted, subscription and inspection-driven revenue earns higher multiples than project work, so how revenue is presented matters."),
            ("Talent as a strategic asset", "In professional services, licensed people and their client relationships drive value, which puts retention planning and deal structure at the center of the process."),
            ("Tech enablement", "Firms that use technology to deliver services more efficiently, or to give clients better data, stand out to buyers seeking scalable models."),
        ],
        "value": [
            ("Recurring revenue", "Contracted, subscription, inspection or renewal revenue with demonstrated retention."),
            ("Client diversification", "Long-tenured relationships without outsized concentration."),
            ("Scalable operations", "Systems, KPIs and leadership that can support add-on acquisitions."),
        ],
    },
    {
        "slug": "consumer",
        "name": "Consumer",
        "count": 80,
        "tagline": "Advising founders of food, consumer brand, foodservice and consumer services businesses.",
        "short": "Food and beverage, consumer brands and products, foodservice and distribution, and consumer services.",
        "overview": [
            "Consumer buyers look for brands with pricing power, loyal customers, channel diversity and room to grow distribution. Strategic acquirers use acquisitions to add brands, categories and capabilities. Consumer-focused private equity firms and family offices back founders who have built a differentiated product and want a partner to scale it.",
            "Our Consumer group represents food and beverage producers, consumer brand owners, foodservice suppliers and distributors, and multi-site consumer services businesses. We present the brand's story, unit economics and growth runway in the way buyers underwrite them.",
        ],
        "segments": [
            ("Food & Beverage", "Producers and distributors of food and beverage products with quality certifications and loyal wholesale and retail customers.",
             ["Bakery & specialty foods", "Dairy & ingredients distribution", "Seafood import & processing", "Nutritional supplements", "Confectionery"]),
            ("Consumer Brands & Products", "Branded products with recognized names, enthusiast followings and multi-channel distribution.",
             ["Outdoor & recreation", "Beauty & wellness", "Sporting goods & accessories", "Flags & specialty manufacturing", "Containers & storage"]),
            ("Foodservice & Distribution", "Equipment, parts and supply distributors that keep restaurants, hospitality and retail operating.",
             ["Foodservice equipment & supplies", "Commercial coffee equipment", "Outdoor kitchen appliances", "CPG sales agencies", "Dealer distribution"]),
            ("Consumer Services & Retail", "Multi-site and route-based consumer services with recurring local demand.",
             ["Car wash & auto care", "Collision repair", "Equipment rental & storage", "Home services"]),
        ],
        "themes": [
            ("Brands with pricing power", "Buyers favor brands that have held price and volume through inflation, and that can show it in their data."),
            ("Omnichannel growth", "Businesses balanced across wholesale, retail, foodservice and e-commerce are less exposed to any single channel and easier to scale."),
            ("Strategic portfolio building", "Strategic acquirers buy niche brands and distribution businesses to fill category gaps faster than they could build them."),
            ("Multi-site consolidation", "Consumer services categories such as car wash, collision repair and home services keep consolidating under sponsor-backed platforms."),
        ],
        "value": [
            ("Brand equity", "Recognized brands, loyal customers and demonstrable pricing power."),
            ("Channel diversity", "Balanced exposure across retail, foodservice, e-commerce and wholesale."),
            ("Margin & capacity", "Gross-margin resilience and production or distribution capacity a buyer can fill."),
        ],
    },
    {
        "slug": "healthcare",
        "name": "Healthcare",
        "count": 55,
        "tagline": "Advising healthcare providers, life sciences and medical products companies, and pharmacy and healthcare services businesses.",
        "short": "Provider services, life sciences and diagnostics, medical products and distribution, and pharmacy and healthcare services.",
        "overview": [
            "Healthcare remains one of the most resilient and actively consolidated sectors in the middle market. Demand is essential and growing, and health systems, public strategics and private equity platforms continue to acquire providers and suppliers to extend their reach.",
            "Our Healthcare group represents physician and therapy practices, urgent care operators, laboratories, medical device and product companies, and pharmacy and healthcare services businesses. We show buyers the clinical quality, payer mix and growth behind each business while managing the regulatory and diligence complexity these transactions bring.",
        ],
        "segments": [
            ("Provider Services", "Clinics, practices and care providers with strong referral relationships and clinical reputations.",
             ["Urgent care", "Optometry & eye care", "Pediatric & physical therapy", "Multi-specialty medical groups", "Emergency medical services", "Renal care"]),
            ("Life Sciences & Diagnostics", "Laboratories, research sites and product-development firms serving pharma, biotech and device companies.",
             ["Clinical & pathology labs", "Biologics & reagents", "Clinical research sites", "Human-factors & device design"]),
            ("Medical Products & Distribution", "Manufacturers and distributors of medical devices, consumables and equipment.",
             ["Surgical instrument reprocessing", "Emergency medical supplies", "Respiratory & anesthesia products", "Dental devices", "Orthopedic products"]),
            ("Pharmacy & Healthcare Services", "Pharmacy, infusion, staffing and logistics businesses supporting providers and patients.",
             ["Specialty & mail-order pharmacy", "Home infusion", "Pharmaceutical delivery", "Clinical staffing"]),
        ],
        "themes": [
            ("Health system and payer consolidation", "Hospital systems and national operators keep adding outpatient and urgent care sites to capture patients closer to home."),
            ("Outsourcing and specialization", "Providers and pharma companies increasingly outsource labs, research, staffing and logistics to specialists."),
            ("Strategic interest in med-tech niches", "Public strategics acquire focused device and product companies to add patented technology and clinical relationships."),
            ("Care moving to the home", "Home infusion, home care and delivery services benefit as care shifts away from inpatient settings."),
        ],
        "value": [
            ("Payer & revenue quality", "A balanced payer mix and clean revenue-cycle performance."),
            ("Clinical reputation", "Quality outcomes, referral relationships and regulatory standing."),
            ("Platform scalability", "Systems and leadership ready for new sites and add-on acquisitions."),
        ],
    },
    {
        "slug": "technology",
        "name": "Technology",
        "count": 105,
        "tagline": "Advising founders of software, IT services and technology businesses with recurring revenue and mission-critical products.",
        "short": "Vertical software, enterprise and infrastructure software, IT and managed services, and communications and hardware.",
        "overview": [
            "Vertical software and mission-critical technology businesses command some of the strongest buyer interest in the market. Software consolidators, strategic acquirers and private equity firms compete for products that are deeply embedded in customer workflows, with recurring revenue and high switching costs.",
            "Our Technology group has represented pharmacy software, field-service, lending, CAD/CAM and IT management platforms, as well as managed service providers and technology consultancies. We know how to present ARR, retention, unit economics and the product roadmap, and we bring buyers ranging from software holding companies to large-cap private equity.",
        ],
        "segments": [
            ("Vertical Software", "Industry-specific software that runs critical workflows for its customers.",
             ["Pharmacy & healthcare software", "Field service management", "Lending & financial software", "CAD/CAM & manufacturing software", "Marketing analytics"]),
            ("Enterprise & Infrastructure Software", "Horizontal software for IT, data and communications teams.",
             ["Endpoint & desktop management", "Database performance", "Email & communications governance"] ),
            ("IT & Managed Services", "IT providers and software development firms with contracted and recurring revenue.",
             ["Managed IT for education", "Microsoft-stack consulting", "Custom software development", "Data conversion & migration", "Government training & simulation"]),
            ("Communications & Hardware", "Telecom, electronics and specialized technology talent businesses.",
             ["Cloud communications", "Telecom services", "Optical inspection systems", "Cybersecurity & IT staffing"]),
        ],
        "themes": [
            ("Software consolidators", "Serial acquirers of vertical software are active buyers of founder-led companies with loyal niche customer bases."),
            ("Sponsor appetite for recurring revenue", "Private equity continues to favor ARR, high net revenue retention and low churn."),
            ("AI and data", "Buyers are looking for proprietary data and workflows that position a product to benefit from AI rather than be displaced by it."),
            ("Managed services and security", "Demand for managed IT and cybersecurity keeps pulling platforms toward MSPs with contracted revenue and certified talent."),
        ],
        "value": [
            ("Recurring revenue", "ARR growth, net revenue retention and low churn."),
            ("Mission-critical product", "Deep workflow integration and high switching costs."),
            ("Scalable unit economics", "Efficient customer acquisition and a credible product roadmap."),
        ],
    },
]
SECTOR_BY_SLUG = {s["slug"]: s for s in SECTORS}

# ─────────────────────────────────────────────────────────────────────────────
# Team
# ─────────────────────────────────────────────────────────────────────────────
TEAM_LEAD = [
    ("Jordan Houtz", "Managing Director", "jordan-houtz",
     ["As Head of Mid-Market, Jordan represents clients with revenues ranging from $75 million to $500 million across the United States. He is a seasoned investment banking and capital raising professional with more than 15 years of experience originating and executing complex domestic and cross-border M&A transactions for corporate and private equity clients.",
      "His deep experience on both the buy and sell sides of M&A transactions gives his clients a unique advantage in understanding deal dynamics and achieving their objectives. By leading full-cycle processes from idea and thesis generation through valuation, diligence, and negotiation, he is intimately involved in accomplishing his clients’ objectives. Jordan prides himself on building deep client relationships while achieving desired outcomes for stakeholders."]),
    ("Jared Hardin", "Managing Director", "jared-hardin",
     ["Mr. Hardin was raised in a military family, spending his early years traveling through Utah, Missouri, Ohio, Korea, Idaho, and Hong Kong. He ultimately landed in Texas where he has resided for the last two decades. His scholastic journey spanned a wide spectrum of learning, from Fine Arts to International Business to Management of Information Systems. He was driven to attain his MBA because he genuinely enjoys helping others learn and grow, but he also has a competitive nature that drives him toward success. His career has been quite diverse, having held the titles of Owner, COO, CIO, and CMO, and starting small businesses that gave him a role in everything from sales to HR and from IT to manufacturing. For these reasons, he understands and appreciates the intricacies of many different businesses.",
      "Jared’s role at Benchmark is about creating opportunities. In addition to his love for learning about businesses and introducing their owners to the distinctive tools and expertise that we offer, he is able to leverage his experience in deeply meaningful ways for our clients. He is driven to deliver results and get business owners truly excited about what is possible for the future."]),
    ("Alex Zykov", "Transaction Director", "alex-zykov",
     ["As a Transaction Director in Mid-Market, Alex leads the execution of our clients’ transactions from onboarding through signing and closing. He oversees every aspect of the process for middle-market clients across the industrial, consumer, business services, healthcare, and technology sectors. He makes sure clients understand each step and feel confident along the way, supporting them and our team through due diligence, evaluating competing offers, and leading negotiations through to the finish line.",
      "Alex’s career spans corporate development, executing transactions on Wall Street, and cofounding and running boutique advisory firms serving small and mid-sized businesses. Each step was deliberate: building the breadth of knowledge and experience needed to give his clients the best possible advice and help them achieve their goals. He discovered his passion for corporate finance at MIT, where he earned dual degrees in Economics and Management Science, and later earned his MBA from the University of Virginia’s Darden School of Business."]),
    ("Shannon Hess", "Client Engagement Director", "shannon-hess",
     ["Ms. Hess grew up in a military family, living on Army bases until she was nine years old. She enjoyed living in Germany and Hawaii, and traveling to many wonderful places. Because she is from a military family, her youth was a disciplined way of life with importance placed on punctuality, respect and loyalty.",
      "Shannon’s role at Benchmark International involves working with our Field Directors and clients we have met with that have had an interest in engaging our services, but have yet to do so. She is an additional internal point of contact for clients when they wish to speak with someone with the same or a different perspective when they need someone to discuss their fears or challenges. She has been with Benchmark International long enough to see many deals through from start to finish, and she conveys her valuable insights to address any questions clients may have."]),
]
TEAM_SUPPORT = [
    ("Sunny Garten", "Senior Deal Associate", "sunny-garten"),
    ("Michael Wynn", "Senior Deal Associate", "michael-wynn"),
    ("Jason Lisiak", "Research Associate", "jason-lisiak"),
    ("Alexandra Barr", "Transaction Support Associate", "alexandra-barr"),
    ("Josiah Warren", "Transaction Support Associate", "josiah-warren"),
    ("Luke Ernst", "Deal Analyst", "luke-ernst"),
]

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
    ("VDeyO2atUAU", "Seller Motivation", "What Goes Into the Decision to Sell?", "Deciding to sell your business is one of the most significant decisions you'll ever make. While maximizing proceeds is crucial, it's not the only factor that should influence your decision."),
    ("3oH70E1oJdQ", "Growth & Exit Strategy", "Taking Control of Your Growth and Exit", "Managing Director Jared Hardin discusses taking control of your growth and exit strategy. Learn more about various considerations and the right time to be on market."),
    ("wmGj-xUypSs", "Webinar", "The Process of Selling Your Business", "Are you considering selling your business but unsure where to start? This webinar will guide you through the entire process of selling your business, from preparation to negotiation."),
]

TOMBSTONES = json.load(open(os.path.join(HERE, "tombstones.json"), encoding="utf-8"))
for t in TOMBSTONES:
    t["sector_name"] = SECTOR_BY_SLUG[t["sector"]]["name"]


# ─────────────────────────────────────────────────────────────────────────────
# Partials
# ─────────────────────────────────────────────────────────────────────────────
def e(s):
    return escape(s, quote=True)


def head(title, desc, root, canonical=""):
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
<link rel="icon" href="{root}assets/img/brand/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(root, current=""):
    def cur(k):
        return ' aria-current="page"' if k == current else ""
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{root}index.html" aria-label="Benchmark International Mid-Market home">
      <img src="{root}assets/img/brand/benchmark-logo-white.png" alt="Benchmark International" width="138" height="26">
      <span class="brand-tag">Mid-Market</span>
    </a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Primary">
      <a href="{root}index.html#clients"{cur('clients')}>Clients</a>
      <a href="{root}industries/index.html"{cur('industries')}>Industries</a>
      <a href="{root}transactions.html"{cur('transactions')}>Transactions</a>
      <a href="{root}index.html#team"{cur('team')}>Team</a>
      <a href="{root}index.html#library"{cur('library')}>CEO Library</a>
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


def footer(root):
    ext = ' target="_blank" rel="noopener"'
    social = "".join(
        f'<a href="{href}" aria-label="{name}"{"" if name == "Email" else ext}><svg viewBox="0 0 24 24" aria-hidden="true">{path}</svg></a>'
        for name, (href, path) in SOCIAL.items())
    sectors = "".join(f'<li><a href="{root}industries/{s["slug"]}.html">{e(s["name"])}</a></li>' for s in SECTORS)
    sectors += f'<li><a href="{root}industries/index.html">All Industries</a></li>'
    pages = (f'<li><a href="{root}transactions.html">Transactions</a></li><li><a href="{root}index.html#team">Team</a></li>'
             f'<li><a href="{root}index.html#library">CEO Library</a></li><li><a href="{root}index.html#form">Contact</a></li>')
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{root}assets/img/brand/benchmark-logo-white.png" alt="Benchmark International" width="138" height="26">
        <p>Mid-Market represents privately held companies across the United States in sell-side M&amp;A, recapitalizations and growth partnerships.</p>
        <p><a href="{PHONE_HREF}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <div class="social">{social}</div>
      </div>
      <div><h4>Industries</h4><ul>{sectors}</ul></div>
      <div><h4>Mid-Market</h4><ul>{pages}</ul></div>
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
      <span>&copy; 2026 Benchmark International. All rights reserved.</span>
      <span><a href="https://www.benchmarkintl.com/terms/">Terms</a> &nbsp;/&nbsp; <a href="https://www.benchmarkintl.com/privacy-policy/">Privacy Policy</a></span>
    </div>
  </div>
</footer>
<script src="{root}assets/js/main.js" defer></script>
</body>
</html>
"""


def cta(root, title="It All Starts With a Conversation", form=False):
    form_html = ""
    if form:
        form_html = f"""
    <div class="form-wrap" id="form">
      <script charset="utf-8" src="https://js.hsforms.net/forms/embed/v2.js"></script>
      <script>
        if (window.hbspt) {{ hbspt.forms.create({{ region: "{HUBSPOT['region']}", portalId: "{HUBSPOT['portalId']}", formId: "{HUBSPOT['formId']}" }}); }}
        else {{ document.currentScript.insertAdjacentHTML('afterend', '<p>Call <a href="{PHONE_HREF}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a> to start the conversation.</p>'); }}
      </script>
    </div>"""
    button = "" if form else f'<div class="btn-row"><a class="btn" href="{root}index.html#form">Start the Conversation</a><a class="btn btn--light" href="{PHONE_HREF}">Call {PHONE}</a></div>'
    return f"""<section class="section section--knot cta" id="contact">
  <div class="wrap center reveal">
    <p class="eyebrow">Confidential. No pressure. No commitments.</p>
    <h2 class="display">{e(title)}</h2>
    <p class="lead">Our first step is always a confidential conversation exploring your goals, your company, and your options.</p>
    {button}
    <p class="contact-line">Call to speak with an M&amp;A expert at <a href="{PHONE_HREF}">{PHONE}</a></p>{form_html}
  </div>
</section>
"""


def tombstone(t, root, show_sector=False):
    text = e(f"{t['seller']} {t['buyer']} {t['sector_name']} {t.get('segment', '')} {t.get('desc', '')}".lower())
    if t.get("image"):
        face = f'<div class="tomb-face tomb-face--img"><img src="{root}{t["image"]}" alt="{e(t["seller"])} {e(t["verb"].lower())} {e(t["buyer"])}" loading="lazy" width="200" height="200"></div>'
    else:
        face = (f'<div class="tomb-face"><img src="{root}{t["seller_logo"]}" alt="{e(t["seller"])}" loading="lazy">'
                f'<span class="tomb-verb">{e(t["verb"])}</span>'
                f'<img src="{root}{t["buyer_logo"]}" alt="{e(t["buyer"])}" loading="lazy"></div>')
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


def industry_card(s, root):
    tags = "".join(f"<li>{e(seg[0])}</li>" for seg in s["segments"])
    return f"""<a class="ind-card" href="{root}industries/{s['slug']}.html">
  <div class="ind-icon">{icon(s['slug'])}</div>
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


def team_html(root):
    lead = ""
    for name, role, img, bio in TEAM_LEAD:
        paras = "".join(f"<p>{e(p)}</p>" for p in bio)
        lead += f"""<article class="member reveal">
  <img src="{root}assets/img/team/{img}.jpg" alt="{e(name)}" loading="lazy" width="480" height="480">
  <div class="member-body"><h3>{e(name)}</h3><div class="role">{e(role)}</div>
  <details><summary>Read Bio</summary>{paras}</details></div>
</article>"""
    support = "".join(
        f'<div class="member"><img src="{root}assets/img/team/{img}.jpg" alt="{e(n)}" loading="lazy" width="120" height="120"><div class="member-body"><h3>{e(n)}</h3><div class="role">{e(r)}</div></div></div>'
        for n, r, img in TEAM_SUPPORT)
    return f'<div class="team-lead">{lead}</div><div class="team-support">{support}</div>'


def write(rel, html):
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
        f'<a href="{e(t["link"])}" target="_blank" rel="noopener" title="{e(t["seller"])} / {e(t["buyer"])}"><img src="{t["image"]}" alt="{e(t["seller"])} {e(t["verb"].lower())} {e(t["buyer"])}" width="170" height="170"></a>'
        if t.get("link") else
        f'<a href="transactions.html" title="{e(t["seller"])} / {e(t["buyer"])}"><img src="{t["image"]}" alt="{e(t["seller"])} {e(t["verb"].lower())} {e(t["buyer"])}" width="170" height="170"></a>'
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
    cards = "".join(industry_card(s, root) for s in SECTORS) + cta_card(root)
    awards = "".join(f'<img src="assets/img/awards/award-{i}.png" alt="Benchmark International award" loading="lazy" width="520" height="300">' for i in range(1, 5))

    html = head("Mid-Market | Benchmark International",
                "Benchmark International's Mid-Market team advises owners of privately held companies with $75M–$500M in revenue on sales, recapitalizations and growth partnerships across Industrial, Business Services, Consumer, Healthcare and Technology.", root)
    html += header(root)
    html += f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Benchmark International · <span class="nowrap">Mid-Market</span></p>
    <h1 class="display">Selling a Business Isn't the End, <em>It’s a Beginning.</em></h1>
    <p class="lead">Maximize your company's value and achieve your goals with the world's #1 privately owned sell-side M&amp;A advisor.</p>
    <div class="btn-row">
      <a class="btn" href="#form">Start the Conversation</a>
      <a class="btn btn--light" href="industries/index.html">Explore Our Industries</a>
    </div>
  </div>
</section>

<section class="section--dark section--tight">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><div class="stat-num">#1</div><div class="stat-label">Privately owned sell-side M&amp;A advisor worldwide<sup>*</sup></div></div>
      <div class="stat"><div class="stat-num">$75M–$500M</div><div class="stat-label">Client revenue range we serve</div></div>
      <div class="stat"><div class="stat-num">5</div><div class="stat-label">Focused industry groups with dedicated sector expertise</div></div>
      <div class="stat"><div class="stat-num">15</div><div class="stat-label">Global offices across the Americas, Europe &amp; Africa</div></div>
    </div>
    <p class="note">* Based on PitchBook’s Q2 2026 Global League Tables.</p>
  </div>
</section>

<section class="section section--tight awards-band" id="recognition">
  <div class="wrap"><div class="awards reveal">{awards}</div></div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">You Built an Extraordinary Company</p>
      <h2 class="h2">Let's Talk About What's Next.</h2>
      <hr class="rule">
      <p>Most business owners only sell once in a lifetime. The stakes couldn’t be higher. Yet many don’t realize that an exit can take many forms, from a minority recapitalization to a full sale. Each option comes with different implications for your wealth, your family, and your company’s future.</p>
      <p>Benchmark International helps you explore these options with clarity, discretion, and a global network of qualified buyers.</p>
      <p>Whether you’re exploring a full exit, a partial sale, or simply preparing for the future, the right strategy ensures you maximize value, protect your legacy, and stay in control.</p>
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
      <p class="lead">We focus on serving Presidents, CEOs, Founders and business owners of privately held companies across Industrial, Business Services, Consumer, Healthcare and Technology. As you consider the next step in your legacy most business owners want three things:</p>
    </div>
    <div class="pillars">
      <div class="pillar reveal"><div class="pillar-num">01</div><h3 class="h3">Understand Every Option</h3><p>We'll make it possible for you to explore a full, partial, or partnership path. From local to global - we have you covered.</p></div>
      <div class="pillar reveal"><div class="pillar-num">02</div><h3 class="h3">Be Positioned for Maximum Value</h3><p>We'll help you to see your company through the eyes of buyers and investors so you can position your company to maximize the value.</p></div>
      <div class="pillar reveal"><div class="pillar-num">03</div><h3 class="h3">Execute with Confidence</h3><p>As you understand your options and position yourself to meet your goals, our highly experienced team works as your partner to navigate a discreet process that secures the right deal on your terms.</p></div>
    </div>
  </div>
</section>

<section class="section section--dark" id="who-we-help">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">Who We Help</p>
      <h2 class="h2" style="color:#fff">Perfect for Business Owners Who Are</h2>
    </div>
    <div class="fit">
      <div class="fit-item reveal"><h3>Looking to retire</h3><p>Looking to sell your business for retirement or move on to other business ventures.</p></div>
      <div class="fit-item reveal"><h3>Approached by a buyer</h3><p>Approached by a buyer and want to ensure you receive a fair offer on your deal.</p></div>
      <div class="fit-item reveal"><h3>Looking for a partner</h3><p>In need of a strategic partner or additional capital to grow your business and fit your needs.</p></div>
      <div class="fit-item reveal"><h3>Want to learn more</h3><p>Interested in learning the value of your company in order to plan for the future.</p></div>
    </div>
  </div>
</section>

<section class="section section--cream" id="clients">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">In Their Words</p>
      <h2 class="h2">We Have Been Working With Clients Around the World</h2>
    </div>
    <div class="testimonials">{testimonials}</div>
  </div>
</section>

<section class="section" id="industries">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Industry Expertise</p>
        <h2 class="h2">Five Industries. Deep Expertise.</h2>
        <p class="lead">Sector knowledge matters. We focus on five industries where we know the buyers, the valuation drivers and the questions that will come up in diligence.</p>
      </div>
      <a class="link-arrow" href="industries/index.html">View all industries</a>
    </div>
    <div class="ind-grid reveal">{cards}</div>
  </div>
</section>

<section class="section section--paper" id="transactions">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Businesses We've Served</p>
        <h2 class="h2">Selected Transactions</h2>
      </div>
      <a class="link-arrow" href="transactions.html">View all transactions by sector</a>
    </div>
  </div>
  <div class="marquee reveal"><div class="marquee-track">{marquee_items}{marquee_items.replace('<a ', '<a aria-hidden="true" tabindex="-1" ')}</div></div>
</section>

<section class="section" id="team">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">Mid-Market</p>
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
  </div>
</section>

"""
    html += cta(root, form=True)
    html += footer(root)
    write("index.html", html)


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
    <div class="ind-icon">{icon(s['slug'])}</div>
    <p class="eyebrow">{s['count']}+ completed transactions<sup>†</sup></p>
    <h2 class="h2">{e(s['name'])}</h2>
    <p class="lead">{e(s['tagline'])}</p>
    <p>{e(s['overview'][0])}</p>
    <h3 class="h3">Segments</h3>
    <ul class="seg-links">{segs}</ul>
    <div class="btn-row"><a class="btn" href="{s['slug']}.html">Explore {e(s['name'])}</a><a class="btn btn--ghost" href="{root}transactions.html#{s['slug']}">{len(deals)} Selected Transactions</a></div>
  </div>
  <div class="ind-row-deals tomb-grid tomb-grid--compact">{minis}</div>
</article>"""
    html = head("Industries | Mid-Market | Benchmark International",
                "Benchmark International's Mid-Market team focuses on five industries: Industrial, Business Services, Consumer, Healthcare and Technology.", root)
    html += header(root, "industries")
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Mid-Market</a> / Industries</div>
    <p class="eyebrow">Industry Expertise</p>
    <h1 class="display">Five Industries. Deep Expertise.</h1>
    <p class="lead">We focus on five industries where we have deep transaction experience and long relationships with the most active strategic and financial buyers. Sector focus means we know what drives value, who is buying, and how to run a process that gets you the best outcome.</p>
    <nav class="jump" aria-label="Industries">{''.join(f'<a href="#{s["slug"]}">{e(s["name"])}</a>' for s in SECTORS)}</nav>
  </div>
</section>

<section class="section--dark section--tight">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><div class="stat-num">5</div><div class="stat-label">Focused industry groups</div></div>
      <div class="stat"><div class="stat-num">{total}+</div><div class="stat-label">Completed transactions across these industries<sup>†</sup></div></div>
      <div class="stat"><div class="stat-num">{len(TOMBSTONES)}</div><div class="stat-label">Selected transactions featured on this site</div></div>
      <div class="stat"><div class="stat-num">#1</div><div class="stat-label">Privately owned sell-side M&amp;A advisor<sup>*</sup></div></div>
    </div>
    <p class="note">† Completed transactions tagged to these industries on benchmarkintl.com/about/our-success, as of {AS_OF}. * PitchBook Q2 2026 Global League Tables.</p>
  </div>
</section>

<section class="section">
  <div class="wrap ind-rows">{rows}</div>
</section>
"""
    html += cta(root)
    html += footer(root)
    write("industries/index.html", html)


def page_sector(i, s):
    root = "../"
    deals = deals_in(s["slug"])
    deals.sort(key=lambda t: (bool(t.get("cross")), not t.get("featured"), not t.get("desc"), -int(t.get("year") or 0)))
    tombs = "".join(tombstone(t, root) for t in deals)
    seg_counts = {seg[0]: sum(1 for t in deals if t.get("segment") == seg[0]) for seg in s["segments"]}
    chips = '<button class="chip" data-filter="all" aria-pressed="true">All Segments</button>' + "".join(
        f'<button class="chip" data-filter="{e(seg[0])}" aria-pressed="false">{e(seg[0])} <span>{seg_counts[seg[0]]}</span></button>'
        for seg in s["segments"])
    segments = "".join(f"""<article class="segment reveal" id="seg-{k + 1}">
  <div class="segment-num">{k + 1:02d}</div>
  <div class="segment-body">
    <h3>{e(name)}</h3>
    <p>{e(desc)}</p>
    <ul class="ind-tags">{''.join(f'<li>{e(x)}</li>' for x in subs)}</ul>
    <button class="link-arrow seg-jump" data-segment="{e(name)}">{seg_counts[name]} selected transactions</button>
  </div>
</article>""" for k, (name, desc, subs) in enumerate(s["segments"]))
    glance = "".join(f'<li><a href="#seg-{k + 1}">{e(seg[0])}</a><span>{seg_counts[seg[0]]}</span></li>' for k, seg in enumerate(s["segments"]))
    themes = "".join(f'<article class="theme reveal"><span class="theme-num">{k + 1:02d}</span><h3>{e(h)}</h3><p>{e(p)}</p></article>'
                     for k, (h, p) in enumerate(s["themes"]))
    value = "".join(f'<li><span class="vnum">0{k + 1}</span><div><h4>{e(h)}</h4><p>{e(p)}</p></div></li>' for k, (h, p) in enumerate(s["value"]))
    seen, buyers = set(), []
    for t in deals:
        b = t["buyer"].strip()
        if b.lower() in seen or any(w in b.lower() for w in ("individual", "undisclosed", "trust")):
            continue
        seen.add(b.lower())
        buyers.append(b)
    buyer_list = "".join(f"<li>{e(b)}</li>" for b in buyers[:18])
    services = "".join(f'<article class="service reveal"><h3>{e(h)}</h3><p>{e(p)}</p></article>' for h, p in SERVICES)
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
    team_cards = "".join(f"""<article class="member reveal">
  <img src="{root}assets/img/team/{img}.jpg" alt="{e(name)}" loading="lazy" width="480" height="480">
  <div class="member-body"><h3>{e(name)}</h3><div class="role">{e(role)}</div></div>
</article>""" for name, role, img, _ in TEAM_LEAD)
    cur = ' aria-current="page"'
    tabs = "".join(f'<a href="{x["slug"]}.html"{cur if x is s else ""}>{e(x["name"])}</a>' for x in SECTORS)

    html = head(f"{s['name']} | Mid-Market | Benchmark International",
                f"{s['name']} M&A advisory from Benchmark International's Mid-Market team. {s['tagline']}", root)
    html += header(root, "industries")
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Mid-Market</a> / <a href="index.html">Industries</a> / {e(s['name'])}</div>
    <div class="ind-icon" style="color:var(--gold)">{icon(s['slug'])}</div>
    <h1 class="display">{e(s['name'])}</h1>
    <p class="lead">{e(s['tagline'])}</p>
    <div class="btn-row"><a class="btn" href="#deals">Selected Transactions</a><a class="btn btn--light" href="{root}index.html#form">Discuss Your Business</a></div>
  </div>
</section>
<nav class="sector-tabs" aria-label="Industries"><div class="wrap">{tabs}</div></nav>

<section class="section--dark section--tight">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><div class="stat-num">{s['count']}+</div><div class="stat-label">Completed transactions<sup>†</sup></div></div>
      <div class="stat"><div class="stat-num">{len(s['segments'])}</div><div class="stat-label">Focus segments</div></div>
      <div class="stat"><div class="stat-num">{len(deals)}</div><div class="stat-label">Selected transactions below</div></div>
      <div class="stat"><div class="stat-num">{len(buyers)}</div><div class="stat-label">Distinct acquirers in those deals</div></div>
    </div>
    <p class="note">† Completed transactions tagged to {e(s['name'].lower())} industries on benchmarkintl.com/about/our-success, as of {AS_OF}.</p>
  </div>
</section>

<section class="section">
  <div class="wrap split split--top">
    <div class="reveal">
      <p class="eyebrow">Overview</p>
      <h2 class="h2">{e(s['name'])} M&amp;A Advisory</h2>
      <hr class="rule">
      {''.join(f'<p>{e(p)}</p>' for p in s['overview'])}
      <p>Every engagement is led by our Mid-Market team and backed by Benchmark International's global network of strategic acquirers, private equity groups, family offices and independent sponsors.</p>
    </div>
    <aside class="glance reveal">
      <p class="eyebrow">At a Glance</p>
      <h3>Segments We Cover</h3>
      <ul>{glance}</ul>
      <a class="btn" href="#deals">View Transactions</a>
    </aside>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Sector Coverage</p>
      <h2 class="h2">Where We Focus</h2>
      <p class="lead">We advise companies across {len(s['segments'])} segments of {e(s['name'].lower())}, including the sub-sectors listed below.</p>
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
    <div class="filter-bar" role="group" aria-label="Filter by segment">{chips}</div>
    <p class="result-count" aria-live="polite"></p>
    <div class="tomb-grid tomb-grid--detail" data-tomb-filter data-filter-key="segment" data-limit="12">{tombs}</div>
    <div class="center"><button class="btn btn--ghost show-more" hidden>Show All Transactions</button></div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Market Perspective</p>
      <h2 class="h2" style="color:#fff">What We're Seeing in {e(s['name'])}</h2>
    </div>
    <div class="themes">{themes}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--top">
    <div class="reveal">
      <p class="eyebrow">What Buyers Value</p>
      <h2 class="h2">Seeing Your Company Through a Buyer's Eyes</h2>
      <p class="lead">We build the story around the factors that drive valuation in {e(s['name'].lower())}, so qualified buyers compete on your terms.</p>
      <ul class="value-list">{value}</ul>
    </div>
    <div class="reveal">
      <p class="eyebrow">Who Is Buying</p>
      <h3 class="h3">Acquirers and Investors in Our Selected {e(s['name'])} Transactions</h3>
      <ul class="buyer-list">{buyer_list}</ul>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">How We Help</p>
      <h2 class="h2">Advisory Built Around Your Goals</h2>
      <p class="lead">An exit can take many forms. We help {e(s['name'].lower())} owners choose the path that fits their wealth, family and company goals.</p>
    </div>
    <div class="services">{services}</div>
  </div>
</section>

{feature}

<section class="section">
  <div class="wrap">
    <div class="section-head center reveal"><p class="eyebrow">Your Deal Team</p><h2 class="h2">Leadership Team</h2></div>
    <div class="team-lead">{team_cards}</div>
    <div class="center" style="margin-top:36px"><a class="link-arrow" href="{root}index.html#team">Meet the full team</a></div>
  </div>
</section>

<section class="section section--tight section--paper">
  <div class="wrap sector-nav">
    <a href="{prev_s['slug']}.html"><small>← Previous industry</small><strong>{e(prev_s['name'])}</strong></a>
    <a href="{next_s['slug']}.html" style="text-align:right"><small>Next industry →</small><strong>{e(next_s['name'])}</strong></a>
  </div>
</section>
"""
    html += cta(root, f"Considering a Transaction in {s['name']}?")
    html += footer(root)
    write(f"industries/{s['slug']}.html", html)


def page_legacy(old, new):
    write(f"industries/{old}.html", f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Redirecting…</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{new}.html">
<meta http-equiv="refresh" content="0; url={new}.html">
</head><body><p>This page has moved to <a href="{new}.html">{e(SECTOR_BY_SLUG[new]['name'])}</a>.</p></body></html>
""")


def page_transactions():
    root = ""
    chips = '<button class="chip" data-filter="all" aria-pressed="true">All Industries</button>' + "".join(
        f'<button class="chip" data-filter="{s["slug"]}" aria-pressed="false">{e(s["name"])} <span>{len(deals_in(s["slug"]))}</span></button>' for s in SECTORS)
    order = {s["slug"]: k for k, s in enumerate(SECTORS)}
    items = sorted(TOMBSTONES, key=lambda t: (order[t["sector"]], not t.get("featured"), -int(t.get("year") or 0)))
    tombs = "".join(tombstone(t, root, show_sector=True) for t in items)
    html = head("Transactions | Mid-Market | Benchmark International",
                "Selected completed transactions advised by Benchmark International across Industrial, Business Services, Consumer, Healthcare and Technology.", root)
    html += header(root, "transactions")
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Mid-Market</a> / Transactions</div>
    <p class="eyebrow">Our Success</p>
    <h1 class="display">Selected Transactions</h1>
    <p class="lead">A curated selection of completed transactions across our five industries. Tombstones marked <strong style="color:var(--gold)">Featured</strong> are signature Mid-Market transactions.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="filter-bar" role="group" aria-label="Filter by industry">{chips}</div>
    <input class="search" type="search" placeholder="Search by company, acquirer or segment" aria-label="Search transactions">
    <p class="result-count" aria-live="polite"></p>
    <div class="tomb-grid tomb-grid--detail" data-tomb-filter data-filter-key="sector">{tombs}</div>
    <p class="note">Source: Benchmark International transaction announcements and benchmarkintl.com/about/our-success, as of {AS_OF}. Selected transactions shown.</p>
  </div>
</section>
"""
    html += cta(root)
    html += footer(root)
    write("transactions.html", html)


if __name__ == "__main__":
    page_home()
    page_industries()
    for i, s in enumerate(SECTORS):
        page_sector(i, s)
    for old, new in LEGACY.items():
        page_legacy(old, new)
    page_transactions()
