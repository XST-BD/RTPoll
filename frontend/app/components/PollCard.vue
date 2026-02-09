<script setup>
import { Icon } from "@iconify/vue";

defineProps({
    question: String,
    votes: Number,
    topPick: String,
    topPickPercentage: Number
})
</script>

<template>
    <div class="w-full max-w-[25em] border border-green-300 hover:border-green-400 rounded-lg py-3 px-5 flex flex-col gap-3 bg-green-50 hover:bg-gradient-to-br from-green-50 via-green-100 to-green-50 transition duration-300 cursor-pointer">
        <h4 class="text-2xl font-black">{{ question }}</h4>

        <div class="flex justify-between items-center gap-6">
            <p class="truncate">
                <span class="font-bold text-green-400">Top Pick: </span>
                <span>{{ topPick }}</span>
            </p>

            <div class="flex gap-1 justify-center items-center">
                <Icon icon="streamline:trending-content-remix" :ssr="true" class="text-lg text-green-400" />
                <span>{{ votes }}</span>
            </div>
        </div>
    </div>
</template>