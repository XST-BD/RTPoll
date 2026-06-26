export default defineNuxtRouteMiddleware(async (to) => {
    if (import.meta.server) return

    const { isLoggedIn, refresh } = useAuth()

    if (!isLoggedIn.value) {
        const ok = await refresh()

        if (ok) return

        return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`, { replace: true })
    }
})