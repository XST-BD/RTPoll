<script setup>
import { Icon } from "@iconify/vue";

const { logout } = useAuth()
const { showPopup, showError } = usePopup()

const loading = ref(false)

async function handleLogout() {
    loading.value = true

    try {
        await logout()

        showPopup("Logged out successfully", "success")

        await navigateTo('/login')
    } catch (err) {
        showError(err, "Failed to logout.")
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