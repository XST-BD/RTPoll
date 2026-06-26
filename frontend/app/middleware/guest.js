export default defineNuxtRouteMiddleware(() => {
    if (import.meta.server) return

    const { isLoggedIn, refresh } = useAuth()

    if (isLoggedIn.value) {
        return navigateTo('/dashboard', { replace: true })
    }

    refresh().then((ok) => {
        if (ok) {
            navigateTo('/dashboard', { replace: true })
        }
    })
})