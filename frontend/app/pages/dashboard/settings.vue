<script setup>
definePageMeta({
    middleware: 'auth',
    layout: 'dashboard',
    ssr: false
})

useHead({
    title: 'Settings',
})
</script>

<template>
    <div class="dashboard-body max-w-xl flex-col items-center gap-12">
        <h2>Account Settings</h2>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <form class="w-full flex flex-col gap-10" @submit.prevent="handleSave">
            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-1">
                    <label for="email">Enter Your Email</label>
                    <input id="email" v-model="email" class="ipt" required>
                </div>

                <div class="flex flex-col gap-1">
                    <label for="password">Enter Your Current Password</label>
                    <input id="password" v-model="password" type="password" class="ipt" required>
                </div>

                <div class="flex flex-col gap-1">
                    <label for="new_password">Enter Your New Password</label>
                    <input id="new_password" v-model="new_password" type="password" class="ipt" required>
                </div>

                <div class="flex flex-col gap-1">
                    <label for="confirm_password">Confirm Your New Password</label>
                    <input id="confirm_password" v-model="confirm_password" type="password" class="ipt" required>
                </div>
            </div>

            <button type="submit" :disabled="loading" class="btn">
                {{ loading ? 'Saving...' : 'Save' }}
            </button>
        </form>

        <hr class="w-full border-t border-red-400">

        <h2 class="text-red-500">Danger Zone</h2>

        <DeleteAccountBtn />
    </div>
</template>