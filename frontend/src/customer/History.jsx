import useFetch from './useFetch'

function History() {
  const { data, error } = useFetch('/me/history')
  if (error) return <p className="error">{error}</p>
  if (!data) return <p className="muted">Loading…</p>
  return (
    <div className="page">
      <h1>History</h1>
      {data.length === 0 && <p className="muted">Nothing yet.</p>}
      {data.map((e) => (
        <div className="card row" key={`${e.kind}-${e.created_at}`}>
          <div>
            <strong>{e.label}</strong>
            <div className="muted">{new Date(e.created_at).toLocaleString()}</div>
          </div>
          <span className={e.points > 0 ? 'earned' : 'spent'}>
            {e.points > 0 ? '+' : ''}{e.points}
          </span>
        </div>
      ))}
    </div>
  )
}

export default History
