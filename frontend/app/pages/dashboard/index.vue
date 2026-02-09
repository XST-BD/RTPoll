<script setup>
import PollCard from "@/components/PollCard.vue";

definePageMeta({
    middleware: 'auth',
    layout: 'dashboard'
})

useHead({
    title: 'Home',
})
</script>

<template>
    <div class="w-full max-w-[1400px] p-5 flex flex-wrap justify-center gap-6">
        <PollCard question="What is this?" :votes="100" top-pick="Blah blah" />
        
        <PollCard question="What is this?" :votes="100" top-pick="Blah blah" />
        <PollCard question="What is this?" :votes="100" top-pick="Blah blah" />
        
        <PollCard question="What is this?" :votes="100" top-pick="Blah blah" />
        <PollCard question="What is this?" :votes="100" top-pick="Blah blah" />
        
        <PollCard question="What is this?" :votes="100" top-pick="Blah blah" />
    </div>
</template>