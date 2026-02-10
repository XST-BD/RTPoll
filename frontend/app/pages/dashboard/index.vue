<script setup>
import PollCard from "@/components/PollCard.vue";

definePageMeta({
    middleware: 'auth',
    layout: 'dashboard'
})

useHead({
    title: 'Dashboard'
})

const { public: { apiBase } } = useRuntimeConfig()

const running_polls = ref([])
const closed_polls = ref([])
const running_error = ref(null)
const closed_error = ref(null)
const running_loading = ref(false)
const closed_loading = ref(false)

async function fetchRunningPolls() {
    running_loading.value = true
    running_error.value = null

    try {
        const res = await $fetch(`${apiBase}/dashboard/poll/view/all`, {
            method: 'GET',
            headers: { "Content-Type": "application/json" },
            credentials: 'include',
            query: {
                expired: false
            }
        })

        console.log(res)

        running_polls.value = res.items
    } catch (err) {
        running_error.value = 'Failed to load running polls'
    } finally {
        running_loading.value = false
    }
}

async function fetchClosedPolls() {
    closed_loading.value = true
    closed_error.value = null

    try {
        const res = await $fetch(`${apiBase}/dashboard/poll/view/all`, {
            method: 'GET',
            headers: { "Content-Type": "application/json" },
            credentials: 'include',
            query: {
                expired: true
            }
        })

        closed_polls.value = res.items
    } catch (err) {
        closed_error.value = 'Failed to load closed polls'
    } finally {
        closed_loading.value = false
    }
}

onMounted(() => {
    fetchRunningPolls()
    fetchClosedPolls()
})
</script>

<template>
    <div class="dashboard-body flex-col max-w-[2000px] gap-12">
        <div class="w-full flex flex-col justify-center items-center gap-6">
            <h2>Running Polls</h2>

            <Loading v-if="running_loading" />

            <p v-else-if="running_error" class="error-msg">
                {{ running_error }}
            </p>

            <p v-else-if="running_polls.length === 0" class="text-gray-400">( No running polls )</p>

            <div v-else class="w-full flex flex-wrap justify-center items-center gap-3">
                <PollCard v-for="poll in running_polls" :key="poll.id" @click="navigateTo(`/dashboard/poll/${poll.id}`)" :question="poll.question" :votes="poll.votes" :top-pick="poll.top_pick" />
            </div>
        </div>

        <div class="w-full flex flex-col justify-center items-center gap-6">
            <h2>Closed Polls</h2>

            <Loading v-if="closed_loading" />

            <p v-else-if="closed_error" class="error-msg">
                {{ closed_error }}
            </p>

            <p v-else-if="closed_polls.length === 0" class="text-gray-400">( No closed polls )</p>

            <div v-else class="w-full flex flex-wrap justify-center items-center gap-3">
                <PollCard v-for="poll in closed_polls" :key="poll.id" @click="navigateTo(`/dashboard/poll/${poll.id}`)" :question="poll.question" :votes="poll.votes" :top-pick="poll.top_pick" />
            </div>
        </div>
    </div>
</template>