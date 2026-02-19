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
const error = ref(null)
const loading = ref(false)

async function register() {
    error.value = null
    loading.value = true

    try {
        const res = await $fetch(`${apiBase}/user/register`, {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            credentials: 'include',
            body: {
                email: email.value,
                password: password.value,
            }
        })

        alert(res.message)

        navigateTo('/login')
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
            <h2 class="">Register an Account</h2>

            <p v-if="error" class="error-msg">{{ error }}</p>

            <form class="w-full flex flex-col gap-10" @submit.prevent="register">
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
                    {{ loading ? 'Registering...' : 'Register' }}
                </button>
            </form>

            <hr class="w-[85%] border-t border-green-300">

            <p class="text-md">
                Already have an account?
                <NuxtLink to="/login" class="link text-green-400 font-medium hover:text-green-500">Login here</NuxtLink>
            </p>
        </div>
    </section>
</template>