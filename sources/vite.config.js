import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import { viteSingleFile } from 'vite-plugin-singlefile';
const LANGUE = process.env.VITE_LANGUE || 'fr';
const TITRES = {
  fr: 'Au Conseil européen, la gauche pourrait tomber à son plus bas niveau depuis 2004',
  es: 'En el Consejo Europeo, la izquierda podría caer a su nivel más bajo desde 2004',
  it: 'Al Consiglio europeo la sinistra potrebbe scendere al livello più basso dal 2004'
};
export default defineConfig({
  plugins: [svelte(), viteSingleFile(), {
    name: 'langue',
    transformIndexHtml: (h) => h.replace('<html lang="fr">', `<html lang="${LANGUE}">`).replace(/<title>.*<\/title>/, `<title>${TITRES[LANGUE]}</title>`)
  }],
  build: { outDir: 'dist-' + LANGUE, target: 'es2019', cssCodeSplit: false, assetsInlineLimit: 100000000 }
});
