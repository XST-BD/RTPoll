<script setup>
const { authFetch } = useAuth()
const { showPopup, showError } = usePopup()
const { requirePassword, validatePasswordLength, validatePasswordMatch } = useValidation()
const { apiBase } = useApi()

const old_password = ref('')
const new_password = ref('')
const confirm_password = ref('')
const loading = ref(false)

async function handleChangePassword() {
    loading.value = true

    if (!requirePassword(old_password.value, 'current password') ||
        !requirePassword(new_password.value, 'new password') ||
        !requirePassword(confirm_password.value, 'confirm password') ||
        !validatePasswordLength(old_password.value) ||
        !validatePasswordLength(new_password.value) ||
        !validatePasswordLength(confirm_password.value) ||
        !validatePasswordMatch(new_password.value, confirm_password.value)) {
        loading.value = false
        return
    }

    try {
        const data = await authFetch(`${apiBase}${apiBase.endsWith('/') ? '' : '/'}user`, {
            method: 'PUT',
            body: {
                old_password: old_password.value,
                new_password: new_password.value
            }
        })

        showPopup(data?.detail || 'Password updated successfully.', 'success')
    } catch (err) {
        showError(err, 'Failed to update password. Please try again.')
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
                <label for="old_password">Enter your current password</label>
                <input id="old_password" type="password" v-model="old_password" :disabled="loading" class="ipt"
                    required>
            </div>

            <div class="flex flex-col gap-1">
                <label for="new_password">Enter your new password</label>
                <input id="new_password" type="password" v-model="new_password" :disabled="loading" class="ipt"
                    required>
            </div>

            <div class="flex flex-col gap-1">
                <label for="confirm_password">Confirm your new password</label>
                <input id="confirm_password" type="password" v-model="confirm_password" :disabled="loading" class="ipt"
                    required>
            </div>

            <button type="submit" :disabled="loading" :class="loading ? 'btn-disabled' : 'btn'">
                {{ loading ? 'Changing...' : 'Change Password' }}
            </button>
        </form>
    </div>
</template>