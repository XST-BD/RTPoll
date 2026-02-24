export default defineNuxtRouteMiddleware(async () => {
    const { isLoggedIn, restoreUser, refresh, isTokenExpired } = useAuth()

    restoreUser()

    if (!isLoggedIn.value || isTokenExpired()) {
        const ok = await refresh()
        if (!ok) return navigateTo('/login', { replace: true })
    }
})