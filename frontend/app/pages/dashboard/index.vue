<script setup>
definePageMeta({
    middleware: 'auth',
    layout: 'dashboard',
})

useHead({
    title: 'Dashboard'
})

const activeTab = ref('running')
</script>

<template>
    <div class="dashboard-body flex-col max-w-[2000px] gap-10">
        <div class="flex justify-center items-center">
            <button @click="activeTab = 'running'"
                class="px-4 py-3 rounded-l-full border border-r-0 text-sm font-semibold transition-all duration-500 ease-in-out"
                :class="activeTab === 'running' ? 'bg-indigo-400 text-white border-indigo-400 hover:bg-indigo-500' : 'border-indigo-400 text-indigo-400 hover:bg-indigo-100 hover:text-indigo-500 hover:border-indigo-500'">
                Running Polls
            </button>

            <button @click="activeTab = 'closed'"
                class="px-4 py-3 rounded-r-full border border-l-0 text-sm font-semibold transition-all duration-500 ease-in-out"
                :class="activeTab === 'closed' ? 'bg-indigo-400 text-white border-indigo-400 hover:bg-indigo-500' : 'border-indigo-400 text-indigo-400 hover:bg-indigo-100 hover:text-indigo-500 hover:border-indigo-500'">
                Closed Polls
            </button>
        </div>

        <RunningPollView v-if="activeTab === 'running'" />

        <ClosedPollView v-if="activeTab === 'closed'" />
    </div>
</template>