<script setup>
import { Icon } from "@iconify/vue";

const { logout } = useAuth()

const loading = ref(false)

async function handleLogout() {
    loading.value = true

    try {
        await logout()

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
    <button @click="handleLogout" :disabled="loading" title="Logout" class="link-icon">
        <Icon icon="carbon:logout" class="text-3xl" />
    </button>
</template>