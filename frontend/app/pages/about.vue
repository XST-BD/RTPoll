<script setup>
definePageMeta({
    layout: 'marketing'
})

useHead({
    title: 'About Us'
})
</script>

<template>
    <main class="flex-1 sm:p-10 p-16 flex justify-center items-center flex-wrap gap-14">
        <ProfileCard name="Atia Farha" role="Frontend Developer" github="https://github.com/Atia-Farha"
            linkedin="https://www.linkedin.com/in/atia-farha/" />

        <ProfileCard name="S.M Nazmus Sadat" role="Backend Developer" github="https://github.com/smsadat1"
            linkedin="https://www.linkedin.com/in/sm-sadat-461755369/" />
    </main>
</template>