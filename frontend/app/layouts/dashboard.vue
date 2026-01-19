<script setup>
import SideBar from '@/components/side-bar.vue';

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
        <header class="px-3 pb-3 pt-2 border-b border-gray-200 flex flex-row justify-between items-center">
            <h1 class="text-3xl font-bold text-green-400">RTPoll</h1>

            <button @click="logout" :disabled="loading" class="p-1 bg-green-100 rounded-full transition duration-200 focus:outline-none hover:scale-95 active:scale-90">
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24">
                    <path fill="#05DF72"
                        d="M5 21q-.825 0-1.412-.587T3 19V5q0-.825.588-1.412T5 3h6q.425 0 .713.288T12 4t-.288.713T11 5H5v14h6q.425 0 .713.288T12 20t-.288.713T11 21zm12.175-8H10q-.425 0-.712-.288T9 12t.288-.712T10 11h7.175L15.3 9.125q-.275-.275-.275-.675t.275-.7t.7-.313t.725.288L20.3 11.3q.3.3.3.7t-.3.7l-3.575 3.575q-.3.3-.712.288t-.713-.313q-.275-.3-.262-.712t.287-.688z" />
                </svg>
            </button>
        </header>

        <main class="flex-1 flex flex-row">
            <SideBar />

            <slot />
        </main>
    </div>
</template>