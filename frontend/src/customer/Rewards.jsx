import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'
import useFetch from './useFetch'

function Rewards() {
  const navigate = useNavigate()
  const me = useFetch('/me')
  const rewards = useFetch('/rewards')
  const [error, setError] = useState(null)

  async function redeem(reward) {
    if (!window.confirm(`Spend ${reward.points_cost} points on ${reward.name}?`)) return
    try {
      await api('/me/coupons', { method: 'POST', body: { reward_id: reward.id } })
      navigate('/coupons')
    } catch (e) {
      setError(e.message)
    }
  }

  if (rewards.error || me.error) return <p className="error">{rewards.error || me.error}</p>
  if (!rewards.data || !me.data) return <p className="muted">Loading…</p>
  return (
    <div className="page">
      <h1>Rewards</h1>
      <p className="muted">You have {me.data.balance} points</p>
      {error && <p className="error">{error}</p>}
      {rewards.data.map((r) => (
        <div className="card row" key={r.id}>
          <div>
            <strong>{r.name}</strong>
            <div className="muted">{r.description}</div>
            <div className="cost">{r.points_cost} pts</div>
          </div>
          <button className="btn small" disabled={me.data.balance < r.points_cost} onClick={() => redeem(r)}>
            Redeem
          </button>
        </div>
      ))}
    </div>
  )
}

export default Rewards
