<script setup>
import Sidebar from '@/components/Sidebar.vue';
import LogoutBtn from '@/components/LogoutBtn.vue';
</script>

<template>
    <div class="min-h-screen flex flex-col overflow-hidden">
        <header class="px-3 py-2 border-b border-green-300 flex flex-row justify-between items-center">
            <h1>RTPoll</h1>

            <LogoutBtn />
        </header>

        <main class="flex-1 flex flex-row">
            <Sidebar />

            <section class="w-full flex flex-col items-center">
                <slot />
            </section>
        </main>
    </div>
</template>