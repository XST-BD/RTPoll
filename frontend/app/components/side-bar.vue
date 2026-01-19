<template>
    <aside class="flex flex-col gap-3 p-2 border-r">
        <nav class="flex flex-col gap-3">
            <router-link to="/dashboard" title="Home" class="p-2 flex items-center gap-2 rounded-md text-sm text-green-400 transition duration-200 hover:bg-green-100 hover:text-green-500 active:scale-90 active:text-green-500">
                <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24">
                    <path fill="#4ade80" d="M11.336 2.253a1 1 0 0 1 1.328 0l9 8a1 1 0 0 1-1.328 1.494L20 11.45V19a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-7.55l-.336.297a1 1 0 0 1-1.328-1.494zM6 9.67V19h3v-5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v5h3V9.671l-6-5.333zM13 19v-4h-2v4z" />
                </svg>
            </router-link>

            <router-link to="/dashboard/create" title="Create Poll" class="p-2 flex items-center gap-2 rounded-md text-sm text-green-400 transition duration-200 hover:bg-green-100 hover:text-green-500 active:scale-90">
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 21 21">
                    <g fill="none" fill-rule="evenodd" stroke="#4ADE80" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.7">
                        <path d="M10 4.5H5.5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V11" />
                        <path d="M17.5 3.467a1.46 1.46 0 0 1-.017 2.05L10.5 12.5l-3 1l1-3l6.987-7.046a1.41 1.41 0 0 1 1.885-.104zm-2 2.033l.953 1" />
                    </g>
                </svg>
            </router-link>

            <router-link to="/dashboard/overview" title="Overview" class="p-2 flex items-center gap-2 rounded-md text-sm text-green-400 transition duration-200 hover:bg-green-100 hover:text-green-500 active:scale-90">
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24">
                    <g fill="none" stroke="#4ADE80" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                        <path d="M3.5 4v13.5a3 3 0 0 0 3 3H20" />
                        <path d="m6.5 15l4.5-4.5l3.5 3.5L20 8.5" />
                    </g>
                </svg>
            </router-link>
        </nav>
    </aside>
</template>