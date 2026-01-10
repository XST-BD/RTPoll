<template>
    <aside class="flex flex-col gap-3 p-2 border-r">
        <nav class="flex flex-col gap-3">
            <router-link to="/" title="Home" class="p-2 flex items-center gap-2 rounded-md text-sm text-green-400 transition duration-200 hover:bg-green-100 hover:text-green-500 active:scale-90 active:text-green-500">
                <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24">
                    <path fill="#4ade80" d="M11.336 2.253a1 1 0 0 1 1.328 0l9 8a1 1 0 0 1-1.328 1.494L20 11.45V19a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-7.55l-.336.297a1 1 0 0 1-1.328-1.494zM6 9.67V19h3v-5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v5h3V9.671l-6-5.333zM13 19v-4h-2v4z" />
                </svg>
            </router-link>

            <router-link to="/create" title="Create Poll" class="p-2 flex items-center gap-2 rounded-md text-sm text-green-400 transition duration-200 hover:bg-green-100 hover:text-green-500 active:scale-90">
                <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 512 512">
                    <path fill="none" stroke="#4ade80" stroke-linecap="round" stroke-linejoin="round" stroke-width="45" d="M384 224v184a40 40 0 0 1-40 40H104a40 40 0 0 1-40-40V168a40 40 0 0 1 40-40h167.48" />
                    <path fill="#4ade80"
                        d="M459.94 53.25a16.06 16.06 0 0 0-23.22-.56L424.35 65a8 8 0 0 0 0 11.31l11.34 11.32a8 8 0 0 0 11.34 0l12.06-12c6.1-6.09 6.67-16.01.85-22.38M399.34 90L218.82 270.2a9 9 0 0 0-2.31 3.93L208.16 299a3.91 3.91 0 0 0 4.86 4.86l24.85-8.35a9 9 0 0 0 3.93-2.31L422 112.66a9 9 0 0 0 0-12.66l-9.95-10a9 9 0 0 0-12.71 0" />
                </svg>
            </router-link>

            <router-link to="/overview" title="Overview" class="p-2 flex items-center gap-2 rounded-md text-sm text-green-400 transition duration-200 hover:bg-green-100 hover:text-green-500 active:scale-90">
                <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24">
                    <path fill="#4ade80"
                        d="M2 3a1 1 0 0 1 2 0v10.365l2.217-1.846l.334-.266c.786-.59 1.61-.966 2.512-.91c1.021.066 1.864.67 2.62 1.426l.007.006l.25.239c.556.499.909.61 1.143.614c.28.004.7-.142 1.413-.766l5.846-5.115a1 1 0 0 1 1.316 1.506l-5.846 5.114c-.818.716-1.716 1.274-2.754 1.26c-.92-.011-1.723-.465-2.467-1.137l-.316-.3l-.006-.007c-.655-.655-1.055-.826-1.332-.843c-.234-.015-.59.067-1.175.505l-.265.21l-3.491 2.908c.006.463.018.849.045 1.182c.05.606.142.954.276 1.217l.115.206c.289.47.702.853 1.196 1.105l.103.049c.251.108.584.184 1.113.227C7.471 20 8.264 20 9.4 20H21l.102.005a1 1 0 0 1 0 1.99L21 22H9.4c-1.103 0-1.991.001-2.709-.058c-.637-.052-1.208-.154-1.737-.381l-.224-.106a5 5 0 0 1-2.092-2.01l-.093-.175c-.302-.593-.428-1.233-.487-1.961a24 24 0 0 1-.053-1.714a1 1 0 0 1-.001-.185Q2 15.026 2 14.6z" />
                </svg>
            </router-link>
        </nav>
    </aside>
</template>