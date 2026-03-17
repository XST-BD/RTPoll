<script setup>
definePageMeta({
    middleware: 'guest'
})

useHead({
    title: 'Login'
})

const { public: { apiBase } } = useRuntimeConfig()
const { login } = useAuth()
const { showPopup, showError } = usePopup()

const email = ref('')
const password = ref('')
const resend_mail = ref(false)
const loading = ref(false)
const showForgotWindow = ref(false)
const resend_loading = ref(false)

async function handleLogin() {
    loading.value = true
    resend_mail.value = false

    try {
        await login(email.value, password.value)

        showPopup("Login successful", "success")

        await navigateTo('/dashboard')
    } catch (err) {
        showError(err, "Failed to login. Please try again.")

        if (err?.response?.status === 428) {
            resend_mail.value = true
        }
    } finally {
        loading.value = false
    }
}

async function resendVerificationEmail() {
    resend_loading.value = true

    try {
        const data = await $fetch(`${apiBase}/auth/email/resend`, {
            method: 'POST',
            body: {
                type: 'registration',
                email: email.value
            }
        })

        showPopup(data?.detail || "Verification email sent successfully", "success")
    } catch (err) {
        showPopup(err?.data?.detail || "Something went wrong", "error")
    } finally {
        resend_loading.value = false
    }
}
</script>

<template>
    <section class="w-full min-h-screen px-5 py-10 bg-grid flex flex-col justify-center items-center gap-12">
        <PopupMessage />

        <div class="w-full max-w-2xl flex flex-col justify-center items-center gap-12 bg-white backdrop-blur-[100px] rounded-xl sm:px-10 px-5 py-10 shadow-md border border-indigo-300">
            <h2 class="text-3xl">Login to Your Account</h2>

            <form class="w-full flex flex-col gap-10" @submit.prevent="handleLogin">
                <div class="flex flex-col gap-4">
                    <div class="flex flex-col gap-1">
                        <label for="email">Enter Your Email</label>
                        <input id="email" v-model="email" class="ipt" required>
                    </div>

                    <div class="flex flex-col gap-1">
                        <label for="password">Enter Your Password</label>
                        <input id="password" v-model="password" type="password" class="ipt" required>
                    </div>

                    <div class="flex flex-col gap-1">
                        <a @click="showForgotWindow = true" class="link text-sm text-indigo-400 hover:text-indigo-500 self-end transition-all duration-300 ease-in-out">
                            Forgot password?
                        </a>
                    </div>
                </div>

                <button type="submit" :disabled="loading" class="btn">
                    {{ loading ? 'Logging in...' : 'Login' }}
                </button>

                <p v-if="resend_mail" class="text-md text-center">
                    Verification email not received?
                    <a @click="resendVerificationEmail" :disabled="resend_loading" class="link text-indigo-400 font-medium hover:text-indigo-500">
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

        <ForgotPasswordWindow :open="showForgotWindow" @close="showForgotWindow = false" />
    </section>
</template>