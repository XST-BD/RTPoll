<script setup>
import { Icon } from "@iconify/vue";

const { logout } = useAuth()
const { showPopup } = usePopup()

const loading = ref(false)

async function handleLogout() {
    loading.value = true

    try {
        await logout()

        showPopup("Logged out successfully", "success")

        await navigateTo('/login')
    } catch (err) {
        showPopup(err?.data?.detail || "Something went wrong", "error")
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