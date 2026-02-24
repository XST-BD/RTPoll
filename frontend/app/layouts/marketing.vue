<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<template>
    <div class="min-h-screen flex flex-col select-none">
        <Navbar />

        <slot />

        <footer class="w-full sm:min-h-70 sm:py-8 pt-16 pb-6 bg-green-400 flex flex-col-reverse sm:flex-row justify-evenly items-center gap-10 text-white">
            <NuxtLink to="/" class="text-8xl font-[Anton]">RTPoll</NuxtLink>

            <nav class="flex flex-col justify-center items-center gap-3">
                <NuxtLink to="/login" class="link">Login</NuxtLink>
                <NuxtLink to="/register" class="link">Sign Up</NuxtLink>
                <NuxtLink to="/#features" class="link">Features</NuxtLink>
                <NuxtLink to="/about" class="link">About Us</NuxtLink>
            </nav>
        </footer>
    </div>
</template>