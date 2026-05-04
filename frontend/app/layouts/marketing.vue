<script setup>
import Navbar from '~/components/marketing/Navbar.vue'
import Footer from '~/components/marketing/Footer.vue'
</script>

<template>
    <div class="min-h-screen flex flex-col">
        <Navbar />

        <slot />

        <Footer />
    </div>
</template>