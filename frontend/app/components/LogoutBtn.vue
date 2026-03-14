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
    <button @click="handleLogout" :disabled="loading" title="Logout" class="link-icon">
        <Icon icon="carbon:logout" class="text-3xl" />
    </button>
</template>