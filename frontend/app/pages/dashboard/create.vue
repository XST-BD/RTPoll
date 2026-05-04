<script setup>
definePageMeta({
    middleware: 'auth',
    layout: 'dashboard',
    ssr: false
})

useHead({
    title: 'Create Poll',
})

const { public: { apiBase } } = useRuntimeConfig()
const { authFetch } = useAuth()
const { showPopup, showError } = usePopup()

const duration = ref('infinite')
const showResults = ref('no')
const customDuration = ref('')
const question = ref('')
const options = ref(['', ''])
const loading = ref(false)

const now = computed(() => new Date().toISOString().slice(0, 16))

function addOption() {
    if (options.value.length < 10) {
        options.value.push('')
    }
    else {
        showPopup('Maximum 10 options are allowed.', 'error')
    }
}

function removeOption(index) {
    if (options.value.length > 2) {
        options.value.splice(index, 1)
    }
}

async function createPoll() {
    const cleanedOptions = options.value.filter(opt => opt.trim() !== '')

    if (!question.value.trim()) {
        showPopup('Please enter a question for your poll.', 'error')
        return
    }

    if (cleanedOptions.length < 2) {
        showPopup('At least 2 options are required.', 'error')
        return
    }

    for (const option of cleanedOptions) {
        if (!option.trim()) {
            showPopup('Any option cannot be empty.', 'error')
            return
        }
    }

    if (question.value.length > 1024) {
        showPopup('Question cannot exceed 1024 characters.', 'error')
        return
    }

    for (const option of cleanedOptions) {
        if (option.length > 256) {
            showPopup('Each option cannot exceed 256 characters.', 'error')
            return
        }
    }

    try {
        loading.value = true

        const data = await authFetch(`${apiBase}/poll`, {
            method: 'POST',
            body: {
                question: question.value.trim(),
                options: cleanedOptions,
                expires_at: duration.value === 'custom' && customDuration.value ? new Date(customDuration.value).toISOString() : null,
                result_public: showResults.value === 'yes'
            }
        })

        showPopup(data?.detail || "Poll created successfully.", "success")

        navigateTo(`/dashboard/poll/${data.id}`)
    } catch (err) {
        showError(err, "Failed to create poll. Please try again.")
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="dashboard-body max-w-2xl flex-col items-center gap-10">
        <h2>Create A Poll</h2>

        <form class="w-full flex flex-col gap-10" @submit.prevent="createPoll">
            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-1">
                    <label for="duration">Enter poll duration</label>
                    <select id="duration" v-model="duration" :disabled="loading">
                        <option value="infinite">Infinite</option>
                        <option value="custom">Custom Duration</option>
                    </select>
                </div>

                <div v-if="duration === 'custom'" class="flex flex-col gap-1">
                    <label for="custom_duration">Enter custom poll duration</label>
                    <input type="datetime-local" :min="now" v-model="customDuration" :disabled="loading" class="ipt"
                        required />
                </div>

                <div class="flex flex-col gap-1">
                    <label for="show_results">Show poll result publicly</label>

                    <select id="show_results" v-model="showResults" :disabled="loading">
                        <option value="yes">Yes</option>
                        <option value="no">No</option>
                    </select>
                </div>

                <div class="flex flex-col gap-1">
                    <label for="question">Enter your question or opinion</label>
                    <textarea id="question" v-model="question" :disabled="loading" class="ipt h-20 resize-none"
                        required />
                </div>

                <div class="flex flex-col gap-2">
                    <div class="flex items-center justify-between">
                        <label>Add options</label>

                        <button type="button" @click="addOption" :disabled="loading"
                            class="text-sm text-indigo-400 hover:text-indigo-500 font-semibold transition-all duration-500 ease-in-out">
                            + Add Option
                        </button>
                    </div>

                    <div class="flex flex-col gap-2">
                        <div v-for="(option, idx) in options" :key="idx" class="flex items-center gap-2">
                            <input type="text" :placeholder="`Option ${idx + 1}`" v-model="options[idx]"
                                :disabled="loading" class="ipt flex-1" required>

                            <button type="button"
                                class="p-2 text-sm text-red-500 hover:text-red-600 font-bold transition-all duration-500 ease-in-out"
                                :class="{ 'opacity-50 cursor-not-allowed': options.length === 2 }"
                                :disabled="options.length === 2 || loading" title="Remove option"
                                @click="removeOption(idx)">
                                ✕
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <button type="submit" :disabled="loading" :class="loading ? 'btn-disabled' : 'btn'">
                {{ loading ? 'Creating...' : 'Create' }}
            </button>
        </form>
    </div>
</template>