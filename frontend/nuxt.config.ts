export default defineNuxtConfig({
	compatibilityDate: '2025-07-15',
	devtools: { enabled: false },
	modules: ['@nuxtjs/tailwindcss'],
	css: ['@/assets/css/global.css'],
	runtimeConfig: {
		public: {
			apiBase: import.meta.env.BACKEND_NETWORK_URL 
		}
	}
})
