<script setup>
definePageMeta({
    middleware: 'auth',
    layout: 'dashboard',
    ssr: false
})

useHead({
    title: 'Create Poll',
})

const { authFetch } = useAuth()
const { public: { apiBase } } = useRuntimeConfig()

const duration = ref('infinite')
const showResults = ref('no')
const customDuration = ref('')
const question = ref('')
const options = ref(['', ''])
const loading = ref(false)
const error = ref(null)

const now = computed(() => new Date().toISOString().slice(0, 16))

function addOption() {
    if (options.value.length < 10) {
        options.value.push('')
    }
}

function removeOption(index) {
    if (options.value.length > 2) {
        options.value.splice(index, 1)
    }
}

async function createPoll() {
    error.value = null

    const cleanedOptions = options.value.filter(opt => opt.trim() !== '')

    if (!question.value.trim()) {
        error.value = 'Question is required'
        return
    }

    if (question.value.length > 1024) {
        error.value = 'Question cannot exceed 1024 characters'
        return
    }

    if (cleanedOptions.length < 2) {
        error.value = 'At least 2 options are required'
        return
    }

    for (const option of cleanedOptions) {
        if (option.length > 256) {
            error.value = 'Each option cannot exceed 256 characters'
            return
        }
    }

    try {
        loading.value = true

        const res = await authFetch(`${apiBase}/poll`, {
            method: 'POST',
            body: {
                question: question.value,
                options: cleanedOptions,
                expires_at: duration.value === 'custom' && customDuration.value ? new Date(customDuration.value).toISOString() : null,
                result_public: showResults.value === 'yes'
            }
        })

        navigateTo(`/dashboard/poll/${res.id}`)

    } catch (err) {
        error.value = 'Failed to create poll'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="dashboard-body max-w-xl flex-col items-center gap-10">
        <h2>Create A Poll</h2>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <form class="w-full flex flex-col gap-10" @submit.prevent="createPoll">
            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-1">
                    <label for="duration">Enter Poll Duration</label>
                    <select id="duration" v-model="duration">
                        <option value="infinite">Infinite</option>
                        <option value="custom">Custom Duration</option>
                    </select>
                </div>

                <div v-if="duration === 'custom'" class="flex flex-col gap-1">
                    <label for="custom_duration">Enter Poll Duration</label>
                    <input type="datetime-local" v-model="customDuration" :min="now" class="ipt" required />
                </div>

                <div class="flex flex-col gap-1">
                    <label for="show_results">Show Poll Result Publicly</label>
                    <select id="show_results" v-model="showResults">
                        <option value="yes">Yes</option>
                        <option value="no">No</option>
                    </select>
                </div>

                <div class="flex flex-col gap-1">
                    <label for="question">Enter Your Question or Opinion</label>
                    <textarea id="question" v-model="question" class="ipt h-20 resize-none" required />
                </div>

                <div class="flex flex-col gap-2">
                    <div class="flex items-center justify-between">
                        <label>Add Options</label>
                        <button type="button" class="text-sm text-indigo-400 hover:text-indigo-500 font-semibold transition-all duration-300 ease-in-out" @click="addOption">
                            + Add option
                        </button>
                    </div>

                    <div class="flex flex-col gap-2">
                        <div v-for="(option, idx) in options" :key="idx" class="flex items-center gap-2">
                            <input v-model="options[idx]" :placeholder="`Option ${idx + 1}`" class="ipt flex-1" required>
                            <button type="button" class="p-2 text-sm text-red-500 hover:text-red-600 font-bold transition-all duration-300 ease-in-out" :disabled="options.length === 2" title="Remove option" @click="removeOption(idx)">
                                ✕
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <button type="submit" :disabled="loading" class="btn">
                {{ loading ? 'Creating...' : 'Create' }}
            </button>
        </form>
    </div>
</template>