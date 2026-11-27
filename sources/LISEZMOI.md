# Composition du Conseil européen par famille politique, 1er mai 2004 – 27 novembre 2026

## Fichiers
- `mandats_conseil_europeen.csv` : un membre votant du Conseil européen par ligne (pays, nom, début, fin, famille), avec la source du codage et des notes. Une fin vide signifie en poste au 27/11/2026. Fin exclusive : la date de fin est le premier jour du successeur.
- `composition_mensuelle.csv` : nombre de membres par famille au 1er de chaque mois (et au 27/11/2026).
- `pays_dates_cles.csv` : format long (date, pays, membre, famille) au 01/05/2004, au 1er janvier de chaque année de 2005 à 2026 et au 27/11/2026. Base du diagramme alluvial.
- `journal_ecarts.csv` : écarts relevés avec ParlGov, l'EPRS et Europe Elects, et décision prise.
- `comparaison_europe_elects.csv` : comparaison mois par mois (2019-2026).
- `parlgov_cabinets_2004_2023.csv` et `ecarts_parlgov.csv` : extraction ParlGov et passations non retrouvées.

## Règle de codage
- Membre : chef d'État ou de gouvernement qui siège (président en France, à Chypre, en Lituanie et en Roumanie ; président en Bulgarie quand l'ancienne Constitution interdisait au Premier ministre intérimaire de siéger).
- Famille (règle de l'EPRS, briefing « European Council: Facts and figures », mars 2024) : groupe du Parlement européen où siègent les eurodéputés du parti national du membre ; à défaut d'eurodéputés, parti européen dont ce parti est membre ; membre sans parti, ou eurodéputés non inscrits : « Indépendants ».
- Familles : Gauche, S&D (PSE), Verts, Renew (ALDE/Renew), Indépendants, PPE, ECR (et prédécesseurs : UEN), PfE.
- Contrôle : effectifs identiques à la série EPRS au 1er janvier pour 2011-2017 et 2023 ; écarts d'un ou deux membres les autres années, documentés dans `journal_ecarts.csv`. Effectifs S&D identiques à l'EPRS (2011-2024, sauf 2020) et à Europe Elects (chaque mois, 2019-2026).

## Sources
- Ossature : frise Wikipedia « Template:European Council Members Timeline » (dates et famille), corrigée.
- ParlGov (Döring & Manow), via GitHub hdigital/parlgov-web : passations de Premiers ministres 2004 – juin 2023.
- EPRS, « Current membership of the European Council », 8 juin 2026 (texte et graphique) ; repères EPRS de 2019 et du 18 juin 2024.
- EPRS, « European Council: Facts and figures », mars 2024, p. 15 : composition au 1er janvier, 2011-2024 (`eprs_serie_2011_2024.csv`, relevé sur le graphique).
- Europe Elects, European Council Tracker (données mensuelles 2019-2026, GitHub Pages).

## Points à vérifier
Papadopoulos (DIKO, 2004-2008), Prodi (2006-2008), Kučinskis (2016-2019), maintien des eurodéputés du Smer au groupe PSE pendant la suspension du parti (2006-2008), Suède (Kristersson en affaires courantes).
