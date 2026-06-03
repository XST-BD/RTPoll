<script setup>
import { Icon } from "@iconify/vue"
import FingerprintJS from '@fingerprintjs/fingerprintjs'

definePageMeta({
    ssr: false
})

useHead({
    title: 'Vote in Poll',
})

const { api } = useApi()
const { ensureToken, token } = usePollToken('visitor')

await ensureToken()

const { public: { wsBase } } = useRuntimeConfig()
const { showPopup } = usePopup()

const route = useRoute()
const id = route.params.id

const Vue3FlipCountdown = defineAsyncComponent(() =>
    import('vue3-flip-countdown').then(m => m.Countdown)
)

const poll = ref(null)
const notice = ref(null)
const error = ref(null)
const loading = ref(true)
const selectedOption = ref(null)
const fingerprint = ref(null)

async function getVisitorId() {
    const fp = await FingerprintJS.load()
    const result = await fp.get()
    return result.visitorId
}

function handleWSMessage(data) {
    if (data.type === 'results' && poll.value) {
        console.log('[WS] Received results:', data)
        poll.value.total_votes = data.total_votes

        const option = poll.value.options.find(opt => opt[0] === data.option_id)
        if (option) {
            option[3] = data.option_perc
        }
        return
    }

    if (data.type === 'error') {
        console.log('[WS] Received error:', data)
        showPopup(data.message || 'An error occurred.', 'error')
        return
    }

    if (data.type === 'notice') {
        console.log('[WS] Received notice:', data)
        showPopup(data.message, 'info')
        return
    }
}

const { status: wsStatus, connect: connectWS, send: wsSend } = useWebSocket(() => {
    if (!token.value || !fingerprint.value) {
        return null
    }
    else {
        return `${wsBase}/${id}?t=${token.value}&fp=${fingerprint.value}`
    }
}, {
    onMessage: handleWSMessage
})

function vote(optionId) {
    selectedOption.value = optionId

    const payload = {
        type: "update",
        option_id: optionId
    }
    console.log('[WS] Sending update:', payload)

    const sent = wsSend(payload)

    if (sent) {
        showPopup('Vote submitted successfully.', 'success')
    }
    else {
        showPopup('Connection lost. Please wait...', 'error')
    }
}

async function fetchPollDetails() {
    loading.value = true
    error.value = null

    try {
        const data = await api(`/voter/${id}`)
        poll.value = data

        fingerprint.value = await getVisitorId()
        connectWS()
    } catch (err) {
        error.value = 'Failed to load poll information. Please reload the page and try again.'
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchPollDetails()
})
</script>

<template>
    <main class="w-full min-h-screen flex flex-col justify-center items-center">
        <PopupMessage />

        <section class="grow w-full max-w-2xl px-1.5 py-4 flex flex-col justify-center items-center">
            <Loading v-if="loading" />

            <p v-else-if="error"
                class="notice text-red-500 text-center border-4 border-double border-red-500 px-4 py-2">
                {{ error }}
            </p>

            <p v-else-if="notice"
                class="notice text-indigo-400 text-center border-4 border-double border-indigo-400 px-4 py-2">
                {{ notice }}
            </p>

            <div v-else class="w-full flex flex-col items-center gap-3">
                <ClientOnly>
                    <vue3-flip-countdown v-if="poll.expires_at !== 'Never'" :deadlineISO="poll.expires_at"
                        mainColor="#ffffffff" secondFlipColor="#ffffffff" mainFlipBackgroundColor="#6366F1"
                        secondFlipBackgroundColor="#818CF8" labelColor="#818CF8" countdownSize="clamp(0px, 10vw, 3.5em)"
                        labelSize="clamp(0px, 5vw, 1.5em)" />
                </ClientOnly>

                <div class="w-full">
                    <div class="bg-indigo-400 p-4 rounded-t-xl flex justify-between gap-4">
                        <h2 class="text-white">{{ poll.question }}</h2>
                    </div>

                    <div class="overflow-hidden border-2 border-indigo-400 rounded-b-xl">
                        <label v-for="(option, index) in poll.options" :key="index"
                            class="border-t border-indigo-400 flex cursor-pointer justify-between items-center gap-3 p-4 transition-all has-[:checked]:bg-indigo-100">
                            <div class="flex justify-center items-center gap-3">
                                <input type="radio" name="plan" :value="option[0]"
                                    :checked="selectedOption === option[0]" @change="vote(option[0])"
                                    class="peer sr-only" />

                                <div
                                    class="h-5 w-5 shrink-0 rounded-full border border-indigo-400 bg-white transition-all peer-checked:border-[6px] peer-focus-visible:ring-2 peer-focus-visible:ring-indigo-400 peer-focus-visible:ring-offset-2">
                                </div>

                                <span class="font-medium text-slate-700">{{ option[1] }}</span>
                            </div>

                            <span v-if="option[3] >= 0"
                                class="shrink-0 font-[Anton] text-sm text-right text-indigo-400">{{ option[3]
                                }}%</span>
                        </label>
                    </div>
                </div>

                <p title="Total Votes" v-if="poll.total_votes >= 0"
                    class="w-full mr-5 text-center text-indigo-400 flex items-center justify-end">
                    <Icon icon="lets-icons:fire-fill" class="text-indigo-400 text-xl" />
                    <span class="text-sm">{{ formatNumber(poll.total_votes) }}</span>
                </p>
            </div>
        </section>

        <PoweredByFooter />
    </main>
</template>