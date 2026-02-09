<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

useHead({
    title: 'Register',
})

const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref(null)
const loading = ref(false)

async function register() {
    error.value = null
    loading.value = true

    try {
        const res = await $fetch('http://127.0.0.1:8000/api/v0/user/register', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            credentials: 'include',
            body: {
                email: email.value,
                password: password.value,
            }
        })

        alert(res.message)

        router.push('/login')

        email.value = ''
        password.value = ''
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
    <section class="w-full min-h-screen p-5 flex flex-col justify-center items-center gap-12">
        <h2 class="">Register an Account</h2>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <form class="w-full max-w-xl flex flex-col gap-10" @submit.prevent="register">
            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-1">
                    <label for="email" class="font-medium">Email</label>
                    <input id="email" v-model="email" required>
                </div>

                <div class="flex flex-col gap-1">
                    <label for="password" class="font-medium">Password</label>
                    <input id="password" v-model="password" type="password" required>
                </div>
            </div>

            <button type="submit" :disabled="loading" class="btn">
                {{ loading ? 'Registering...' : 'Register' }}
            </button>
        </form>

        <p class="text-md">
            Already have an account?
            <NuxtLink to="/login" class="link text-green-400 font-medium hover:text-green-500">Login here</NuxtLink>
        </p>
    </section>
</template>