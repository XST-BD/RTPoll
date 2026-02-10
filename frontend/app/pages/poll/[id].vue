<template>
    <main class="w-full min-h-screen flex justify-center items-center">
        <section class="dashboard-body max-w-xl flex-col gap-5">
            <h1>What is your name?</h1>

            <div class="flex flex-col gap-3">
                <label class="flex items-center cursor-pointer">
                    <input type="radio" name="custom" value="option2" class="hidden peer">
                    <span class="w-3 h-3 rounded-full border border-green-400 flex items-center justify-center
                peer-checked:bg-green-400 peer-checked:border-green-400 transition-colors duration-200">
                    </span>

                    <span class="text-gray-700 font-medium">Green Option</span>
                </label>

                <label class="flex items-center cursor-pointer">
                    <input type="radio" name="custom" value="option2" class="hidden peer">
                    <span class="w-3 h-3 rounded-full border border-green-400 flex items-center justify-center
                peer-checked:bg-green-400 peer-checked:border-green-400 transition-colors duration-200">
                    </span>

                    <span class="text-gray-700 font-medium">Green Option</span>
                </label>

                <label class="flex items-center cursor-pointer">
                    <input type="radio" name="custom" value="option2" class="hidden peer">
                    <span class="w-3 h-3 rounded-full border border-green-400 flex items-center justify-center
                peer-checked:bg-green-400 peer-checked:border-green-400 transition-colors duration-200">
                    </span>

                    <span class="text-gray-700 font-medium">Green Option</span>
                </label>
            </div>

        </section>
    </main>
</template>