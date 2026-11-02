import { useEffect, useState } from 'react'
import QRCode from 'qrcode'

function Qr({ text, size = 200 }) {
  const [src, setSrc] = useState('')
  useEffect(() => {
    QRCode.toDataURL(text, { margin: 1, width: size }).then(setSrc)
  }, [text, size])
  return src ? <img className="qr" src={src} width={size} height={size} alt={`QR code ${text}`} /> : null
}

export default Qr
