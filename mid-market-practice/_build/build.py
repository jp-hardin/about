#!/usr/bin/env python3
"""Static site generator for the Benchmark International Mid-Market Practice site.

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
    "architecture-engineering": '<path d="M3 21h18M5 21V9l7-5 7 5v12M9 21v-6h6v6M9 11h.01M15 11h.01"/>',
    "business-services": '<rect x="3" y="7" width="18" height="13" rx="1"/><path d="M8 7V5a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2M3 13h18"/>',
    "construction": '<path d="M2 20h20M4 20V10l6-3v13M10 9l10-4v15M14 12h2M14 16h2M6 13h2M6 16h2"/>',
    "consumer-food-retail": '<path d="M4 7h16l-1.5 12.5a1 1 0 0 1-1 .5h-11a1 1 0 0 1-1-.5L4 7zM9 7V5a3 3 0 0 1 6 0v2"/>',
    "energy-utilities": '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    "environmental-recycling": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6C9.5 14.5 12 13 13 12"/>',
    "financial-services": '<path d="M3 21h18M4 10h16M12 3l9 5H3l9-5zM6 10v8M10 10v8M14 10v8M18 10v8"/>',
    "healthcare": '<path d="M12 21s-7.5-4.6-9.3-9.5C1.5 8.2 3.6 4.5 7.2 4.5c2 0 3.5 1 4.8 2.7 1.3-1.7 2.8-2.7 4.8-2.7 3.6 0 5.7 3.7 4.5 7-1.8 4.9-9.3 9.5-9.3 9.5zM8 12h2.5l1-2 2 4 1-2H16"/>',
    "industrial": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
    "software": '<path d="m8 9-4 3 4 3M16 9l4 3-4 3M14 5l-4 14"/>',
    "technology": '<rect x="5" y="5" width="14" height="14" rx="1"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
    "transportation": '<path d="M1 6h13v10H1zM14 10h4l3 3v3h-7M5.5 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM17.5 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/>',
}


def icon(slug):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[slug] + "</svg>")


# ─────────────────────────────────────────────────────────────────────────────
# Sectors
# `count` = completed transactions tagged to this industry on
# benchmarkintl.com/about/our-success (≈1,000 most recent closings, as of AS_OF).
# ─────────────────────────────────────────────────────────────────────────────
SECTORS = [
    {
        "slug": "architecture-engineering",
        "name": "Architecture & Engineering",
        "count": 44,
        "short": "Design, engineering and surveying firms whose licensed talent and long client relationships attract both strategic roll-ups and private equity.",
        "overview": "Consolidation across A&E has accelerated as national platforms and their private equity sponsors compete for licensed professionals, geographic density and public-sector contract vehicles. We help founders of architecture, civil, structural, MEP and surveying firms show buyers what makes their backlog, people and client relationships durable, and we run competitive processes that put a value on them.",
        "coverage": [
            ("Architecture & Interior Design", "K-12, higher education, healthcare, commercial and civic design studios."),
            ("Civil & Site Engineering", "Land development, transportation, water and municipal engineering."),
            ("Structural & MEP Engineering", "Building systems, structural, mechanical, electrical and plumbing design."),
            ("Surveying & Geospatial", "Land surveying, mapping, scanning and GIS services."),
            ("Forensic & Specialty Consulting", "Expert witness, claims, testing and inspection engineering."),
            ("Environmental & Planning", "Permitting, environmental compliance and planning consultancies."),
        ],
        "value": [
            ("Backlog & contract visibility", "Multi-year public and private backlog, master service agreements and repeat-client revenue."),
            ("Licensed talent", "Depth of PEs, RAs and PLSs, plus a retention plan that keeps the team in place after closing."),
            ("Platform or add-on fit", "Geographic density, service-line breadth and certifications that fill a buyer's gaps."),
        ],
    },
    {
        "slug": "business-services",
        "name": "Business Products & Services",
        "count": 169,
        "short": "Outsourced, tech-enabled and recurring-revenue service providers, one of the most active categories for private equity platform investment.",
        "overview": "Business services is Benchmark International's most active category. Buyers pay a premium for recurring or re-occurring revenue, a diverse customer base and scalable delivery models. Whether a company manages documents, staffing, marketing, facilities or B2B distribution, we position its contracts, retention and margin profile for both strategic acquirers and financial sponsors.",
        "coverage": [
            ("Managed Print & Document Services", "Office technology, MPS, imaging and records management."),
            ("Marketing & Communications", "Agencies, branding, digital marketing and promotional products."),
            ("Staffing & Human Capital", "Commercial, professional and specialty staffing; training and HR services."),
            ("Testing, Inspection & Compliance", "Labs, certification, safety and regulatory services."),
            ("Facility & Field Services", "Maintenance, uniform, landscaping and route-based services."),
            ("Consulting & Outsourced Services", "Management consulting, BPO, sales outsourcing and IT services."),
        ],
        "value": [
            ("Recurring revenue", "Contracted, subscription or route-based revenue with demonstrated retention."),
            ("Customer diversification", "No outsized concentration, with long tenure across blue-chip accounts."),
            ("Scalable operations", "Systems, KPIs and a management team that can support add-on acquisitions."),
        ],
    },
    {
        "slug": "construction",
        "name": "Construction",
        "count": 100,
        "short": "Specialty trades, infrastructure and building-products businesses benefiting from infrastructure spending and residential demand.",
        "overview": "Infrastructure investment, the shift to service-and-maintenance revenue, and an ageing owner base have made construction services one of the deepest buyer markets in the middle market. We represent specialty contractors, infrastructure builders and building-products companies, and we help buyers see past project lumpiness to the value of crews, bonding capacity, equipment and customer relationships.",
        "coverage": [
            ("Specialty Trades", "Mechanical, electrical, plumbing, roofing, fire and life safety."),
            ("Infrastructure & Heavy Civil", "Marine, utility, site work, concrete and crane services."),
            ("Building Products & Distribution", "Lumber, millwork, windows, doors and specialty supply."),
            ("Residential Services", "HVAC, plumbing, pools, landscaping and home services."),
            ("Testing & Inspection", "Materials testing, NDT and quality assurance."),
            ("Sports & Specialty Construction", "Athletic facilities, recreational and niche contracting."),
        ],
        "value": [
            ("Service & maintenance mix", "Recurring service revenue alongside project work smooths cash flow."),
            ("Crews & equipment", "Skilled, retained labor and a well-maintained fleet are hard to replicate."),
            ("Bonding & backlog", "Bonding capacity, a signed backlog and win rates that support the forecast."),
        ],
    },
    {
        "slug": "consumer-food-retail",
        "name": "Consumer, Food & Retail",
        "count": 83,
        "short": "Branded products, food manufacturing and distribution, and multi-channel retailers with loyal customers and defensible brands.",
        "overview": "Consumer buyers look for brands with pricing power, channel diversity and room to grow distribution. We represent food and beverage producers, consumer packaged goods companies, outdoor and lifestyle brands, and distributors, putting the brand's story and unit economics in front of strategic acquirers and consumer-focused private equity.",
        "coverage": [
            ("Food & Beverage", "Manufacturing, co-packing, specialty foods, beverages and spirits."),
            ("Consumer Brands", "Outdoor, recreation, personal care and lifestyle products."),
            ("Foodservice & Distribution", "Foodservice equipment, parts and broadline distribution."),
            ("Packaging", "Containers, packaging supplies and converters serving consumer brands."),
            ("Sales & Marketing Agencies", "Brokers and outsourced sales for consumer goods."),
            ("Retail & E-commerce", "Specialty retail, DTC and omnichannel businesses."),
        ],
        "value": [
            ("Brand equity", "Recognized brands, loyal customers and demonstrable pricing power."),
            ("Channel diversity", "Balanced exposure across retail, foodservice, e-commerce and wholesale."),
            ("Margin & capacity", "Gross-margin resilience and available capacity for a buyer to fill."),
        ],
    },
    {
        "slug": "energy-utilities",
        "name": "Energy, Resources & Utilities",
        "count": 27,
        "short": "Energy services, power generation, utility contractors and the energy transition, where buyers want technical expertise and long-standing customer relationships.",
        "overview": "Grid modernization, electrification and the energy transition are reshaping buyer appetite across energy services. We advise owners of utility contractors, power-systems integrators, energy consultancies and oilfield and industrial service providers, matching each business with strategic and financial buyers who value its technical credentials and installed base.",
        "coverage": [
            ("Power Generation & Backup Power", "Generators, power systems and critical-power services."),
            ("Utility & Grid Services", "Electrical, line and utility infrastructure contractors."),
            ("Energy Consulting & Efficiency", "Engineering, efficiency and sustainability advisory."),
            ("Oilfield & Industrial Services", "Equipment, chemicals and field services."),
            ("Renewables & Transition", "Solar, storage and clean-energy installers."),
            ("Water & Process", "Water treatment, chemicals and process solutions."),
        ],
        "value": [
            ("Technical credentials", "Licenses, safety record and OEM relationships that open doors."),
            ("Installed base", "Service agreements on equipment already in the field."),
            ("Transition exposure", "Positioning to benefit from electrification and decarbonization."),
        ],
    },
    {
        "slug": "environmental-recycling",
        "name": "Environmental & Recycling",
        "count": 25,
        "short": "Waste, remediation, recycling and environmental services, where regulation drives non-discretionary demand.",
        "overview": "Environmental services benefit from regulatory tailwinds and essential, non-discretionary demand. Buyers from global environmental platforms to infrastructure funds want permitted assets, technical expertise and recurring customer relationships. We help owners make sure their permits, safety culture and route density are fully valued.",
        "coverage": [
            ("Waste & Recycling", "Collection, recycling, organics and specialty waste streams."),
            ("Remediation & Abatement", "Environmental cleanup, abatement and restoration."),
            ("Environmental Consulting", "Ecology, compliance, monitoring and permitting."),
            ("Water & Wastewater", "Treatment technologies, pumps and water solutions."),
            ("Industrial Cleaning & Response", "Emergency response and industrial cleaning services."),
            ("Sustainable Materials", "Recycled plastics, containers and circular-economy businesses."),
        ],
        "value": [
            ("Permits & compliance", "Hard-to-obtain permits and an excellent regulatory record."),
            ("Non-discretionary demand", "Demand driven by regulation that holds up across cycles."),
            ("Route & asset density", "Route density, facilities and equipment that lower a buyer's costs."),
        ],
    },
    {
        "slug": "financial-services",
        "name": "Financial Services",
        "count": 19,
        "short": "Insurance distribution, wealth management, financial technology and specialty finance businesses with recurring fee income.",
        "overview": "Consolidators in insurance brokerage, wealth management and financial technology keep competing for books of business with recurring fees and strong client retention. We represent agencies, advisory firms, claims and valuation providers and financial software companies, framing producer economics, retention and regulatory standing for strategic and sponsor-backed buyers.",
        "coverage": [
            ("Insurance Distribution", "P&C and benefits agencies, brokerages and MGAs."),
            ("Claims & Adjusting", "Independent adjusting, TPA and claims services."),
            ("Wealth & Asset Management", "RIAs, financial planning and family-office services."),
            ("Financial Technology", "Trading, payments and financial data platforms."),
            ("Valuation & Appraisal", "Appraisal management and valuation services."),
            ("Accounting & Tax", "CPA, tax and outsourced finance practices."),
        ],
        "value": [
            ("Recurring fee income", "Commissions, AUM-based fees and renewals with high retention."),
            ("Producer & advisor depth", "A team not dependent on a single rainmaker."),
            ("Compliance standing", "Clean regulatory history and scalable compliance infrastructure."),
        ],
    },
    {
        "slug": "healthcare",
        "name": "Healthcare",
        "count": 57,
        "short": "Providers, life sciences, medical products and healthcare services: an essential, resilient sector with broad strategic and sponsor interest.",
        "overview": "Healthcare remains among the most resilient and actively consolidated sectors in the middle market. From urgent-care operators acquired by national health systems to life-science suppliers acquired by public strategics, we help owners show buyers their clinical quality, payer mix and growth while handling the regulatory and diligence complexity these transactions bring.",
        "coverage": [
            ("Provider Services", "Urgent care, physician practices, therapy, home health and EMS."),
            ("Life Sciences & Lab", "Reagents, biologics, diagnostics and laboratory services."),
            ("Medical Devices & Products", "Device design, equipment, consumables and distribution."),
            ("Healthcare Staffing", "Clinical, travel and specialty staffing."),
            ("Pharmacy & Pharma Services", "Specialty and infusion pharmacy and pharma services."),
            ("Healthcare IT & RCM", "Revenue-cycle management, data and software."),
        ],
        "value": [
            ("Payer & revenue quality", "A balanced payer mix and clean revenue-cycle performance."),
            ("Clinical reputation", "Quality outcomes, referral relationships and regulatory standing."),
            ("Platform scalability", "Systems and leadership ready for de novo growth and add-ons."),
        ],
    },
    {
        "slug": "industrial",
        "name": "Industrial",
        "count": 115,
        "short": "Manufacturing, distribution and industrial services, where engineering know-how and customer stickiness are the core of the business.",
        "overview": "Reshoring, automation and supply-chain resilience have put middle-market industrial companies at the top of many buyers' lists. We advise precision manufacturers, fabricators, industrial distributors and service providers, translating machine capability, certifications, engineered-to-order know-how and customer stickiness into the terms strategic and financial buyers use to value them.",
        "coverage": [
            ("Precision Manufacturing", "Machining, fabrication, tooling and contract manufacturing."),
            ("Industrial Distribution", "Gases, MRO, fluid power, parts and specialty supplies."),
            ("Industrial Services", "Maintenance, field service, fire protection and inspection."),
            ("Automation & Controls", "Robotics, drives, controls and systems integration."),
            ("Plastics & Packaging", "Molding, converting and industrial packaging."),
            ("Equipment & Specialty Vehicles", "Equipment OEMs, upfitting and vehicle components."),
        ],
        "value": [
            ("Engineering know-how", "Proprietary processes, certifications and engineered products."),
            ("Customer stickiness", "Approved-vendor status and long-standing OEM relationships."),
            ("Capacity & capex", "Modern equipment, available capacity and documented maintenance."),
        ],
    },
    {
        "slug": "software",
        "name": "Software",
        "count": 34,
        "short": "Vertical SaaS and mission-critical software businesses that attract the most active private equity and strategic acquirers.",
        "overview": "Vertical software with recurring revenue and high switching costs commands some of the strongest valuations in the market. We have represented pharmacy software, field-service, legal and compliance platforms in transactions with buyers ranging from software consolidators to large-cap private equity, and we know how to present ARR, retention, unit economics and the product roadmap.",
        "coverage": [
            ("Vertical SaaS", "Industry-specific platforms for healthcare, legal, trades and more."),
            ("Pharmacy & Healthcare Software", "Pharmacy management, clinical and practice software."),
            ("Field Service & Operations", "Inspection, workflow and mobile-workforce applications."),
            ("Enterprise & ERP", "ERP, CRM and business management systems."),
            ("Fintech & Payments Software", "Payments, billing and financial workflow tools."),
            ("Custom Development & Digital Agencies", "Product engineering and app development studios."),
        ],
        "value": [
            ("Recurring revenue", "ARR growth, net revenue retention and low churn."),
            ("Mission-critical product", "Deep workflow integration and high switching costs."),
            ("Scalable unit economics", "Efficient customer acquisition and a credible roadmap."),
        ],
    },
    {
        "slug": "technology",
        "name": "Technology",
        "count": 72,
        "short": "IT services, managed services, telecom and technology hardware businesses with contracted revenue and specialized engineering talent.",
        "overview": "Demand for cybersecurity, cloud, communications and IT infrastructure keeps pulling strategic acquirers and sponsor-backed platforms toward middle-market technology companies. We represent managed service providers, telecom and UCaaS companies, systems integrators and electronics businesses, putting contracted revenue, certified talent and vendor partnerships at the center of the story.",
        "coverage": [
            ("Managed IT & Cloud Services", "MSPs, cloud, data center and IT outsourcing."),
            ("Cybersecurity", "Security software, services and identity management."),
            ("Telecom & UCaaS", "Communications, VoIP and network services."),
            ("Systems Integration", "Infrastructure, AV and enterprise integration."),
            ("Electronics & Hardware", "Electronics manufacturing, test and specialty hardware."),
            ("Government Technology", "IT services and solutions for public-sector clients."),
        ],
        "value": [
            ("Contracted revenue", "Managed-service contracts and recurring support revenue."),
            ("Certified talent", "Engineering depth, certifications and security clearances."),
            ("Vendor partnerships", "Top-tier partner status with leading technology vendors."),
        ],
    },
    {
        "slug": "transportation",
        "name": "Transportation & Logistics",
        "count": 26,
        "short": "Trucking, logistics, specialized transport and marine businesses with asset-light models and diversified shippers.",
        "overview": "Supply-chain reconfiguration has heightened buyer interest in logistics businesses with specialized capabilities and diversified customers. We advise asset-based and asset-light carriers, 3PLs, crating and rigging specialists and marine businesses, showing buyers the value of network density, customer relationships, safety records and technology.",
        "coverage": [
            ("Trucking & Freight", "Truckload, LTL, expedited and dedicated carriers."),
            ("Third-Party Logistics", "Brokerage, freight forwarding and supply-chain management."),
            ("Last Mile & Courier", "Final-mile delivery, courier and parcel logistics."),
            ("Specialized Transport", "Crating, rigging, heavy-haul and project logistics."),
            ("Marine & Subsea", "Marine services, vessels and subsea technology."),
            ("Passenger & Fleet Services", "Coach, fleet and transportation services."),
        ],
        "value": [
            ("Network density", "Lanes, terminals and coverage that complement a buyer's network."),
            ("Shipper diversification", "Long-tenured customers across end markets."),
            ("Safety & technology", "Strong safety scores, telematics and visibility systems."),
        ],
    },
]
SECTOR_BY_SLUG = {s["slug"]: s for s in SECTORS}

# ─────────────────────────────────────────────────────────────────────────────
# Team
# ─────────────────────────────────────────────────────────────────────────────
TEAM_LEAD = [
    ("Jordan Houtz", "Managing Director", "jordan-houtz",
     ["As Head of the Mid-Market Practice, Jordan represents clients with revenues ranging from $100 million to $500 million across the United States. He is a seasoned investment banking and capital raising professional with more than 15 years of experience originating and executing complex domestic and cross-border M&A transactions for corporate and private equity clients.",
      "His deep experience on both the buy and sell sides of M&A transactions gives his clients a unique advantage in understanding deal dynamics and achieving their objectives. By leading full-cycle processes from idea and thesis generation through valuation, diligence, and negotiation, he is intimately involved in accomplishing his clients’ objectives. Jordan prides himself on building deep client relationships while achieving desired outcomes for stakeholders."]),
    ("Jared Hardin", "Managing Director", "jared-hardin",
     ["Mr. Hardin was raised in a military family, spending his early years traveling through Utah, Missouri, Ohio, Korea, Idaho, and Hong Kong. He ultimately landed in Texas where he has resided for the last two decades. His scholastic journey spanned a wide spectrum of learning, from Fine Arts to International Business to Management of Information Systems. He was driven to attain his MBA because he genuinely enjoys helping others learn and grow, but he also has a competitive nature that drives him toward success. His career has been quite diverse, having held the titles of Owner, COO, CIO, and CMO, and starting small businesses that gave him a role in everything from sales to HR and from IT to manufacturing. For these reasons, he understands and appreciates the intricacies of many different businesses.",
      "Jared’s role at Benchmark is about creating opportunities. In addition to his love for learning about businesses and introducing their owners to the distinctive tools and expertise that we offer, he is able to leverage his experience in deeply meaningful ways for our clients. He is driven to deliver results and get business owners truly excited about what is possible for the future."]),
    ("Alex Zykov", "Transaction Director", "alex-zykov",
     ["As a Transaction Director in Benchmark International’s Mid-Market Practice, Alex leads the execution of our clients’ transactions from onboarding through signing and closing. He oversees every aspect of the process for middle-market clients across the industrial, consumer, business services, healthcare, and technology sectors. He makes sure clients understand each step and feel confident along the way, supporting them and our team through due diligence, evaluating competing offers, and leading negotiations through to the finish line.",
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
    ("158933030", "Software", "software", "How pharmacy software leader Rx30 secured a strategic investment from PE giant GTCR to accelerate growth and innovation"),
    ("254578384", "Finance", "financial-services", "The strategic acquisition of Silexx by industry leader CBOE to deliver advanced analytics and execution tools globally"),
    ("696225328", "Energy & Power", "energy-utilities", "Why business executive Tim Wood decided to sell to explore new opportunities"),
    ("766180085", "Engineering", "architecture-engineering", "Joe Maynard shares how he was able to transition into the legacy and lifestyle he envisioned"),
    ("736906177", "Healthcare", "healthcare", "How leading provider of medical equipment O'Flynn Group scaled market presence to new heights"),
]

TESTIMONIALS = [
    ("Family Business", "We chose Benchmark International as our advisor in this process to ensure that we received best and highest value. The Benchmark International team played a pivotal role in terms of both deal structure, as well as guiding all parties through to a successful closing.", "Gina Gruenwald", "CEO of Blue Wave", "software"),
    ("Perfect Fit", "The Benchmark International team did a great job finding and matching us up with a perfect fit in a partner for an acquisition. We look forward to a great future thanks to their efforts in finding a partner that fits us very well and offers unlimited potential for our company and team going forward, and we couldn’t have asked for a better result!", "Greg Galante", "CEO of ACS", None),
    ("New Heights", "From our initial conversation through the final closing, Benchmark International was thoughtful, responsive, and clearly had our best interests top of mind. Thanks to them, we were able to find the perfect buyer for this next phase of our growth.", "Meighan Newhouse", "Co-Founder and CEO, Inspirant Group", "business-services"),
    ("Efficient M&A", "My thanks to the Benchmark International team. The process was far more complex than I ever thought it could be. They were right there every step of the way not only handling the issues but also walking me through the key points so that I could make the best decision for my employees, family, and customers.", "Luke Reinstetle", "Founder and CEO of Morgan Wood", "transportation"),
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
    <a class="brand" href="{root}index.html" aria-label="Benchmark International Mid-Market Practice home">
      <img src="{root}assets/img/brand/benchmark-logo-white.png" alt="Benchmark International" width="138" height="26">
      <span class="brand-tag">Mid-Market Practice</span>
    </a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Primary">
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
    sectors = "".join(f'<li><a href="{root}industries/{s["slug"]}.html">{e(s["name"])}</a></li>' for s in SECTORS[:6])
    sectors2 = "".join(f'<li><a href="{root}industries/{s["slug"]}.html">{e(s["name"])}</a></li>' for s in SECTORS[6:])
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{root}assets/img/brand/benchmark-logo-white.png" alt="Benchmark International" width="138" height="26">
        <p>The Mid-Market Practice represents privately held companies across the United States in sell-side M&amp;A, recapitalizations and growth partnerships.</p>
        <p><a href="{PHONE_HREF}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <div class="social">{social}</div>
      </div>
      <div><h4>Industries</h4><ul>{sectors}</ul></div>
      <div><h4>&nbsp;</h4><ul>{sectors2}</ul></div>
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
    text = e(f"{t['seller']} {t['buyer']} {t['sector_name']}".lower())
    if t.get("image"):
        face = f'<div class="tomb-face tomb-face--img"><img src="{root}{t["image"]}" alt="{e(t["seller"])} {e(t["verb"].lower())} {e(t["buyer"])}" loading="lazy" width="200" height="200"></div>'
    else:
        face = (f'<div class="tomb-face"><img src="{root}{t["seller_logo"]}" alt="{e(t["seller"])}" loading="lazy">'
                f'<span class="tomb-verb">{e(t["verb"])}</span>'
                f'<img src="{root}{t["buyer_logo"]}" alt="{e(t["buyer"])}" loading="lazy"></div>')
    sector = f'<span class="tomb-sector">{e(t["sector_name"])}</span>' if show_sector else ""
    badge = '<span class="tomb-badge">Featured</span>' if t.get("featured") else ""
    cap = f'<div class="tomb-cap"><strong>{e(t["seller"])}</strong><span>{e(t["verb"].lower())} {e(t["buyer"])}</span>{sector}</div>'
    attrs = f'data-sector="{t["sector"]}" data-text="{text}"'
    if t.get("link"):
        return f'<a class="tomb" href="{e(t["link"])}" target="_blank" rel="noopener" {attrs}>{badge}{face}{cap}</a>'
    return f'<div class="tomb" {attrs}>{badge}{face}{cap}</div>'


def vimeo(vid, title):
    return (f'<iframe src="https://player.vimeo.com/video/{vid}?badge=0&amp;autopause=0&amp;dnt=1" loading="lazy" '
            f'allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="{e(title)}"></iframe>')


def yt(vid, title):
    return (f'<button class="yt" data-id="{vid}" aria-label="Play: {e(title)}" '
            f'style="background-image:url(https://i.ytimg.com/vi/{vid}/hqdefault.jpg)"></button>')


def industry_card(s, root):
    tags = "".join(f"<li>{e(c[0])}</li>" for c in s["coverage"][:4])
    return f"""<a class="ind-card" href="{root}industries/{s['slug']}.html">
  <div class="ind-icon">{icon(s['slug'])}</div>
  <h3>{e(s['name'])}</h3>
  <p>{e(s['short'])}</p>
  <ul class="ind-tags">{tags}</ul>
  <div class="ind-meta"><span class="ind-count">{s['count']}+ recent transactions</span><span class="ind-go">Explore</span></div>
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
    cards = "".join(industry_card(s, root) for s in SECTORS)
    awards = "".join(f'<img src="assets/img/awards/award-{i}.png" alt="Benchmark International award" loading="lazy" width="520" height="300">' for i in range(1, 5))

    html = head("Mid-Market Practice | Benchmark International",
                "Benchmark International's Mid-Market Practice advises owners of privately held companies with $100M–$500M in revenue on sales, recapitalizations and growth partnerships across 12 industry sectors.", root)
    html += header(root)
    html += f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Benchmark International · Mid-Market Practice</p>
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
      <div class="stat"><div class="stat-num">$100M–$500M</div><div class="stat-label">Client revenue range we serve</div></div>
      <div class="stat"><div class="stat-num">100+</div><div class="stat-label">Industries served in the privately held middle market</div></div>
      <div class="stat"><div class="stat-num">15</div><div class="stat-label">Global offices across the Americas, Europe &amp; Africa</div></div>
    </div>
    <p class="note">* Based on PitchBook’s Q2 2026 Global League Tables.</p>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">You Built an Extraordinary Company</p>
      <h2 class="h2">Let's Talk About What's Next.</h2>
      <hr class="rule">
      <p>Most business owners only sell once in a lifetime. The stakes couldn’t be higher. Yet many don’t realize that an exit can take many forms — from a minority recapitalization to a full sale. Each option comes with different implications for your wealth, your family, and your company’s future.</p>
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
      <p class="lead">We focus on serving Presidents, CEOs, Founders and business owners in the privately-held middle market for more than 100 industries. As you consider the next step in your legacy most business owners want three things:</p>
    </div>
    <div class="pillars">
      <div class="pillar reveal"><div class="pillar-num">01</div><h3 class="h3">Understand Every Option</h3><p>We'll make it possible for you to explore a full, partial, or partnership path. From local to global - we have you covered.</p></div>
      <div class="pillar reveal"><div class="pillar-num">02</div><h3 class="h3">Be Positioned for Maximum Value</h3><p>We'll help you to see your company through the eyes of buyers and investors so you can position your company to maximize the value.</p></div>
      <div class="pillar reveal"><div class="pillar-num">03</div><h3 class="h3">Execute with Confidence</h3><p>As you understand your options and position yourself to meet your goals, our highly experienced team works as your partner to navigate a discreet process that secures the right deal on your terms.</p></div>
    </div>
  </div>
</section>

<section class="section" id="industries">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Industry Expertise</p>
        <h2 class="h2">Industries We Serve</h2>
        <p class="lead">Sector knowledge matters. Our dealmakers bring transaction experience across twelve industry groups, so we know the buyers, the valuation drivers and the questions that will come up in diligence.</p>
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
      <p class="eyebrow">Mid-Market Practice</p>
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

<section class="section section--cream">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">In Their Words</p>
      <h2 class="h2">We Have Been Working With Clients Around the World</h2>
    </div>
    <div class="testimonials">{testimonials}</div>
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

<section class="section section--dark">
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

<section class="section section--tight">
  <div class="wrap"><div class="awards reveal">{awards}</div></div>
</section>
"""
    html += cta(root, form=True)
    html += footer(root)
    write("index.html", html)


def page_industries():
    root = "../"
    cards = "".join(industry_card(s, root) for s in SECTORS)
    total = sum(s["count"] for s in SECTORS)
    html = head("Industries | Mid-Market Practice | Benchmark International",
                "Industry coverage of Benchmark International's Mid-Market Practice: architecture & engineering, business services, construction, consumer, energy, environmental, financial services, healthcare, industrial, software, technology and transportation.", root)
    html += header(root, "industries")
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Mid-Market Practice</a> / Industries</div>
    <p class="eyebrow">Industry Expertise</p>
    <h1 class="display">Sector Knowledge That Moves Deals Forward</h1>
    <p class="lead">Buyers pay for what they understand. Our industry groups combine sector-specific transaction experience with Benchmark International's global buyer network to position your company and run a competitive process.</p>
  </div>
</section>

<section class="section--dark section--tight">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><div class="stat-num">12</div><div class="stat-label">Industry groups</div></div>
      <div class="stat"><div class="stat-num">{total}+</div><div class="stat-label">Recent completed transactions across these sectors<sup>†</sup></div></div>
      <div class="stat"><div class="stat-num">100+</div><div class="stat-label">Industries served</div></div>
      <div class="stat"><div class="stat-num">#1</div><div class="stat-label">Privately owned sell-side M&amp;A advisor<sup>*</sup></div></div>
    </div>
    <p class="note">† Completed transactions tagged by industry on benchmarkintl.com/about/our-success, as of {AS_OF}. * PitchBook Q2 2026 Global League Tables.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Our Industries</p>
      <h2 class="h2">Explore Our Coverage</h2>
      <p class="lead">Choose an industry to see the sub-sectors we cover, what buyers value most, and selected transactions we have completed.</p>
    </div>
    <div class="ind-grid reveal">{cards}</div>
  </div>
</section>
"""
    html += cta(root)
    html += footer(root)
    write("industries/index.html", html)


def page_sector(i, s):
    root = "../"
    deals = [t for t in TOMBSTONES if t["sector"] == s["slug"]]
    tombs = "".join(tombstone(t, root) for t in deals)
    coverage = "".join(f'<div class="coverage-item reveal"><h4>{e(n)}</h4><p>{e(d)}</p></div>' for n, d in s["coverage"])
    value = "".join(f'<li><span class="vnum">0{k + 1}</span><div><h4>{e(h)}</h4><p>{e(p)}</p></div></li>' for k, (h, p) in enumerate(s["value"]))
    story = next((x for x in STORIES if x[2] == s["slug"]), None)
    quote = next((x for x in TESTIMONIALS if x[4] == s["slug"]), None)
    feature = ""
    if story or quote:
        left = ""
        if story:
            left = f'<article class="story reveal"><div class="story-media">{vimeo(story[0], story[3])}</div><div class="story-body"><p class="eyebrow">Client Story</p><p>{e(story[3])}</p></div></article>'
        right = ""
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

    html = head(f"{s['name']} | Mid-Market Practice | Benchmark International",
                f"{s['name']} M&A advisory from Benchmark International's Mid-Market Practice. {s['short']}", root)
    html += header(root, "industries")
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Mid-Market Practice</a> / <a href="index.html">Industries</a> / {e(s['name'])}</div>
    <div class="ind-icon" style="color:var(--gold)">{icon(s['slug'])}</div>
    <h1 class="display">{e(s['name'])}</h1>
    <p class="lead">{e(s['short'])}</p>
    <div class="btn-row"><a class="btn" href="#deals">Selected Transactions</a><a class="btn btn--light" href="{root}index.html#form">Discuss Your Business</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Overview</p>
      <h2 class="h2">Positioning {e(s['name'])} Companies for Maximum Value</h2>
      <hr class="rule">
      <p>{e(s['overview'])}</p>
      <p>Every engagement is led by the Mid-Market Practice and backed by Benchmark International's global network of strategic acquirers, private equity groups, family offices and independent sponsors.</p>
    </div>
    <div class="reveal">
      <div class="stats stats--light" style="grid-template-columns:1fr 1fr">
        <div class="stat"><div class="stat-num">{s['count']}+</div><div class="stat-label">Recent completed transactions in this sector<sup>†</sup></div></div>
        <div class="stat"><div class="stat-num">{len(deals)}</div><div class="stat-label">Featured below</div></div>
      </div>
      <p class="note">† Completed transactions tagged {e(s['name'])} on benchmarkintl.com/about/our-success, as of {AS_OF}.</p>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Sector Coverage</p>
      <h2 class="h2">Where We Focus</h2>
    </div>
    <div class="coverage">{coverage}</div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">What Buyers Value</p>
      <h2 class="h2" style="color:#fff">Seeing Your Company Through a Buyer's Eyes</h2>
      <p class="lead">We build the story around the factors that drive valuation in {e(s['name'].lower())}, so qualified buyers compete on your terms.</p>
    </div>
    <ul class="value-list reveal">{value}</ul>
  </div>
</section>

<section class="section" id="deals">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Selected Transactions</p>
        <h2 class="h2">{e(s['name'])} Tombstones</h2>
      </div>
      <a class="link-arrow" href="{root}transactions.html#{s['slug']}">All transactions</a>
    </div>
    <div class="tomb-grid">{tombs}</div>
  </div>
</section>

{feature}

<section class="section section--paper">
  <div class="wrap">
    <div class="section-head center reveal"><p class="eyebrow">Your Deal Team</p><h2 class="h2">Mid-Market Practice Leadership</h2></div>
    <div class="team-lead">{team_cards}</div>
    <div class="center" style="margin-top:36px"><a class="link-arrow" href="{root}index.html#team">Meet the full team</a></div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap sector-nav">
    <a href="{prev_s['slug']}.html"><small>← Previous industry</small><strong>{e(prev_s['name'])}</strong></a>
    <a href="{next_s['slug']}.html" style="text-align:right"><small>Next industry →</small><strong>{e(next_s['name'])}</strong></a>
  </div>
</section>
"""
    html += cta(root, f"Considering a Transaction in {s['name']}?")
    html += footer(root)
    write(f"industries/{s['slug']}.html", html)


def page_transactions():
    root = ""
    chips = '<button class="chip" data-sector="all" aria-pressed="true">All Industries</button>' + "".join(
        f'<button class="chip" data-sector="{s["slug"]}" aria-pressed="false">{e(s["name"])}</button>' for s in SECTORS)
    tombs = "".join(tombstone(t, root, show_sector=True) for t in TOMBSTONES)
    html = head("Transactions | Mid-Market Practice | Benchmark International",
                "Selected completed transactions advised by Benchmark International, organized by industry sector.", root)
    html += header(root, "transactions")
    html += f"""
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Mid-Market Practice</a> / Transactions</div>
    <p class="eyebrow">Our Success</p>
    <h1 class="display">Selected Transactions</h1>
    <p class="lead">A curated selection of completed transactions across our twelve industry groups. Tombstones marked <strong style="color:var(--gold)">Featured</strong> are signature transactions of the Mid-Market Practice.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="filter-bar" role="group" aria-label="Filter by industry">{chips}</div>
    <input class="search" type="search" placeholder="Search by company or acquirer" aria-label="Search transactions">
    <p class="result-count" aria-live="polite"></p>
    <div class="tomb-grid" data-tomb-filter>{tombs}</div>
    <p class="note">Source: benchmarkintl.com/about/our-success, as of {AS_OF}. Selected transactions shown; see the full record at <a href="https://www.benchmarkintl.com/about/our-success/">benchmarkintl.com</a>.</p>
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
    page_transactions()
