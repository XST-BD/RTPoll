<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Icon } from '@iconify/vue'

const { public: { apiBase } } = useRuntimeConfig()
const { authFetch } = useAuth()
const { showPopup, showError } = usePopup()

const props = defineProps({
    pollId: Number
})

const showButton = ref(false)
const showConfirm = ref(false)
const container = ref<HTMLElement | null>(null)

function togglePopup() {
    showButton.value = !showButton.value
}

function openConfirm() {
    showButton.value = false
    showConfirm.value = true
}

async function deletePoll() {
    showConfirm.value = false
    showButton.value = false

    try {
        const data = await authFetch(`${apiBase}/poll/${props.pollId}`, {
            method: 'DELETE'
        })

        showPopup(data?.detail || 'Poll deleted successfully.', 'success')

        navigateTo('/dashboard')
    } catch (err) {
        showError(err, 'Failed to delete poll.')
    }
}

function handleClickOutside(event: MouseEvent) {
    if (container.value && !container.value.contains(event.target as Node)) {
        showButton.value = false
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
    <div class="flex justify-center items-center">
        <div ref="container" class="relative inline-block">
            <Icon icon="solar:settings-bold" class="text-3xl text-indigo-400 cursor-pointer" @click="togglePopup" />

            <div v-if="showButton" class="absolute right-0 mt-2 bg-white text-red-500 border-2 border-red-500 rounded-md shadow-xl px-3 py-1">
                <button @click="openConfirm">
                    Delete
                </button>
            </div>
        </div>

        <div v-if="showConfirm" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-10">
            <div class="w-[400px] bg-white py-10 px-5 m-3 rounded-lg text-center flex flex-col justify-center items-center gap-4">
                <p class="font-['Anton'] text-xl text-red-500">
                    Delete This Poll?
                </p>

                <p class="text-sm text-gray-500">
                    This action cannot be undone
                </p>

                <div class="flex justify-center items-center gap-3">
                    <button @click="showConfirm = false" class="px-4 py-2 border border-gray-300 hover:border-gray-400 rounded-md transition-all duration-300 ease-in-out">
                        Cancel
                    </button>

                    <button @click="deletePoll" class="px-4 py-2 bg-red-500 text-white rounded-md transition-all duration-300 ease-in-out hover:bg-red-600">
                        Confirm
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>