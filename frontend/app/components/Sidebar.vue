<script setup>
import { Icon } from "@iconify/vue";
</script>

<template>
    <aside class="bg-white flex flex-col gap-3 p-2 border-r border-green-300">
        <nav class="flex flex-col gap-3">
            <router-link to="/dashboard" title="Home" class="link-icon">
                <Icon icon="ion:file-tray-outline" class="text-3xl" />
            </router-link>

            <router-link to="/dashboard/create" title="Create Poll" class="link-icon">
                <Icon icon="system-uicons:create" class="text-3xl" style="stroke-width: 1.2;" />
            </router-link>

            <router-link to="/dashboard/overview" title="Overview" class="link-icon">
                <Icon icon="proicons:graph" class="text-3xl" />
            </router-link>
        </nav>
    </aside>
</template>