<script setup>
import { Icon } from "@iconify/vue"

defineProps({
    question: String,
    top_option: String,
    total_votes: Number,
    expires_at: String
})
</script>

<template>
    <div class="grow w-full max-w-[400px] h-[180px] border border-indigo-300 hover:border-indigo-400 rounded-lg py-3 px-5 flex flex-col gap-4 bg-indigo-50 hover:bg-gradient-to-br from-indigo-50 via-indigo-100 to-indigo-50 transition-all duration-300 cursor-pointer active:scale-90">
        <h5 class="grow text-2xl font-black line-clamp-2">
            {{ question }}
        </h5>

        <p class="text-lg truncate">
            <span class="font-bold text-indigo-400">Top Pick: </span>
            <span>{{ top_option }}</span>
        </p>

        <div class="flex justify-between items-center gap-2">
            <div title="Expiry Time" class="text-sm flex justify-center items-center gap-2">
                <Icon icon="pajamas:expire" class="text-indigo-400 text-xl" />
                <span>{{ expires_at }}</span>
            </div>

            <div title="Total Votes" class="text-sm flex justify-center items-center gap-1">
                <Icon icon="lets-icons:fire-fill" class="text-indigo-400 text-2xl" />
                <span>{{ formatNumber(total_votes) }}</span>
            </div>
        </div>
    </div>
</template>