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
    <div class="dashboard-body max-w-[2000px] flex-col items-center gap-12">
        <h2>Account Settings</h2>

        <div class="w-full flex justify-center items-center gap-10 sm:gap-5 flex-wrap">
            <ChangeEmail />
            <ChangePassword />
        </div>

        <h2 class="w-full text-center text-red-500 border-t border-b border-red-500 pt-3 pb-3">Danger Zone</h2>

        <div class="w-full max-w-xl flex flex-col gap-5">
            <div class="flex justify-center items-center gap-3 flex-wrap">
                <DeleteClosedPollBtn />
                <DeleteAllPollBtn />
            </div>

            <DeleteAccountBtn />
        </div>
    </div>
</template>