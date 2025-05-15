// src/pages/Logout.tsx
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Cookies from 'js-cookie'

const Logout = () => {
  const navigate = useNavigate()

  useEffect(() => {
    Cookies.remove('token')
    Cookies.remove('user')
    navigate('/login')
  }, [navigate])

  return null
}

export default Logout
