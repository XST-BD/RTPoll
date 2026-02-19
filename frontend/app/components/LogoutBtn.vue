<script setup>
import { Icon } from "@iconify/vue";

const loading = ref(false)

const token = useCookie('access_token')

async function logout() {
    loading.value = true

    try {
        await $fetch('http://127.0.0.1:8000/api/v0/user/logout', {
            method: 'POST'
        })

        token.value = null

        await navigateTo('/login')
    } catch (err) {
        const data = err?.data

        if (Array.isArray(data?.detail)) {
            console.log(data.detail[0]?.msg)
        }
        else if (typeof data?.detail === 'string') {
            console.log(data.detail)
        }
        else {
            console.log('Something went wrong')
        }
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <button @click="logout" :disabled="loading" title="Logout" class="link-icon">
        <Icon icon="carbon:logout" :ssr="true" class="text-3xl" />
    </button>
</template>