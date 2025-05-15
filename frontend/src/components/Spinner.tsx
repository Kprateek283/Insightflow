import React from 'react'

interface SpinnerProps {
  message?: string
}

const Spinner: React.FC<SpinnerProps> = ({ message }) => {
  return (
    <div className="flex flex-col items-center justify-center py-6">
      <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
      {message && <p className="mt-3 text-gray-700 text-sm">{message}</p>}
    </div>
  )
}

export default Spinner
