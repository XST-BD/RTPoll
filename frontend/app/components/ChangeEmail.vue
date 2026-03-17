<script setup>
const props = defineProps({
    email: String
})

const { public: { apiBase } } = useRuntimeConfig()
const { authFetch } = useAuth()
const { showPopup, showError } = usePopup()

const showConfirm = ref(false)
const email = ref(props.email)
const password = ref('')
const loading = ref(false)

async function handleChangeEmail() {
    loading.value = true

    try {
        const data = await authFetch(`${apiBase}/user`, {
            method: 'POST',
            body: {
                recovery: true,
                new_email: email.value,
                password: password.value
            }
        })

        showPopup(data?.detail || 'Email updated successfully.', 'success')
    } catch (err) {
        showError(err, 'Failed to update email.')
    } finally {
        loading.value = false
    }
}

watch(
    () => props.email,
    (value) => {
        email.value = value
    },
    { immediate: true }
)
</script>

<template>
    <form @submit.prevent="showConfirm = true" class="flex flex-col justify-center gap-3 text-nowrap">
        <div class="flex flex-col gap-1">
            <label for="email">Account Email</label>
            <input type="email" id="email" v-model="email" class="ipt" required>
        </div>

        <button type="submit" :disabled="loading" class="btn">
            {{ loading ? 'Changing' : 'Change Email' }}
        </button>
    </form>

    <div v-if="showConfirm" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-10">
        <div class="w-[400px] bg-white py-10 px-5 m-3 rounded-lg text-center flex flex-col justify-center items-center gap-4">
            <p class="font-['Anton'] text-xl text-indigo-400">
                Change Email?
            </p>

            <p class="text-sm text-gray-500">
                A confirmation email will be sent to your new email address. You need to confirm the change within 24 hours, otherwise the request will expire and you will have to try again.
            </p>

            <p class="w-full text-sm text-gray-500">
                <input type="password" v-model="password" placeholder="Enter your password to confirm" class="w-full ipt" required />
            </p>

            <div class="flex justify-center items-center gap-3">
                <button @click="showConfirm = false" class="px-4 py-2 border border-gray-300 hover:border-gray-400 rounded-md transition-all duration-300 ease-in-out">
                    Cancel
                </button>

                <button @click="handleChangeEmail" class="px-4 py-2 bg-indigo-400 text-white rounded-md transition-all duration-300 ease-in-out hover:bg-indigo-500">
                    Confirm
                </button>
            </div>
        </div>
    </div>
</template>