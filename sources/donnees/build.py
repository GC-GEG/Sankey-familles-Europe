import csv, datetime as dt, collections, unicodedata, re

W = './'
FAM = {'EPP': 'PPE', 'S&D': 'S&D', 'LIB': 'Renew', 'CON': 'ECR', 'PfE': 'PfE',
       'LFT': 'Gauche', 'GRN': 'Verts', 'UNA': 'Indépendants'}
END = '2026-11-27'  # date de l'extraction
START = '2004-05-01'

rows = list(csv.DictReader(open(W + 'wiki_timeline_raw.csv', encoding='utf-8')))
for r in rows:
    r['famille'] = FAM[r['family_wiki']]
    r['source_famille'] = 'Wikipedia (frise Template:European Council Members Timeline)'
    r['note'] = ''

def split(name, country, pieces, note):
    """Remplace la ligne (country,name) contenant pieces[0][0] par plusieurs segments."""
    global rows
    out = []
    for r in rows:
        if r['country'] == country and r['name'] == name and r['start'] <= pieces[0][0] < (r['end'] or '9999'):
            for (s, e, f) in pieces:
                n = dict(r); n['start'], n['end'], n['famille'] = s, e, f
                n['source_famille'] = 'correction'; n['note'] = note
                out.append(n)
        else:
            out.append(r)
    rows = out

def setfam(country, name, start, fam, note):
    for r in rows:
        if r['country'] == country and r['name'] == name and r['start'] == start:
            r['famille'] = fam; r['source_famille'] = 'correction'; r['note'] = note

def addnote(country, name, note):
    for r in rows:
        if r['country'] == country and r['name'] == name:
            r['note'] = (r['note'] + ' ; ' if r['note'] else '') + note

# REGLE (EPRS, briefing « European Council: Facts and figures », mars 2024) : famille = groupe du Parlement
# européen où siègent les eurodéputés du parti national ; à défaut d'eurodéputés, parti européen dont il est membre ;
# membre sans parti, ou eurodéputés non inscrits = « Indépendants ».
R = "Règle EPRS (groupe PE du parti national) : "
# Orbán : Fidesz quitte le groupe PPE le 03/03/2021 ; groupe Patriotes constitué le 08/07/2024
split('Viktor Orbán', 'HU', [('2010-05-29', '2021-03-03', 'PPE'), ('2021-03-03', '2024-07-08', 'Indépendants'),
      ('2024-07-08', '2026-05-09', 'PfE')],
      R + "Fidesz quitte le groupe PPE le 03/03/2021 (non-inscrits), rejoint les Patriotes à leur constitution le 08/07/2024")
# Présidents sans parti (la Constitution roumaine interdit au président d'être membre d'un parti)
setfam('RO', 'Traian Băsescu', '2007-01-01', 'Indépendants', R + "président sans parti (ex-PD-L) ; l'EPRS le range dans « autres »")
setfam('RO', 'Klaus Iohannis', '2014-12-21', 'Indépendants', R + "président sans parti (ex-PNL) ; l'EPRS le range dans « autres »")
setfam('CY', 'Nikos Christodoulides', '2023-02-28', 'Indépendants', R + "élu sans parti (ex-DISY) ; compté indépendant par l'EPRS en 2024 et par Europe Elects, mais coloré PPE sur le graphique EPRS de juin 2026")
setfam('LV', 'Andris Kulbergs', '2026-05-28', 'Indépendants', R + "sans parti (élu sur la Liste unie), comme l'EPRS ; Europe Elects : ECR")
# Partis sans eurodéputés au moment du mandat
split('Emmanuel Macron', 'FR', [('2017-05-14', '2019-07-02', 'Indépendants'), ('2019-07-02', '', 'Renew')],
      R + "LREM n'a pas d'eurodéputés avant le 02/07/2019 (groupe Renew) ; l'EPRS le range dans « autres » en 2018")
setfam('SI', 'Miro Cerar', '2014-09-18', 'Renew', R + "SMC sans eurodéputés mais membre de l'ALDE : Renew (EPRS 2015-2017 ; « autres » en 2018)")
setfam('SI', 'Marjan Šarec', '2018-09-13', 'Renew', R + "LMŠ sans eurodéputés avant juillet 2019 mais rattaché à l'ALDE : Renew (comme l'EPRS en 2019)")
setfam('SI', 'Alenka Bratušek', '2013-03-20', 'Renew', R + "Slovénie positive sans eurodéputés mais membre de l'ALDE : Renew (comme l'EPRS)")
setfam('LV', 'Māris Kučinskis', '2016-02-11', 'Renew', R + "Parti de Liepāja, membre de l'alliance ZZS, dont l'unique eurodéputée siège au groupe ALDE de 2015 à 2019 ; comme Europe Elects et l'EPRS en 2017 (« autres » en 2018) ; Wikipedia : PPE")
setfam('BG', 'Kiril Petkov', '2021-12-13', 'Renew', R + "PP sans eurodéputés avant 2024, rattaché à la famille libérale (Europe Elects : RE)")
setfam('BG', 'Nikolai Denkov', '2023-06-06', 'Renew', R + "PP sans eurodéputés avant 2024, rattaché à la famille libérale (Europe Elects et EPRS 2024)")
addnote('LV', 'Indulis Emsis', "Parti vert letton (membre du Parti vert européen) : Verts")
addnote('EE', 'Juhan Parts', "Res Publica, membre du parti PPE, sans eurodéputés : PPE")
# Groupe PE différent du codage Wikipedia
split('Brian Cowen', 'IE', [('2008-05-07', '2009-07-14', 'ECR'), ('2009-07-14', '2011-03-09', 'Renew')],
      R + "eurodéputés Fianna Fáil au groupe UEN (famille ECR) jusqu'à la fin de la législature, puis ALDE")
setfam('CZ', 'Mirek Topolánek', '2006-09-04', 'PPE', R + "eurodéputés ODS au groupe PPE-DE jusqu'en 2009")
setfam('CY', 'Tassos Papadopoulos', '2004-05-01', 'Renew', R + "unique eurodéputé DIKO (Matsakis) au groupe ELDR puis ALDE du 01/05/2004 au 13/07/2009 ; le Parlement européen l'enregistre comme DIKO jusqu'en 2009 et le parti n'a pas prononcé son exclusion en 2005 ; DIKO non rattaché à un parti européen ; Wikipedia : S&D")
addnote('SK', 'Robert Fico', "Smer suspendu du PSE du 12/10/2006 au 14/02/2008 ; ses eurodéputés restent au groupe socialiste (J. M. Wiersma, The Slovak Spectator, oct. 2006) : S&D")
setfam('IT', 'Romano Prodi', '2006-05-17', 'Renew', R + "sans parti, rattaché à titre individuel au Parti démocrate européen (eurodéputés au groupe ALDE) pendant tout le mandat, y compris après la fondation du PD le 14/10/2007, selon les tableaux annuels de Wikipedia ; ParlGov code le parti du chef du gouvernement comme la coalition « Centre-gauche » (L'Unione) ; Wikipedia frise : S&D")
# 4b. Belka : Premier ministre dès le 2 mai 2004 (démission de Miller), pas le 5 août (ParlGov)
for r in rows:
    if r['country'] == 'PL' and r['name'] == 'Leszek Miller': r['end'] = '2004-05-02'; r['note'] = 'Fin corrigée d\'après ParlGov (Wikipedia : 05/08/2004)'
    if r['country'] == 'PL' and r['name'] == 'Marek Belka': r['start'] = '2004-05-02'; r['note'] = 'Début corrigé d\'après ParlGov (Wikipedia : 05/08/2004)'
# 5. Intérims autrichiens absents de la frise
for c, n, s, e, note in [('AT', 'Reinhold Mitterlehner', '2016-05-09', '2016-05-17', 'Chancelier par intérim (ÖVP), absent de la frise'),
                         ('AT', 'Hartwig Löger', '2019-05-28', '2019-06-03', 'Chancelier par intérim (ÖVP), absent de la frise')]:
    rows.append(dict(country=c, family_wiki='EPP', start=s, end=e, name=n, famille='PPE', source_famille='ajout', note=note))
# notes de vigilance (sans changement de codage)
for r in rows:
    if r['country']=='SK' and r['name']=='Robert Fico' and r['start']=='2023-10-25':
        r['note']="Eurodéputés du Smer suspendus du groupe S&D le 12/10/2023 puis non-inscrits ; compté indépendant (comme l'EPRS)"

# combler les trous d'un jour (passation de pouvoir)
rows.sort(key=lambda r: (r['country'], r['start']))
for a, b in zip(rows, rows[1:]):
    if a['country'] == b['country'] and a['end'] and a['end'] < b['start'] and \
       (dt.date.fromisoformat(b['start']) - dt.date.fromisoformat(a['end'])).days <= 2:
        a['end'] = b['start']
# bornes
for r in rows:
    if r['end'] == '':
        r['end_ouvert'] = 'oui'; r['end'] = ''
    else:
        r['end_ouvert'] = ''
rows.sort(key=lambda r: (r['country'], r['start']))

cols = ['country', 'name', 'start', 'end', 'famille', 'family_wiki', 'source_famille', 'note']
with open(W + 'mandats_conseil_europeen.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

# --- instantanés -------------------------------------------------------
def members_at(d):
    out = {}
    for r in rows:
        if r['start'] <= d and (r['end'] == '' or d < r['end']):
            out[r['country']] = r
    return out

def counts(d):
    m = members_at(d)
    return collections.Counter(r['famille'] for r in m.values()), m

# contrôle de couverture : chaque jour, chaque État membre doit avoir exactement un membre
acc = {'AT':'1995','BE':'1958','BG':'2007-01-01','HR':'2013-07-01','CY':'2004-05-01','CZ':'2004-05-01','DK':'1973',
       'EE':'2004-05-01','FI':'1995','FR':'1958','DE':'1958','GR':'1981','HU':'2004-05-01','IE':'1973','IT':'1958',
       'LV':'2004-05-01','LT':'2004-05-01','LU':'1958','MT':'2004-05-01','NL':'1958','PL':'2004-05-01','PT':'1986',
       'RO':'2007-01-01','SK':'2004-05-01','SI':'2004-05-01','ES':'1986','SE':'1995','GB':'1973'}
gaps = []
d = dt.date(2004, 5, 1)
while d <= dt.date(2026, 11, 27):
    ds = d.isoformat()
    m = members_at(ds)
    for c, a in acc.items():
        member = a <= ds and not (c == 'GB' and ds >= '2020-01-31')
        if member and c not in m: gaps.append((c, ds))
        overl = [r for r in rows if r['country'] == c and r['start'] <= ds and (r['end'] == '' or ds < r['end'])]
        if len(overl) > 1: gaps.append((c, ds, 'overlap', [o['name'] for o in overl]))
    d += dt.timedelta(days=1)
print('trous/chevauchements :', len(gaps))
for g in gaps[:40]: print(g)

# --- sorties pour graphiques -------------------------------------------
ORDER = ['Gauche', 'S&D', 'Verts', 'Renew', 'Indépendants', 'PPE', 'ECR', 'PfE']
# 1. composition au 1er de chaque mois
out = []
y, mth = 2004, 5
while (y, mth) <= (2026, 11):
    ds = f'{y}-{mth:02d}-01'
    c, m = counts(ds)
    out.append({'date': ds, **{k.lower(): c.get(k, 0) for k in ORDER}, 'total': len(m)})
    mth += 1
    if mth == 13: y, mth = y + 1, 1
c, m = counts(END)
out.append({'date': END, **{k.lower(): c.get(k, 0) for k in ORDER}, 'total': len(m)})
with open(W + 'composition_mensuelle.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)

# 2. pays x dates clés (pour le Sankey / diagramme alluvial)
keys = ['2004-05-01'] + [f'{a}-01-01' for a in range(2005, 2027)] + [END]
names = {'AT':'Autriche','BE':'Belgique','BG':'Bulgarie','HR':'Croatie','CY':'Chypre','CZ':'Tchéquie','DK':'Danemark',
         'EE':'Estonie','FI':'Finlande','FR':'France','DE':'Allemagne','GR':'Grèce','HU':'Hongrie','IE':'Irlande',
         'IT':'Italie','LV':'Lettonie','LT':'Lituanie','LU':'Luxembourg','MT':'Malte','NL':'Pays-Bas','PL':'Pologne',
         'PT':'Portugal','RO':'Roumanie','SK':'Slovaquie','SI':'Slovénie','ES':'Espagne','SE':'Suède','GB':'Royaume-Uni'}
long = []
for k in keys:
    m = members_at(k)
    for cc, r in sorted(m.items()):
        long.append({'date': k, 'code': cc, 'pays': names[cc], 'membre': r['name'], 'famille': r['famille']})
with open(W + 'pays_dates_cles.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(long[0])); w.writeheader(); w.writerows(long)
print('mensuel', len(out), '| pays x dates', len(long))
