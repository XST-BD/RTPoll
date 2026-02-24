const refreshVersion = ref(0)

export const useAuth = () => {
    const user = useState('auth:user', () => null)
    const isLoggedIn = computed(() => !!accessToken.value)

    const accessToken = useCookie('access_token')

    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    let refreshPromise = null

    function decodeToken(token) {
        try {
            const base64 = token.split('.')[1]
            const json = atob(base64.replace(/-/g, '+').replace(/_/g, '/'))
            return JSON.parse(json)
        } catch {
            return null
        }
    }

    function setUser(token) {
        const payload = decodeToken(token)
        user.value = payload || null
    }

    function restoreUser() {
        if (accessToken.value && !user.value) {
            setUser(accessToken.value)
        }
    }

    function isTokenExpired() {
        if (!accessToken.value) return true

        const payload = decodeToken(accessToken.value)
        if (!payload?.exp) return true

        const now = Math.floor(Date.now() / 1000)
        return payload.exp - now < 30
    }

    function clearAuth() {
        accessToken.value = null
        user.value = null
    }

    async function login(email, password) {
        const data = await $fetch(`${apiBase}/user/login`, {
            method: 'POST',
            body: { email, password },
            credentials: 'include',
        })

        accessToken.value = data.access_token
        setUser(data.access_token)
        refreshVersion.value++
    }

    async function refresh() {
        if (refreshPromise) return refreshPromise

        refreshPromise = _doRefresh()

        try {
            return await refreshPromise
        } finally {
            refreshPromise = null
        }
    }

    async function _doRefresh() {
        try {
            console.log('[auth] Attempting refresh...')

            const data = await $fetch(`${apiBase}/auth/refresh`, {
                method: 'POST',
                credentials: 'include',
            })

            accessToken.value = data.access_token
            setUser(data.access_token)

            console.log('[auth] Refresh successful')
            return true
        } catch (err) {
            console.error('[auth] Refresh failed:', err?.response?.status, err?.data || err?.message)
            clearAuth()
            return false
        }
    }

    async function logout() {
        await $fetch(`${apiBase}/user/logout`, {
            method: 'POST',
            credentials: 'include',
        })

        clearAuth()
    }

    async function authFetch(url, opts = {}) {
        if (isTokenExpired()) {
            const ok = await refresh()
            if (!ok) throw new Error('Session expired')
        }

        const headers = {
            ...opts.headers,
            Authorization: `Bearer ${accessToken.value}`,
        }

        try {
            return await $fetch(url, { ...opts, headers, credentials: 'include' })
        } catch (err) {
            if (err?.response?.status === 401) {
                const ok = await refresh()
                if (ok) {
                    headers.Authorization = `Bearer ${accessToken.value}`
                    return await $fetch(url, { ...opts, headers, credentials: 'include' })
                }
            }
            throw err
        }
    }

    return {
        user,
        isLoggedIn,
        accessToken,
        refreshVersion,
        login,
        logout,
        refresh,
        restoreUser,
        isTokenExpired,
        authFetch,
    }
}