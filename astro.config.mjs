// @ts-check
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://terbiye.org',
	vite: {
		resolve: {
			alias: {
				'~': fileURLToPath(new URL('./src', import.meta.url)),
			},
		},
	},
	integrations: [
		starlight({
			title: {
				uy: 'تەربىيە',
				en: 'Terbiye',
			},
			logo: {
				light: './src/assets/logo-light.svg',
				dark: './src/assets/logo-dark.svg',
				alt: 'Terbiye',
			},
			defaultLocale: 'root',
			locales: {
				root: {
					label: 'ئۇيغۇرچە',
					lang: 'uy',
					dir: 'rtl',
				},
				en: {
					label: 'English',
					lang: 'en',
					dir: 'ltr',
				},
			},
			sidebar: [
				{
					label: 'مۇقەددىمە',
					translations: {
						en: 'Introduction',
					},
					items: [
						{ label: 'كىرىش سۆز', slug: 'introduction', translations: { en: 'Foreword' } },
					],
				},
				{
					label: '1. ئۆسمۈرلەر باسقۇچى',
					translations: {
						en: '1. Adolescents Stage',
					},
					items: [{ autogenerate: { directory: '1-osmurler' } }],
				},
				{
					label: '2. ياشلار باسقۇچى',
					translations: {
						en: '2. Youth Stage',
					},
					items: [{ autogenerate: { directory: '2-yashlar' } }],
				},
				{
					label: '3. تەييارلىق باسقۇچى',
					translations: {
						en: '3. Preparatory Stage',
					},
					items: [{ autogenerate: { directory: '3-tayyarliqs' } }],
				},
				{
					label: '4. تەشكىللەش باسقۇچى',
					translations: {
						en: '4. Organizational Stage',
					},
					items: [{ autogenerate: { directory: '4-tashkillash' } }],
				},
				{
					label: '5. دەۋەتچى يېتىلدۈرۈش باسقۇچى',
					translations: {
						en: '5. Dawah Specialist Stage',
					},
					items: [{ autogenerate: { directory: '5-dawatchi' } }],
				},
				{
					label: '6. يېتەكچى ئۇستاز يېتىلدۈرۈش باسقۇچى',
					translations: {
						en: '6. Master Mentor Stage',
					},
					items: [{ autogenerate: { directory: '6-yetakchi' } }],
				},
			],
			customCss: [
				'./src/styles/custom.css',
			],
			components: {
				Header: './src/components/Header.astro',
				Footer: './src/components/Footer.astro',
			},
		}),
	],
});
