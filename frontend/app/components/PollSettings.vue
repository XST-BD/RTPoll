<script setup>
import { Icon } from '@iconify/vue'

const { public: { apiBase } } = useRuntimeConfig()
const { authFetch } = useAuth()
const { showPopup, showError } = usePopup()

const props = defineProps({
    pollId: Number
})

const showButton = ref(false)
const container = ref(null)
const showConfirm = ref(false)
const loading = ref(false)

function togglePopup() {
    showButton.value = !showButton.value
}

function openConfirm() {
    showButton.value = false
    showConfirm.value = true
}

async function deletePoll() {
    showButton.value = false
    loading.value = true

    try {
        const data = await authFetch(`${apiBase}/poll/${props.pollId}`, {
            method: 'DELETE'
        })

        showPopup(data?.detail || 'Poll deleted successfully.', 'success')

        navigateTo('/dashboard')
    } catch (err) {
        showError(err, 'Failed to delete poll.')
    } finally {
        loading.value = false
    }
}

function handleClickOutside(event) {
    if (container.value && !container.value.contains(event.target)) {
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

            <div v-if="showButton" class="absolute right-0 mt-2 shadow-xl">
                <button @click="openConfirm" :disabled="loading"
                    class="btn-alert flex justify-center items-center gap-2">
                    <Icon icon="ic:round-delete" />
                    Delete
                </button>
            </div>
        </div>

        <div v-if="showConfirm" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-10 z-40">
            <div
                class="w-[400px] bg-white py-10 px-5 m-3 rounded-lg text-center flex flex-col justify-center items-center gap-4">
                <h4>Delete This Poll?</h4>

                <p class="text-sm text-gray-500">
                    This action cannot be undone
                </p>

                <div class="flex justify-center items-center gap-3">
                    <button @click="showConfirm = false" :disabled="loading"
                        :class="loading ? 'btn-cancel-disabled' : 'btn-cancel'">
                        Cancel
                    </button>

                    <button @click="deletePoll" :disabled="loading"
                        :class="loading ? 'btn-alert-disabled' : 'btn-alert'">
                        Confirm
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>