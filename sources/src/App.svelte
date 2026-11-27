<script>
  import { L } from './textes.js';
  import DATA from './data.json';
  import { area, curveBumpX, curveBasis } from 'd3-shape';

  // Ordre du spectre (sert à départager les égalités) et couleurs des blocs.
  const BLOCS = ['gauche', 'centre', 'ind', 'droite', 'nat'];
  const COUL = { gauche: '#dd203c', centre: '#f2b600', ind: '#b9b9bd', droite: '#3d8fd6', nat: '#1d2f86' };
  // Ordre de dessin : la gauche passe au premier plan aux croisements.
  const DESSIN = ['ind', 'nat', 'centre', 'droite', 'gauche'];
  const N = DATA.length, IAUJ = N - 2, ISC = N - 1;

  let w = 1000;
  let sel = IAUJ;

  $: tel = w < 600;
  $: u = tel ? 9 : 12;                 // hauteur d'un membre (px)
  $: g = 2;                           // écart entre rubans : les flux se détachent
  $: labW = tel ? 70 : 160;            // colonne des étiquettes à droite
  $: y0 = 42;
  $: hmax = 28 * u + 4 * g;
  $: H = y0 + hmax + 6;
  $: plot = Math.max(200, w - labW - 6);
  // 22 points annuels (2004-2025), puis le 27/11/2026 (1,9 an après le 1/1/2025), puis le scénario.
  $: pas = plot / (21 + 1.9 + 2.4);
  $: X = DATA.map((d, i) => 2 + (i <= 21 ? i * pas : i === IAUJ ? (21 + 1.9) * pas : (21 + 1.9 + 2.4) * pas));

  // Positions : à chaque date, le bloc le plus nombreux en haut.
  // En cas d'égalité, chaque bloc garde son rang de l'année précédente (pas de croisement artificiel).
  $: P = (() => {
    const out = []; let prec = BLOCS.slice();
    DATA.forEach((d) => {
      const ord = BLOCS.map((b) => ({ b, n: d[b], r: prec.indexOf(b) })).sort((a, c) => c.n - a.n || a.r - c.r);
      const pleins = ord.filter((a) => a.n);
      const haut = pleins.reduce((t, a) => t + a.n * u, 0) + (pleins.length - 1) * g;
      let y = y0 + (hmax - haut) / 2; const o = {};
      ord.forEach((a) => { o[a.b] = { y, n: a.n }; if (a.n) y += a.n * u + g; });
      prec = ord.map((a) => a.b); out.push(o);
    });
    return out;
  })();

  // Rubans : longues courbes douces sur la période passée (B-spline), S net vers le scénario.
  function ruban(b, X, P, u, i0, i1, courbe) {
    return area().x((d) => X[d]).y0((d) => P[d][b].y).y1((d) => P[d][b].y + P[d][b].n * u)
      .curve(courbe)(DATA.map((_, i) => i).slice(i0, i1 + 1));
  }
  const NB = 9; // largeur des barres de nœud (px)

  $: ANNEES = tel ? [0, 11] : [0, 6, 11, 16];
  const an = (i) => (i === 0 ? 2004 : 2004 + i);
  $: libelle = sel === ISC ? L.scenLong : sel === IAUJ ? L.aujLong : sel === 0 ? L.mai : L.an(an(sel));

  let svg;
  function survol(e) {
    const r = svg.getBoundingClientRect();
    const x = (e.clientX - r.left) * (w / r.width);
    let best = 0, dmin = Infinity;
    X.forEach((xx, i) => { const dd = Math.abs(xx - x); if (dd < dmin) { dmin = dd; best = i; } });
    sel = best;
  }
</script>

<main class="bloc">
  <header>
    <h1>{L.titre}</h1>
    <p class="chapo">{L.chapo}</p>
  </header>

  <ul class="cle" aria-label="Clé de lecture">
    {#each BLOCS as b}
      <li><svg width="14" height="10" aria-hidden="true"><rect width="14" height="10" rx="2" fill={COUL[b]} /></svg>{L.cle[b]}</li>
    {/each}
  </ul>

  <div class="repere" aria-live="polite">
    <span class="jour">{libelle}</span>
    <span class="valeurs">
      {#each BLOCS as b}
        <span class="val"><i style="background:{COUL[b]}"></i>{L.courts[b]} <b>{DATA[sel][b]}</b></span>
      {/each}
    </span>
  </div>

  <div class="scene" bind:clientWidth={w}>
    <svg bind:this={svg} viewBox="0 0 {w} {H}" width={w} height={H} role="img" aria-label={L.desc}
         on:pointermove={survol} on:pointerleave={() => (sel = IAUJ)}>
      <defs>
        <clipPath id="passe"><rect x="-10" y="0" width={X[IAUJ] + 10} height={H} /></clipPath>
        <clipPath id="scenario"><rect x={X[IAUJ]} y="0" width={w} height={H} /></clipPath>
      </defs>
      {#each DESSIN as b}
        <path d={ruban(b, X, P, u, 0, IAUJ, curveBasis)} fill={COUL[b]} fill-opacity="0.5" />
        <path d={ruban(b, X, P, u, IAUJ, ISC, curveBumpX)} fill={COUL[b]} fill-opacity="0.22" />
      {/each}
      {#each [[0, X[0]], [IAUJ, X[IAUJ] - NB], [ISC, X[ISC] - NB]] as [i, x]}
        {#each BLOCS as b}{#if P[i][b].n}
          <rect x={x} y={P[i][b].y} width={NB} height={P[i][b].n * u} fill={COUL[b]} fill-opacity={i === ISC ? 0.55 : 1} />
        {/if}{/each}
      {/each}

      {#if sel !== IAUJ}
        <line x1={X[sel]} x2={X[sel]} y1={y0 - 6} y2={H - 2} class="guide" />
        {#each BLOCS as b}{#if P[sel][b].n}<circle cx={X[sel]} cy={P[sel][b].y + P[sel][b].n * u / 2} r="3" fill="#fff" stroke={COUL[b]} stroke-width="1.5" />{/if}{/each}
      {/if}

      <g class="axe">
        {#each ANNEES as i}
          <text x={X[i]} y="16" text-anchor={i === 0 ? 'start' : 'middle'}>{an(i)}</text>
        {/each}
        <text x={X[IAUJ]} y="16" text-anchor="end" class="fort">{L.auj}</text>
        <text x={X[ISC]} y="16" text-anchor="start" class="scen">
          {#if tel}
            <tspan x={X[ISC] - 4}>{L.scen.split(' ').slice(0, 2).join(' ')}</tspan><tspan x={X[ISC] - 4} dy="13">{L.scen.split(' ').slice(2).join(' ')}</tspan>
          {:else}{L.scen}{/if}
        </text>
      </g>

      <g class="etiquettes">
        {#each BLOCS as b}
          {#if P[ISC][b].n}
            <text x={X[ISC] + 8} y={P[ISC][b].y + (P[ISC][b].n * u) / 2 + 4.5} class:gauche={b === 'gauche'}>
              {(tel ? L.courts[b] : L.blocs[b]) + '\u00a0'}<tspan class="n">{P[ISC][b].n}</tspan>
            </text>
          {/if}
        {/each}
      </g>
    </svg>
  </div>

  <p class="source">{L.source}</p>
</main>

<style>
  .bloc{max-width:1040px;margin:0 auto;padding:6px var(--marge) 10px;display:flex;flex-direction:column;gap:14px}
  header{display:flex;flex-direction:column;gap:6px}
  h1{font-family:var(--titre);font-weight:700;font-size:clamp(21px,3.3vw,28px);line-height:1.16;text-wrap:balance}
  .chapo{font-size:15px;line-height:1.4;color:var(--gris);max-width:70ch}
  .cle{list-style:none;display:flex;flex-wrap:wrap;gap:6px 18px;font-size:12.5px;line-height:1.3;color:#3b3b40}
  .cle li{display:flex;align-items:center;gap:6px;white-space:nowrap}
  .cle svg{flex:none;display:block}
  .repere{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 16px;margin-bottom:-6px;min-height:28px}
  .jour{font-family:var(--titre);font-weight:700;font-size:19px;line-height:1.2}
  .valeurs{display:flex;flex-wrap:wrap;gap:2px 12px;font-size:13px;color:var(--gris);font-variant-numeric:tabular-nums}
  .val{display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
  .val i{width:8px;height:8px;border-radius:2px;display:inline-block}
  .val b{color:var(--encre);font-weight:600}
  .scene{position:relative;line-height:0;touch-action:pan-y}
  .scene svg{display:block;overflow:visible}
  .guide{stroke:#141414;stroke-opacity:.35;stroke-width:1}
  .axe text{font-family:var(--texte);font-size:12.5px;fill:var(--gris);font-variant-numeric:lining-nums}
  .axe text.fort{fill:var(--encre);font-weight:600}
  .axe text.scen{fill:var(--gris);font-style:italic}
  .etiquettes text{font-family:var(--texte);font-size:13px;font-weight:500;fill:#2a2a2d}
  .etiquettes text.gauche{fill:var(--rouge);font-weight:600}
  .etiquettes .n{font-weight:700}
  .source{font-size:12px;line-height:1.45;color:var(--gris);border-top:1px solid var(--filet);padding-top:10px}
  @media (max-width:600px){
    .bloc{gap:12px}
    .chapo{font-size:14px}
    .cle{gap:5px 14px;font-size:12px}
    .jour{font-size:17px}
    .valeurs{font-size:12px;gap:2px 9px}
    .axe text{font-size:11.5px}
    .etiquettes text{font-size:11.5px}
  }
</style>
