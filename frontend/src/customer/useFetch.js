import { useEffect, useState } from 'react'
import { api } from '../api'

// Returns { data, error } for a GET; data stays null until it loads.
export default function useFetch(path, staff = false) {
  const [state, setState] = useState({ data: null, error: null })
  useEffect(() => {
    api(path, { staff }).then(
      (data) => setState({ data, error: null }),
      (e) => setState({ data: null, error: e.message }),
    )
  }, [path, staff])
  return state
}
