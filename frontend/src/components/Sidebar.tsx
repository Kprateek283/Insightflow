import { useNavigate } from 'react-router-dom'

const Sidebar = () => {
  const navigate = useNavigate()

  return (
    <div className="w-64 h-screen bg-white shadow-md p-4">
      <div className="space-y-6">
        <button
          onClick={() => navigate('/home')}
          className="block w-full text-left py-2 px-4 text-gray-700 hover:bg-indigo-100 rounded-lg"
        >
          Home
        </button>
        <button
          onClick={() => navigate('/profile')}
          className="block w-full text-left py-2 px-4 text-gray-700 hover:bg-indigo-100 rounded-lg"
        >
          Profile
        </button>
        <button
          onClick={() => navigate('/myuploads')}
          className="block w-full text-left py-2 px-4 text-gray-700 hover:bg-indigo-100 rounded-lg"
        >
          My Uploads
        </button>
        <button
          onClick={() => {
            // Handle logout here
            navigate('/')
          }}
          className="block w-full text-left py-2 px-4 text-gray-700 hover:bg-indigo-100 rounded-lg"
        >
          Logout
        </button>
      </div>
    </div>
  )
}

export default Sidebar
