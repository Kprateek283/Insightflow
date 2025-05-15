import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const Signup = () => {
  const navigate = useNavigate()

  // State for form inputs
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  const handleSignup = async () => {
    setError(null) // clear error if any
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/signup`, {
        name,
        email,
        password
      })

      const data = response.data

      if (response.status < 200 || response.status >= 300) {
        throw new Error(data.detail || 'Signup failed')
      }

      // Redirect to home on success
      navigate('/home')
    } catch (err: any) {
      setError(err.message)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {/* Header */}
      <div className="w-full flex justify-between p-4 bg-white shadow-md">
        <div className="font-bold text-xl text-gray-700">AI Q&A Tool</div>
      </div>

      {/* Form */}
      <div className="w-full max-w-sm p-6 bg-white shadow-lg rounded-lg space-y-6">
        <h2 className="text-2xl font-bold text-center text-gray-700">Sign Up</h2>

        {error && <p className="text-red-500 text-sm text-center">{error}</p>}

        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-md"
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-md"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-md"
        />
        <button
          onClick={handleSignup}
          className="w-full bg-green-500 text-white py-3 rounded-md hover:bg-green-600"
        >
          Sign Up
        </button>
        <div className="text-center text-gray-600">
          Already have an account?{' '}
          <button
            onClick={() => navigate('/login')}
            className="text-blue-500 hover:underline"
          >
            Login
          </button>
        </div>
      </div>
    </div>
  )
}

export default Signup
