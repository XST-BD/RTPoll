<script setup>
defineProps({
    question: String,
    expires_at: String
})
</script>

<template>
    <div class="grow w-full max-w-[400px] h-[120px] border border-green-300 hover:border-green-400 rounded-lg py-3 px-5 flex flex-col gap-3 bg-green-50 hover:bg-gradient-to-br from-green-50 via-green-100 to-green-50 transition-all duration-300 cursor-pointer">
        <h4 class="grow text-2xl font-black overflow-hidden wrap-break-word">{{ question }}</h4>

        <p class="text-center text-sm">Poll Ends: {{ expires_at }}</p>
    </div>
</template>