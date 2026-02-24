<script setup>
import { Icon } from '@iconify/vue';

defineProps({
    name: String,
    role: String,
    github: String,
    linkedin: String
})
</script>

<template>
    <div class="w-[19em] border-2 border-green-400 rounded-xl overflow-hidden">
        <div class="p-9 pb-6 flex flex-col gap-3">
            <h2 class="text-center">{{ name }}</h2>

            <h4 class="text-center">
                {{ role }}
            </h4>
        </div>

        <div class="flex justify-center items-center border-t-2 border-green-400">
            <a :href="github" target="_blank" class="w-full bg-green-400 hover:bg-green-500 p-3 flex justify-center transition-all duration-300 ease-in-out">
                <Icon icon="mdi:github" class="text-3xl text-white" />
            </a>

            <a :href="linkedin" target="_blank" class="w-full bg-green-400 hover:bg-green-500 p-3 flex justify-center transition-colors duration-300 ease-in-out">
                <Icon icon="mdi:linkedin" class="text-3xl text-white" />
            </a>
        </div>
    </div>
</template>