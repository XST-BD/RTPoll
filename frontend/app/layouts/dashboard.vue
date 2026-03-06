<script setup>
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
        <header class="sticky top-0 z-10 px-3 py-1 bg-white border-b border-green-300 flex flex-row justify-between items-center gap-2 shadow-sm">
            <h1>
                <NuxtLink to="/dashboard" class="flex items-center justify-center gap-2 flex-wrap">
                    <span>RTPoll</span>

                    <svg width="130" height="28">
                        <text x="50%" y="27" text-anchor="middle" font-family="Anton" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" class="text-green-400">Dashboard</text>
                    </svg>
                </NuxtLink>
            </h1>

            <LogoutBtn />
        </header>

        <main class="flex-1 flex flex-row pb-20">
            <FloatingNavPanel />

            <section class="w-full flex flex-col items-center">
                <slot />
            </section>
        </main>
    </div>
</template>