import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  // SUSTITUYE ESTO POR TU ENLACE REAL DE VERCEL
    site: 'https://comparador-laptops.vercel.app', 
    integrations: [sitemap()],
});