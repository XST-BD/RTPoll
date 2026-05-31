<script setup>
useHead({
    title: 'Register'
})

definePageMeta({
    middleware: 'guest'
})

const { showPopup, showError } = usePopup()
const { requireEmail, requirePassword, validatePasswordLength, validatePasswordMatch } = useValidation()
const { register } = useAuth()

const email = ref('')
const password = ref('')
const confirm_password = ref('')
const loading = ref(false)

async function handleRegister() {
    loading.value = true

    if (!requireEmail(email.value) ||
        !requirePassword(password.value) ||
        !requirePassword(confirm_password.value, "confirm password") ||
        !validatePasswordLength(password.value) ||
        !validatePasswordMatch(password.value, confirm_password.value)) {
        loading.value = false
        return
    }

    try {
        const data = await register(
            email.value.trim(),
            password.value,
            confirm_password.value
        )

        showPopup(data?.detail || "Registration successful. Please check your email to verify your account.", "success")

        navigateTo('/login')
    } catch (err) {
        showError(err, "Failed to register. Please try again.")
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <section class="w-full min-h-screen px-5 py-10 bg-grid flex flex-col justify-center items-center gap-12">
        <PopupMessage />

        <div
            class="w-full max-w-2xl flex flex-col justify-center items-center gap-12 bg-white backdrop-blur-[100px] rounded-xl sm:px-10 px-5 py-10 shadow-md border border-indigo-300">
            <h2 class="">Register an Account</h2>

            <form class="w-full flex flex-col gap-10" @submit.prevent="handleRegister">
                <div class="flex flex-col gap-4">
                    <div class="flex flex-col gap-1">
                        <label for="email">Enter your email</label>
                        <input id="email" type="email" v-model="email" :disabled="loading" class="ipt" required>
                    </div>

                    <div class="flex flex-col gap-1">
                        <label for="password">Enter your password</label>
                        <input id="password" type="password" v-model="password" :disabled="loading" class="ipt"
                            required>
                    </div>

                    <div class="flex flex-col gap-1">
                        <label for="confirm_password">Confirm your password</label>
                        <input id="confirm_password" type="password" v-model="confirm_password" :disabled="loading"
                            class="ipt" required>
                    </div>
                </div>

                <button type="submit" :disabled="loading" :class="loading ? 'btn-disabled' : 'btn'">
                    {{ loading ? 'Registering...' : 'Register' }}
                </button>
            </form>

            <hr class="w-[85%] border-t border-indigo-300">

            <p class="text-md">
                Already have an account?
                <NuxtLink to="/login" class="link text-indigo-400 font-medium hover:text-indigo-500">Login here
                </NuxtLink>
            </p>
        </div>
    </section>
</template>