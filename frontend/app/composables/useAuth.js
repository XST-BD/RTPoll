let channel = null;
const LOCK_KEY = "auth_refresh_lock";
let refreshPromise = null;

export const useAuth = () => {
	const isLoggedIn = computed(() => !!accessToken.value);

	// Access token stored in-memory (useState) to prevent XSS cookie extraction
	const accessToken = useState("auth_access_token", () => null);

	const { api } = useApi();

	const TAB_ID = import.meta.client ? (crypto.randomUUID?.() || String(Math.random())) : "";

	const acquireLock = () => {
		if (import.meta.server) return true;
		const existing = localStorage.getItem(LOCK_KEY);
		const lockTime = Number(localStorage.getItem("auth_refresh_lock_time") || 0);

		if (existing && existing !== TAB_ID) {
			// If lock is older than 10 seconds, treat it as stale
			if (Date.now() - lockTime > 10000) {
				localStorage.setItem(LOCK_KEY, TAB_ID);
				localStorage.setItem("auth_refresh_lock_time", String(Date.now()));
				// Check-after-write to reduce race window
				if (localStorage.getItem(LOCK_KEY) !== TAB_ID) return false;
				return true;
			}
			return false;
		}

		localStorage.setItem(LOCK_KEY, TAB_ID);
		localStorage.setItem("auth_refresh_lock_time", String(Date.now()));
		// Check-after-write to reduce race window
		if (localStorage.getItem(LOCK_KEY) !== TAB_ID) return false;
		return true;
	};

	const releaseLock = () => {
		if (import.meta.server) return;
		const existing = localStorage.getItem(LOCK_KEY);
		if (existing === TAB_ID) {
			localStorage.removeItem(LOCK_KEY);
			localStorage.removeItem("auth_refresh_lock_time");
		}
	};

	if (import.meta.client && !channel) {
		channel = new BroadcastChannel("auth_channel");
		channel.onmessage = (event) => {
			const { type, accessToken: newAccessToken } = event.data;
			if (type === "LOGIN" || type === "REFRESH_SUCCESS") {
				accessToken.value = newAccessToken;
				scheduleRefresh();
				if (refreshPromise && typeof refreshPromise._resolve === "function") {
					refreshPromise._resolve(true);
				}
			} else if (type === "LOGOUT") {
				clearAuth();
				if (refreshPromise && typeof refreshPromise._resolve === "function") {
					refreshPromise._resolve(false);
				}
			}
		};

		// Clean up on HMR to prevent channel leaks during development
		if (import.meta.hot) {
			import.meta.hot.dispose(() => {
				channel?.close();
				channel = null;
			});
		}
	}

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

		if (channel) {
			channel.postMessage({ type: "LOGIN", accessToken: data.access_token });
		}
	}

	async function register(email, password, confirm_password) {
		return await api("/auth/register", {
			method: "POST",
			body: { email, password, confirm_password },
		});
	}

	async function verifyEmail(token, newPassword = null) {
		const body = { token };
		if (newPassword !== null) {
			body.new_password = newPassword;
		}
		return await api("/auth/email/verify", {
			method: "POST",
			body,
		});
	}

	async function resendVerification(email, type = "login") {
		return await api("/auth/email/resend", {
			method: "POST",
			body: { email, type },
		});
	}

	async function sendPasswordResetEmail(email) {
		return await api("/user", {
			method: "PATCH",
			body: { email },
		});
	}

	async function changePassword(oldPassword, newPassword) {
		return await authFetch("/user", {
			method: "PUT",
			body: {
				old_password: oldPassword,
				new_password: newPassword,
			},
		});
	}

	async function changeEmail(newEmail, password) {
		return await authFetch("/user", {
			method: "POST",
			body: {
				recovery: true,
				new_email: newEmail,
				password,
			},
		});
	}

	async function deleteAccount(password) {
		return await authFetch("/user", {
			method: "DELETE",
			body: { password },
		});
	}

	async function refresh() {
		if (refreshPromise) return refreshPromise;

		const gotLock = acquireLock();

		if (!gotLock) {
			// Another tab is currently refreshing. Wait for its broadcast.
			let resolveFn;
			const promise = new Promise((resolve) => {
				resolveFn = resolve;
				// Fallback timeout of 5 seconds in case the lock owner tab crashes
				setTimeout(() => {
					if (refreshPromise === promise) {
						refreshPromise = null;
						resolve(refresh());
					}
				}, 5000);
			});
			promise._resolve = resolveFn;
			refreshPromise = promise;
			return promise;
		}

		const promise = (async () => {
			try {
				const data = await api("/auth/refresh", {
					method: "POST",
				});

				accessToken.value = data.access_token;
				scheduleRefresh();

				if (channel) {
					channel.postMessage({ type: "REFRESH_SUCCESS", accessToken: data.access_token });
				}

				return true;
			} catch {
				clearAuth();
				if (channel) {
					channel.postMessage({ type: "LOGOUT" });
				}
				return false;
			} finally {
				releaseLock();
				refreshPromise = null;
			}
		})();

		refreshPromise = promise;
		return promise;
	}

	async function logout() {
		try {
			await api("/auth/logout", {
				method: "POST",
			});
		} finally {
			clearAuth();
			if (channel) {
				channel.postMessage({ type: "LOGOUT" });
			}
		}
	}

	async function authFetch(url, opts = {}) {
		const fetcher = url.startsWith('/') ? api : (path, options) => $fetch(path, { credentials: "include", ...options });

		try {
			return await fetcher(url, {
				...opts,
				headers: {
					...opts.headers,
					Authorization: `Bearer ${accessToken.value}`,
				},
			});
		} catch (err) {
			if (err?.response?.status === 401) {
				const ok = await refresh();

				if (ok) {
					return await fetcher(url, {
						...opts,
						headers: {
							...opts.headers,
							Authorization: `Bearer ${accessToken.value}`,
						},
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
		register,
		logout,
		refresh,
		authFetch,
		verifyEmail,
		resendVerification,
		sendPasswordResetEmail,
		changePassword,
		changeEmail,
		deleteAccount,
	};
};
