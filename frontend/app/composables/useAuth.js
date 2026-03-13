export const useAuth = () => {
    const isLoggedIn = computed(() => !!accessToken.value)

    const accessToken = useCookie('access_token')

    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    function getTokenExpiresIn(token) {
        try {
            const base64 = token.split('.')[1]
            const json = atob(base64.replace(/-/g, '+').replace(/_/g, '/'))
            const payload = JSON.parse(json)
            
            if (!payload?.exp) return 0

            return payload.exp - Math.floor(Date.now() / 1000)
        } catch {
            return 0
        }
    }

    let timer

    function scheduleRefresh() {
        if (import.meta.server) return

        stopTimer()

        if (!accessToken.value) return

        const expiresIn = getTokenExpiresIn(accessToken.value)
        if (expiresIn <= 0) return

        const delay = Math.max((expiresIn - 30) * 1000, 5000)

        timer = setTimeout(async () => {
            const ok = await refresh()
            if (ok) scheduleRefresh()
        }, delay)
    }

    function stopTimer() {
        if (timer) {
            clearTimeout(timer)
            timer = null
        }
    }

    function clearAuth() {
        stopTimer()
        accessToken.value = null
    }

    async function login(email, password) {
        const data = await $fetch(`${apiBase}/user/login`, {
            method: 'POST',
            credentials: 'include',
            body: { email, password }
        })

        accessToken.value = data.access_token
        scheduleRefresh()
    }

    async function refresh() {
        try {
            const data = await $fetch(`${apiBase}/auth/refresh`, {
                method: 'POST',
                credentials: 'include'
            })

            accessToken.value = data.access_token
            scheduleRefresh()

            return true
        } catch {
            clearAuth()

            return false
        }
    }

    async function logout() {
        await $fetch(`${apiBase}/user/logout`, {
            method: 'POST',
            credentials: 'include'
        })

        clearAuth()
    }

    async function authFetch(url, opts = {}) {
        try {
            return await $fetch(url, {
                ...opts,
                headers: {
                    ...opts.headers,
                    Authorization: `Bearer ${accessToken.value}`,
                },
                credentials: 'include',
            })
        } catch (err) {
            if (err?.response?.status === 401) {
                const ok = await refresh()

                if (ok) {
                    return await $fetch(url, {
                        ...opts,
                        headers: {
                            ...opts.headers,
                            Authorization: `Bearer ${accessToken.value}`,
                        },
                        credentials: 'include',
                    })
                }
            }

            throw err
        }
    }

    return {
        isLoggedIn,
        accessToken,
        login,
        logout,
        refresh,
        authFetch,
    }
}