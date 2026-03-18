<script setup>
defineProps({
    open: Boolean
})

const { public: { apiBase } } = useRuntimeConfig()
const { showPopup, showError } = usePopup()

const emit = defineEmits(["close"])

const email = ref('')
const loading = ref(false)

function handleClose() {
    if (loading.value) return

    email.value = ''
    emit("close")
}

async function handleForgotPassword() {
    loading.value = true

    try {
        const data = await $fetch(`${apiBase}/user`, {
            method: 'PATCH',
            body: {
                email: email.value
            }
        })

        showPopup(data?.detail || "Password reset email sent successfully. Please check your inbox.", "success")

        handleClose()
    } catch (err) {
        showError(err, "Failed to send password reset email. Please try again.")
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div v-if="open" @click.self="handleClose" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-10">
        <div class="w-[400px] bg-white py-10 px-5 m-3 rounded-lg text-center flex flex-col justify-center items-center gap-4">
            <p class="font-['Anton'] text-xl text-indigo-400">
                Forgot Password?
            </p>

            <p class="text-sm text-gray-500">
                Enter your email address and we'll send a link to your inbox to reset your password.
            </p>

            <form class="w-full flex flex-col gap-4" @submit.prevent="handleForgotPassword">
                <input type="email" v-model="email" :disabled="loading" class="ipt w-full" required>

                <button type="submit" :disabled="loading" class="w-full" :class="loading ? 'btn-disabled' : 'btn'">
                    {{ loading ? 'Sending...' : 'Send' }}
                </button>
            </form>
        </div>
    </div>
</template>