import csv, unicodedata, re, datetime as dt
W = './'
iso3 = {'AUT':'AT','BEL':'BE','BGR':'BG','HRV':'HR','CYP':'CY','CZE':'CZ','DNK':'DK','EST':'EE','FIN':'FI','FRA':'FR',
        'DEU':'DE','GRC':'GR','HUN':'HU','IRL':'IE','ITA':'IT','LVA':'LV','LTU':'LT','LUX':'LU','MLT':'MT','NLD':'NL',
        'POL':'PL','PRT':'PT','ROU':'RO','SVK':'SK','SVN':'SI','ESP':'ES','SWE':'SE','GBR':'GB'}
norm = lambda s: re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower())
pg = list(csv.DictReader(open(W + 'parlgov_cabinets_2004_2023.csv', encoding='utf-8')))
mand = list(csv.DictReader(open(W + 'mandats_conseil_europeen.csv', encoding='utf-8')))
# ParlGov : changements de chef de gouvernement (nom du cabinet sans numéro romain)
skip = {'FR', 'CY', 'LT', 'RO'}  # représentés par le président
out = []
for c in sorted(set(iso3.values()) - skip):
    cabs = [r for r in pg if iso3[r['country']] == c]
    pms, prev = [], None
    for r in cabs:
        pmname = re.sub(r'\s+(I|II|III|IV|V|VI|VII|VIII)$', '', r['cabinet'].strip())
        pmname = re.sub(r'\s+\w$', '', pmname) if pmname.split()[-1] in ('F', 'L', 'K', 'G', 'Kos', 'Kyr') else pmname
        pmname = pmname.replace(' Kos', '').replace(' Kyr', '')
        if pmname != prev:
            pms.append((r['start'], pmname, r['pm_party'], r['caretaker']))
            prev = pmname
    ms = [m for m in mand if m['country'] == c and (m['end'] == '' or m['end'] >= '2004-05-01') and m['start'] <= '2023-06-26']
    for s, n, p, ct in pms:
        if s < '2004-05-01' or s > '2023-06-26':
            continue
        key = norm(n.split()[0])
        match = [m for m in ms if key[:5] in norm(m['name'])]
        near = [m for m in match if abs((dt.date.fromisoformat(m['start']) - dt.date.fromisoformat(s)).days) <= 10]
        if near:
            continue
        # continuité (même personne déjà en poste) ?
        cont = [m for m in match if m['start'] <= s and (m['end'] == '' or s < m['end'])]
        out.append(dict(country=c, parlgov_start=s, parlgov_pm=n, parlgov_party=p, caretaker=ct,
                        mandats_match='; '.join(f"{m['name']} {m['start']}→{m['end']}" for m in match) or '—',
                        statut='même personne, mandat déjà ouvert' if cont else 'écart de date ou PM absent'))
with open(W + 'ecarts_parlgov.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
for o in out:
    print(o['country'], o['parlgov_start'], o['parlgov_pm'], o['parlgov_party'], 'ct=' + o['caretaker'], '|', o['statut'], '|', o['mandats_match'])
