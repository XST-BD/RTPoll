<script setup>
definePageMeta({
    middleware: 'guest'
})

useHead({
    title: 'Login'
})

const route = useRoute()
const { login, resendVerification } = useAuth()
const { showPopup, showError } = usePopup()
const { requireEmail, requirePassword, validatePasswordLength } = useValidation()

const email = ref('')
const password = ref('')
const resend_mail = ref(false)
const loading = ref(false)
const resend_loading = ref(false)
const showForgotWindow = ref(false)

async function handleLogin() {
    loading.value = true
    resend_mail.value = false

    if (!requireEmail(email.value) || !requirePassword(password.value) || !validatePasswordLength(password.value)) {
        loading.value = false
        return
    }

    try {
        await login(email.value.trim(), password.value)

        const redirectUrl = route.query.redirect || '/dashboard'
        await navigateTo(redirectUrl)
    } catch (err) {
        showError(err, "Failed to login. Please try again.")

        if (err?.status === 428) {
            resend_mail.value = true
        }
    } finally {
        loading.value = false
    }
}

async function resendVerificationEmail() {
    resend_loading.value = true

    try {
        const data = await resendVerification(email.value, 'login')

        showPopup(data?.detail || "Verification email sent successfully.", "success")
    } catch (err) {
        showError(err, "Failed to resend verification email. Please try again.")
    } finally {
        resend_loading.value = false
    }
}
</script>

<template>
    <section class="w-full min-h-screen px-5 py-10 bg-grid flex flex-col justify-center items-center gap-12">
        <PopupMessage />

        <div
            class="w-full max-w-2xl flex flex-col justify-center items-center gap-12 bg-white backdrop-blur-[100px] rounded-xl sm:px-10 px-5 py-10 shadow-md border border-indigo-300">
            <h2 class="text-3xl">Login to Your Account</h2>

            <form class="w-full flex flex-col gap-10" @submit.prevent="handleLogin">
                <div class="flex flex-col gap-4">
                    <div class="flex flex-col gap-1">
                        <label for="email">Enter your email</label>
                        <input id="email" type="email" v-model="email" :disabled="loading || resend_loading" class="ipt"
                            required>
                    </div>

                    <div class="flex flex-col gap-1">
                        <label for="password">Enter your password</label>
                        <input id="password" type="password" v-model="password" :disabled="loading || resend_loading"
                            class="ipt" required>
                    </div>

                    <div class="flex flex-col gap-1">
                        <button type="button" @click="showForgotWindow = true" :disabled="loading || resend_loading"
                            class="link text-sm text-indigo-400 hover:text-indigo-500 self-end transition-all duration-500 ease-in-out">
                            Forgot password?
                        </button>
                    </div>
                </div>

                <button type="submit" :disabled="loading || resend_loading" :class="loading ? 'btn-disabled' : 'btn'">
                    {{ loading ? 'Logging in...' : 'Login' }}
                </button>
            </form>

            <p v-if="resend_mail" class="text-md text-center">
                Verification email not received?
                <button type="button" @click="resendVerificationEmail" :disabled="loading || resend_loading"
                    class="font-medium text-indigo-400 hover:text-indigo-500"
                    :class="resend_loading ? 'link-disabled' : 'link'">
                    {{ resend_loading ? 'Resending...' : 'Resend verification email' }}
                </button>
            </p>

            <hr class="w-[85%] border-t border-indigo-300">

            <p class="text-md">
                Don't have an account?
                <NuxtLink to="/register" class="link text-indigo-400 font-medium hover:text-indigo-500">Register here
                </NuxtLink>
            </p>
        </div>

        <ForgotPasswordWindow :open="showForgotWindow" @close="showForgotWindow = false" />
    </section>
</template>