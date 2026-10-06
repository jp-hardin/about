# New pages from the revised, stress-tested version. exec'd inside gen.py after the helpers exist.
U.update(dict(
 alt2='https://www.altarum.org/news-and-insights/september-2026-health-sector-economic-indicators-briefs',
 nhefs='https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data/nhe-fact-sheet',
 pfsf='https://www.cms.gov/newsroom/fact-sheets/calendar-year-cy-2027-medicare-physician-fee-schedule-proposed-rule',
 oppsr='https://www.cms.gov/medicare/payment/prospective-payment-systems/hospital-outpatient/regulations-notices',
 maf='https://www.cms.gov/newsroom/fact-sheets/2027-medicare-advantage-part-d-rate-announcement',
 teleh='https://telehealth.hhs.gov/providers/telehealth-policy/telehealth-policy-updates',
 mcaid='https://www.medicaid.gov/resources-for-states/working-families-tax-cut-legislation',
 ptax='https://www.cms.gov/newsroom/fact-sheets/amending-indirect-hold-harmless-threshold-health-care-related-taxes-proposed-rule-cms-2452-p',
 whp='https://www.whitehouse.gov/presidential-actions/2026/04/adjusting-imports-of-pharmaceuticals-and-pharmaceutical-ingredients-into-the-united-states/',
 cah10k='https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm',
 omipr='https://www.owens-minor.com/pressreleases/owens-minor-announces-definitive-agreement-to-divest-products-healthcare-services-segment-to-platinum-equity-for-375mm-in-cash-and-a-retained-equity-stake/',
))

def dtable(cols, head, rows, pad=5, fs=11.2):
    g = f'display: grid; grid-template-columns: {cols}; column-gap: 16px'
    o = [f'<div style="font-size: {fs}px; line-height: 16px; letter-spacing: 0.15px">',
         f'<div style="{g}; padding: 7px 12px; background: #2E2E2E; color: #FFFFFF; font-weight: 700; font-size: 9.5px; line-height: 14px; letter-spacing: 1.6px; text-transform: uppercase; align-items: center">' + ''.join(f'<div>{h}</div>' for h in head) + '</div>']
    for r in rows:
        o.append(f'<div style="{g}; padding: {pad}px 12px; border-bottom: 1px solid #D9D3CA">' + ''.join((f'<div style="font-weight: 700">{c}</div>' if i == 0 else f'<div>{c}</div>') for i, c in enumerate(r)) + '</div>')
    o.append('</div>')
    return '\n'.join(o)

def H3(t, m='6px 0 0'):
    return f'<h3 style="margin: {m}; {SERIF}; font-weight: 600; font-size: 16px; line-height: 22px; letter-spacing: 0; color: #B68757">{t}</h3>'

def NOTE(t):
    return f'<div style="margin-top: auto; font-size: 10.5px; line-height: 15px; letter-spacing: 0.2px">{t}</div>'

IMPL = '150px 1fr 1fr'

def add_policy():
    b = EYE('Policy and price') + H2('How reimbursement and trade policy reach the value of an individual business') + P(
        'Program-wide payment updates are the starting point for a buyer&#39;s analysis. Buyers then model the company&#39;s own payer contracts, billing codes, service mix and geography, because a Medicare Advantage plan payment update reaches providers only through their individual contracts and an aggregate home health estimate differs from the rate change at any one agency.'
    ) + dtable(IMPL, ['Exposure', 'How buyers model it', 'What an owner can prepare'], [
        ['Physician services', 'Buyers model the proposed conversion-factor change together with code-level relative value units, site-of-service rules and commercial contracts, and they apply the higher factor only to clinicians who qualify under an advanced alternative payment model', 'A revenue bridge by code and payer that shows reimbursement, volume and wage sensitivities separately'],
        ['Home health and outpatient', 'Buyers separate base-rate changes, adjustments, wage indices and procedure eligibility from the headline update', 'The historical service mix repriced under the proposed schedule, and updated when the final rule is issued'],
        ['Medicaid and coverage', 'Eligibility changes affect applicable adults and state programs differently, and enrollment loss, authorization delays and uncompensated care can reduce revenue and collections', 'Exposure mapped by state and patient category, with the expansion-adult rules applied only to the patients and service lines they cover'],
        ['Pharmaceutical manufacturing', 'Tariff treatment depends on product, origin and company agreement, so buyers ask for evidence of eligibility before they credit US capacity with a tariff advantage or a higher valuation', 'A schedule of exposure by product, customer and origin, the contractual pass-through terms and evidence of qualifying treatment'],
    ]) + H3('Pharmaceutical tariffs in detail') + P(
        f'The April 2 proclamation sets a 100% default rate on covered patented products and ingredients, effective July 31 for the companies named in Annex III and September 29 for others. Approved onshoring treatment carries a 20% rate that rises to 100% on April 2, 2030. Specified products from the European Union, Japan, South Korea, Switzerland and Liechtenstein receive 15% unless a lower rate applies, and the United Kingdom framework starts at 10%, with any reduction contingent on a further agreement and notice. Companies with qualifying most-favored-nation pricing and onshoring arrangements pay zero through January 20, 2029, and further conditional product exclusions apply. Generics, including biosimilars, remain excluded ({L("White House proclamation, clauses 3 to 6", U["whp"])}).'
    ) + P('In an acquisition, the importer&#39;s eligibility and agreement terms, including any change-of-control provisions, determine whether a reduced rate carries over to the new owner, and buyers will ask to see the agreement itself.'
    ) + NOTE('Proposed rules remain proposed as of October 5, 2026.')
    page('X-policy', 'Policy and price', b, 0)

def add_prov_impl():
    b = EYE('Provider Services: what this means for buyers and owners') + H2('Each care model is valued on different evidence') + dtable(IMPL, ['Care model', 'What supports a premium', 'What buyers test, and who is buying'], [
        ['Physician practice management and eye care', 'Clinician retention, organic visit growth, ancillary earnings, transferable contracts and a compliant ownership structure', 'Earnings and compensation by provider after closing, referral concentration and state ownership restrictions. Buyers include specialty platforms and MyEyeDr.'],
        ['Surgery centers', 'Case mix, surgeon commitment, block utilization, payer rates and repeatable local density', 'Surgeon and referral concentration, facility investment and ownership economics. Buyers include health systems and specialist surgery center operators'],
        ['Urgent and occupational care', 'Site-level contribution, density of access points, employer contracts and same-site demand', 'The ramp of new sites, staffing coverage, seasonality and episodic volumes. Buyers include HCA, Concentra and regional operators'],
        ['Behavioral health and applied behavior analysis', 'Documented outcomes, authorized capacity, clinician retention and disciplined utilization', 'Medical necessity, coding, authorization denials and Medicaid exposure. Buyers include specialist strategic and sponsor-backed platforms'],
        ['Physical therapy', 'Visits, net revenue per visit, therapist productivity and durable same-clinic growth', 'Wage pressure, patient acquisition and founder retention. Buyers include U.S. Physical Therapy and regional platforms'],
        ['Home health', 'Referral diversity, case mix, collection quality and scalable clinical supervision', 'Exposure to Medicare&#39;s home health payment model, coding, eligibility and agency-level reimbursement. Buyers include home care platforms and sponsors'],
        ['Hospice', 'Clinical quality, referral breadth and stable operating leadership', 'Eligibility documentation, length of stay, cap exposure and survey history. Buyers include specialist hospice and home care platforms'],
        ['Personal care', 'Contract durability, caregiver capacity, density and alignment of wages with rates', 'State Medicaid rates, authorizations and labor availability. Buyers include Addus and regional care platforms'],
    ]) + H3('What this means for owners') + P(
        'A practice with $4 million of EBITDA, diversified referrals, durable clinician coverage and proven economics at new sites can attract interest as a platform. The same EBITDA produced largely by the founder, or resting on one fragile reimbursement stream, is more likely to be valued as an add-on or to carry contingent consideration. Owners who assemble provider, site, payer and referral schedules before setting price expectations enter those conversations better prepared, and a commercially insured patient mix supports value when realized rates, collections and retention support the earnings.'
    ) + NOTE('The buyers named are examples drawn from the results and transactions on the preceding pages.')
    page('X-prov', 'Provider Services: buyers and owners', b, 0)

def add_ls_impl():
    b = EYE('Life Sciences & Diagnostics: what this means for buyers and owners') + H2('Testing volume, research backlog and recurring products are valued separately') + dtable(IMPL, ['Business model', 'What supports a premium', 'What buyers test, and who is buying'], [
        ['Clinical and outreach laboratories', 'Durable ordering relationships, test mix, accreditation and profitable collection of billed revenue', 'Reimbursement by code, medical necessity, denials and customer concentration. Buyers include Labcorp and Quest'],
        ['Clinical research sites', 'Repeat sponsor awards, investigator depth, enrollment performance and geographic density', 'Study concentration, investigator departures, cancellations and pass-through revenue. Buyers include networks such as Headlands and Summit'],
        ['Contract research and research services', 'Quality of executable backlog, repeat clients and sustainable staff utilization', 'Conversion of bookings to cash, cancellation rights, biotech funding and project profitability. Buyers include research strategics and specialist sponsors'],
        ['Contract development and manufacturing', 'Validated processes, repeat contracted work, capacity utilization and required quality standards', 'Customer and program concentration, transfer costs, capital spending, inspection history and tariff eligibility by product. Buyers include manufacturing strategics and sponsors'],
        ['Tools, reagents and pathology consumables', 'Repeat purchasing, an installed base, differentiated chemistry and a place in the customer&#39;s workflow', 'Durability of intellectual property, customer qualification, substitution and margin after manufacturing investment. Buyers include Danaher, Thermo Fisher and Merck KGaA'],
        ['Device development and testing', 'Regulatory expertise, repeat programs and engineering depth beyond the founder', 'Project dependence, utilization and transferability of expertise. Buyers include strategic networks such as Resonetics and NAMSA'],
    ]) + H3('What this means for owners') + P(
        'A recurring consumables company earns its premium by demonstrating repeat orders, customer qualification and durable gross margin. A research business demonstrates executable backlog and continuity of investigators or technical staff, and a laboratory bridges billed revenue to cash by code and payer. Presenting the business on the evidence that fits its model serves an owner better than a single life sciences median, which conceals the reason a buyer would pay a premium.'
    ) + H3('Exposures to resolve before going to market') + P(
        f'Laboratory owners can model the scheduled 2027 reductions to the Clinical Laboratory Fee Schedule test by test, which gives a more accurate result than a 15% cut applied to total revenue ({L("CMS proposed rule", U["pfsf"])}). Research businesses can distinguish funded awards from proposals and cancellable work. Manufacturers can quantify the investment needed to fulfill committed production, because buyers value contracted earnings and give little credit for unused capacity.'
    ) + NOTE('The buyers named are examples drawn from the results and transactions on the preceding pages.')
    page('X-ls', 'Life Sciences & Diagnostics: buyers and owners', b, 0)

def add_mp_impl():
    b = EYE('Medical Products & Distribution: what this means for buyers and owners') + H2('Protected economics matter more than the size of the business') + dtable(IMPL, ['Business model', 'What supports a premium', 'What buyers test, and who is buying'], [
        ['Proprietary devices', 'Protected technology, clinical adoption, required clearances and a durable installed base', 'Product concentration, reimbursement, competing technology and post-market quality. Buyers include strategics such as Stryker and Danaher'],
        ['Contract manufacturing', 'Qualified programs, recurring production and capabilities that are difficult to replace', 'Customer concentration, requalification risk, scrap, capacity and maintenance capital spending. Buyers include manufacturing strategics and specialist sponsors'],
        ['Consumables and reprocessing', 'Repeat purchase demand, clinical preference and recurring use in the customer&#39;s workflow', 'Substitution, pricing pressure, supplier risk and support for product claims. Buyers include Aspen Surgical and product strategics'],
        ['Dental products and laboratories', 'Repeat demand, proprietary products or meaningful local laboratory density', 'Exposure to discretionary procedures, dentist concentration and technician retention. Buyers include dental strategics and consolidators'],
        ['Medical-surgical distribution', 'Exclusive access, customer retention, route density and reliable conversion of working capital to cash', 'Purchasing-group pricing, inventory obsolescence, vendor concentration and commodity margins. Buyers include distributors and operationally focused sponsors'],
        ['Home equipment and supplies', 'Recurring service or supply demand, collection discipline and geographic density', 'Payer authorization, equipment utilization, competitive bidding and compliance. Buyers include Hanger, Cardinal Health and specialist platforms'],
    ]) + H3('What this means for owners') + P(
        'A manufacturer substantiates its regulatory status, quality history and the durability of customer qualification. A distributor shows contractual access, retention and cash conversion after inventory investment. Both benefit from identifying tariff exposure and presenting sustainable earnings after one-time refunds or reversals, because buyers will discount high recurring revenue when margins, working capital or customer access are fragile.'
    ) + H3('Reading the Owens & Minor transaction') + P(
        f'The $375 million cash payment was accompanied by a 5% retained interest and preferred equity economics, and the seller also kept specified tax assets ({L("Owens & Minor announcement", U["omipr"])}). A comparison across sub-sectors therefore requires the full consideration, comparable EBITDA, debt, the scope acquired and normalized cash conversion.'
    ) + NOTE('The buyers named are examples drawn from the results and transactions on the preceding pages.')
    page('X-mp', 'Medical Products & Distribution: buyers and owners', b, 0)

def add_ph_impl():
    b = EYE('Pharmacy & Healthcare Services: what this means for buyers and owners') + H2('Buyers underwrite gross profit, cash conversion and contract durability') + dtable(IMPL, ['Business model', 'What supports a premium', 'What buyers test, and who is buying'], [
        ['Specialty pharmacy and infusion', 'Durable payer and manufacturer access, clinical capability and patient retention', 'Net margin by therapy, access to limited-distribution drugs, authorizations, inventory and receivables. Buyers include Option Care Health and Soleo Health'],
        ['Long-term care pharmacy', 'Facility retention, service quality, operating capacity and profitable resident growth', 'Effects of negotiated prices, facility concentration, rebates and reimbursement lag. Buyers include Guardian and regional operators'],
        ['Locum tenens', 'Credentialing quality, repeat facility demand and durable clinician relationships', 'Specialty concentration, fill rates, compliance and dependence on individual recruiters. Buyers include specialist platforms such as VeloSource'],
        ['Travel and per diem staffing', 'Recurring accounts, workforce diversity and margin at normal bill rates', 'Crisis revenue, spread compression, payroll funding and client churn. Buyers include platforms such as Care Career and Elite365'],
        ['Perfusion and specialist outsourced care', 'Multi-year contracts, retention and dependable clinical coverage', 'Hospital concentration, change-of-control consents and specialist retention. Buyers include Strata Critical Medical'],
        ['Healthcare logistics', 'Reliable service levels, network density and specialized handling', 'Customer concentration, quality failures and required network investment. Buyers include strategic and sponsor-backed platforms such as Life Couriers'],
    ]) + H3('What this means for owners') + P(
        'Pharmacy revenue growth can reflect drug prices or an expensive therapy mix without producing equivalent gross profit or cash, and staffing revenue can recover while wage spreads remain weak. Owners in these businesses are best served by leading with a bridge from revenue to gross profit, EBITDA and cash, by showing contract retention, reimbursement lag and working capital needs, and by separating recurring specialist demand from strike, crisis and pandemic activity.'
    ) + H3('Physician alignment is part of the price') + P(
        f'The Specialty Alliance acquired Solaris Health in November 2025 for approximately $1.9 billion in cash, and Cardinal Health owned approximately 76% of the alliance after closing. The alliance also issued units to physicians and management, and Cardinal&#39;s filing accounts for part of that value as compensation after the combination, so the units cannot simply be added to the cash price to estimate enterprise value ({L("Cardinal Health Form 10-K, Note 2", U["cah10k"])}).'
    ) + NOTE('The buyers named are examples drawn from the results and transactions on the preceding pages.')
    page('X-ph', 'Pharmacy & Healthcare Services: buyers and owners', b, 0)

def add_bridge():
    b = EYE('Valuation: from reference data to a private company') + H2('A private company&#39;s value is built from matched evidence') + dtable(IMPL, ['Evidence', 'What it shows', 'What makes it comparable'], [
        ['Public trading', 'Relative market sentiment toward minority, liquid shares, expressed as enterprise value', 'A matching sub-sector and EBITDA definition, with allowance for control premiums, size and growth'],
        ['Strategic precedents', 'What specific acquirers paid for control or for assets', 'Separation of synergies, partial interests, earnouts, distressed sales and retained economics'],
        ['Sponsor platforms', 'Pricing for businesses that can support a standalone investment', 'Matching scale, management, leverage, growth and recurring cash generation'],
        ['Private add-ons', 'Value to an existing operating platform', 'Integration can remove overhead and scarcity can raise the price, so an add-on can sell at or above platform pricing'],
        ['Founder-owned private transactions', 'The closest pricing evidence when business model, size and risk align', 'Verified consideration and earnings the buyer accepted, with all-industry surveys as context'],
    ]) + dtable(IMPL, ['EBITDA scale', 'The question buyers ask', 'Evidence that answers it'], [
        ['$2 million to $5 million', 'Whether the business can stand alone as an investment or fits best inside a larger platform', 'The cost of replacing the owner, clinician and customer concentration, and finance and compliance infrastructure'],
        ['$5 million to $10 million', 'Whether the operating model can sustain growth without the founder', 'Management depth, unit economics by site or customer, repeatable growth and capital needs'],
        ['$10 million and above', 'Whether scale translates into a durable platform', 'Leadership, reporting, integration capability and cash conversion across locations'],
    ]) + H3('Illustration: the earnings a buyer accepts drive proceeds') + P(
        'Assume a company reports adjusted EBITDA of $7.0 million, and a buyer deducts $0.6 million for the recurring cost of replacing the owner and $0.4 million of earnings it considers unsustainable, leaving $6.0 million of accepted EBITDA. At an assumed multiple of 8.0x, enterprise value is $48.0 million. After $8.0 million of net debt and $2.0 million of seller fees, proceeds before tax are $38.0 million in a full cash sale with no other adjustments. Valuing the unadjusted $7.0 million at the same multiple would overstate enterprise value by $8.0 million.'
    ) + NOTE('All figures in the illustration are hypothetical, and 8.0x is an arithmetic assumption. The size bands describe how buyers frame their questions and do not represent pricing tiers. Earnouts, rollover equity, escrows, leases and working capital adjustments also affect the cash received at closing.')
    page('X-bridge', 'Valuation bridge', b, 0)

def add_ready():
    b = EYE('Seller readiness: timing and proceeds') + H2('Should an owner transact now, prepare or wait?') + P(
        'The decision rests on expected net proceeds and execution risk for the owner&#39;s own business, and the quarter&#39;s largest transaction or a public-company median says little about either. An owner&#39;s desired liquidity, future role, control, clinician continuity and patient-care objectives come first, and they shape the choice of buyer and process.'
    ) + dtable(IMPL, ['Path', 'When it is compelling', 'What must be true'], [
        ['Launch a process', 'Durable earnings, retention and reporting can already be demonstrated, and several buyers have a credible strategic reason to engage', 'The earnings hold up through a quality-of-earnings review, and contracts, licenses and regulatory timelines support a closing'],
        ['Prepare for 6 to 12 months', 'A discrete, achievable improvement in reporting, retention, a contract renewal or a seasoned group of sites can reduce a visible discount', 'The improvement is measurable, and the expected increase in proceeds exceeds the cost of preparation and the risk of delay'],
        ['Wait and retain ownership', 'Important growth or reimbursement outcomes remain unresolved, or current terms fall short of the owner&#39;s economic and operating goals', 'Remaining independent is adequately funded and attractive after capital spending, working capital and exposure to downside scenarios'],
        ['Consider a partial sale', 'The owner wants liquidity and continued participation, or a partner can provide capital and operating infrastructure', 'Rollover valuation, governance, dilution, distributions, exit rights and compensation are acceptable on their own terms, apart from the headline price'],
    ]) + H3('What buyers will request first') + P(
        '<span style="font-weight: 700">Financial:</span> three years of monthly statements, trailing results, an EBITDA bridge supported by evidence, revenue, margin and cash by site or service, and schedules of debt, leases, capital spending and working capital.<br><span style="font-weight: 700">Commercial and clinical:</span> payer, customer and referral concentration, contracts and their change-of-control terms, clinician employment, compensation, retention and credentialing, and growth and retention by patient or customer cohort.<br><span style="font-weight: 700">Regulatory:</span> licenses, accreditation, billing and coding reviews, audit history, quality metrics, privacy and cybersecurity controls, and the transaction requirements of each state involved.'
    ) + H3('Measuring the cost of waiting') + P(
        'A sale today can be compared with a later sale weighted by its probability, including interim cash distributions, the investment in preparation, taxes and the risk of lower earnings or pricing. A projected increase in EBITDA adds value for the owner only when it exceeds the capital the owner must fund and the added uncertainty of a later exit, and the comparison is most useful when it includes both a base case and a downside case for reimbursement and retention.'
    ) + NOTE('Statutory review periods, payer consents and enrollment requirements depend on jurisdiction, transaction structure and the specific contracts.')
    page('X-ready', 'Seller readiness', b, 0)

PRIMARY = [
    ('Altarum Health Sector Economic Indicators, September 28, 2026', 'alt2'), ('CMS National Health Expenditure fact sheet', 'nhefs'),
    ('CMS 2027 Physician Fee Schedule proposed rule', 'pfsf'), ('CMS hospital outpatient regulations and notices', 'oppsr'),
    ('CMS 2027 home health proposed rule fact sheet', 'hh'), ('CMS 2027 Medicare Advantage and Part D rate announcement', 'maf'),
    ('HHS Medicare telehealth policy updates', 'teleh'), ('Medicaid.gov implementation materials', 'mcaid'),
    ('CMS provider-tax proposed rule, July 21, 2026', 'ptax'), ('White House proclamation on pharmaceutical imports, April 2, 2026', 'whp'),
    ('Cardinal Health fiscal 2026 Form 10-K', 'cah10k'), ('Owens & Minor announcement, October 7, 2025', 'omipr'),
]
