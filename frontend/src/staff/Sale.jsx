import { useState } from 'react'
import { api } from '../api'
import useFetch from '../customer/useFetch'
import Scanner from './Scanner'
import './Staff.css'

const cents = (price) => Math.round(price * 100)
const money = (c) => (c / 100).toFixed(2)

function Sale() {
  const [member, setMember] = useState(null)
  const [qty, setQty] = useState({}) // product id -> quantity
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const products = useFetch('/products', true)

  async function lookup(code) {
    setError(null)
    try {
      setMember(await api(`/members/${encodeURIComponent(code)}`, { staff: true }))
    } catch (e) {
      setError(e.message)
    }
  }

  function reset() {
    setMember(null)
    setQty({})
    setResult(null)
    setError(null)
  }

  const lines = (products.data || []).filter((p) => qty[p.id] > 0)
  const total = lines.reduce((sum, p) => sum + cents(p.price) * qty[p.id], 0)

  async function confirm() {
    setError(null)
    try {
      const items = lines.map((p) => ({ product_id: p.id, qty: qty[p.id] }))
      setResult(await api('/sales', { method: 'POST', staff: true, body: { member_code: member.code, items } }))
    } catch (e) {
      setError(e.message)
    }
  }

  if (result) {
    return (
      <div className="page center">
        <h1>Sale done</h1>
        <div className="big">+{result.points_awarded}</div>
        <p className="muted">points for {result.member_name}</p>
        <p>Total ${money(cents(result.total))} · balance {result.balance} pts</p>
        <button className="btn" onClick={reset}>New sale</button>
      </div>
    )
  }

  if (!member) {
    return (
      <div className="page">
        <h1>New sale</h1>
        <p className="muted">Scan the customer's member QR.</p>
        <Scanner onCode={lookup} placeholder="Member code" />
        {error && <p className="error">{error}</p>}
      </div>
    )
  }

  return (
    <div className="page">
      <div className="card row">
        <div>
          <strong>{member.name}</strong>
          <div className="muted">{member.code} · {member.balance} pts</div>
        </div>
        <button className="btn small ghost" onClick={reset}>Change</button>
      </div>
      {products.error && <p className="error">{products.error}</p>}
      {(products.data || []).map((p) => (
        <div className="card row" key={p.id}>
          <div>
            <strong>{p.name}</strong>
            <div className="muted">${money(cents(p.price))}</div>
          </div>
          <div className="stepper">
            <button aria-label={`Remove ${p.name}`} disabled={!qty[p.id]}
                    onClick={() => setQty((q) => ({ ...q, [p.id]: q[p.id] - 1 }))}>−</button>
            <span>{qty[p.id] || 0}</span>
            <button aria-label={`Add ${p.name}`}
                    onClick={() => setQty((q) => ({ ...q, [p.id]: (q[p.id] || 0) + 1 }))}>+</button>
          </div>
        </div>
      ))}
      {error && <p className="error">{error}</p>}
      <div className="checkout">
        <strong>Total ${money(total)}</strong>
        <button className="btn" disabled={total === 0} onClick={confirm}>Confirm sale</button>
      </div>
    </div>
  )
}

export default Sale
