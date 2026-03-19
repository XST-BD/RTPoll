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

    if (!email.value.trim()) {
        showPopup('Please enter your new email first.', 'error')
        loading.value = false
        return
    }

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
        const data = await authFetch(`${apiBase}/user`, {
            method: 'POST',
            body: {
                recovery: true,
                new_email: email.value.trim(),
                password: password.value
            }
        })

        showPopup(data?.detail || 'Email updated successfully.', 'success')
        showConfirm.value = false
    } catch (err) {
        showError(err, 'Failed to update email. Please try again.')
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
            <label for="email">Account email</label>
            <input type="email" id="email" v-model="email" class="ipt" required>
        </div>

        <button type="submit" :disabled="loading" class="btn">
            Change Email
        </button>
    </form>

    <div v-if="showConfirm" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-10">
        <div class="w-[400px] bg-white py-10 px-5 m-3 rounded-lg text-center flex flex-col justify-center items-center gap-4">
            <h4>Change Email?</h4>

            <p class="text-sm text-gray-500">
                A confirmation email will be sent to your new email address. You need to confirm the change within 24 hours, otherwise the request will expire and you will have to try again.
            </p>

            <input type="password" placeholder="Enter your password to confirm" v-model="password" :disabled="loading" class="w-full ipt text-sm" />

            <div class="flex justify-center items-center gap-3">
                <button @click="showConfirm = false" :disabled="loading" :class="loading ? 'btn-cancel-disabled' : 'btn-cancel'">
                    Cancel
                </button>

                <button @click="handleChangeEmail" :disabled="loading" :class="loading ? 'btn-disabled' : 'btn'">
                    Confirm
                </button>
            </div>
        </div>
    </div>
</template>