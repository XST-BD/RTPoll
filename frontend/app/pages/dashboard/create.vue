<script setup>
import { ref } from 'vue'

definePageMeta({
    middleware: 'auth',
    layout: 'dashboard'
})

useHead({
    title: 'Create Poll',
})

const question = ref('')
const options = ref(['', ''])
const loading = ref(false)
const error = ref(null)

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

        const res = await $fetch('http://127.0.0.1:8000/api/v0/createpoll/', {
            method: 'POST',
            body: {
                question: question.value,
                options: cleanedOptions
            }
        })

        alert('Poll created:', res)

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
    <section class="w-full p-5 flex flex-col items-center gap-5">
        <h2 class="text-green-400 font-bold text-3xl">Create A Poll</h2>

        <p v-if="error" class="text-red-400 text-sm">{{ error }}</p>

        <form class="w-full max-w-xl flex flex-col gap-10" @submit.prevent="createPoll">
            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-1">
                    <label for="question" class="font-medium">Enter your question or opinion</label>
                    <textarea id="question" v-model="question" class="w-full h-20 p-2 border rounded-md border-green-300 transition duration-200 resize-none focus:outline-none focus:border-green-400 focus:ring-4 focus:ring-green-400 focus:ring-opacity-20" required />
                </div>

                <div class="flex flex-col gap-2">
                    <div class="flex items-center justify-between">
                        <label class="font-medium">Enter options</label>
                        <button type="button" class="text-sm text-green-400 hover:text-green-500 font-medium" @click="addOption">
                            + Add option
                        </button>
                    </div>

                    <div class="flex flex-col gap-2">
                        <div v-for="(opt, idx) in options" :key="idx" class="flex items-center gap-2">
                            <input v-model="options[idx]" :placeholder="`Option ${idx + 1}`" class="flex-1 p-2 border rounded-md border-green-300 transition duration-200 focus:outline-none focus:border-green-400 focus:ring-4 focus:ring-green-400 focus:ring-opacity-20" required>
                            <button type="button" class="p-2 text-sm text-red-400 hover:text-red-500" :disabled="options.length === 2" title="Remove option" @click="removeOption(idx)">
                                ✕
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <button type="submit" :disabled="loading" class="w-full p-2 bg-green-400 text-white font-medium rounded-md transition duration-200 hover:bg-green-500 hover:ring-4 hover:ring-green-400 hover:ring-opacity-20 focus:outline-none focus:bg-green-500 active:scale-95">
                {{ loading ? 'Creating...' : 'Create' }}
            </button>
        </form>
    </section>
</template>