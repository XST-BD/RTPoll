<script setup lang="ts">
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
])

const options = ref({
    chart: { type: "bar", toolbar: { show: false } },
    colors: ['#818CF8'],
    stroke: { curve: "smooth" },
    xaxis: {
        type: "datetime",
        labels: { format: "dd MMM yyyy" },
    },
    tooltip: {
        x: { format: "dd-mm-yyyy" },
    },
})
</script>

<template>
    <ClientOnly>
        <apexchart type="bar" :options="options" :series="series" class="w-full" height="350" />
    </ClientOnly>
</template>