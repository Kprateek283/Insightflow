import React, { useEffect } from 'react'

interface ToastProps {
  type?: 'success' | 'error' | 'info'
  message: string
  onClose: () => void
  duration?: number 
}

const Toast: React.FC<ToastProps> = ({ type = 'info', message, onClose, duration = 2000 }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose()
    }, duration)

    return () => clearTimeout(timer)
  }, [onClose, duration])

  const getBackgroundColor = () => {
    switch (type) {
      case 'success': return 'bg-green-100 text-green-800 border-green-300'
      case 'error': return 'bg-red-100 text-red-800 border-red-300'
      default: return 'bg-blue-100 text-blue-800 border-blue-300'
    }
  }

  return (
    <div className={`fixed top-4 right-4 px-4 py-2 border rounded-xl shadow-md z-50 ${getBackgroundColor()}`}>
      <p className="text-sm">{message}</p>
    </div>
  )
}

export default Toast
