<script setup>
import { Icon } from "@iconify/vue"
import FingerprintJS from '@fingerprintjs/fingerprintjs'
const Vue3FlipCountdown = defineAsyncComponent(() =>
    import('vue3-flip-countdown').then(m => m.Countdown)
)

definePageMeta({
    ssr: false
})

useHead({
    title: 'Vote in Poll',
})

const { public: { wsBase } } = useRuntimeConfig()

let socket = null

const route = useRoute()
const id = route.params.id

const poll = ref(null)
const notice = ref(null)
const error = ref(null)
const loading = ref(true)
const selectedOption = ref(null)

function closeWS() {
    if (socket) {
        socket.onclose = null
        socket.close()
        socket = null
    }
}

async function getVisitorId() {
    const fp = await FingerprintJS.load()
    const result = await fp.get()

    return result.visitorId
}

async function vote(id) {
    selectedOption.value = id
    const visitorId = await getVisitorId()

    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: "send_vote",
            option_id: id
        }))

        console.log('Vote sent:', id)
    }
}

async function connectWS(pollId) {
    closeWS()

    loading.value = true
    error.value = null
    poll.value = null

    socket = new WebSocket(`${wsBase}/vote/${pollId}`)

    socket.onopen = () => {
        console.log('WS Connected')

        socket.send(JSON.stringify({
            type: "get_vote"
        }))
    }

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data)

        console.log('Received data:', data)

        if (data.type === 'error') {
            error.value = data.message
            notice.value = null
            loading.value = false
            return
        }

        if (data.type === 'notice') {
            error.value = null
            notice.value = data.message
            loading.value = false
            return
        }

        error.value = null
        notice.value = null
        poll.value = data
        loading.value = false
    }

    socket.onerror = () => {
        error.value = 'Failed to load poll'
        loading.value = false
    }

    socket.onclose = () => {
        console.log('WS Disconnected')
    }
}

watch(
    () => id,
    (newId) => {
        if (newId) connectWS(newId)
    },
    { immediate: true }
)

onBeforeUnmount(() => {
    closeWS()
})
</script>

<template>
    <main class="w-full min-h-screen flex flex-col justify-center items-center">
        <section class="grow w-full max-w-xl px-1.5 py-4 flex flex-col justify-center items-center">
            <Loading v-if="loading" />

            <p v-else-if="error" class="notice text-red-500 text-center border-4 border-double border-red-500 px-4 py-2">
                {{ error }}
            </p>

            <p v-else-if="notice" class="notice text-indigo-400 text-center border-4 border-double border-indigo-400 px-4 py-2">
                {{ notice }}
            </p>

            <div v-else class="w-full flex flex-col items-center gap-3">
                <ClientOnly>
                    <vue3-flip-countdown v-if="poll.expiry !== 'Never'" :deadlineISO="poll.expiry" mainColor="#ffffffff" secondFlipColor="#ffffffff" mainFlipBackgroundColor="#6366F1" secondFlipBackgroundColor="#818CF8" labelColor="#818CF8" countdownSize="clamp(0px, 10vw, 3.5em)"
                        labelSize="clamp(0px, 5vw, 1.5em)" />
                </ClientOnly>

                <div class="w-full">
                    <div class="bg-indigo-400 p-4 rounded-t-xl flex justify-between gap-4">
                        <h2 class="text-white">{{ poll.question }}</h2>
                    </div>

                    <div class="overflow-hidden border-2 border-indigo-400 rounded-b-xl">
                        <label v-for="(option, index) in poll.options" :key="index" class="border-t border-indigo-400 flex cursor-pointer justify-between items-center gap-3 p-4 transition-all has-[:checked]:bg-indigo-100">
                            <div class="flex justify-center items-center gap-3">
                                <input type="radio" name="plan" :value="option.id" :checked="selectedOption === option.id" @change="vote(option.id)" class="peer sr-only" />

                                <div class="h-5 w-5 shrink-0 rounded-full border border-indigo-400 bg-white transition-all peer-checked:border-[6px] peer-focus-visible:ring-2 peer-focus-visible:ring-indigo-400 peer-focus-visible:ring-offset-2"></div>

                                <span class="font-medium text-slate-700">{{ option.text }}</span>
                            </div>

                            <span v-if="option.votes_perc >= 0" class="shrink-0 font-[Anton] text-sm text-right text-indigo-400">{{ option.votes_perc }}%</span>
                        </label>
                    </div>
                </div>

                <p v-if="poll.total_votes >= 0" class="w-full mr-5 text-center text-indigo-400 flex items-center justify-end">
                    <Icon icon="lets-icons:fire-fill" class="text-indigo-400 text-xl" />
                    <span class="text-sm">{{ formatNumber(poll.total_votes) }}</span>
                </p>
            </div>
        </section>

        <footer class="w-full p-3 flex justify-center items-center">
            <p class="text-sm text-gray-400">Powered by <NuxtLink to="/" class="text-indigo-400">RTPoll</NuxtLink>
            </p>
        </footer>
    </main>
</template>