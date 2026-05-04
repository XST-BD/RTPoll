<script setup>
const { public: { apiBase } } = useRuntimeConfig()
const { authFetch, logout } = useAuth()
const { showPopup, showError } = usePopup()

const password = ref('')
const showConfirm = ref(false)
const loading = ref(false)

async function deleteAccount() {
    loading.value = true

    if (!password.value) {
        showPopup('Please enter your password first.', 'error')
        loading.value = false
        return
    }

    if (password.value.length < 8) {
        showPopup('Password must contain at least 8 characters.', 'error')
        loading.value = false
        return
    }

    try {
        await authFetch(`${apiBase}/user`, {
            method: 'DELETE',
            body: {
                password: password.value
            }
        })

        showPopup('Account deleted successfully.', 'success')

        showConfirm.value = false

        await logout()
        await navigateTo('/login')
    } catch (err) {
        showError(err, "Failed to delete account. Please make sure your password is correct and try again.")
    } finally {
        loading.value = false
        password.value = ''
    }
}
</script>

<template>
    <div class="flex-1">
        <button @click="showConfirm = true" :disabled="loading"
            class="w-full text-nowrap p-2 bg-red-500 text-white font-medium rounded-md transition-all duration-500 hover:bg-red-600 hover:ring-4 hover:ring-red-500 hover:ring-opacity-30 focus:outline-none focus:bg-red-600 active:scale-95 cursor-pointer">
            Delete Account
        </button>

        <div v-if="showConfirm" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-10">
            <div
                class="w-[400px] bg-white py-10 px-5 m-3 rounded-lg text-center flex flex-col justify-center items-center gap-4">
                <h4 class="text-red-500">Delete Account Permanently?</h4>

                <p class="text-sm text-gray-500">
                    All your polls and data will be lost. This action cannot be undone.
                </p>

                <input type="password" placeholder="Enter your password to confirm" v-model="password"
                    class="w-full p-2 border rounded-md border-red-300 transition duration-500 focus:outline-none focus:border-red-400 focus:ring-4 focus:ring-red-400 focus:ring-opacity-30" />

                <div class="flex justify-center items-center gap-3">
                    <button @click="showConfirm = false" :disabled="loading"
                        :class="loading ? 'btn-cancel-disabled' : 'btn-cancel'">
                        Cancel
                    </button>

                    <button @click="deleteAccount" :disabled="loading"
                        :class="loading ? 'btn-alert-disabled' : 'btn-alert'">
                        Confirm
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>