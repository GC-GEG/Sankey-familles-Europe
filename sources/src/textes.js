// Textes du graphique en trois langues. La langue est choisie à la compilation (VITE_LANGUE = fr, es ou it).
export const LANGUES = {
  fr: {
    html: 'fr',
    titre: 'Au Conseil européen, la gauche pourrait tomber à son plus bas niveau depuis 2004',
    chapo: 'Membres du Conseil européen par famille politique au 1er janvier de chaque année (au 1er mai pour 2004, date de l’élargissement), au 27 novembre 2026 et en cas de défaite de Pedro Sánchez aux législatives espagnoles du 29 novembre',
    blocs: { gauche: 'Gauche', centre: 'Centre', ind: 'Indépendants', droite: 'Droite', nat: 'ECR et Patriotes' },
    courts: { gauche: 'Gauche', centre: 'Centre', ind: 'Indép.', droite: 'Droite', nat: 'ECR, PfE' },
    cle: { gauche: 'Gauche (S&D, Verts, Gauche)', centre: 'Centre (Renew)', ind: 'Indépendants', droite: 'Droite (PPE)', nat: 'ECR et Patriotes' },
    auj: 'Aujourd’hui', scen: 'Si Sánchez perd',
    an: (a) => `1er janvier ${a}`, mai: '1er mai 2004', aujLong: '27 novembre 2026', scenLong: 'Si Sánchez perd le 29 novembre',
    survol: 'Survolez le graphique pour lire une année',
    source: 'Sources : EPRS, ParlGov, Europe Elects, Groupe d’études géopolitiques · Graphique : Le Grand Continent',
    desc: 'Graphique en rubans : chaque année, les familles politiques du Conseil européen sont classées de la plus nombreuse à la moins nombreuse. La gauche, première en 2016 avec dix membres, n’en compte plus que trois et tomberait à deux en cas de défaite de Pedro Sánchez.'
  },
  es: {
    html: 'es',
    titre: 'En el Consejo Europeo, la izquierda podría caer a su nivel más bajo desde 2004',
    chapo: 'Miembros del Consejo Europeo por familia política a 1 de enero de cada año (a 1 de mayo en 2004, fecha de la ampliación), a 27 de noviembre de 2026 y en caso de derrota de Pedro Sánchez en las elecciones generales españolas del 29 de noviembre',
    blocs: { gauche: 'Izquierda', centre: 'Centro', ind: 'Independientes', droite: 'Derecha', nat: 'ECR y Patriotas' },
    courts: { gauche: 'Izquierda', centre: 'Centro', ind: 'Indep.', droite: 'Derecha', nat: 'ECR, PfE' },
    cle: { gauche: 'Izquierda (S&D, Verdes, Izquierda)', centre: 'Centro (Renew)', ind: 'Independientes', droite: 'Derecha (PPE)', nat: 'ECR y Patriotas' },
    auj: 'Hoy', scen: 'Si Sánchez pierde',
    an: (a) => `1 de enero de ${a}`, mai: '1 de mayo de 2004', aujLong: '27 de noviembre de 2026', scenLong: 'Si Sánchez pierde el 29 de noviembre',
    survol: 'Pase el cursor por el gráfico para leer un año',
    source: 'Fuentes: EPRS, ParlGov, Europe Elects, Grupo de Estudios Geopolíticos · Gráfico: El Grand Continent',
    desc: 'Gráfico de cintas: cada año, las familias políticas del Consejo Europeo se ordenan de la más numerosa a la menos numerosa. La izquierda, primera en 2016 con diez miembros, solo cuenta ya con tres y bajaría a dos en caso de derrota de Pedro Sánchez.'
  },
  it: {
    html: 'it',
    titre: 'Al Consiglio europeo la sinistra potrebbe scendere al livello più basso dal 2004',
    chapo: 'Membri del Consiglio europeo per famiglia politica al 1º gennaio di ogni anno (al 1º maggio per il 2004, data dell’allargamento), al 27 novembre 2026 e in caso di sconfitta di Pedro Sánchez alle elezioni politiche spagnole del 29 novembre',
    blocs: { gauche: 'Sinistra', centre: 'Centro', ind: 'Indipendenti', droite: 'Destra', nat: 'ECR e Patrioti' },
    courts: { gauche: 'Sinistra', centre: 'Centro', ind: 'Indip.', droite: 'Destra', nat: 'ECR, PfE' },
    cle: { gauche: 'Sinistra (S&D, Verdi, Sinistra)', centre: 'Centro (Renew)', ind: 'Indipendenti', droite: 'Destra (PPE)', nat: 'ECR e Patrioti' },
    auj: 'Oggi', scen: 'Se Sánchez perde',
    an: (a) => `1º gennaio ${a}`, mai: '1º maggio 2004', aujLong: '27 novembre 2026', scenLong: 'Se Sánchez perde il 29 novembre',
    survol: 'Passa il cursore sul grafico per leggere un anno',
    source: 'Fonti: EPRS, ParlGov, Europe Elects, Gruppo di studi geopolitici · Grafico: Il Grand Continent',
    desc: 'Grafico a nastri: ogni anno le famiglie politiche del Consiglio europeo sono ordinate dalla più numerosa alla meno numerosa. La sinistra, prima nel 2016 con dieci membri, ne conta ormai solo tre e scenderebbe a due in caso di sconfitta di Pedro Sánchez.'
  }
};
export const L = LANGUES[import.meta.env.VITE_LANGUE || 'fr'];
