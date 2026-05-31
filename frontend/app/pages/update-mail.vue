<script setup>
definePageMeta({
    layout: 'mail-redirect',
    ssr: false
})

const { verifyEmail } = useAuth()
const route = useRoute()

const loading = ref(true)
const error = ref(null)
const message = ref(null)

onMounted(async () => {
    const token = route.query.t

    if (!token) {
        error.value = "Invalid verification link."
        loading.value = false
        return
    }

    try {
        const data = await verifyEmail(token)

        loading.value = false
        message.value = data?.detail || "Email verification successful."

        setTimeout(() => {
            navigateTo("/login")
        }, 2000)
    } catch (err) {
        loading.value = false
        error.value = Array.isArray(err?.data?.detail)
            ? err.data.detail.map(e => e.msg).join(', ')
            : err?.data?.detail || "Verification failed. Please try again."
    }
})
</script>

<template>
    <div class="w-full">
        <div v-if="loading">
            <p class="text-indigo-400 notice">Verifying your email</p>
            <p class="text-gray-500 mt-4">Please wait...</p>
        </div>

        <div v-else-if="error">
            <p class="text-red-500 notice">
                {{ error }}
            </p>

            <NuxtLink to="/login" class="link text-indigo-400 font-semibold mt-4 inline-block">
                Go to Login
            </NuxtLink>
        </div>

        <div v-else>
            <p class="text-indigo-400 notice">
                {{ message }}
            </p>

            <p class="text-gray-500 mt-4">Redirecting to login...</p>
        </div>
    </div>
</template>