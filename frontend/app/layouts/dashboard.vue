<script setup>
import SideBar from '~/components/side-bar.vue';

</script>

<template>
    <div class="min-h-screen flex flex-col">
        <header class="px-3 pb-3 pt-2 border-b border-gray-200">
            <h1 class="text-3xl font-bold text-green-400">RTPoll</h1>
        </header>

        <main class="flex-1 flex flex-row">
            <SideBar />

            <slot />
        </main>
    </div>
</template>