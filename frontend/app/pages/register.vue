<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

useHead({
    title: 'Register',
})

const router = useRouter()

const username = ref('')
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
                username: username.value,
                email: email.value,
                password: password.value,
            }
        })

        alert(res.message)

        router.push('/login')

        username.value = ''
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
        <h2 class="text-green-400 font-bold text-3xl">Register an Account</h2>

        <p v-if="error" class="text-red-400 text-sm">{{ error }}</p>

        <form class="w-full max-w-xl flex flex-col gap-10" @submit.prevent="register">
            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-1">
                    <label for="username" class="font-medium">Username</label>
                    <input id="username" v-model="username" class="w-full h-10 p-2 border rounded-md border-green-300 transition duration-200 focus:outline-none focus:border-green-400 focus:ring-4 focus:ring-green-400 focus:ring-opacity-20" required>
                </div>

                <div class="flex flex-col gap-1">
                    <label for="email" class="font-medium">Email</label>
                    <input id="email" v-model="email" class="w-full h-10 p-2 border rounded-md border-green-300 transition duration-200 focus:outline-none focus:border-green-400 focus:ring-4 focus:ring-green-400 focus:ring-opacity-20" required>
                </div>

                <div class="flex flex-col gap-1">
                    <label for="password" class="font-medium">Password</label>
                    <input id="password" v-model="password" type="password" class="w-full h-10 p-2 border rounded-md border-green-300 transition duration-200 focus:outline-none focus:border-green-400 focus:ring-4 focus:ring-green-400 focus:ring-opacity-20" required>
                </div>
            </div>

            <button type="submit" :disabled="loading" class="w-full p-2 bg-green-400 text-white font-medium rounded-md transition duration-200 hover:bg-green-500 hover:ring-4 hover:ring-green-400 hover:ring-opacity-20 focus:outline-none focus:bg-green-500 active:scale-95">
                {{ loading ? 'Registering...' : 'Register' }}
            </button>
        </form>
    </section>
</template>