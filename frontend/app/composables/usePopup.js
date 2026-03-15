export const usePopup = () => {
    const popups = useState("popups", () => [])

    function showPopup(message, type = "success") {
        const id = Date.now() + Math.random()

        popups.value.unshift({ id, message, type })

        setTimeout(() => {
            popups.value = popups.value.filter(p => p.id !== id)
        }, 4000)
    }

    return { popups, showPopup }
}