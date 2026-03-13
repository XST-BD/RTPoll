<script setup>
const { authFetch } = useAuth()
const { public: { apiBase } } = useRuntimeConfig()

const old_email = ref('')
const new_email = ref('')
const password = ref('')
const loading = ref(false)

async function handleChangeEmail() {
    loading.value = true

    try {
        await authFetch(`${apiBase}/auth/manage`, {
            method: 'POST',
            body: {
                recovery: true,
                old_email: old_email.value,
                new_email: new_email.value,
                password: password.value
            }
        })

        alert('Email changed successfully')
    } catch (err) {
        console.log(err)
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="flex-1 flex flex-col justify-center gap-5">
        <h3>Change Email</h3>

        <form @submit.prevent="handleChangeEmail" class="flex flex-col justify-center gap-3 text-nowrap">
            <div class="flex flex-col gap-1">
                <label for="old_email">Enter Your Old Email</label>
                <input id="old_email" v-model="old_email" type="email" class="ipt" required>
            </div>

            <div class="flex flex-col gap-1">
                <label for="new_email">Enter Your New Email</label>
                <input id="new_email" v-model="new_email" type="email" class="ipt" required>
            </div>

            <div class="flex flex-col gap-1">
                <label for="password">Enter Your Password</label>
                <input id="password" v-model="password" type="password" class="ipt" required>
            </div>

            <button type="submit" :disabled="loading" class="btn">
                {{ loading ? 'Changing' : 'Change Email' }}
            </button>
        </form>
    </div>
</template>