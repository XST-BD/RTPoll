<script setup>
definePageMeta({
    middleware: 'guest'
})

useHead({
    title: 'Login'
})

const { login } = useAuth()
const { public: { apiBase } } = useRuntimeConfig()

const email = ref('')
const password = ref('')
const error = ref(null)
const loading = ref(false)
const resend_mail = ref(false)

async function handleLogin() {
    error.value = null
    loading.value = true
    resend_mail.value = false

    try {
        await login(email.value, password.value)
        await navigateTo('/dashboard')
    } catch (err) {
        const data = err?.data

        if (Array.isArray(data?.detail)) {
            error.value = data.detail[0]?.msg ?? 'Validation error'
        }
        else if (typeof data?.detail === 'string') {
            error.value = data.detail

            if (data.detail.includes('User is not verified')) {
                resend_mail.value = true
            }
        }
        else {
            error.value = 'Something went wrong'
        }
    } finally {
        loading.value = false
    }
}

async function resendVerificationEmail() {
    error.value = null
    loading.value = true

    try {
        const res = await $fetch(`${apiBase}/auth/resend_mail`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: { email: email.value }
        })

        alert(res.message)
        email.value = ''
    } catch (err) {
        const data = err?.data

        if (Array.isArray(data?.detail)) {
            error.value = data.detail[0]?.msg ?? 'Validation error'
        }
        else if (typeof data?.detail === 'string') {
            error.value = data.detail
        }
        else {
            error.value = 'Something went wrong'
        }
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <section class="w-full min-h-screen p-5 bg-grid flex flex-col justify-center items-center gap-12">
        <div class="w-full max-w-xl flex flex-col justify-center items-center gap-12 bg-white backdrop-blur-[100px] rounded-xl sm:p-10 p-5 shadow-md border border-green-300">
            <h2 class="text-3xl">Login to Your Account</h2>

            <p v-if="error" class="error-msg">{{ error }}</p>

            <form class="w-full flex flex-col gap-10" @submit.prevent="handleLogin">
                <div class="flex flex-col gap-4">
                    <div class="flex flex-col gap-1">
                        <label for="email">Email</label>
                        <input id="email" v-model="email" required>
                    </div>

                    <div class="flex flex-col gap-1">
                        <label for="password">Password</label>
                        <input id="password" v-model="password" type="password" required>
                    </div>
                </div>

                <button type="submit" :disabled="loading" class="btn">
                    {{ loading ? 'Logging in...' : 'Login' }}
                </button>

                <p v-if="resend_mail" class="text-md text-center">
                    Verification email not received?
                    <a @click="resendVerificationEmail" :disabled="loading" class="link text-green-400 font-medium hover:text-green-500">
                        Resend verification email
                    </a>
                </p>
            </form>

            <hr class="w-[85%] border-t border-green-300">

            <p class="text-md">
                Don't have an account?
                <NuxtLink to="/register" class="link text-green-400 font-medium hover:text-green-500">Register here</NuxtLink>
            </p>
        </div>
    </section>
</template>