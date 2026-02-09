<script setup>
import { ref } from 'vue'
import { Icon } from "@iconify/vue";

definePageMeta({
    middleware: 'auth',
    layout: 'dashboard'
})

useHead({
    title: 'Poll Details',
})

const route = useRoute()
const id = route.params.id

const poll = ref(null)
const expires_at = ref(null)
const error = ref(null)
const loading = ref(false)

async function fetchPoll() {
    loading.value = true
    error.value = null

    try {
        const res = await $fetch(`http://127.0.0.1:8000/api/v0/dashboard/poll/view`, {
            method: 'GET',
            headers: { "Content-Type": "application/json" },
            credentials: 'include',
            query: { poll_id: id }
        })

        poll.value = res
        expires_at.value = new Date(res.expires_at).toLocaleString('en-US', {
            year: 'numeric',
            month: 'long',
            day: '2-digit',
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        })
    } catch (err) {
        error.value = 'Failed to load poll'
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchPoll()
})

function sharePoll(id) {
    const url = `${window.location.origin}/poll/${id}`

    if (navigator.share) {
        navigator.share({
            title: 'Vote on this poll',
            text: 'Check out this poll and vote!',
            url: url
        })
    } else {
        navigator.clipboard.writeText(url)
        alert('Link copied to clipboard!')
    }
}
</script>

<template>
    <div class="w-full max-w-xl p-5 flex flex-col items-center gap-10">
        <div v-if="loading" class="text-green-400">
            <Icon icon="eos-icons:bubble-loading" :ssr="true" class="text-6xl" />
        </div>

        <p v-else-if="error" class="error-msg">{{ error }}</p>

        <p v-else-if="!poll" class="error-msg">Poll not found</p>

        <div v-else class="w-full flex flex-col items-center gap-4">
            <div>
                <div class="bg-green-400 p-4 rounded-t-xl flex justify-between gap-4">
                    <h2 class="text-white">{{ poll.question }}</h2>

                    <Icon @click="sharePoll(id)" icon="majesticons:share" :ssr="true" class="text-3xl text-white shrink-0 cursor-pointer" />
                </div>

                <ul class="border-2 border-green-400 rounded-b-xl">
                    <li v-for="(option, index) in poll.options" :key="index" class="flex items-start gap-3 border-t-2 border-green-400 p-4 text-green-400 text-xl">
                        <span class="font-[Anton] text-md">{{ index + 1 }}.</span>
                        <span>{{ option }}</span>
                    </li>
                </ul>
            </div>

            <p class="text-sm font-bold text-gray-400">
                {{ expires_at ? `Expires at: ${expires_at}` : 'Expires at: Never' }}
            </p>
        </div>
    </div>
</template>
