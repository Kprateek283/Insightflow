import { useState, useEffect } from "react";
import axios from "axios";
import Spinner from "../components/Spinner";
import Cookies from "js-cookie";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import Header from "../components/Header";

interface QAItem {
  question: string;
  answer: string;
}

interface DocumentDetails {
  alias: string;
  summary: string;
  filetype: string;
  created_at: string;
  transcription?: string;
  is_confidential: string; // changed from boolean to string
}

const token = Cookies.get("token");

const Chats: React.FC = () => {
  const { documentId } = useParams<{ documentId: string }>();
  const [loading, setLoading] = useState(false);
  const [documentDetails, setDocumentDetails] = useState<DocumentDetails | null>(null);
  const [qas, setQas] = useState<QAItem[]>([]);
  const [question, setQuestion] = useState("");
  const [sending, setSending] = useState(false);
  const [showAll, setShowAll] = useState(false);

  const [unlock, setUnlock] = useState(false);
  const [unlockPassword, setUnlockPassword] = useState("");

  const [showSummaryMore, setShowSummaryMore] = useState(false);
  const [showTranscriptionMore, setShowTranscriptionMore] = useState(false);

  const API_BASE = import.meta.env.VITE_API_BASE_URL;

  useEffect(() => {
    const fetchDocumentDetails = async () => {
      try {
        setLoading(true);
        const res = await axios.get(`${API_BASE}/documents/${documentId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setDocumentDetails(res.data);
      } catch (error) {
        console.error("Error fetching document details:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDocumentDetails();
  }, [documentId]);

  const loadAllQAs = async () => {
    try {
      const res = await axios.get(`${API_BASE}/qnaAll?document_id=${documentId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setQas(res.data);
      setShowAll(true);
    } catch (error) {
      console.error("Error loading all QAs:", error);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;

    if (documentDetails?.is_confidential === "yes" && !unlock) {
      toast.warning("Unlock this document to start asking questions.");
      return;
    }

    setSending(true);
    try {
      const res = await axios.post(`${API_BASE}/ask`, {
        document_id: documentId,
        question,
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });

      const latestQA = res.data.qas[res.data.qas.length - 1];
      setQas([...qas, latestQA]);
      setQuestion("");
    } catch (error) {
      console.error("Error asking question:", error);
    } finally {
      setSending(false);
    }
  };

  const handleUnlock = async () => {
    if (!unlockPassword.trim()) {
      toast.error("Please enter a password.");
      return;
    }

    try {
      const headers = { Authorization: `Bearer ${token}` };

      // Send a single request to unlock both summary and transcription
      const res = await axios.post(`${API_BASE}/documents/${documentId}/unlock`, {
        password: unlockPassword,
      }, { headers });

      const { summary, transcription } = res.data; // Get decrypted summary and transcription from the response

      // Set the decrypted text for summary and transcription in the document details
      setDocumentDetails(prev => ({
        ...prev!,
        summary: summary,
        transcription: transcription,
      }));

      setUnlock(true);
      toast.success("Document unlocked successfully!");
    } catch (error) {
      toast.error("Failed to unlock document. Check your password.");
      console.error("Unlock error:", error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full mt-10">
        <Spinner message="Loading your chats" />
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <Header />
      <header className="text-xl font-semibold">Chats</header>


      {/* Unlock Section */}
      {documentDetails?.is_confidential === "yes" && !unlock && (
        <div className="bg-red-50 p-4 rounded-xl border border-red-300 space-y-2">
          <p className="text-red-600 font-medium">This is a confidential document.</p>
          <input
            type="password"
            placeholder="Enter password to unlock"
            className="border p-2 w-full rounded-md"
            value={unlockPassword}
            onChange={(e) => setUnlockPassword(e.target.value)}
          />
          <button
            onClick={handleUnlock}
            className="bg-red-600 text-white px-4 py-2 rounded-md mt-2"
          >
            Unlock Document
          </button>
        </div>
      )}

      {/* Document Details Section */}
      {documentDetails && (
        <div className="space-y-4">
          <div className="bg-gray-100 p-4 rounded-xl shadow-sm">
            <div><strong>Alias:</strong> {documentDetails.alias}</div>
            <div><strong>Created At:</strong> {new Date(documentDetails.created_at).toLocaleString()}</div>
            <div><strong>File Type:</strong> {documentDetails.filetype}</div>

            {documentDetails?.is_confidential == "no" && (
              <div>
                <strong>Summary:</strong>
                <div className={`${!showSummaryMore ? "line-clamp-2" : ""} mt-1`}>
                  {documentDetails.summary}
                </div>
                {documentDetails.summary.length > 100 && (
                  <button
                    className="text-blue-500 text-sm mt-1 hover:underline"
                    onClick={() => setShowSummaryMore(!showSummaryMore)}
                  >
                    {showSummaryMore ? "Show Less" : "Read More"}
                  </button>
                )}
              </div>
            )}


            {documentDetails.transcription && (
              <div>
                <strong>Transcription:</strong>
                <div className={`${!showTranscriptionMore ? "line-clamp-2" : ""} mt-1`}>
                  {documentDetails.transcription}
                </div>
                {documentDetails.transcription.length > 100 && (
                  <button
                    className="text-blue-500 text-sm mt-1 hover:underline"
                    onClick={() => setShowTranscriptionMore(!showTranscriptionMore)}
                  >
                    {showTranscriptionMore ? "Show Less" : "Read More"}
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Q&A Section */}
      <div className="space-y-4">
        {qas.map((qa, index) => (
          <div key={index} className="flex items-start">
            <div className="w-1/2 bg-gray-100 p-3 rounded-2xl shadow-sm">
              <strong>Q:</strong> {qa.question}
            </div>
            <div className="w-1/2 bg-green-100 p-3 rounded-2xl shadow-sm ml-2">
              <strong>A:</strong> {qa.answer}
            </div>
          </div>
        ))}

        {!showAll && (
          <button
            className="text-blue-500 text-sm mt-2 hover:underline"
            onClick={loadAllQAs}
          >
            Show past chats
          </button>
        )}
      </div>

      {/* Ask a Question Section */}
      <div className="flex items-center mt-6">
        <input
          type="text"
          placeholder="Ask a question..."
          className="flex-1 border p-2 rounded-l-xl focus:outline-none"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-r-xl disabled:opacity-50"
          onClick={handleAsk}
          disabled={sending}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chats;
