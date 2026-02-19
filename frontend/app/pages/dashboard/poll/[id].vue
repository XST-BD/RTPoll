<script setup>
import { Icon } from "@iconify/vue";
import Loading from "@/components/Loading.vue";

definePageMeta({
    middleware: 'auth',
    layout: 'dashboard'
})

useHead({
    title: 'Poll Details',
})

let socket = null

const route = useRoute()
const id = route.params.id

const poll = ref(null)
const expires_at = ref(null)
const error = ref(null)
const loading = ref(false)

// async function fetchPoll() {
//     loading.value = true
//     error.value = null

//     try {
//         const res = await $fetch(`${apiBase}/dashboard/poll/view`, {
//             method: 'GET',
//             headers: { "Content-Type": "application/json" },
//             credentials: 'include',
//             query: { poll_id: id }
//         })

//         poll.value = res

//         if (res.expires_at == "Never") {
//             expires_at.value = res.expires_at
//         }
//         else {
//             expires_at.value = new Date(res.expires_at).toLocaleString('en-US', {
//                 year: 'numeric',
//                 month: 'long',
//                 day: '2-digit',
//                 hour: 'numeric',
//                 minute: '2-digit',
//                 hour12: true
//             })
//         }
//     } catch (err) {
//         error.value = 'Failed to load poll'
//     } finally {
//         loading.value = false
//     }
// }


function connectWS(pollId) {
    socket = new WebSocket(`ws://127.0.0.1:8000/ws/poll/${pollId}`)

    socket.onopen = () => {
        console.log('WS Connected')
        loading.value = false

        socket.send(JSON.stringify({
            type: "poll_view"
        }));
    }

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data)

        if (data.type == "poll_view") {
            console.log("WS Data:", data)
        }

        console.log("WS Data:", data)

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

                    <Icon @click="sharePoll(id)" icon="majesticons:share" :ssr="true" class="text-3xl text-white shrink-0 cursor-pointer" />
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
