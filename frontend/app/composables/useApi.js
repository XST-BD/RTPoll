/**
 * Description placeholder
 *
 * @returns {{ api: (path: any, opts?: {}) => any; apiBase: any; }} 
 */
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
