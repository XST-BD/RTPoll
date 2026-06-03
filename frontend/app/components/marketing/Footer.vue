<script setup>
const PLATFORM_LINKS = [
    { label: 'Features', to: '/#features' },
    { label: 'About Us', to: '/about' }
]

const ACCOUNT_LINKS = [
    { label: 'Login', to: '/login' },
    { label: 'Sign Up', to: '/register' }
]

const LEGAL_SUPPORT_LINKS = [
    { label: 'Contact Us', to: '/contact' },
    { label: 'Privacy Policy', to: '/privacy-policy' }
]
</script>

<template>
    <footer
        class="w-full sm:min-h-70 sm:py-20 pt-16 pb-6 bg-indigo-400 flex flex-col-reverse sm:flex-row justify-evenly items-center gap-10 text-white">
        <NuxtLink to="/" class="text-8xl font-[Anton]">RTPoll</NuxtLink>

        <div class="flex flex-col sm:flex-row gap-10 sm:gap-16">
            <div class="flex flex-col items-center sm:items-start gap-3">
                <span class="font-black opacity-75 text-xs tracking-wider uppercase">Platform</span>
                <nav class="flex flex-col items-center sm:items-start gap-2">
                    <NuxtLink v-for="link in PLATFORM_LINKS" :key="link.to" :to="link.to" class="link">
                        {{ link.label }}
                    </NuxtLink>
                </nav>
            </div>

            <div class="flex flex-col items-center sm:items-start gap-3">
                <span class="font-black opacity-75 text-xs tracking-wider uppercase">Account</span>
                <nav class="flex flex-col items-center sm:items-start gap-2">
                    <NuxtLink v-for="link in ACCOUNT_LINKS" :key="link.to" :to="link.to" class="link">
                        {{ link.label }}
                    </NuxtLink>
                </nav>
            </div>

            <div class="flex flex-col items-center sm:items-start gap-3">
                <span class="font-black opacity-75 text-xs tracking-wider uppercase">Support</span>
                <nav class="flex flex-col items-center sm:items-start gap-2">
                    <NuxtLink v-for="link in LEGAL_SUPPORT_LINKS" :key="link.to" :to="link.to" class="link">
                        {{ link.label }}
                    </NuxtLink>
                </nav>
            </div>
        </div>
    </footer>
</template>