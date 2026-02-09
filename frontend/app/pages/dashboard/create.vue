<script setup>
import { ref, computed } from 'vue'

definePageMeta({
    middleware: 'auth',
    layout: 'dashboard'
})

useHead({
    title: 'Create Poll',
})

const duration = ref('infinite')
const customDuration = ref('')
const question = ref('')
const options = ref(['', ''])
const loading = ref(false)
const error = ref(null)

const now = computed(() => new Date().toISOString().slice(0,16))

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

    if (cleanedOptions.length < 2) {
        error.value = 'At least 2 options are required'
        return
    }

    try {
        loading.value = true

        const res = await $fetch('http://127.0.0.1:8000/api/v0/dashboard/poll/create', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            credentials: 'include',
            body: {
                question: question.value,
                options: cleanedOptions,
                expires_at: duration.value === 'custom' && customDuration.value ? new Date(customDuration.value).toISOString() : ''
            }
        })

        navigateTo(`/dashboard/poll/${res.id}`)

        question.value = ''
        options.value = ['', '']

    } catch (err) {
        error.value = 'Failed to create poll'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="w-full max-w-xl p-5 flex flex-col items-center gap-10">
        <h2>Create A Poll</h2>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <form class="w-full flex flex-col gap-10" @submit.prevent="createPoll">
            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-1">
                    <label for="duration" class="font-medium">Enter Poll Duration</label>
                    <select id="duration" v-model="duration">
                        <option value="infinite">Infinite</option>
                        <option value="custom">Custom Duration</option>
                    </select>
                </div>

                <div v-if="duration === 'custom'" class="flex flex-col gap-1">
                    <label for="custom_duration" class="font-medium">Enter Poll Duration</label>
                    <input type="datetime-local" v-model="customDuration" :min="now" required />
                </div>

                <div class="flex flex-col gap-1">
                    <label for="question" class="font-medium">Enter your question or opinion</label>
                    <textarea id="question" v-model="question" class="h-20 resize-none" required />
                </div>

                <div class="flex flex-col gap-2">
                    <div class="flex items-center justify-between">
                        <label class="font-medium">Enter options</label>
                        <button type="button" class="text-sm text-green-400 hover:text-green-500 font-bold" @click="addOption">
                            + Add option
                        </button>
                    </div>

                    <div class="flex flex-col gap-2">
                        <div v-for="(option, idx) in options" :key="idx" class="flex items-center gap-2">
                            <input v-model="options[idx]" :placeholder="`Option ${idx + 1}`" class="flex-1" required>
                            <button type="button" class="p-2 text-sm text-red-400 hover:text-red-500 font-bold transition duration-300 ease-in-out" :disabled="options.length === 2" title="Remove option" @click="removeOption(idx)">
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