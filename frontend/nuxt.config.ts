export default defineNuxtConfig({
	compatibilityDate: '2025-07-15',
	devtools: { enabled: false },
	modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
	css: ['@/assets/css/global.css'],
	devServer: {
		host: '0.0.0.0'
	},
	runtimeConfig: {
		public: {
			apiBase: import.meta.env.API_URL,
			wsBase: import.meta.env.WS_URL
		}
	},
	routeRules: {
		'/verify-mail': { ssr: false }
	},
	vite: {
		optimizeDeps: {
			include: ['vue3-apexcharts', 'apexcharts']
		}
	},
	nitro: {
		preset: 'cloudflare-pages'
	},
})
