export async function isLoggedIn() {
    try {
        const res = await $fetch('http://127.0.0.1:8000/api/v0/auth/check', {
            method: "GET",
            credentials: 'include',
            cache: 'no-store'
        })

        return true
        // return res.authenticated === true
    } catch {
        return false
    }
}