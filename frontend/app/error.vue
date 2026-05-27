<script setup>
const props = defineProps({
    error: Object
})
</script>

<template>
    <NuxtLayout name="marketing">
        <div class="flex-grow flex flex-col justify-center items-center gap-5 text-center px-4 py-20">
            <h1 class="text-9xl font-[Anton] text-indigo-400 tracking-widest">{{ error.statusCode || 'Error' }}</h1>

            <h2 class="text-4xl font-bold text-indigo-400">
                {{ error.statusCode === 404 ? 'Page Not Found' : 'Something went wrong' }}
            </h2>

            <p class="text-lg max-w-md">
                {{ error.statusCode === 404 ? "Oops! The page you are looking for doesn't exist or has been moved." :
                    error.message }}
            </p>

            <NuxtLink to="/"
                class="py-3 px-6 bg-indigo-400 text-white font-medium rounded-full transition-all duration-500 hover:bg-indigo-500 hover:ring-4 hover:ring-indigo-400 hover:ring-opacity-30 outline-none focus:bg-indigo-500 active:scale-95 cursor-pointer">
                Return Home
            </NuxtLink>
        </div>
    </NuxtLayout>
</template>
