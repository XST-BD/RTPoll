export default defineNuxtPlugin(async () => {
    const { accessToken, restoreUser, refresh, isTokenExpired } = useAuth()

    if (accessToken.value && !isTokenExpired()) {
        restoreUser()
    } else {
        const ok = await refresh()
        if (ok) restoreUser()
    }
})