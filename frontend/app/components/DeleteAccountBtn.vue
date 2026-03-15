<script setup>
const { public: { apiBase } } = useRuntimeConfig()
const { authFetch, logout } = useAuth()
const { showPopup } = usePopup()

const password = ref('')
const error = ref(null)
const showConfirm = ref(false)

async function deleteAccount() {
    error.value = null

    try {
        await authFetch(`${apiBase}/user`, {
            method: 'DELETE',
            body: {
                password: password.value
            }
        })

        showPopup('Account deleted successfully', 'success')
        
        await logout()
        await navigateTo('/login')
    } catch (err) {
        showPopup(err?.data?.detail || 'Failed to delete account', 'error')
    } finally {
        password.value = ''
        showConfirm.value = false
    }
}
</script>

<template>
    <div class="flex-1">
        <button @click="showConfirm = true" class="w-full text-nowrap p-2 bg-red-500 text-white font-medium rounded-md transition-all duration-300 hover:bg-red-600 hover:ring-4 hover:ring-red-500 hover:ring-opacity-30 focus:outline-none focus:bg-red-600 active:scale-95 cursor-pointer">
            Delete Account
        </button>

        <div v-if="showConfirm" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-10">
            <div class="bg-white py-10 px-5 m-3 rounded-lg text-center flex flex-col justify-center items-center gap-4">
                <p class="font-['Anton'] text-xl text-red-500">
                    Delete Account Permanently?
                </p>

                <p class="text-sm text-gray-500">
                    All your polls and data will be lost. This action cannot be undone.
                </p>

                <p class="w-full text-sm text-gray-500">
                    <input type="password" v-model="password" placeholder="Enter your password to confirm" class="w-full  p-2 border rounded-md border-red-300 transition duration-300 focus:outline-none focus:border-red-400 focus:ring-4 focus:ring-red-400 focus:ring-opacity-30" />
                </p>

                <div class="flex justify-center items-center gap-3">
                    <button @click="showConfirm = false" class="px-4 py-2 border border-gray-300 hover:border-gray-400 rounded-md transition-all duration-300 ease-in-out">
                        Cancel
                    </button>

                    <button @click="deleteAccount" class="px-4 py-2 bg-red-500 text-white rounded-md transition-all duration-300 ease-in-out hover:bg-red-600">
                        Confirm
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>