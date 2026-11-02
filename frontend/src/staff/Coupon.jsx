import { useState } from 'react'
import { api } from '../api'
import Scanner from './Scanner'
import './Staff.css'

function Coupon() {
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  async function redeem(code) {
    setError(null)
    setResult(null)
    try {
      setResult(await api(`/coupons/${encodeURIComponent(code)}/redeem`, { method: 'POST', staff: true }))
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div className="page">
      <h1>Validate coupon</h1>
      <p className="muted">Scan the customer's coupon. It can only be used once.</p>
      <Scanner onCode={redeem} placeholder="Coupon code" />
      {error && <p className="error">{error}</p>}
      {result && (
        <div className="card ok">
          <strong>✓ {result.reward_name}</strong>
          <div className="muted">for {result.member_name} · {result.code}</div>
        </div>
      )}
    </div>
  )
}

export default Coupon
