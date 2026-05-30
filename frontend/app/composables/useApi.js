export const useApi = () => {
	const {
		public: { apiBase },
	} = useRuntimeConfig();

	function api(path, opts = {}) {
		return $fetch(`${apiBase}${path}`, {
			credentials: "include",
			...opts,
		});
	}

	return { api, apiBase };
};
