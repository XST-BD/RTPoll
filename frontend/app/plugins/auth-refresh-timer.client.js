export default defineNuxtPlugin(() => {
    const { accessToken, refresh, refreshVersion } = useAuth()

    let timer = null

    function scheduleRefresh() {
        if (timer) {
            clearTimeout(timer)
            timer = null
        }

        if (!accessToken.value) return

        try {
            const payload = JSON.parse(atob(accessToken.value.split('.')[1]))
            if (!payload?.exp) return

            const now = Math.floor(Date.now() / 1000)
            const secondsLeft = payload.exp - now

            if (secondsLeft <= 0) return

            const delay = Math.max((secondsLeft - 30) * 1000, 5000)

            console.log(`[auth-timer] Next refresh in ${Math.round(delay / 1000)}s`)

            timer = setTimeout(async () => {
                timer = null
                const ok = await refresh()
                if (ok) scheduleRefresh()
            }, delay)
        } catch {}
    }

    if (accessToken.value) scheduleRefresh()

    watch(refreshVersion, () => {
        console.log('[auth-timer] Token changed, scheduling')
        scheduleRefresh()
    })
})