export default defineNuxtConfig({
	compatibilityDate: '2025-07-15',

	devtools: {
		enabled: false
	},

	debug: false,

	modules: [
		'@nuxtjs/tailwindcss'
	],

	css: [
		'@/assets/css/global.css'
	],

	devServer: {
		host: '0.0.0.0'
	},

	runtimeConfig: {
		public: {
			apiBase: process.env.API_URL,
			wsBase: process.env.WS_URL
		}
	},

	ssr: true,

	routeRules: {
		'/': { ssr: true },
		'/about': { ssr: true },
		'/login': { ssr: false },
		'/register': { ssr: false },

		'/recover-pass': { ssr: false },
		'/verify-mail': { ssr: false },
		'/update-mail': { ssr: false },
		'/dashboard/**': { ssr: false },
		'/poll/**': { ssr: false },
	},

	vite: {
		optimizeDeps: {
			include: [
				'apexcharts',
				'vue3-apexcharts'
			]
		}
	},

	nitro: {
		preset: 'cloudflare-pages',
		cloudflare: {
            nodeCompat: true
        }
	}
})