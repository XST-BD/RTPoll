<script setup>
definePageMeta({
    middleware: 'auth',
    layout: 'dashboard'
})

useHead({
    title: 'Home',
})
</script>

<template>
    <section class="w-full flex flex-col gap-10">
        <h1>Home</h1>

        <p v-if="error" class="text-red-400 text-sm">{{ error }}</p>
    </section>
</template>