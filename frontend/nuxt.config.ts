export default defineNuxtConfig({
	compatibilityDate: '2025-07-15',
	devtools: { enabled: false },
	modules: ['@nuxtjs/tailwindcss'],
	css: ['@/assets/css/global.css'],
	devServer: {
		host: '0.0.0.0'
	},
	runtimeConfig: {
		public: {
			apiBase: import.meta.env.BACKEND_URL,
			wsBase: import.meta.env.WS_URL
		}
	},
	routeRules: {
		'/verify-mail': { ssr: false }
	}
})
