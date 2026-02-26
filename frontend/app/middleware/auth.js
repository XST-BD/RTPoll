export default defineNuxtRouteMiddleware(async () => {
    const { isLoggedIn, refresh } = useAuth()

    if (!isLoggedIn.value) {
        const ok = await refresh()
        
        if (ok) return

        return navigateTo('/login', { replace: true })
    }
})