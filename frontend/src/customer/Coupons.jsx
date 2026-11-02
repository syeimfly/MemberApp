import Qr from '../Qr'
import useFetch from './useFetch'

function Coupons() {
  const { data, error } = useFetch('/me/coupons')
  if (error) return <p className="error">{error}</p>
  if (!data) return <p className="muted">Loading…</p>
  return (
    <div className="page">
      <h1>My coupons</h1>
      {data.length === 0 && <p className="muted">No coupons yet. Redeem a reward first.</p>}
      {data.map((c) => (
        <div className={'card coupon' + (c.status === 'redeemed' ? ' used' : '')} key={c.code}>
          <strong>{c.reward_name}</strong>
          {c.status === 'issued' ? (
            <>
              <Qr text={c.code} size={160} />
              <p className="member-code">{c.code}</p>
            </>
          ) : (
            <p className="muted">Used {new Date(c.redeemed_at).toLocaleDateString()}</p>
          )}
        </div>
      ))}
    </div>
  )
}

export default Coupons
