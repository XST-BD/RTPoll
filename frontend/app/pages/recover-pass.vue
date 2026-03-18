<script setup>
definePageMeta({
    layout: 'mail-redirect',
    ssr: false
})

const { public: { apiBase } } = useRuntimeConfig()
const route = useRoute()
const { showPopup, showError } = usePopup()

const password = ref('')
const loading = ref(false)
const error = ref(null)

const token = computed(() => route.query.t)

onMounted(() => {
    if (!token.value) {
        error.value = "Invalid verification link.\nPlease request a new password reset email."
    }
})

async function handlePasswordReset() {
    loading.value = true
    error.value = null

    if (!token.value) {
        error.value = "Invalid verification link.\nPlease request a new password reset email."
        loading.value = false
        return
    }

    if (password.value.length < 8) {
        showPopup("Password must contain at least 8 characters.", "error")
        loading.value = false
        return
    }

    try {
        const data = await $fetch(`${apiBase}/auth/email/verify`, {
            method: "POST",
            body: {
                token: token.value,
                new_password: password.value
            }
        })

        loading.value = false
        showPopup(data?.detail || "Password updated successfully.", "success")

        setTimeout(() => {
            navigateTo("/login")
        }, 2000)
    } catch (err) {
        loading.value = false

        if (err?.status === 406) {
            showError(err, "Password must contain at least 8 characters.")
        }
        else {
            error.value = Array.isArray(err?.data?.detail)
                ? err.data.detail.map(e => e.msg).join(', ')
                : err?.data?.detail || "Failed to update password. Please try again."
        }
    }
}
</script>

<template>
    <div class="w-full">
        <PopupMessage />

        <div v-if="error">
            <p class="text-red-500 notice">
                {{ error }}
            </p>

            <NuxtLink to="/login" class="link text-indigo-400 font-semibold mt-4 inline-block">
                Go to Login
            </NuxtLink>
        </div>

        <form v-else @submit.prevent="handlePasswordReset" class="flex flex-col justify-center items-center gap-5">
            <div class="flex flex-col justify-center items-center gap-4">
                <label for="password" class="text-indigo-400 notice">Enter your new password</label>
                <input id="password" v-model="password" type="password" class="ipt w-full" required>
            </div>

            <button type="submit" :disabled="loading" :class="loading ? 'btn-disabled' : 'btn'">
                {{ loading ? 'Updating...' : 'Update' }}
            </button>
        </form>
    </div>
</template>