<script setup>
import { Icon } from "@iconify/vue"
const Vue3FlipCountdown = defineAsyncComponent(() =>
    import('vue3-flip-countdown').then(m => m.Countdown)
)

definePageMeta({
    middleware: 'auth',
    layout: 'dashboard',
    ssr: false
})

useHead({
    title: 'Poll Details',
})

const { public: { wsBase } } = useRuntimeConfig()
const { accessToken, refresh } = useAuth()

let socket = null

const route = useRoute()
const id = route.params.id

const poll = ref(null)
const created_at = ref(null)
const expires_at = ref(null)
const error = ref(null)
const loading = ref(true)

const url = computed(() => {
    if (import.meta.server) return ''
    return `${window.location.origin}/poll/${id}`
})

function closeWS() {
    if (socket) {
        socket.onclose = null
        socket.close()
        socket = null
    }
}

async function connectWS(pollId) {
    closeWS()

    if (!accessToken.value) {
        const ok = await refresh()
        if (!ok) {
            error.value = 'Authentication failed'
            loading.value = false
            return
        }
    }

    socket = new WebSocket(`${wsBase}/poll/${pollId}`)

    socket.onopen = () => {
        console.log('WS Connected')

        socket.send(JSON.stringify({
            type: "poll_view",
            token: accessToken.value
        }))
    }

    socket.onmessage = (event) => {
        loading.value = false
        const data = JSON.parse(event.data)

        console.log('Received data:', data)

        if (data.type === 'error') {
            error.value = data.message
            return
        }

        error.value = null
        poll.value = data

        created_at.value = new Date(poll.value.creation).toLocaleString('en-US', {
            year: 'numeric',
            month: 'long',
            day: '2-digit',
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        })

        if (poll.value.expiry === "Never") {
            expires_at.value = "Never"
        } else if (poll.value.expiry) {
            expires_at.value = new Date(poll.value.expiry).toLocaleString('en-US', {
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
    connectWS(id)
})

onBeforeUnmount(() => {
    closeWS()
})

watch(() => accessToken.value, (newToken) => {
    if (newToken && socket) {
        connectWS(id)
    }
})

function sharePoll(id) {
    if (navigator.share) {
        navigator.share({
            title: 'Vote on this poll',
            text: 'Check out this poll and vote!',
            url: url.value
        })
    } else {
        navigator.clipboard.writeText(url.value)
        alert('Link copied to clipboard!')
    }
}

const getBackground = (percentage) => {
    if (percentage < 0) return {}

    return {
        background: `linear-gradient(to right, #E0E7FF ${percentage}%, white ${percentage}%)`
    }
}
</script>

<template>
    <div class="dashboard-body max-w-xl flex-col items-center gap-10">
        <Loading v-if="loading" />

        <p v-else-if="error" class="error-msg">{{ error }}</p>

        <p v-else-if="!poll" class="error-msg">Poll not found</p>

        <div v-else class="w-full flex flex-col items-center gap-4">
            <div class="w-full flex justify-center items-center gap-2">
                <div class="w-full flex justify-center">
                    <input class="flex-1 px-3 py-1 flex font-mono border-2 border-r-0 border-indigo-400 rounded-l-full" :value="url" readonly @click="$event.target.select()">

                    <button @click="sharePoll(id)" class="bg-indigo-400 rounded-r-full py-1 px-4 hover:bg-indigo-500 transition-all duration-300 ease-in-out">
                        <Icon icon="fluent:share-16-regular" class="text-white text-2xl shrink-0" />
                    </button>
                </div>

                <PollSettings :pollId="Number(id)" class="cursor-pointer" />
            </div>

            <div class="w-full">
                <div class="bg-indigo-400 p-4 rounded-t-xl flex justify-between gap-4">
                    <h2 class="text-white">{{ poll.question }}</h2>
                </div>

                <ul class="border-2 border-indigo-400 rounded-b-xl overflow-hidden">
                    <li v-for="(option, index) in poll.options" :key="index" class="flex justify-between gap-3 items-center border-t-2 border-indigo-400 p-4 text-xl" :style="getBackground(option.votes_perc)">
                        <div class="text-indigo-400 flex items-start gap-3">
                            <span class="font-[Anton] text-md">{{ index + 1 }}.</span>
                            <span>{{ option.text }}</span>
                        </div>

                        <span class="shrink-0 font-[Anton] text-sm text-right">{{ option.votes_perc }}%</span>
                    </li>
                </ul>
            </div>

            <ClientOnly>
                <vue3-flip-countdown v-if="poll.expiry !== 'Never' && new Date(poll.expiry) > new Date()" :deadlineISO="poll.expiry" mainColor="#ffffffff" secondFlipColor="#ffffffff" mainFlipBackgroundColor="#6366F1" secondFlipBackgroundColor="#818CF8" labelColor="#818CF8"
                    countdownSize="clamp(0px, 8vw, 3.5em)" labelSize="clamp(0px, 4vw, 1.5em)" />
            </ClientOnly>

            <div v-if="poll.expiry !== 'Never' && new Date(poll.expiry) <= new Date()" class="w-full flex flex-col justify-center items-center border-4 border-double border-gray-300 text-gray-400 p-4 rounded-lg">
                Poll is expired
            </div>

            <div class="w-full text-white text-center grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div class="flex flex-col justify-center items-center gap-1 bg-indigo-400 p-4 rounded-lg">
                    <span class="font-[Anton] text-lg">Creation Time</span>
                    <span>{{ created_at }}</span>
                </div>

                <div class="flex flex-col justify-center items-center gap-1 bg-indigo-400 p-4 rounded-lg">
                    <span class="font-[Anton] text-lg">Expiry Time</span>
                    <span>{{ expires_at }}</span>
                </div>

                <div class="flex flex-col justify-center items-center gap-1 bg-indigo-400 p-4 rounded-lg">
                    <span class="font-[Anton] text-lg">Total Votes</span>
                    <span>{{ poll.total_votes }}</span>
                </div>

                <div class="flex flex-col justify-center items-center gap-1 bg-indigo-400 p-4 rounded-lg">
                    <span class="font-[Anton] text-lg">Poll Results</span>
                    <span>{{ poll.result_public ? 'Public' : 'Private' }}</span>
                </div>
            </div>

            <div class="w-full flex items-center overflow-x-auto">
                <table class="w-full text-center overflow-x-auto">
                    <thead>
                        <tr>
                            <th class="border-2 border-indigo-400 font-[Anton] text-lg text-indigo-400 font-normal">
                                Option No.
                            </th>
                            <th class="border-2 border-indigo-400 font-[Anton] text-lg text-indigo-400 font-normal">
                                Votes Received
                            </th>
                        </tr>
                    </thead>

                    <tr v-for="(option, index) in poll.options" :key="index">
                        <td class="shrink-0 border-2 border-indigo-400">{{ index + 1 }}</td>
                        <td class="border-2 border-indigo-400">{{ option.votes.toLocaleString() }}</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</template>