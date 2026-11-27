import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import { viteSingleFile } from 'vite-plugin-singlefile';
const LANGUE = process.env.VITE_LANGUE || 'fr';
const TITRES = {
  fr: 'Une défaite de Sánchez en Espagne laisserait seulement deux dirigeants de gauche au Conseil européen',
  es: 'Una derrota de Sánchez en España dejaría solo a dos dirigentes de izquierda en el Consejo Europeo',
  it: 'Una sconfitta di Sánchez in Spagna lascerebbe solo due leader di sinistra nel Consiglio europeo'
};
export default defineConfig({
  plugins: [svelte(), viteSingleFile(), {
    name: 'langue',
    transformIndexHtml: (h) => h.replace('<html lang="fr">', `<html lang="${LANGUE}">`).replace(/<title>.*<\/title>/, `<title>${TITRES[LANGUE]}</title>`)
  }],
  build: { outDir: 'dist-' + LANGUE, target: 'es2019', cssCodeSplit: false, assetsInlineLimit: 100000000 }
});
