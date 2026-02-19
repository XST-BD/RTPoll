<script setup>
useHead({
    title: 'Vote in Poll',
})

const { public: { apiBase } } = useRuntimeConfig()

const route = useRoute()
const id = route.params.id

const poll = ref(null)
const error = ref(null)
const loading = ref(false)

async function fetchPoll() {
    loading.value = true
    error.value = null

    try {
        const res = await $fetch(`${apiBase}/vote/poll/view`, {
            method: 'GET',
            query: { poll_id: id }
        })

        poll.value = res
    } catch (err) {
        error.value = 'Failed to load poll'
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchPoll()
})
</script>

<template>
    <main class="w-full min-h-screen flex flex-col justify-center items-center">
        <section class="grow w-full max-w-xl px-1.5 py-4 flex flex-col justify-center items-center">
            <Loading v-if="loading" />

            <p v-else-if="error" class="error-msg">{{ error }}</p>

            <p v-else-if="!poll" class="error-msg">Poll not found</p>

            <div v-else class="w-full">
                <div class="bg-green-400 p-4 rounded-t-xl flex justify-between gap-4">
                    <h2 class="text-white">{{ poll.question }}</h2>
                </div>

                <div class="overflow-hidden border-2 border-green-400 rounded-b-xl">
                    <label v-for="(option, index) in poll.options" :key="index" class="border-t border-green-400 flex cursor-pointer items-center gap-4 p-4 transition-all has-[:checked]:bg-green-100">
                        <input type="radio" name="plan" :value="option" class="peer sr-only" />

                        <div class="h-5 w-5 shrink-0 rounded-full border border-green-200 bg-white transition-all peer-checked:border-[6px] peer-checked:border-green-400 peer-focus-visible:ring-2 peer-focus-visible:ring-green-400 peer-focus-visible:ring-offset-2"></div>

                        <span class="font-medium text-slate-700">{{ option }}</span>
                    </label>
                </div>
            </div>
        </section>

        <footer class="w-full p-3 flex justify-center items-center">
            <p class="text-sm text-gray-400">Powered by <NuxtLink to="/" class="text-green-400">RTPoll</NuxtLink>
            </p>
        </footer>
    </main>
</template>