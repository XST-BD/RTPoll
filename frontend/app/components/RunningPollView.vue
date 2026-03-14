<script setup>
const { authFetch } = useAuth()
const { public: { apiBase } } = useRuntimeConfig()

const running_polls = ref([])
const running_error = ref(null)
const running_loading = ref(false)
const running_page = ref(1)
const running_pages = ref(1)

async function fetchRunningPolls() {
    running_loading.value = true
    running_error.value = null

    try {
        const res = await authFetch(`${apiBase}/poll`, {
            method: 'GET',
            query: {
                expired: false,
                page: running_page.value
            }
        })

        running_polls.value = res.items
        running_pages.value = res.pages
        running_page.value = res.page
    } catch (err) {
        running_error.value = 'Failed to load running polls'
    } finally {
        running_loading.value = false
    }
}

function nextRunningPage() {
    if (running_page.value < running_pages.value) {
        running_page.value++
        fetchRunningPolls()
    }
}

function prevRunningPage() {
    if (running_page.value > 1) {
        running_page.value--
        fetchRunningPolls()
    }
}

function goRunningPage(page) {
    running_page.value = page
    fetchRunningPolls()
}

const runningVisiblePages = computed(() => {
    const pages = []
    const total = running_pages.value
    const current = running_page.value

    const start = Math.max(1, current - 2)
    const end = Math.min(total, current + 2)

    if (start > 1) {
        pages.push(1)
        if (start > 2) pages.push('...')
    }

    for (let i = start; i <= end; i++) {
        pages.push(i)
    }

    if (end < total) {
        if (end < total - 1) pages.push('...')
        pages.push(total)
    }

    return pages
})

onMounted(() => {
    fetchRunningPolls()
})
</script>

<template>
    <div class="w-full flex flex-col justify-center items-center gap-6">
        <h2>Running Polls</h2>

        <Loading v-if="running_loading" />

        <p v-else-if="running_error" class="error-msg">
            {{ running_error }}
        </p>

        <p v-else-if="running_polls.length === 0" class="text-gray-400">( No running poll )</p>

        <div v-else class="w-full flex flex-col justify-center items-center gap-5">
            <div class="w-full flex flex-wrap justify-center items-center gap-3">
                <PollCard v-for="poll in running_polls" :key="poll.id" @click="navigateTo(`/dashboard/poll/${poll.id}`)" :question="poll.question" :top_option="poll.top_option" :total_votes="poll.total_votes" :expires_at="poll.expires_at.split('T')[0].split('-').reverse().join('-')" />
            </div>

            <div v-if="running_pages > 1" class="flex justify-center items-center gap-2 text-xs">
                <button @click="prevRunningPage" :disabled="running_page === 1" class="px-3 py-1 rounded-lg border border-indigo-400 text-indigo-400 hover:bg-indigo-100 hover:border-indigo-500 hover:text-indigo-500 active:scale-90  disabled:opacity-35 transition-all duration-300 ease-in-out">
                    &#10229;
                </button>

                <button v-for="page in runningVisiblePages" :key="page" :disabled="page === '...'" @click="page !== '...' && goRunningPage(page)" class="px-3 py-1 rounded-lg border active:scale-90"
                    :class="page === running_page ? 'bg-indigo-400 text-white border-indigo-400' : 'border-gray-400 text-gray-400 hover:bg-indigo-100 hover:border-indigo-500 hover:text-indigo-500 transition-all duration-300 ease-in-out'">
                    {{ page }}
                </button>

                <button @click="nextRunningPage" :disabled="running_page === running_pages" class="px-3 py-1 rounded-lg border border-indigo-400 text-indigo-400 hover:bg-indigo-100 hover:border-indigo-500 hover:text-indigo-500 active:scale-90 disabled:opacity-35 transition-all duration-300 ease-in-out">
                    &#10230;
                </button>
            </div>
        </div>
    </div>
</template>