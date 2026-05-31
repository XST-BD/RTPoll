<script setup>
const { authFetch } = useAuth()
const { showPopup, showError } = usePopup()

const showConfirm = ref(false)
const loading = ref(false)

async function deleteClosedPolls() {
    loading.value = true

    try {
        const data = await authFetch('/poll', {
            method: 'DELETE',
            query: {
                expired: true
            }
        })

        showPopup(data?.detail || 'All closed polls deleted successfully.', 'success')

        showConfirm.value = false
    } catch (err) {
        showError(err, 'Failed to delete all closed polls. Please try again.')
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="flex-1">
        <button @click="showConfirm = true" :disabled="loading"
            class="w-full text-nowrap p-2 border-2 border-red-500 text-red-500 font-medium rounded-md transition-all duration-500 ease-in-out hover:ring-4 hover:ring-red-500 hover:ring-opacity-30 active:scale-95 cursor-pointer">
            Delete All Closed Polls
        </button>

        <div v-if="showConfirm" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-10">
            <div
                class="w-[400px] bg-white py-10 px-5 m-3 rounded-lg text-center flex flex-col justify-center items-center gap-4">
                <h4 class="text-red-500">Delete All Closed Polls?</h4>

                <p class="text-sm text-gray-500">
                    This action cannot be undone
                </p>

                <div class="flex justify-center items-center gap-3">
                    <button @click="showConfirm = false" :disabled="loading"
                        :class="loading ? 'btn-cancel-disabled' : 'btn-cancel'">
                        Cancel
                    </button>

                    <button @click="deleteClosedPolls" :disabled="loading"
                        :class="loading ? 'btn-alert-disabled' : 'btn-alert'">
                        Confirm
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>