<script setup>
import { Icon } from "@iconify/vue";
import Sidebar from '@/components/Sidebar.vue';

const error = ref(null)
const loading = ref(false)

async function logout() {
    error.value = null
    loading.value = true

    try {
        await $fetch('http://127.0.0.1:8000/api/v0/user/logout', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            credentials: 'include'
        })

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
    <div class="min-h-screen flex flex-col overflow-hidden">
        <header class="px-3 py-2 border-b border-green-300 flex flex-row justify-between items-center">
            <h1>RTPoll</h1>

            <a @click="logout" :disabled="loading" class="link-icon">
                <Icon icon="carbon:logout" :ssr="true" class="text-3xl" />
            </a>
        </header>

        <main class="flex-1 flex flex-row">
            <Sidebar />

            <section class="w-full flex flex-col items-center">
                <slot />
            </section>
        </main>
    </div>
</template>