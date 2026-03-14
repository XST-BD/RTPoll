<script setup>
const { authFetch } = useAuth()
const { public: { apiBase } } = useRuntimeConfig()

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
        await authFetch(`${apiBase}/auth/manage`, {
            method: 'PUT',
            body: {
                recovery: true,
                old_password: old_password.value,
                new_password: new_password.value
            }
        })

        alert('Password changed successfully')
    } catch (err) {
        alert('Failed to change password')
        console.error(err)
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="flex-1 flex flex-col justify-center gap-5">
        <h3>Change Password</h3>

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