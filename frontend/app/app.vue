<script setup>
useSeoMeta({
    title: 'RTPoll',
    titleTemplate: '%s | RTPoll',
    description: 'A real time polling website',
    ogTitle: '%s | RTPoll',
    ogDescription: 'A real time polling website',
    ogType: 'website',
    ogSiteName: 'RTPoll',
    twitterTitle: 'RTPoll',
    twitterDescription: 'A real time polling website',
})

useHead({
    htmlAttrs: {
        lang: 'en',
    }
})
</script>

<template>
    <NuxtLayout>
        <NuxtPage />
    </NuxtLayout>
</template>