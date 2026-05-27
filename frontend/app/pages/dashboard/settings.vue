<script setup>
definePageMeta({
    middleware: 'auth',
    layout: 'dashboard',
    ssr: false
})

useHead({
    title: 'Settings',
})

const { authFetch } = useAuth()
const { showError } = usePopup()
const { apiBase } = useApi()

const user = ref(null)

onMounted(async () => {
    try {
        const data = await authFetch(`${apiBase}${apiBase.endsWith('/') ? '' : '/'}user`, {
            method: 'GET'
        })

        user.value = data
    } catch (err) {
        showError(err, "Failed to load user data.")
    }
})
</script>

<template>
    <div class="dashboard-body max-w-[2000px] flex-col items-center gap-12">
        <h2>Settings</h2>

        <div class="w-full max-w-2xl flex justify-center items-center gap-12 flex-col">
            <div class="w-full flex flex-col justify-center gap-5">
                <h3 class="w-full md:border-0 border-t border-b border-indigo-500 pt-3 pb-3">
                    Account Info
                </h3>

                <ChangeEmail :email="user?.email.trim()" />

                <div v-if="user" class="w-full flex flex-col justify-center items-center gap-5">
                    <div
                        class="w-full text-center text-indigo-400 border-4 border-double border-indigo-400 rounded-lg p-3">
                        <span class="font-bold">Account Created:</span>
                        {{ user?.created_at ? new Date(user.created_at).toLocaleDateString('en-US', {
                            month: 'long',
                            day: 'numeric', year: 'numeric'
                        }) : '' }}
                    </div>

                    <div
                        class="w-full flex justify-center items-center flex-nowrap md:flex-row flex-col gap-3 text-white text-nowrap">
                        <div
                            class="w-full flex flex-col justify-center items-center gap-1 bg-indigo-400 p-4 rounded-lg">
                            <span class="font-[Anton]">Total Polls</span>
                            <span>{{ user?.total_polls.toLocaleString() }}</span>
                        </div>

                        <div
                            class="w-full flex flex-col justify-center items-center gap-1 bg-indigo-400 p-4 rounded-lg">
                            <span class="font-[Anton]">Running Polls</span>
                            <span>{{ user?.running_polls.toLocaleString() }}</span>
                        </div>

                        <div
                            class="w-full flex flex-col justify-center items-center gap-1 bg-indigo-400 p-4 rounded-lg">
                            <span class="font-[Anton]">Closed Polls</span>
                            <span>{{ user?.expired_polls.toLocaleString() }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <ChangePassword />
        </div>

        <h3 class="w-full text-center text-red-500 pt-3 pb-3">
            Danger Zone
        </h3>

        <div class="w-full max-w-2xl flex flex-col gap-5">
            <div class="flex justify-center items-center gap-3 flex-wrap">
                <DeleteClosedPollBtn />
                <DeleteAllPollBtn />
            </div>

            <DeleteAccountBtn />
        </div>
    </div>
</template>