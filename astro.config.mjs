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
						{ label: 'ئومۇمىي بايان', link: '/derslik/', translations: { en: 'Overview' } },
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
				{
					label: '2000 سوئال-جاۋاب',
					translations: {
						en: '2000 Q&A',
					},
					items: [
						{
							label: 'ئومۇمىي بايان',
							link: '/2000/', // 2000/index overview portal
							translations: {
								en: 'Overview',
							},
						},
						{
							label: '00-مۇقەددىمە',
							translations: {
								en: '00-Introduction',
							},
							items: [{ autogenerate: { directory: '2000/00-muqeddimu' } }],
						},
						{
							label: '01-ئېتىقاد بۆلۈمى (1–163-سوئاللار)',
							translations: {
								en: '01-Creed (Q1–163)',
							},
							items: [{ autogenerate: { directory: '2000/01-etiqad' } }],
						},
						{
							label: '02-ئىبادەت بۆلۈمى (164–647-سوئاللار)',
							translations: {
								en: '02-Worship (Q164–647)',
							},
							items: [{ autogenerate: { directory: '2000/02-ibadet' } }],
						},
						{
							label: '03-ئەخلاق بۆلۈمى (648–967-سوئاللار)',
							translations: {
								en: '03-Morals & Ethics (Q648–967)',
							},
							items: [{ autogenerate: { directory: '2000/03-exlaq' } }],
						},
						{
							label: '04-سىيرەت ۋە تۇرمۇش بۆلۈمى (968–1317-سوئاللار)',
							translations: {
								en: '04-Seerah & Life (Q968–1317)',
							},
							items: [{ autogenerate: { directory: '2000/04-sehiret' } }],
						},
						{
							label: '05-ھارام ۋە چەكلەنگەن ئىشلار (1318–1555-سوئاللار)',
							translations: {
								en: '05-Prohibitions (Q1318–1555)',
							},
							items: [{ autogenerate: { directory: '2000/05-haram-cheklengen' } }],
						},
						{
							label: '06-قۇرئان ۋە سۈننەت (1556–1680-سوئاللار)',
							translations: {
								en: '06-Quran & Sunnah (Q1556–1680)',
							},
							items: [{ autogenerate: { directory: '2000/06-quran-sunnet' } }],
						},
						{
							label: '07-ئىسلامىي ئىلىملەر ۋە مەزھەبلەر (1681–1839-سوئاللار)',
							translations: {
								en: '07-Islamic Sciences & Madhhabs (Q1681–1839)',
							},
							items: [{ autogenerate: { directory: '2000/07-islamiy-ilimler' } }],
						},
						{
							label: '08-قۇرئان كەرىمنىڭ مۆجىزىلىرى (1840–1845-سوئاللار)',
							translations: {
								en: '08-Miracles of the Quran (Q1840–1845)',
							},
							items: [{ autogenerate: { directory: '2000/08-quran-mojiziliri' } }],
						},
						{
							label: '09-مۇقەددەس جايلار ۋە بىلىم يۇرتلىرى (1846–1894-سوئاللار)',
							translations: {
								en: '09-Sacred Places & Institutions (Q1846–1894)',
							},
							items: [{ autogenerate: { directory: '2000/09-muqeddes-jaylar' } }],
						},
						{
							label: '10-ئاتېئىزم ۋە ئاللاھنىڭ بارلىقى (1895–1938-سوئاللار)',
							translations: {
								en: '10-Atheism & Existence of Allah (Q1895–1938)',
							},
							items: [{ autogenerate: { directory: '2000/10-ateizm-allahning-barliqi' } }],
						},
						{
							label: '11-شەك-شۈبھىلەرگە رەددىيە (1939–1958-سوئاللار)',
							translations: {
								en: '11-Refuting Doubts (Q1939–1958)',
							},
							items: [{ autogenerate: { directory: '2000/11-shek-shubhiler' } }],
						},
						{
							label: '12-ئىسلام دۆلىتى ۋە خەلىپىلىكلەر (1959–2000-سوئاللار)',
							translations: {
								en: '12-Islamic State & Caliphates (Q1959–2000)',
							},
							items: [{ autogenerate: { directory: '2000/12-islam-dowliti' } }],
						},
					],
				},
				{
					label: 'قىرىق ھەدىس',
					translations: {
						en: 'Forty Hadith',
					},
					items: [
						{
							label: 'ئومۇمىي بايان',
							link: '/40hedis/',
							translations: {
								en: 'Overview',
							},
						},
						{
							label: '00-مۇقەددىمە',
							translations: {
								en: '00-Introduction',
							},
							items: [{ autogenerate: { directory: '40hedis/00-muqeddimu' } }],
						},
						{
							label: '1–10-ھەدىسلەر: ئىسلام ۋە ئىمان ئاساسلىرى',
							slug: '40hedis/01-hedis-01-10',
							translations: {
								en: 'Hadiths 1–10',
							},
						},
						{
							label: '11–20-ھەدىسلەر: تەقۋالىق، پاكلىق ۋە ئەخلاق',
							slug: '40hedis/02-hedis-11-20',
							translations: {
								en: 'Hadiths 11–20',
							},
						},
						{
							label: '21–30-ھەدىسلەر: ئىستىقامەت، ياخشىلىق ۋە ئىبادەت',
							slug: '40hedis/03-hedis-21-30',
							translations: {
								en: 'Hadiths 21–30',
							},
						},
						{
							label: '31–42-ھەدىسلەر: زۇھد، مەرھەمەت ۋە ئاللاھنىڭ كەڭ مەغپىرىتى',
							slug: '40hedis/04-hedis-31-42',
							translations: {
								en: 'Hadiths 31–42',
							},
						},
					],
				},
				{
					label: 'ھىسنۇل مۇسلىم (دۇئا ۋە زىكىرلەر)',
					translations: {
						en: 'Hisnul Muslim (Dua)',
					},
					items: [
						{
							label: 'ئومۇمىي بايان',
							link: '/dua/',
							translations: {
								en: 'Overview',
							},
						},
						{
							label: '00-مۇقەددىمە',
							translations: {
								en: '00-Introduction',
							},
							items: [{ autogenerate: { directory: 'dua/00-muqeddimu' } }],
						},
						{
							label: '1. كۈندىلىك تۇرمۇش ۋە ناماز زىكىرلىرى',
							slug: 'dua/01-kundilik-namaz',
							translations: {
								en: 'Daily & Prayer Azkar',
							},
						},
						{
							label: '2. ئەتىگەن-ئاخشام، ئۇيقۇ ۋە ۋىتىر دۇئالىرى',
							slug: 'dua/02-etigen-axsham-uyqu',
							translations: {
								en: 'Morning, Evening & Sleep Duas',
							},
						},
						{
							label: '3. مۇسىبەت، كېسەللىك ۋە جىنازا دۇئالىرى',
							slug: 'dua/03-musibet-kesel-jinaza',
							translations: {
								en: 'Hardship, Illness & Funeral Duas',
							},
						},
						{
							label: '4. تەبىئەت، تائام، سورۇن ۋە سەپەر دۇئالىرى',
							slug: 'dua/04-tebiet-taam-seper',
							translations: {
								en: 'Nature, Meals & Travel Duas',
							},
						},
						{
							label: '5. ھەج-ئۆمرە، تەۋبە ۋە ئەدەپ-ئەخلاق',
							slug: 'dua/05-hej-istiqpar-exlaq',
							translations: {
								en: 'Hajj, Repentance & Character',
							},
						},
					],
				},
			],
			customCss: [
				'./src/styles/custom.css',
			],
			components: {
				Header: './src/components/Header.astro',
				Footer: './src/components/Footer.astro',
				Sidebar: './src/components/Sidebar.astro',
				SiteTitle: './src/components/SiteTitle.astro',
				Head: './src/components/Head.astro',
				LanguageSelect: './src/components/LanguageSelect.astro',
				Pagination: './src/components/Pagination.astro',
			},
		}),
	],
});
