<script setup>
const { popups } = usePopup()
</script>

<template>
    <TransitionGroup name="toast" tag="div" class="fixed top-10 right-6 flex flex-col gap-3 z-50">
        <div v-for="popup in popups" :key="popup.id" class="w-[280px] px-4 py-3 rounded-lg shadow-lg border-2 font-medium" :class="popup.type === 'success' ? 'bg-green-50 text-green-500 border-green-500' : 'bg-red-50 text-red-500 border-red-500'">
            {{ popup.message }}
        </div>
    </TransitionGroup>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s ease;
}

.toast-enter-from {
    opacity: 0;
    transform: translateX(40px);
}

.toast-leave-to {
    opacity: 0;
    transform: translateX(40px);
}

.toast-move {
    transition: transform 0.3s ease;
}
</style>