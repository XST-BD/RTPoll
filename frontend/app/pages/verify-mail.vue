<script setup>
definePageMeta({
    ssr: false
})

const { public: { apiBase } } = useRuntimeConfig()
const route = useRoute()

const loading = ref(true)
const error = ref(null)
const massage = ref(null)

onMounted(async () => {
    const token = route.query.t

    if (!token) {
        error.value = "Invalid verification link"
        loading.value = false
        return
    }

    try {
        const data = await $fetch(`${apiBase}/auth/email/verify`, {
            method: "POST",
            body: {
                type: "registration",
                token: token
            }
        })

        loading.value = false
        error.value = null
        massage.value = data.detail || "Verification successful"

        setTimeout(() => {
            navigateTo("/login")
        }, 2000)
    } catch (err) {
        loading.value = false
        error.value = err?.data?.detail || "Verification failed. Please try again."
    }
})
</script>

<template>
    <div class="min-h-screen flex items-center justify-center px-4">
        <div class="max-w-md w-full text-center space-y-4">

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
                    {{ massage }}
                </p>

                <p class="text-gray-500 mt-4">Redirecting to login...</p>
            </div>
        </div>
    </div>
</template>