<script setup>
const { authFetch } = useAuth()
const { public: { apiBase } } = useRuntimeConfig()

const closed_polls = ref([])
const closed_error = ref(null)
const closed_loading = ref(false)
const closed_page = ref(1)
const closed_pages = ref(1)

async function fetchClosedPolls() {
    closed_loading.value = true
    closed_error.value = null

    try {
        const data = await authFetch(`${apiBase}/poll`, {
            method: 'GET',
            query: {
                expired: true,
                page: closed_page.value
            }
        })

        closed_polls.value = data.items
        closed_pages.value = data.pages
        closed_page.value = data.page
    } catch (err) {
        closed_error.value = 'Failed to load closed polls. Please reload the page and try again.'
    } finally {
        closed_loading.value = false
    }
}

function nextClosedPage() {
    if (closed_page.value < closed_pages.value) {
        closed_page.value++
        fetchClosedPolls()
    }
}

function prevClosedPage() {
    if (closed_page.value > 1) {
        closed_page.value--
        fetchClosedPolls()
    }
}

function goClosedPage(page) {
    closed_page.value = page
    fetchClosedPolls()
}

const closedVisiblePages = computed(() => {
    const pages = []
    const total = closed_pages.value
    const current = closed_page.value

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
    fetchClosedPolls()
})
</script>

<template>
    <div class="w-full flex flex-col justify-center items-center gap-6">
        <h2>Closed Polls</h2>

        <Loading v-if="closed_loading" />

        <p v-else-if="closed_error" class="error-msg">
            {{ closed_error }}
        </p>

        <p v-else-if="closed_polls.length === 0" class="text-gray-400">( No closed poll )</p>

        <div v-else class="w-full flex flex-col justify-center items-center gap-5">
            <div class="w-full flex flex-wrap justify-center items-center gap-3">
                <PollCard v-for="poll in closed_polls" :key="poll.id" @click="navigateTo(`/dashboard/poll/${poll.id}`)" :question="poll.question" :top_option="poll.top_option" :total_votes="poll.total_votes" :expires_at="poll.expires_at.split('T')[0].split('-').reverse().join('-')" />
            </div>

            <div v-if="closed_pages > 1" class="flex justify-center items-center gap-2 text-xs">
                <button @click="prevClosedPage" :disabled="closed_page === 1" class="px-3 py-1 rounded-lg border border-indigo-400 text-indigo-400 hover:bg-indigo-100 hover:border-indigo-500 hover:text-indigo-500 active:scale-90  disabled:opacity-35 transition-all duration-300 ease-in-out">
                    &#10229;
                </button>

                <button v-for="page in closedVisiblePages" :key="page" :disabled="page === '...'" @click="page !== '...' && goClosedPage(page)" class="px-3 py-1 rounded-lg border active:scale-90"
                    :class="page === closed_page ? 'bg-indigo-400 text-white border-indigo-400' : 'border-gray-400 text-gray-400 hover:bg-indigo-100 hover:border-indigo-500 hover:text-indigo-500 transition-all duration-300 ease-in-out'">
                    {{ page }}
                </button>

                <button @click="nextClosedPage" :disabled="closed_page === closed_pages"
                    class="px-3 py-1 rounded-lg border border-indigo-400 text-indigo-400 hover:bg-indigo-100 hover:border-indigo-500 hover:text-indigo-500 active:scale-90 disabled:opacity-35 transition-all duration-300 ease-in-out">
                    &#10230;
                </button>
            </div>
        </div>
    </div>
</template>