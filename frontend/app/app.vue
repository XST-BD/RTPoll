<script setup>
useSeoMeta({
    title: "RTPoll",
    titleTemplate: (title) => title ? `${title} | RTPoll` : "RTPoll",

    description: "A real-time polling platform that allows users to create and share polls via public links, and and track live results through an interactive interface and insightful visual graph.",

    ogTitle: "RTPoll",
    ogDescription: "A real-time polling platform that allows users to create and share polls via public links, and and track live results through an interactive interface and insightful visual graph.",

    ogType: "website",
    ogSiteName: "RTPoll",

    twitterTitle: "RTPoll",
    twitterDescription: "A real-time polling platform that allows users to create and share polls via public links, and and track live results through an interactive interface and insightful visual graph.",
    twitterCard: "summary_large_image",
})

useHead({
    htmlAttrs: {
        lang: "en"
    }
})
</script>

<template>
    <NuxtLayout>
        <NuxtPage />
    </NuxtLayout>
</template>