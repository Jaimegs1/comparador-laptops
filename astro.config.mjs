import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // 👇 ESTA LÍNEA ES LA QUE TE FALTA Y ES OBLIGATORIA
  site: 'https://comparador-laptops.vercel.app', 

  integrations: [sitemap()]
});