<script setup>
const { authFetch } = useAuth()
const { public: { apiBase } } = useRuntimeConfig()

const error = ref(null)
const showConfirm = ref(false)

async function deleteAllPolls() {
    error.value = null

    try {
        await authFetch(`${apiBase}/poll`, {
            method: 'DELETE'
        })
    } catch (err) {
        alert('Failed to delete all polls')
        console.error(err)
    } finally {
        showConfirm.value = false
    }
}
</script>

<template>
    <div class="flex-1">
        <button @click="showConfirm = true" class="w-full text-nowrap p-2 border-2 border-red-500 text-red-500 font-medium rounded-md transition-all duration-300 ease-in-out hover:ring-4 hover:ring-red-500 hover:ring-opacity-30 active:scale-95 cursor-pointer">
            Delete All Polls
        </button>

        <div v-if="showConfirm" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-10">
            <div class="bg-white py-10 px-5 m-3 rounded-lg text-center flex flex-col justify-center items-center gap-4">
                <p class="font-['Anton'] text-xl text-red-500">
                    Delete All Polls?
                </p>

                <p class="text-sm text-gray-500">
                    This action cannot be undone
                </p>

                <div class="flex justify-center items-center gap-3">
                    <button @click="showConfirm = false" class="px-4 py-2 border border-gray-300 hover:border-gray-400 rounded-md transition-all duration-300 ease-in-out">
                        Cancel
                    </button>

                    <button @click="deleteAllPolls" class="px-4 py-2 bg-red-500 text-white rounded-md transition-all duration-300 ease-in-out hover:bg-red-600">
                        Confirm
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>