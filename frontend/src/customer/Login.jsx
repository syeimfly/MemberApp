import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, setToken } from '../api'
import './Login.css'

const POLL_MS = 2000

function Login() {
  const navigate = useNavigate()
  const [link, setLink] = useState(null)
  const [error, setError] = useState(null)
  const timer = useRef(null)

  useEffect(() => () => clearTimeout(timer.current), [])

  function poll(nonce) {
    timer.current = setTimeout(async () => {
      try {
        const res = await api('/auth/verify', { method: 'POST', body: { nonce } })
        if (res.status === 'ok') {
          setToken(res.token)
          navigate('/', { replace: true })
        } else poll(nonce)
      } catch (e) {
        setLink(null)
        setError(e.message)
      }
    }, POLL_MS)
  }

  async function start() {
    setError(null)
    try {
      const res = await api('/auth/start', { method: 'POST' })
      setLink(res.link)
      poll(res.nonce)
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div className="login">
      <h1>MemberApp</h1>
      <p>Sign in with Telegram. No password needed.</p>
      {link ? (
        <>
          <a className="btn" href={link} target="_blank" rel="noreferrer">Open Telegram</a>
          <p className="muted">Press Start in the chat. This page continues on its own.</p>
        </>
      ) : (
        <button className="btn" onClick={start}>Log in with Telegram</button>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  )
}

export default Login
