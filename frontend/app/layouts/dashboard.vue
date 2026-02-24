<script setup>
import Sidebar from '@/components/Sidebar.vue'
import LogoutBtn from '@/components/LogoutBtn.vue'
import { useAuth } from '@/composables/useAuth'

const { refreshToken } = useAuth()
const isLoading = ref(true)

onMounted(async () => {
    try {
        await refreshToken()
    } catch (err) {
        await navigateTo('/login', { replace: true })
    } finally {
        isLoading.value = false
    }
})
</script>

<template>
    <div class="min-h-screen flex flex-col">
        <header class="sticky top-0 z-10 h-14 px-3 py-2 bg-white border-b border-green-300 flex flex-row justify-between items-center">
            <h1>RTPoll</h1>

            <LogoutBtn />
        </header>

        <main class="flex-1 flex flex-row">
            <Sidebar class="sticky top-14 h-[calc(100vh-3.5rem)] overflow-y-auto" />

            <section class="w-full flex flex-col items-center">
                <slot />
            </section>
        </main>
    </div>
</template>