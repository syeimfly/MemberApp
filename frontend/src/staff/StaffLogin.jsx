import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, setStaffKey } from '../api'
import '../customer/Login.css'

function StaffLogin() {
  const navigate = useNavigate()
  const [key, setKey] = useState('')
  const [error, setError] = useState(null)

  async function submit(e) {
    e.preventDefault()
    setStaffKey(key)
    try {
      await api('/products', { staff: true }) // any staff route proves the key works
      navigate('/staff', { replace: true })
    } catch (err) {
      setStaffKey(null)
      setError(err.message)
    }
  }

  return (
    <form className="login" onSubmit={submit}>
      <h1>Staff</h1>
      <p>Enter the shared staff key.</p>
      <input className="input" type="password" value={key} autoFocus
             onChange={(e) => setKey(e.target.value)} />
      <div><button className="btn" disabled={!key}>Log in</button></div>
      {error && <p className="error">{error}</p>}
    </form>
  )
}

export default StaffLogin
