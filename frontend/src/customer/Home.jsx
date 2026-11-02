import Qr from '../Qr'
import useFetch from './useFetch'
import './Home.css'

function Home() {
  const { data: me, error } = useFetch('/me')
  if (error) return <p className="error">{error}</p>
  if (!me) return <p className="muted">Loading…</p>
  return (
    <div className="home">
      <p className="muted">Hi {me.name}</p>
      <div className="balance">{me.balance}</div>
      <p className="muted">points</p>
      <div className="card home-qr">
        <Qr text={me.code} />
        <p className="member-code">{me.code}</p>
        <p className="muted">Show this to staff when you pay</p>
      </div>
    </div>
  )
}

export default Home
