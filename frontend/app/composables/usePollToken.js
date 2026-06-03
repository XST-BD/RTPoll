const pollChannels = new Map();
const pollRefreshPromises = new Map();

export const usePollToken = (type = 'visitor') => {
	const { api } = useApi();
	const { authFetch } = useAuth();

	const cookiePrefix = `${type}_poll`;
	const statePrefix = `${type}PollToken`;

	const tokenCookie = useCookie(`${cookiePrefix}_token`, {
		maxAge: 3 * 24 * 60 * 60,
	});

	const tokenExpiryCookie = useCookie(`${cookiePrefix}_token_expiry`, {
		maxAge: 3 * 24 * 60 * 60,
	});

	const token = useState(`${statePrefix}`, () => tokenCookie.value || null);
	const expiry = useState(
		`${statePrefix}Expiry`,
		() => (tokenExpiryCookie.value ? Number(tokenExpiryCookie.value) : null)
	);

	const LOCK_KEY = `${cookiePrefix}_token_refresh_lock`;
	const CHANNEL_NAME = `${cookiePrefix}_token_channel`;
	const TAB_ID = import.meta.client
		? crypto.randomUUID?.() || String(Math.random())
		: "";

	const TOKEN_ENDPOINT = `/poll/${type}/token`;

	// Store timer ID in useState to prevent duplicate timers across multiple composable calls
	const timerState = useState(`${statePrefix}RefreshTimer`, () => null);

	const acquireLock = () => {
		if (import.meta.server) return true;

		const existing = localStorage.getItem(LOCK_KEY);
		const lockTime = Number(
			localStorage.getItem(LOCK_KEY + "_time") || 0
		);

		if (existing && existing !== TAB_ID) {
			if (Date.now() - lockTime > 10000) {
				localStorage.setItem(LOCK_KEY, TAB_ID);
				localStorage.setItem(
					LOCK_KEY + "_time",
					String(Date.now())
				);
				// Check-after-write to reduce race window
				if (localStorage.getItem(LOCK_KEY) !== TAB_ID)
					return false;
				return true;
			}
			return false;
		}

		localStorage.setItem(LOCK_KEY, TAB_ID);
		localStorage.setItem(LOCK_KEY + "_time", String(Date.now()));
		// Check-after-write to reduce race window
		if (localStorage.getItem(LOCK_KEY) !== TAB_ID) return false;
		return true;
	};

	const releaseLock = () => {
		if (import.meta.server) return;
		const existing = localStorage.getItem(LOCK_KEY);
		if (existing === TAB_ID) {
			localStorage.removeItem(LOCK_KEY);
			localStorage.removeItem(LOCK_KEY + "_time");
		}
	};

	// Set up BroadcastChannel for cross-tab token sync
	if (import.meta.client && !pollChannels.has(type)) {
		const channel = new BroadcastChannel(CHANNEL_NAME);
		channel.onmessage = (event) => {
			const { type: msgType, tokenVal, expiryVal } = event.data;
			if (msgType === "POLL_TOKEN_REFRESHED") {
				token.value = tokenVal;
				tokenCookie.value = tokenVal;
				expiry.value = expiryVal;
				tokenExpiryCookie.value = String(expiryVal);
				scheduleAutoRefresh();
				// Resolve any pending refresh promise from non-lock-holder tabs
				const currentPromise = pollRefreshPromises.get(type);
				if (
					currentPromise &&
					typeof currentPromise._resolve === "function"
				) {
					currentPromise._resolve(true);
				}
			}
		};
		pollChannels.set(type, channel);

		// Clean up on HMR to prevent channel leaks during development
		if (import.meta.hot) {
			import.meta.hot.dispose(() => {
				pollChannels.get(type)?.close();
				pollChannels.delete(type);
			});
		}
	}

	const generateToken = async () => {
		const fetcher = type === 'creator' ? authFetch : api;
		const data = await fetcher(TOKEN_ENDPOINT, {
			method: "POST",
		});

		const tokenVal =
			typeof data === "string" ? data : data?.token || data;

		token.value = tokenVal;
		tokenCookie.value = tokenVal;

		// Prefer server-provided expiry over client-side calculation
		const expiryTime = data?.expires_at
			? new Date(data.expires_at).getTime()
			: data?.expires_in
				? Date.now() + data.expires_in * 1000
				: Date.now() + 3 * 24 * 60 * 60 * 1000;
		expiry.value = expiryTime;
		tokenExpiryCookie.value = String(expiryTime);

		scheduleAutoRefresh();

		return token.value;
	};

	const isExpired = () => {
		if (!token.value || !expiry.value) return true;
		return Date.now() > expiry.value;
	};

	const clearTimer = () => {
		if (timerState.value) {
			clearTimeout(timerState.value);
			timerState.value = null;
		}
	};

	const refreshTokenLocked = async () => {
		// Dedup: if a refresh is already in-flight in this tab, reuse it
		if (pollRefreshPromises.has(type)) return pollRefreshPromises.get(type);

		const gotLock = acquireLock();

		if (!gotLock) {
			// Another tab is refreshing — wait for its broadcast with a fallback timeout
			let resolveFn;
			const promise = new Promise((resolve) => {
				resolveFn = resolve;
				// Fallback: if the lock-holder tab crashes, retry after 5s
				setTimeout(() => {
					if (pollRefreshPromises.get(type) === promise) {
						pollRefreshPromises.delete(type);
						resolve(refreshTokenLocked());
					}
				}, 5000);
			});
			promise._resolve = resolveFn;
			pollRefreshPromises.set(type, promise);
			return promise;
		}

		const promise = (async () => {
			try {
				await generateToken();

				if (import.meta.client) {
					localStorage.setItem(
						`${cookiePrefix}_token_updated`,
						String(Date.now())
					);
				}

				// Broadcast to other tabs
				const channel = pollChannels.get(type);
				if (channel) {
					channel.postMessage({
						type: "POLL_TOKEN_REFRESHED",
						tokenVal: token.value,
						expiryVal: expiry.value,
					});
				}

				return true;
			} catch {
				return false;
			} finally {
				releaseLock();
				pollRefreshPromises.delete(type);
			}
		})();

		pollRefreshPromises.set(type, promise);
		return promise;
	};

	const scheduleAutoRefresh = () => {
		if (import.meta.server) return;
		clearTimer();

		if (!expiry.value) return;

		const refreshTime = expiry.value - Date.now() - 60 * 1000;

		if (refreshTime <= 0) {
			refreshTokenLocked();
			return;
		}

		// Cap delay to prevent issues with extremely long timeouts
		const MAX_DELAY = 24 * 60 * 60 * 1000; // 1 day max
		const safeDelay = Math.min(refreshTime, MAX_DELAY);

		timerState.value = setTimeout(() => {
			refreshTokenLocked();
		}, safeDelay);
	};

	const ensureToken = async () => {
		if (!token.value || isExpired()) {
			await refreshTokenLocked();
			console.log(`${type} poll token refreshTokenLocked:`, token.value);
		} else {
			scheduleAutoRefresh();
			console.log(`${type} poll token scheduleAutoRefresh:`, token.value);
		}

		return token.value;
	};

	const clearToken = () => {
		clearTimer();
		releaseLock();

		token.value = null;
		tokenCookie.value = null;
		tokenExpiryCookie.value = null;
		expiry.value = null;
	};

	if (import.meta.client) {
		// Schedule auto refresh on startup if we already have a valid token
		if (token.value && !isExpired()) {
			scheduleAutoRefresh();
		}

		window.addEventListener("storage", (event) => {
			if (event.key === `${cookiePrefix}_token_updated`) {
				token.value = tokenCookie.value;
				expiry.value = tokenExpiryCookie.value
					? Number(tokenExpiryCookie.value)
					: null;
				scheduleAutoRefresh();
			}

			if (event.key === LOCK_KEY && event.newValue === null) {
				if (!isExpired()) scheduleAutoRefresh();
			}
		});
	}

	return {
		token,
		generateToken,
		ensureToken,
		clearToken,
		isExpired,
	};
};