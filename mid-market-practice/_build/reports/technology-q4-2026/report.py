"""Page list and source grouping shared by the print build (gen.py) and the site build (web.py)."""
import lib
from pages_a import cover, p02, p03, p04, BRIEF, FIGS
from pages_b import p05, p06, p07, p08, p09, p10, p11, p12
from pages_c import p13, p14, p15, p16, p17, p18, p19, p20, sources_pages

# (file stem, canvas title, builder). The sources pages follow these and are built from the links used above.
PAGES = [
    ('Main', '01 Cover', cover),
    ('P02', '02 The six focus areas', p02),
    ('P03', '03 Deal market, financing and demand', p03),
    ('P04', '04 Policy, trade and tax', p04),
    ('P05', '05 Managed IT & Cloud Services', p05),
    ('P06', '06 Managed IT & Cloud Services transactions', p06),
    ('P07', '07 Cybersecurity', p07),
    ('P08', '08 Cybersecurity transactions', p08),
    ('P09', '09 Telecom & UCaaS', p09),
    ('P10', '10 Telecom & UCaaS transactions', p10),
    ('P11', '11 Systems Integration', p11),
    ('P12', '12 Systems Integration transactions', p12),
    ('P13', '13 Electronics & Hardware', p13),
    ('P14', '14 Electronics & Hardware transactions', p14),
    ('P15', '15 Government Technology', p15),
    ('P16', '16 Government Technology transactions', p16),
    ('P17', '17 Public-market valuation', p17),
    ('P18', '18 Benchmark International activity', p18),
    ('P19', '19 What buyers reward and discount', p19),
    ('P20', '20 Contact', p20),
]

# Headings on the sources page, each gathering the links from the named report sections.
MERGE = [
    ('Deal market, financing, demand and policy', ['Cover', 'The six focus areas and the deal market', 'Deal market, financing and demand', 'Policy, trade and tax']),
    ('Managed IT & Cloud Services', ['Managed IT & Cloud Services', 'Managed IT & Cloud Services: announced transactions']),
    ('Cybersecurity', ['Cybersecurity', 'Cybersecurity: announced transactions']),
    ('Telecom & UCaaS', ['Telecom & UCaaS', 'Telecom & UCaaS: announced transactions']),
    ('Systems Integration', ['Systems Integration', 'Systems Integration: announced transactions']),
    ('Electronics & Hardware', ['Electronics & Hardware', 'Electronics & Hardware: announced transactions and indicators']),
    ('Government Technology', ['Government Technology', 'Government Technology: announced transactions']),
    ('Valuation, Benchmark International and seller preparation', ['Public-market valuation', 'Benchmark International', 'What buyers reward and discount']),
]

# Link text that reads clearly in a sentence but not on its own in the sources list.
RELABEL = {'release': 'IBBA and M&A Source Market Pulse, press release'}


def source_groups():
    """The links recorded while the pages were built, grouped under the MERGE headings in order of first use."""
    groups = {}
    for sec, label, url in lib.LINKS:
        # Listed-company pages and Benchmark tombstones are linked where they appear and summarized in one closing entry.
        if 'stockanalysis.com/stocks/' in url or (sec == 'Benchmark International' and 'completed-transactions' in url):
            continue
        label = RELABEL.get(label, label)
        items = groups.setdefault(sec, [])
        if url not in [u for _, u in items]:
            items.append((label, url))
    out = []
    for name, secs in MERGE:
        items = []
        for s in secs:
            for l, u in groups.get(s, []):
                if u not in [x for _, x in items]:
                    items.append((l, u))
        out.append((name, items))
    return out
