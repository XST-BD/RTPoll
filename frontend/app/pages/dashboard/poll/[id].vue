<script setup>
import { Icon } from "@iconify/vue"
import Loading from "@/components/Loading.vue"

definePageMeta({
    middleware: 'auth',
    layout: 'dashboard',
    ssr: false
})

useHead({
    title: 'Poll Details',
})

const { accessToken, refresh } = useAuth()

let socket = null

const route = useRoute()
const id = route.params.id

const poll = ref(null)
const expires_at = ref(null)
const error = ref(null)
const loading = ref(false)

async function connectWS(pollId) {
    if (!accessToken.value) {
        const ok = await refresh()
        if (!ok) {
            error.value = 'Authentication failed'
            loading.value = false
            return
        }
    }

    const token = accessToken.value

    socket = new WebSocket(`ws://127.0.0.1:8000/ws/poll/${pollId}`)

    socket.onopen = () => {
        console.log('WS Connected')
        console.log('Token being sent:', token)

        socket.send(JSON.stringify({
            type: "poll_view",
            token: token
        }))
    }

    socket.onmessage = (event) => {
        loading.value = false
        const data = JSON.parse(event.data)

        console.log("WS Data:", data)

        if (data.type === 'error') {
            error.value = data.message
            return
        }

        poll.value = data

        if (data.expires_at === "Never") {
            expires_at.value = "Never"
        } else if (data.expires_at) {
            expires_at.value = new Date(data.expires_at).toLocaleString('en-US', {
                year: 'numeric',
                month: 'long',
                day: '2-digit',
                hour: 'numeric',
                minute: '2-digit',
                hour12: true
            })
        }
    }

    socket.onerror = () => {
        error.value = 'Failed to load poll'
        loading.value = false
    }

    socket.onclose = () => {
        console.log('WS Disconnected')
    }
}

onMounted(() => {
    loading.value = true
    connectWS(id)
})

onBeforeUnmount(() => {
    if (socket) socket.close()
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
    <div class="dashboard-body max-w-xl flex-col items-center gap-10">
        <Loading v-if="loading" />

        <p v-else-if="error" class="error-msg">{{ error }}</p>

        <p v-else-if="!poll" class="error-msg">Poll not found</p>

        <div v-else class="w-full flex flex-col items-center gap-4">
            <div class="w-full">
                <div class="bg-green-400 p-4 rounded-t-xl flex justify-between gap-4">
                    <h2 class="text-white">{{ poll.question }}</h2>

                    <Icon @click="sharePoll(id)" icon="majesticons:share" class="text-3xl text-white shrink-0 cursor-pointer" />
                </div>

                <ul class="border-2 border-green-400 rounded-b-xl">
                    <li v-for="(option, index) in poll.options" :key="index" class="flex items-start gap-3 border-t-2 border-green-400 p-4 text-green-400 text-xl">
                        <span class="font-[Anton] text-md">{{ index + 1 }}.</span>
                        <span>{{ option }}</span>
                    </li>
                </ul>
            </div>

            <p class="w-full text-center text-sm text-gray-400">
                Poll Ends: {{ poll.is_indefinite ? 'Never' : expires_at }}
            </p>
        </div>
    </div>
</template>