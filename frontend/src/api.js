export const API_BASE = 'http://localhost:8002'

function read(key) {
  try { return localStorage.getItem(key) } catch { return null }
}

function write(key, value) {
  try {
    if (value) localStorage.setItem(key, value)
    else localStorage.removeItem(key)
  } catch { /* storage blocked: user just has to log in again */ }
}

export const getToken = () => read('token')
export const setToken = (token) => write('token', token)
export const getStaffKey = () => read('staffKey')
export const setStaffKey = (key) => write('staffKey', key)

// staff: true sends the shared staff key instead of the customer JWT.
export async function api(path, { method = 'GET', body, staff = false } = {}) {
  const credential = staff ? getStaffKey() : getToken()
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      ...(body && { 'Content-Type': 'application/json' }),
      ...(credential && (staff
        ? { 'X-Staff-Key': credential }
        : { Authorization: `Bearer ${credential}` })),
    },
    body: body && JSON.stringify(body),
  })
  // On a login page the 401 is the answer to a login attempt, not an expired session.
  if (res.status === 401 && !window.location.pathname.endsWith('/login')) {
    if (staff) setStaffKey(null)
    else setToken(null)
    window.location.assign(staff ? '/staff/login' : '/login')
  }
  const data = await res.json().catch(() => null)
  if (!res.ok) throw new Error(data?.detail || `Request failed (${res.status})`)
  return data
}
