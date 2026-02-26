export default defineNuxtRouteMiddleware(async () => {
    const { isLoggedIn, refresh } = useAuth()

    if (!isLoggedIn.value) {
        await refresh()
    }

    if (isLoggedIn.value) {
        return navigateTo('/dashboard', { replace: true })
    }
})