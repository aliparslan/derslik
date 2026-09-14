import { defineMiddleware } from 'astro:middleware';

/**
 * Starlight maps root `lang: 'uy'` into Astro's i18n `path: 'uy'`.
 * Real Uyghur URLs have no prefix (`/introduction/`), but `/uy/...` can still
 * appear (bookmarks, mistaken links). From there, Starlight's language picker
 * treats `uy` as a normal path segment and builds `/en/uy/...`.
 * Strip those phantom prefixes before routing.
 */
export const onRequest = defineMiddleware((context, next) => {
	const { pathname, search } = context.url;
	const fixed = pathname
		.replace(/^\/en\/uy(?=\/|$)/, '/en')
		.replace(/^\/uy(?=\/|$)/, '');
	if (fixed !== pathname) {
		const dest = (fixed === '' ? '/' : fixed) + search;
		return context.redirect(dest, 301);
	}
	return next();
});
