<script setup lang="ts">
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";

definePageMeta({
    middleware: 'auth',
    layout: 'dashboard'
})

useHead({
    title: 'Overview',
    meta: [{
        name: 'description',
        content: 'My amazing site.'
    }]
})

const series = ref([
    {
        name: "amount",
        data: [
            { x: "2024-01-01", y: 30 },
            { x: "2024-01-02", y: 40 },
            { x: "2024-01-03", y: 35 },
            { x: "2024-01-04", y: 50 },
            { x: "2024-01-05", y: 49 },
            { x: "2024-01-06", y: 60 },
            { x: "2024-01-07", y: 70 },
        ],
    },
]);

const options = ref({
    chart: { type: "area", toolbar: { show: false } },
    colors: ['#4ade80'],
    stroke: { curve: "smooth" },
    xaxis: {
        type: "datetime",
        labels: { format: "MMM dd" },
    },
    tooltip: {
        time: { format: "yyyy-MM-dd" },
    },
});
</script>

<template>
    <div class="w-full flex flex-col gap-10">
        <ClientOnly>
            <VueApexCharts type="area" :options="options" :series="series" height="350" />
        </ClientOnly>
    </div>
</template>