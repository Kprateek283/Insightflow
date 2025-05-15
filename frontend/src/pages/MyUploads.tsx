// src/pages/MyUploads.tsx
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import Header from '../components/Header'
import Spinner from '../components/Spinner' // ✅ Import Spinner
import Cookies from 'js-cookie'
import { toast } from 'react-toastify'

interface Document {
  id: string
  alias: string
  filetype: string
  created_at: string
}

const MyUploads = () => {
  const navigate = useNavigate()
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const limit = 5

  const token = Cookies.get('token')

  const fetchDocuments = async (currentPage: number) => {
    setLoading(true)
    try {
      const skip = (currentPage - 1) * limit
      const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/documents?skip=${skip}&limit=${limit}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      setDocuments(response.data)
    } catch (error) {
      console.error('Failed to fetch documents:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDocuments(page)
  }, [page])

  const handleDelete = async (id: string) => {
    try {
      // Send delete request to backend
      const response = await axios.delete(`${import.meta.env.VITE_API_BASE_URL}/documents/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      
      // Show success toast
      toast.success(response.data.message || 'Document deleted successfully.')
  
      // Auto-refresh the documents by re-fetching them
      fetchDocuments(page)
    } catch (error) {
      // Show error toast
      toast.error("Failed to delete document.")
      console.error("Failed to delete document:", error)
    }
  }
  

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gray-50">
        <main className="p-4">
          <h2 className="text-2xl font-bold text-gray-700 mb-6">My Uploads</h2>

          {loading ? (
            <Spinner message="Loading documents..." /> // ✅ Spinner here
          ) : (
            <>
              {documents.length > 0 ? (
                documents.map((doc) => (
                  <div
                    key={doc.id}
                    className="border border-gray-300 p-4 mb-4 rounded-lg shadow-sm"
                  >
                    <p><strong>Alias:</strong> {doc.alias}</p>
                    <p><strong>File Type:</strong> {doc.filetype}</p>
                    <p><strong>Created At:</strong> {new Date(doc.created_at).toLocaleDateString()}</p>
                    <div className="flex space-x-4 mt-4">
                      <button
                        onClick={() => navigate(`/chats/${doc.id}`)}
                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                      >
                        Go to Q&A
                      </button>
                      <button
                        onClick={() => handleDelete(doc.id)}
                        className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-500">No documents found.</p>
              )}

              {/* Pagination Controls */}
              <div className="flex justify-center space-x-4 mt-8">
                <button
                  onClick={() => setPage(page - 1)}
                  disabled={page === 1}
                  className="bg-gray-300 px-4 py-2 rounded hover:bg-gray-400 disabled:opacity-50"
                >
                  Previous
                </button>
                <span className="px-4 py-2">Page {page}</span>
                <button
                  onClick={() => setPage(page + 1)}
                  disabled={documents.length < limit}
                  className="bg-gray-300 px-4 py-2 rounded hover:bg-gray-400 disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            </>
          )}
        </main>
      </div>
    </>
  )
}

export default MyUploads
