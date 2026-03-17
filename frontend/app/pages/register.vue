<script setup>
useHead({
    title: 'Register'
})

definePageMeta({
    middleware: 'guest'
})

const { public: { apiBase } } = useRuntimeConfig()
const { showPopup, showError } = usePopup()

const email = ref('')
const password = ref('')
const confirm_password = ref('')
const loading = ref(false)

async function handleRegister() {
    loading.value = true

    try {
        const data = await $fetch(`${apiBase}/auth/register`, {
            method: 'POST',
            credentials: 'include',
            body: {
                email: email.value,
                password: password.value,
                confirm_password: confirm_password.value
            }
        })

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

        <div class="w-full max-w-2xl flex flex-col justify-center items-center gap-12 bg-white backdrop-blur-[100px] rounded-xl sm:px-10 px-5 py-10 shadow-md border border-indigo-300">
            <h2 class="">Register an Account</h2>

            <form class="w-full flex flex-col gap-10" @submit.prevent="handleRegister">
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
                        <label for="confirm_password">Confirm Your Password</label>
                        <input id="confirm_password" v-model="confirm_password" type="password" class="ipt" required>
                    </div>
                </div>

                <button type="submit" :disabled="loading" class="btn">
                    {{ loading ? 'Registering...' : 'Register' }}
                </button>
            </form>

            <hr class="w-[85%] border-t border-indigo-300">

            <p class="text-md">
                Already have an account?
                <NuxtLink to="/login" class="link text-indigo-400 font-medium hover:text-indigo-500">Login here</NuxtLink>
            </p>
        </div>
    </section>
</template>