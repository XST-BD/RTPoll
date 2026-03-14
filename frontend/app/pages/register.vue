<script setup>
useHead({
    title: 'Register'
})

definePageMeta({
    middleware: 'guest'
})

const { public: { apiBase } } = useRuntimeConfig()

const email = ref('')
const password = ref('')
const confirm_password = ref('')
const loading = ref(false)
const error = ref(null)

async function handleRegister() {
    error.value = null
    loading.value = true

    if (password.value !== confirm_password.value) {
        error.value = 'Passwords do not match'
        loading.value = false
        return
    }

    try {
        const res = await $fetch(`${apiBase}/user/register`, {
            method: 'POST',
            credentials: 'include',
            body: {
                email: email.value,
                password: password.value,
            }
        })

        alert(res.message)

        navigateTo('/login')
    } catch (err) {
        const detail = err?.data?.detail

        error.value = Array.isArray(detail)
            ? (detail[0]?.msg || 'Validation error')
            : (detail || err?.message || 'Something went wrong')
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <section class="w-full min-h-screen px-5 py-10 bg-grid flex flex-col justify-center items-center gap-12">
        <div class="w-full max-w-xl flex flex-col justify-center items-center gap-12 bg-white backdrop-blur-[100px] rounded-xl sm:px-10 px-5 py-10 shadow-md border border-indigo-300">
            <h2 class="">Register an Account</h2>

            <p v-if="error" class="error-msg">{{ error }}</p>

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