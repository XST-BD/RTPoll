import { isLoggedIn } from '@/utils/auth'

export default defineNuxtRouteMiddleware(async () => {
    const ok = await isLoggedIn()

    if (!ok) {
        return navigateTo('/login')
    }
})