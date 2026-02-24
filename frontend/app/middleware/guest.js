export default defineNuxtRouteMiddleware(async () => {
    const { isLoggedIn, restoreUser, refresh, isTokenExpired } = useAuth()

    restoreUser()

    if (!isLoggedIn.value || isTokenExpired()) {
        await refresh()
    }

    if (isLoggedIn.value) {
        return navigateTo('/dashboard', { replace: true })
    }
})