import { useNavigate } from 'react-router-dom'

interface DocumentCardProps {
  alias: string
  fileType: string
  createdAt: string
  id: string
}

const DocumentCard: React.FC<DocumentCardProps> = ({ alias, fileType, createdAt, id }) => {
  const navigate = useNavigate()

  return (
    <div className="p-4 bg-white shadow-md rounded-lg space-y-4">
      <div className="font-semibold text-lg">{alias}</div>
      <div className="text-sm text-gray-600">{fileType}</div>
      <div className="text-xs text-gray-400">Uploaded on {createdAt}</div>
      
      <div className="space-x-4">
        <button
          onClick={() => navigate(`/chats/${id}`)}
          className="bg-indigo-500 text-white px-4 py-2 rounded-lg hover:bg-indigo-600"
        >
          Go to Q&A
        </button>
        <button
          onClick={() => alert('Document deleted!')}
          className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600"
        >
          Delete
        </button>
      </div>
    </div>
  )
}

export default DocumentCard
