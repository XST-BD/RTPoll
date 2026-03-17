<script setup>
definePageMeta({
    ssr: false
})

const { public: { apiBase } } = useRuntimeConfig()
const route = useRoute()
const { showPopup, showError } = usePopup()

const password = ref('')
const loading = ref(false)
const error = ref(null)

onMounted(() => {
    const token = route.query.t

    if (!token) {
        error.value = "Invalid verification link.\nPlease request a new password reset email."
    }
})

async function handlePasswordReset() {
    loading.value = true

    try {
        const data = await $fetch(`${apiBase}/auth/email/verify`, {
            method: "POST",
            body: {
                token: token,
                new_password: password.value
            }
        })

        error.value = null
        showPopup(data?.detail || "Password updated successfully.", "success")

        setTimeout(() => {
            navigateTo("/login")
        }, 2000)

    } catch (err) {
        error.value = null
        showError(err, "Failed to update password. Please try again.")
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="min-h-screen flex flex-col items-center justify-center px-4">
        <div class="flex-1 max-w-md w-full text-center flex items-center justify-center">
            <div v-if="error">
                <p class="text-red-500 notice">
                    {{ error }}
                </p>

                <NuxtLink to="/login" class="link text-indigo-400 font-semibold mt-4 inline-block">
                    Go to Login
                </NuxtLink>
            </div>

            <div v-else class="flex flex-col justify-center items-center gap-5">
                <div class="flex flex-col justify-center items-center gap-4">
                    <label for="password" class="text-indigo-400 notice">Enter your new password</label>
                    <input id="password" v-model="password" type="password" class="ipt w-full" required>
                </div>

                <button type="submit" @click="handlePasswordReset" :disabled="loading" class="btn">
                    {{ loading ? 'Updating...' : 'Update' }}
                </button>
            </div>
        </div>

        <PoweredByFooter />
    </div>
</template>