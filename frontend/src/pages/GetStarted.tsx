import { useNavigate } from 'react-router-dom'

const GetStartedPage = () => {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {/* Header */}
      <div className="w-full flex justify-end p-4 space-x-4">
        <button
          onClick={() => navigate('/login')}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Login
        </button>
        <button
          onClick={() => navigate('/signup')}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        >
          Signup
        </button>
      </div>

      {/* Center Content */}
      <div className="text-center p-4 space-y-4">
        <img src="https://via.placeholder.com/200" alt="placeholder" className="mx-auto" />
        <h2 className="text-2xl font-bold text-gray-700">Welcome to the AI-based Q&A Tool</h2>
        <p className="text-lg text-gray-600">
          This tool allows you to upload documents, audio, or video and ask questions based on the content.
        </p>
        <button
          onClick={() => navigate('/signup')}
          className="bg-indigo-500 text-white px-6 py-2 rounded hover:bg-indigo-600"
        >
          Get Started
        </button>
      </div>
    </div>
  )
}

export default GetStartedPage
