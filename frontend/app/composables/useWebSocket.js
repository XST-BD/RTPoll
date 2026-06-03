export const useWebSocket = (urlRef, options = {}) => {
    const {
        onMessage = () => { },
        onError = () => { },
        maxRetries = 10,
        baseDelay = 1000,
        maxDelay = 16000,
    } = options

    const status = ref('closed')
    let socket = null
    let retryCount = 0
    let retryTimer = null
    let intentionallyClosed = false

    function connect() {
        if (intentionallyClosed) return

        const url = typeof urlRef === 'function' ? urlRef() : unref(urlRef)
        if (!url) return

        cleanup()
        status.value = 'connecting'

        socket = new WebSocket(url)

        socket.onopen = () => {
            status.value = 'open'
            retryCount = 0
        }

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data)
                onMessage(data)
            } catch {
                onMessage(event.data)
            }
        }

        socket.onerror = () => {
            status.value = 'error'
            onError()
        }

        socket.onclose = () => {
            if (intentionallyClosed) {
                status.value = 'closed'
                return
            }
            status.value = 'closed'
            scheduleReconnect()
        }
    }

    function scheduleReconnect() {
        if (intentionallyClosed || retryCount >= maxRetries) return

        const delay = Math.min(baseDelay * Math.pow(2, retryCount), maxDelay)
        retryCount++

        retryTimer = setTimeout(() => {
            connect()
        }, delay)
    }

    function send(data) {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(typeof data === 'string' ? data : JSON.stringify(data))
            return true
        }
        return false
    }

    function cleanup() {
        if (retryTimer) {
            clearTimeout(retryTimer)
            retryTimer = null
        }
        if (socket) {
            socket.onopen = null
            socket.onmessage = null
            socket.onerror = null
            socket.onclose = null
            socket.close()
            socket = null
        }
    }

    function close() {
        intentionallyClosed = true
        cleanup()
        status.value = 'closed'
    }

    onBeforeUnmount(() => {
        close()
    })

    return { status, connect, send, close }
}
