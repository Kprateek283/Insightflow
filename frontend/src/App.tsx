import './index.css'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'

// Import all pages
import ProtectedRoute from './components/ProtectedRoute'
import Login from './pages/Login'
import Signup from './pages/Signup'
import GetStarted from './pages/GetStarted'
import Home from './pages/Home'
import Profile from './pages/Profile'
import MyUploads from './pages/MyUploads'
import Chats from './pages/Chats'
import Logout from './pages/Logout'

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/getStarted" element={<GetStarted />} />

        {/* Protected Routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/myUploads" element={<MyUploads />} />
          <Route path="/chats/:documentId" element={<Chats/>} />
          <Route path="/logout" element={<Logout />} />
        </Route>

        {/* Catch-all route */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  )
}

export default App
