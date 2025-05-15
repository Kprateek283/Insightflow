// src/components/ProtectedRoute.tsx
import { useEffect} from 'react'
import {Outlet } from 'react-router-dom'
import Cookies from 'js-cookie'
import { useToast } from '../context/ToastContext'

const ProtectedRoute = () => {
  const token = Cookies.get('token')
  const { showToast } = useToast()

  useEffect(() => {
    if (!token) {
      showToast('You need to log in first', 'error')
        window.location.href = '/login'
    }
  }, [token, showToast])


  return <Outlet />
}

export default ProtectedRoute
