<script setup>
import { Icon } from "@iconify/vue"

definePageMeta({
    layout: 'marketing'
})

useHead({
    title: 'About Us'
})
</script>

<template>
    <main class="flex-1 w-full flex flex-col items-center pb-20">
        <section class="w-full max-w-4xl px-6 py-16 sm:py-24 text-center flex flex-col items-center gap-6">
            <h2 class="text-4xl sm:text-5xl font-[Anton] text-indigo-400">About RTPoll</h2>

            <p class="text-lg max-w-2xl leading-relaxed mt-4">
                RTPoll is a modern, real-time polling platform designed to make gathering feedback and making decisions
                instantly accessible. Whether you are hosting a live event, streaming to your audience, or just asking a
                quick question to friends, RTPoll provides lightning-fast live voting with a beautiful, interactive
                experience.
            </p>

            <div class="flex flex-wrap justify-center gap-4 mt-8">
                <div
                    class="bg-indigo-50 px-6 py-3 rounded-full border border-indigo-200 flex items-center gap-2 shadow-sm">
                    <Icon icon="fluent:flash-24-filled" class="text-indigo-400 text-xl" />
                    <span class="font-medium text-indigo-900">Real-time Updates</span>
                </div>
                <div
                    class="bg-indigo-50 px-6 py-3 rounded-full border border-indigo-200 flex items-center gap-2 shadow-sm">
                    <Icon icon="fluent:shield-lock-24-filled" class="text-indigo-400 text-xl" />
                    <span class="font-medium text-indigo-900">Secure Voting</span>
                </div>
                <div
                    class="bg-indigo-50 px-6 py-3 rounded-full border border-indigo-200 flex items-center gap-2 shadow-sm">
                    <Icon icon="fluent:data-bar-vertical-24-filled" class="text-indigo-400 text-xl" />
                    <span class="font-medium text-indigo-900">Live Analytics</span>
                </div>
            </div>
        </section>

        <div class="w-full max-w-4xl h-[1.5px] bg-gradient-to-r from-transparent via-indigo-200 to-transparent my-4"></div>

        <section class="w-full px-6 py-16 flex flex-col items-center gap-12">
            <h2 class="text-4xl sm:text-5xl font-[Anton] text-indigo-400">Meet the Team</h2>
            
            <div class="flex justify-center items-center flex-wrap gap-14">
                <ProfileCard name="Atia Farha" role="Frontend Developer" github="https://github.com/Atia-Farha"
                    linkedin="https://www.linkedin.com/in/atia-farha/" />

                <ProfileCard name="S.M Nazmus Sadat" role="Backend Developer" github="https://github.com/smsadat1"
                    linkedin="https://www.linkedin.com/in/sm-sadat-461755369/" />
            </div>
        </section>
    </main>
</template>