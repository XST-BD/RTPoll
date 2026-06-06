<script setup>
import { Icon } from '@iconify/vue'

const { authFetch } = useAuth()

const error = ref(null)
const loading = ref(false)
const series = ref([{
    name: 'Votes',
    data: []
}])

const props = defineProps({
    poll_id: String,
})

async function fetchData() {
    loading.value = true
    try {
        const data = await authFetch(`/poll/${props.poll_id}/history`, {
            method: 'GET'
        })

        console.log('Fetched history data:', data)

        series.value = [{
            name: 'Votes',
            data: data.poll_history_record || []
        }]
    } catch (err) {
        error.value = Array.isArray(err?.data?.detail)
            ? err.data.detail.map((e) => e.msg).join(", ")
            : err.message || 'An error occurred while fetching graph data. Please click the button to try again.'
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchData()
})

const options = ref({
    chart: { type: "bar", toolbar: { show: true } },
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
    <div class="w-full flex flex-col justify-center items-center gap-6 mt-4">
        <h2>Graph View</h2>

        <p class="text-center text-gray-400">(This graph does not update in real time. Click the refresh button to load the latest data.)
        </p>

        <div class="w-full flex justify-end">
            <button @click="fetchData()"
                class="bg-indigo-400 rounded-full px-3 py-1 hover:bg-indigo-500 active:scale-95 transition-all duration-300 ease-in-out text-white flex items-center justify-center gap-2">
                <Icon icon="fluent:arrow-clockwise-16-regular" class="text-xl shrink-0" :class="{ 'spin': loading }" />
                <span>Refresh</span>
            </button>
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <p v-else-if="series.length === 0" class="text-gray-400">( No graph data )</p>

        <div v-else class="w-full flex flex-col justify-center items-center gap-4">
            <ClientOnly>
                <apexchart type="bar" :options="options" :series="series" class="w-full" height="350" />
            </ClientOnly>

            <p class="text-center text-gray-400">(Data is available for up to the last 30 days)</p>
        </div>
    </div>
</template>

<style scoped>
.spin {
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}
</style>