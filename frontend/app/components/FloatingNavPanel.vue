<script setup>
import { Icon } from "@iconify/vue";
</script>

<template>
    <div
        class="fixed bottom-6 left-1/2 -translate-x-1/2 shrink-0 bg-white flex justify-center items-center gap-1 border border-indigo-300 hover:border-indigo-400 rounded-lg z-20 transition-all duration-500 ease-in-out w-52 shadow-lg">
        <nav class="w-full relative flex justify-center items-center">
            <router-link to="/dashboard" title="Home"
                class="flex-1 hover:bg-indigo-100 rounded-lg flex text-indigo-400 justify-start items-center p-2 pl-5 hover:text-indigo-500 transition-all duration-500 ease-in-out">
                <Icon icon="ion:file-tray-outline" class="text-3xl" />
            </router-link>

            <router-link to="/dashboard/create" title="Create Poll"
                class="absolute left-1/2 -translate-x-1/2 rounded-full bg-indigo-400 text-white p-4 w-15 h-15 flex items-center justify-center shrink-0 hover:bg-indigo-500 transition-all duration-500 ease-in-out shadow-lg active:scale-90">
                <Icon icon="system-uicons:create" class="text-4xl" style="stroke-width: 1.2;" />
            </router-link>

            <router-link to="/dashboard/settings" title="Settings"
                class="flex-1 hover:bg-indigo-100 rounded-lg flex justify-end text-indigo-400 items-center p-2 pr-5 hover:text-indigo-500 transition-all duration-500 ease-in-out">
                <Icon icon="solar:settings-outline" class="text-3xl" />
            </router-link>
        </nav>
    </div>
</template>