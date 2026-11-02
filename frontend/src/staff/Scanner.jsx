import { useEffect, useRef, useState } from 'react'
import { Html5Qrcode } from 'html5-qrcode'

const READER_ID = 'qr-reader'

// Camera scan with a type-the-code fallback (works without camera access or on desktop).
function Scanner({ onCode, placeholder = 'Type the code' }) {
  const [scanning, setScanning] = useState(false)
  const [typed, setTyped] = useState('')
  const [error, setError] = useState(null)
  const scanner = useRef(null)

  useEffect(() => {
    if (!scanning) return undefined
    const instance = new Html5Qrcode(READER_ID)
    scanner.current = instance
    instance
      .start({ facingMode: 'environment' }, { fps: 10, qrbox: 220 }, (text) => {
        setScanning(false)
        onCode(text)
      })
      .catch((e) => {
        setScanning(false)
        setError(`Camera unavailable: ${e}`)
      })
    return () => {
      // stop() rejects if start() never finished; nothing to clean up then
      instance.stop().then(() => instance.clear()).catch(() => {})
    }
  }, [scanning, onCode])

  function submit(e) {
    e.preventDefault()
    if (typed.trim()) onCode(typed.trim())
  }

  return (
    <div className="scanner">
      {scanning && <div id={READER_ID} className="reader" />}
      <button className="btn" type="button" onClick={() => { setError(null); setScanning(!scanning) }}>
        {scanning ? 'Stop camera' : 'Scan QR code'}
      </button>
      <form className="row typed" onSubmit={submit}>
        <input className="input" value={typed} placeholder={placeholder}
               onChange={(e) => setTyped(e.target.value)} />
        <button className="btn small" disabled={!typed.trim()}>OK</button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  )
}

export default Scanner
