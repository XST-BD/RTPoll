import { defineStore } from 'pinia'
import FingerprintJS from '@fingerprintjs/fingerprintjs'

export const usePollStore = defineStore('poll', () => {
    const { public: { wsBase } } = useRuntimeConfig()
    const { showPopup } = usePopup()

    const poll = ref(null)
    const notice = ref(null)
    const error = ref(null)
    const loading = ref(true)
    const selectedOption = ref(null)

    let socket = null
    let cachedVisitorId = null

    async function getVisitorId() {
        if (cachedVisitorId) return cachedVisitorId

        const fp = await FingerprintJS.load()
        const result = await fp.get()
        cachedVisitorId = result.visitorId
        
        return cachedVisitorId
    }

    function closeWS() {
        if (socket) {
            socket.onclose = null
            socket.close()
            socket = null
        }
    }

    async function vote(optionId) {
        selectedOption.value = optionId

        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(
                JSON.stringify({
                    type: 'send_vote',
                    option_id: optionId,
                })
            )
            showPopup('Vote submitted successfully.', 'success')
        }
    }

    async function connectWS(pollId) {
        closeWS()
        const visitorId = await getVisitorId()

        socket = new WebSocket(`${wsBase}/${pollId}?fp=${visitorId}`)

        socket.onopen = () => {
            socket.send(JSON.stringify({ type: 'get_vote' }))
        }

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data)

            if (data.type === 'error') {
                error.value = data?.message || 'Failed to load poll. Please reload the page and try again.'
                notice.value = null
                poll.value = null
            } else if (data.type === 'notice') {
                error.value = null
                notice.value = data?.message
                poll.value = null
            } else {
                error.value = null
                notice.value = null
                poll.value = data
            }
            loading.value = false
        }

        socket.onerror = () => {
            error.value = 'Failed to load poll. Please reload the page and try again.'
            notice.value = null
            poll.value = null
            loading.value = false
        }

        socket.onclose = () => {
            error.value = 'Failed to load poll. Please reload the page and try again.'
            notice.value = null
            poll.value = null
            loading.value = false
        }
    }

    async function init(pollId) {
        loading.value = true
        await connectWS(pollId)
    }

    function destroy() {
        closeWS()
    }

    return {
        poll,
        notice,
        error,
        loading,
        selectedOption,

        init,
        vote,
        destroy,

        getVisitorId,
    }
})