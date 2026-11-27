import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
for (const [f,w] of [['FR',1040],['FR',390],['ES',390],['IT',1040],['FR',500],['FR',600],['FR',700],['FR',820],['ES',940],['IT',640],['IT',390],['ES',1040]]) {
  const p = await b.newPage(); await p.setViewport({width:w,height:900,deviceScaleFactor:2});
  await p.goto('file:///home/claude/graph/graphique_conseil_europeen_familles_'+f+'.html'); await new Promise(r=>setTimeout(r,800));
  await p.screenshot({path:`shot_${f}_${w}.png`,fullPage:true});
  const ov = await p.evaluate(()=>{const t=[...document.querySelectorAll('svg text')].map(e=>e.getBoundingClientRect());let n=0;for(let i=0;i<t.length;i++)for(let j=i+1;j<t.length;j++){const a=t[i],c=t[j];if(a.left<c.right&&c.left<a.right&&a.top<c.bottom&&c.top<a.bottom)n++;}const s=document.querySelector('.scene svg').getBoundingClientRect();const out=t.filter(r=>r.right>innerWidth+1||r.left<-1).length;return {chevauchements:n,debordements:out};});
  console.log(f,w,JSON.stringify(ov));
}
await b.close();
