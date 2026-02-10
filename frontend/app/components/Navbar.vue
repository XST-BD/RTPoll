<script setup>
const menu = ref(false)

function toggleMenu() {
    menu.value = !menu.value
}
</script>

<template>
    <header class="self-center w-full py-2 px-5 flex sm:flex-row justify-between flex-col gap-4">
        <section class="flex justify-between items-center">
            <svg width="105" height="50">
                <text x="50%" y="45" text-anchor="middle" font-size="45" font-family="Anton" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-green-400">RTPoll</text>
            </svg>

            <div class="cursor-pointer flex flex-col gap-[5px] sm:hidden" @click="toggleMenu">
                <span class="block bg-green-400 w-6 h-[2px] rounded"></span>
                <span class="block bg-green-400 w-6 h-[2px] rounded"></span>
                <span class="block bg-green-400 w-6 h-[2px] rounded"></span>
            </div>
        </section>

        <nav :class="['self-center bg-green-100 sm:bg-white flex-col sm:flex sm:flex-row sm:gap-3 text-center', menu ? 'flex' : 'hidden sm:flex']">
            <NuxtLink to="/login"
                class="sm:w-fit w-[97vw] py-2 px-6 sm:ring-2 ring-green-400 text-green-400 font-medium sm:rounded-lg hover:bg-green-200 sm:hover:bg-green-500 sm:hover:ring-green-500 sm:hover:text-white duration-300 ease-in-out  hover:scale-98 sm:text-shadow-2xs sm:shadow-md">
                Login
            </NuxtLink>

            <NuxtLink to="/register"
                class="sm:w-fit w-[97vw] py-2 px-6 sm:ring-2 ring-green-400 sm:bg-green-400 sm:text-white text-green-400 font-medium sm:rounded-lg sm:hover:text-white hover:bg-green-200 sm:hover:bg-green-500 sm:hover:ring-green-500 duration-300 ease-in-out hover:scale-98 sm:text-shadow-2xs sm:shadow-md">
                Sign Up
            </NuxtLink>
        </nav>
    </header>
</template>