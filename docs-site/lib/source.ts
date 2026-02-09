import { docs } from 'fumadocs-mdx:collections/server';
import { loader } from 'fumadocs-core/source';
import { icons } from 'lucide-react';
import { createElement } from 'react';

// See https://www.fumadocs.dev/docs/headless/source-api for more info
export const source = loader({
  source: docs.toFumadocsSource(),
  baseUrl: '/docs',
  icon(icon) {
    if (!icon) return;
    if (icon in icons) return createElement(icons[icon as keyof typeof icons]);
  },
});
