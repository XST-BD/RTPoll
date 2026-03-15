<script setup>
definePageMeta({
    middleware: 'guest'
})

useHead({
    title: 'Login'
})

const { public: { apiBase } } = useRuntimeConfig()
const { login } = useAuth()
const { showPopup } = usePopup()

const email = ref('')
const password = ref('')
const resend_mail = ref(false)
const loading = ref(false)

async function handleLogin() {
    loading.value = true
    resend_mail.value = false

    try {
        await login(email.value, password.value)

        showPopup("Login successful", "success")

        await navigateTo('/dashboard')
    } catch (err) {
        showPopup(err?.data?.detail || "Something went wrong", "error")

        if (err.data.detail === 'User is not verified') {
            resend_mail.value = true
        }
    } finally {
        loading.value = false
    }
}

async function resendVerificationEmail() {
    loading.value = true

    try {
        const data = await $fetch(`${apiBase}/auth/email/resend`, {
            method: 'POST',
            body: {
                type: 'registration',
                email: email.value
            }
        })

        showPopup(data.detail, "success")
    } catch (err) {
        showPopup(err?.data?.detail || "Something went wrong", "error")
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <section class="w-full min-h-screen px-5 py-10 bg-grid flex flex-col justify-center items-center gap-12">
        <PopupMessage />

        <div class="w-full max-w-xl flex flex-col justify-center items-center gap-12 bg-white backdrop-blur-[100px] rounded-xl sm:px-10 px-5 py-10 shadow-md border border-indigo-300">
            <h2 class="text-3xl">Login to Your Account</h2>

            <form class="w-full flex flex-col gap-10" @submit.prevent="handleLogin">
                <div class="flex flex-col gap-4">
                    <div class="flex flex-col gap-1">
                        <label for="email">Email</label>
                        <input id="email" v-model="email" class="ipt" required>
                    </div>

                    <div class="flex flex-col gap-1">
                        <label for="password">Password</label>
                        <input id="password" v-model="password" type="password" class="ipt" required>
                    </div>
                </div>

                <button type="submit" :disabled="loading" class="btn">
                    {{ loading ? 'Logging in...' : 'Login' }}
                </button>

                <p v-if="resend_mail" class="text-md text-center">
                    Verification email not received?
                    <a @click="resendVerificationEmail" :disabled="loading" class="link text-indigo-400 font-medium hover:text-indigo-500">
                        Resend verification email
                    </a>
                </p>
            </form>

            <hr class="w-[85%] border-t border-indigo-300">

            <p class="text-md">
                Don't have an account?
                <NuxtLink to="/register" class="link text-indigo-400 font-medium hover:text-indigo-500">Register here</NuxtLink>
            </p>
        </div>
    </section>
</template>