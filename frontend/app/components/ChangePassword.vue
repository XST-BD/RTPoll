<script setup>
const { public: { apiBase } } = useRuntimeConfig()
const { authFetch } = useAuth()
const { showPopup, showError } = usePopup()

const old_password = ref('')
const new_password = ref('')
const confirm_password = ref('')
const loading = ref(false)

async function handleChangePassword() {
    loading.value = true

    if (new_password.value !== confirm_password.value) {
        alert('New password and confirm password do not match')
        loading.value = false
        return
    }

    try {
        const data = await authFetch(`${apiBase}/user`, {
            method: 'PUT',
            body: {
                old_password: old_password.value,
                new_password: new_password.value
            }
        })

        showPopup(data?.detail || 'Password updated successfully.', 'success')
    } catch (err) {
        showError(err, 'Failed to update password.')
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="w-full flex flex-col justify-center gap-5">
        <h3 class="w-full md:border-0 border-t border-b border-indigo-500 pt-3 pb-3">Change Password</h3>

        <form @submit.prevent="handleChangePassword" class="flex flex-col justify-center gap-3 text-nowrap">
            <div class="flex flex-col gap-1">
                <label for="old_password">Enter Your Current Password</label>
                <input id="old_password" v-model="old_password" type="password" class="ipt" required>
            </div>

            <div class="flex flex-col gap-1">
                <label for="new_password">Enter Your New Password</label>
                <input id="new_password" v-model="new_password" type="password" class="ipt" required>
            </div>

            <div class="flex flex-col gap-1">
                <label for="confirm_password">Confirm Your New Password</label>
                <input id="confirm_password" v-model="confirm_password" type="password" class="ipt" required>
            </div>

            <button type="submit" :disabled="loading" class="btn">
                {{ loading ? 'Changing' : 'Change Password' }}
            </button>
        </form>
    </div>
</template>