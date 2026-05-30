/**
 * Description placeholder
 *
 * @returns {{ isLoggedIn: any; accessToken: any; login: (email: any, password: any) => any; logout: () => any; refresh: () => unknown; authFetch: (url: any, opts?: {}) => unknown; }} 
 */
export const useAuth = () => {
	const isLoggedIn = computed(() => !!accessToken.value);

	// Access token stored in-memory (useState) to prevent XSS cookie extraction
	const accessToken = useState("auth_access_token", () => null);

	const { api } = useApi();

	function getTokenExpiresIn(token) {
		try {
			const base64 = token.split(".")[1];
			const json = atob(base64.replace(/-/g, "+").replace(/_/g, "/"));
			const payload = JSON.parse(json);

			if (!payload?.exp) return 0;

			return payload.exp - Math.floor(Date.now() / 1000);
		} catch {
			return 0;
		}
	}

	// Store timer ID in Nuxt useState to avoid leaks across multiple composable references
	const timerState = useState("auth_refresh_timer", () => null);

	function scheduleRefresh() {
		if (import.meta.server) return;

		stopTimer();

		if (!accessToken.value) return;

		const expiresIn = getTokenExpiresIn(accessToken.value);
		if (expiresIn <= 0) return;

		// Set a max delay cap to prevent tampered token infinite timeouts
		const delay = Math.max((expiresIn - 30) * 1000, 5000);
		const MAX_DELAY = 15 * 60 * 1000; // 15 minutes max
		const safeDelay = Math.min(delay, MAX_DELAY);

		timerState.value = setTimeout(async () => {
			const ok = await refresh();
			if (ok) scheduleRefresh();
		}, safeDelay);
	}

	function stopTimer() {
		if (timerState.value) {
			clearTimeout(timerState.value);
			timerState.value = null;
		}
	}

	function clearAuth() {
		stopTimer();
		accessToken.value = null;
	}

	async function login(email, password) {
		const data = await api("/auth/login", {
			method: "POST",
			body: { email, password },
		});

		accessToken.value = data.access_token;
		scheduleRefresh();
	}

	// Prevent concurrent refresh requests using a shared mutex promise
	const refreshPromise = useState("auth_refresh_promise", () => null);

	async function refresh() {
		if (refreshPromise.value) return refreshPromise.value;

		const promise = (async () => {
			try {
				const data = await api("/auth/refresh", {
					method: "POST",
				});

				accessToken.value = data.access_token;
				scheduleRefresh();

				return true;
			} catch {
				clearAuth();
				return false;
			} finally {
				refreshPromise.value = null;
			}
		})();

		refreshPromise.value = promise;
		return promise;
	}

	async function logout() {
		try {
			await api("/auth/logout", {
				method: "POST",
			});
		} finally {
			clearAuth();
		}
	}

	async function authFetch(url, opts = {}) {
		try {
			return await $fetch(url, {
				...opts,
				headers: {
					...opts.headers,
					Authorization: `Bearer ${accessToken.value}`,
				},
				credentials: "include",
			});
		} catch (err) {
			if (err?.response?.status === 401) {
				const ok = await refresh();

				if (ok) {
					return await $fetch(url, {
						...opts,
						headers: {
							...opts.headers,
							Authorization: `Bearer ${accessToken.value}`,
						},
						credentials: "include",
					});
				}
			}

			throw err;
		}
	}

	return {
		isLoggedIn,
		accessToken,
		login,
		logout,
		refresh,
		authFetch,
	};
};
