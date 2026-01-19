<script setup>
import { ref } from 'vue'

const menu = ref(false)

function toggleMenu() {
    menu.value = !menu.value
}
</script>

<template>
    <div class="min-h-screen font-[Poppins] flex flex-col select-none">
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
                <NuxtLink to="/login" class="sm:w-fit w-[97vw] py-2 px-6 sm:ring-2 ring-green-400 text-green-400 font-medium sm:rounded-lg hover:bg-green-200 sm:hover:bg-green-500 sm:hover:ring-green-500 sm:hover:text-white duration-300 ease-in-out  hover:scale-98 sm:text-shadow-2xs sm:shadow-md">
                    Login
                </NuxtLink>

                <NuxtLink to="/register"
                    class="sm:w-fit w-[97vw] py-2 px-6 sm:ring-2 ring-green-400 sm:bg-green-400 sm:text-white text-green-400 font-medium sm:rounded-lg sm:hover:text-white hover:bg-green-200 sm:hover:bg-green-500 sm:hover:ring-green-500 duration-300 ease-in-out hover:scale-98 sm:text-shadow-2xs sm:shadow-md">
                    Sign Up
                </NuxtLink>
            </nav>
        </header>

        <main class="flex-1">
            <section class="min-h-[40vh] pt-20 pb-5 px-4 flex flex-col justify-center items-center gap-10 text-center">
                <h2 class="max-w-xl font-[Anton] text-5xl text-green-400 text-shadow-xs">
                    Make Your Own Polling and Share Easily with RTPoll
                </h2>

                <p class="max-w-3xl text-lg text-shadow-2xs">
                    RTPoll is a platform that allows you to create polls, share them by public links and see the results in real-time.
                </p>
            </section>

            <section>
                <svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svgjs="http://svgjs.dev/svgjs" viewBox="0 0 2400 800">
                    <g fill="#4ade80" transform="matrix(1,0,0,1,0,-91.66220092773438)">
                        <path d="M 0 320.62208412671635 Q 450 553.9851395407129 600 333.41605503906 Q 1050 554.3313591662456 1200 303.32437585903926 Q 1650 564.4988114210746 1800 341.18012636432127 Q 2250 496.25471497957324 2400 325.04619014416653 L 2400 800 L 0 800 L 0 311.61070516382426 Z"
                            transform="matrix(1,0,0,1,0,35)" opacity="0.05"></path>
                        <path d="M 0 320.62208412671635 Q 450 553.9851395407129 600 333.41605503906 Q 1050 554.3313591662456 1200 303.32437585903926 Q 1650 564.4988114210746 1800 341.18012636432127 Q 2250 496.25471497957324 2400 325.04619014416653 L 2400 800 L 0 800 L 0 311.61070516382426 Z"
                            transform="matrix(1,0,0,1,0,70)" opacity="0.21"></path>
                        <path d="M 0 320.62208412671635 Q 450 553.9851395407129 600 333.41605503906 Q 1050 554.3313591662456 1200 303.32437585903926 Q 1650 564.4988114210746 1800 341.18012636432127 Q 2250 496.25471497957324 2400 325.04619014416653 L 2400 800 L 0 800 L 0 311.61070516382426 Z"
                            transform="matrix(1,0,0,1,0,105)" opacity="0.37"></path>
                        <path d="M 0 320.62208412671635 Q 450 553.9851395407129 600 333.41605503906 Q 1050 554.3313591662456 1200 303.32437585903926 Q 1650 564.4988114210746 1800 341.18012636432127 Q 2250 496.25471497957324 2400 325.04619014416653 L 2400 800 L 0 800 L 0 311.61070516382426 Z"
                            transform="matrix(1,0,0,1,0,140)" opacity="0.53"></path>
                        <path d="M 0 320.62208412671635 Q 450 553.9851395407129 600 333.41605503906 Q 1050 554.3313591662456 1200 303.32437585903926 Q 1650 564.4988114210746 1800 341.18012636432127 Q 2250 496.25471497957324 2400 325.04619014416653 L 2400 800 L 0 800 L 0 311.61070516382426 Z"
                            transform="matrix(1,0,0,1,0,175)" opacity="0.68"></path>
                        <path d="M 0 320.62208412671635 Q 450 553.9851395407129 600 333.41605503906 Q 1050 554.3313591662456 1200 303.32437585903926 Q 1650 564.4988114210746 1800 341.18012636432127 Q 2250 496.25471497957324 2400 325.04619014416653 L 2400 800 L 0 800 L 0 311.61070516382426 Z"
                            transform="matrix(1,0,0,1,0,210)" opacity="0.84"></path>
                        <path d="M 0 320.62208412671635 Q 450 553.9851395407129 600 333.41605503906 Q 1050 554.3313591662456 1200 303.32437585903926 Q 1650 564.4988114210746 1800 341.18012636432127 Q 2250 496.25471497957324 2400 325.04619014416653 L 2400 800 L 0 800 L 0 311.61070516382426 Z"
                            transform="matrix(1,0,0,1,0,245)" opacity="1"></path>
                    </g>
                </svg>
            </section>

            <section id="features" class="bg-green-400 pb-16 px-6 flex flex-col justify-center items-center gap-16 text-center">
                <h2 class="font-[Anton] text-5xl font-medium text-white underline underline-offset-8 decoration-wavy text-shadow-md">
                    Features
                </h2>

                <article class="flex flex-row flex-wrap gap-6 justify-center items-center">
                    <div class="max-w-sm bg-white px-5 py-10 rounded-xl flex flex-col flex-wrap justify-center items-center gap-5 duration-300 ease-in-out shadow-md hover:shadow-sm hover:scale-99">
                        <div class="rounded-xl p-2 bg-green-100 shadow-sm">
                            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 20 20">
                                <path fill="#05DF72" d="M18 10a2 2 0 0 0-2-2H4a2 2 0 1 0 0 4h12a2 2 0 0 0 2-2m-8-6a2 2 0 0 0-2-2H4a2 2 0 1 0 0 4h4a2 2 0 0 0 2-2m4 12a2 2 0 0 0-2-2H4a2 2 0 1 0 0 4h8a2 2 0 0 0 2-2" />
                            </svg>
                        </div>

                        <h3 class="text-2xl font-[Anton] text-green-400 text-shadow-2xs">
                            Create Polls
                        </h3>

                        <p class="max-w-3xl text-shadow-2xs">
                            Create polls with multiple options and vote for them.
                        </p>
                    </div>

                    <div class="max-w-sm bg-white px-5 py-10 rounded-xl flex flex-col flex-wrap justify-center items-center gap-5 duration-300 ease-in-out shadow-md hover:shadow-sm hover:scale-99">
                        <div class="rounded-xl p-2 bg-green-100 shadow-sm">
                            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24">
                                <g fill="none">
                                    <path
                                        d="m12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.018-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z" />
                                    <path fill="#05DF72"
                                        d="m17.303 9.524l3.182 3.182a5.5 5.5 0 1 1-7.778 7.778l-1.06-1.06a1.5 1.5 0 1 1 2.12-2.122l1.062 1.061a2.5 2.5 0 0 0 3.535-3.536l-3.182-3.182a2.5 2.5 0 0 0-2.681-.56q-.242.096-.454.196l-.464.217c-.62.28-1.097.4-1.704-.206c-.872-.872-.646-1.677.417-2.41a5.5 5.5 0 0 1 7.007.642m-6.01-6.01l1.06 1.06a1.5 1.5 0 0 1-2.12 2.122l-1.061-1.06A2.5 2.5 0 1 0 5.636 9.17l3.182 3.182a2.5 2.5 0 0 0 2.681.56q.242-.096.454-.196l.464-.217c.62-.28 1.098-.4 1.704.206c.872.872.646 1.677-.417 2.41a5.5 5.5 0 0 1-7.007-.642l-3.182-3.182a5.5 5.5 0 1 1 7.778-7.778Z" />
                                </g>
                            </svg>
                        </div>

                        <h3 class="text-2xl font-[Anton] text-green-400 text-shadow-2xs">
                            Share Polls
                        </h3>

                        <p class="max-w-3xl text-shadow-2xs">
                            Share polls by public links and see the results in real-time.
                        </p>
                    </div>

                    <div class="max-w-sm bg-white px-5 py-10 rounded-xl flex flex-col flex-wrap justify-center items-center gap-5 duration-300 ease-in-out shadow-md hover:shadow-sm hover:scale-99">
                        <div class="rounded-xl p-3 bg-green-100 shadow-sm">
                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 14 14">
                                <path fill="#05DF72" fill-rule="evenodd"
                                    d="M.75 0a.75.75 0 0 1 .75.75v7.055l1.184-1.322A2.4 2.4 0 0 1 2.5 5.5c0-1.28.72-2 2-2s2 .72 2 2q0 .198-.023.377l1.628 1.271Q8.492 7.001 9 7q.18 0 .344.019l.96-2.815C9.781 3.881 9.5 3.3 9.5 2.5c0-1.28.72-2 2-2s2 .72 2 2c0 1.179-.61 1.883-1.707 1.987L10.676 7.76c.213.32.324.737.324 1.24c0 1.28-.72 2-2 2s-2-.72-2-2q0-.408.096-.737L5.72 7.189c-.317.204-.727.311-1.22.311a2.8 2.8 0 0 1-.648-.072L1.5 10.053v1.197c0 .69.56 1.25 1.25 1.25h10.5a.75.75 0 0 1 0 1.5H2.75A2.75 2.75 0 0 1 0 11.25V.75A.75.75 0 0 1 .75 0"
                                    clip-rule="evenodd" />
                            </svg>
                        </div>

                        <h3 class="text-2xl font-[Anton] text-green-400 text-shadow-2xs">
                            Analyze Results
                        </h3>

                        <p class="max-w-3xl text-shadow-2xs">
                            Analyze results visually and see the most popular options.
                        </p>
                    </div>
                </article>
            </section>

            <section class="flex flex-col justify-center items-center text-center">
                <div class="bg-gradient-to-b from-green-400 to-transparent h-[150px] w-full"></div>

                <article class="min-h-[80vh] px-4 py-20 flex flex-col justify-center items-center gap-16 text-center">
                    <h2 class="text-5xl font-[Anton] text-green-400 text-shadow-md">
                        Create Polls in a Minute
                    </h2>

                    <NuxtLink to="/register" class="py-4 px-6 ring-2 ring-green-400 bg-green-400 text-white font-medium rounded-lg hover:bg-green-500 hover:ring-green-500 duration-300 ease-in-out hover:scale-98 shadow-md">Get Started</NuxtLink>
                </article>
            </section>
        </main>

        <footer class="w-full sm:min-h-70 sm:py-8 pt-16 pb-6 bg-green-400 flex flex-col-reverse sm:flex-row justify-evenly items-center gap-10 text-white">
            <NuxtLink to="/" class="text-8xl font-[Anton]">RTPoll</NuxtLink>

            <nav class="flex flex-col justify-center items-center gap-3">
                <NuxtLink to="/#features" class="duration-300 ease-in-out hover:underline underline-offset-8 decoration-wavy">Features</NuxtLink>
                <NuxtLink to="/about" class="duration-300 ease-in-out hover:underline underline-offset-8 decoration-wavy">About Us</NuxtLink>
                <NuxtLink to="/login" class="duration-300 ease-in-out hover:underline underline-offset-8 decoration-wavy">Login</NuxtLink>
                <NuxtLink to="/register" class="duration-300 ease-in-out hover:underline underline-offset-8 decoration-wavy">Sign Up</NuxtLink>
            </nav>
        </footer>
    </div>
</template>