import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import Cookies from 'js-cookie'
import axios from 'axios'

const Login = () => {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = async () => {
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/login`, {
        email,
        password,
      })
      

      const data = response.data

      if (response.status < 200 || response.status >= 300) {
        throw new Error(data.detail || 'Login failed')
      }

      // Save token and user data in cookies
      Cookies.set('token', data.user.token, { expires: 7 }) // token expires in 7 days
      Cookies.set('user', JSON.stringify(data.user), { expires: 7 }) // store user data for 7 days

      // Navigate to home after successful login
      navigate('/home')
    } catch (err) {
      console.error('Login error:', err)
      if (err instanceof Error) {
        alert(err.message)
      } else {
        alert('An unknown error occurred')
      }
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
        <h2 className="text-2xl font-bold text-center text-gray-700">Login</h2>
        <input
          type="email"
          placeholder="Email"
          className="w-full p-3 border border-gray-300 rounded-md"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-3 border border-gray-300 rounded-md"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          onClick={handleLogin}
          className="w-full bg-blue-500 text-white py-3 rounded-md hover:bg-blue-600"
        >
          Login
        </button>
        <div className="text-center text-gray-600">
          Don't have an account?{' '}
          <button
            onClick={() => navigate('/signup')}
            className="text-blue-500 hover:underline"
          >
            Sign up
          </button>
        </div>
      </div>
    </div>
  )
}

export default Login
