import React, { useState } from 'react'
import axios from 'axios'
import Header from '../components/Header'
import Cookies from 'js-cookie'
import Spinner from '../components/Spinner'
import Toast from '../components/Toast'

const Home: React.FC = () => {
    const [file, setFile] = useState<File | null>(null)
    const [link, setLink] = useState('')
    const [alias, setAlias] = useState('')
    const [password, setPassword] = useState('')
    const [isConfidential, setIsConfidential] = useState(false)
    const [loading, setLoading] = useState(false)
    const [loadingMessage, setLoadingMessage] = useState('')
    const [toastMessage, setToastMessage] = useState('')
    const [toastType, setToastType] = useState<'success' | 'error' | 'info'>('info')

    const token = Cookies.get('token')

    // Handle file upload
    const handleFileUpload = async (e: React.FormEvent) => {
        e.preventDefault()
        if (file && alias.trim()) {
            const formData = new FormData()
            formData.append('file', file)
            formData.append('alias', alias)
            formData.append('is_confidential', String(isConfidential))
            if (isConfidential && password) {
                formData.append('password', password)
            }

            if (isConfidential && password.length < 8) {
                setToastMessage("Password must be at least 8 characters.")
                setToastType("error")
                return
            }

            setLoading(true)
            setLoadingMessage('We will notify you once uploading and processing is complete.')
            console.log(isConfidential)
            try {
                const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/file`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        Authorization: `Bearer ${token}`,
                    },
                })
                console.log('File uploaded:', response.data)
                // Reset the form after successful upload
                resetForm()
            } catch (error) {
                console.error('File upload failed:', error)
                setToastMessage('File upload failed. Please try again.')
                setToastType('error')
            } finally {
                setLoading(false)
                setLoadingMessage('')
            }
        }
    }

    // Handle link upload
    const handleLinkUpload = async (e: React.FormEvent) => {
        e.preventDefault()
        if (link.trim() && alias.trim()) {
            const payload = {
                filelink: link,
                alias,
                is_confidential: isConfidential ? "yes" : "no",
                ...(isConfidential && password ? { password } : {}),
            }

            if (isConfidential && password.length < 8) {
                setToastMessage("Password must be at least 8 characters.")
                setToastType("error")
                return
            }

            setLoading(true)
            setLoadingMessage('We will notify you once uploading and processing is complete.')
            try {
                const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/link`, payload, {
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                })
                console.log('Link uploaded:', response.data)
                // Reset the form after successful upload
                resetForm()
            } catch (error) {
                console.error('Link upload failed:', error)
                setToastMessage('Link upload failed. Please try again.')
                setToastType('error')
            } finally {
                setLoading(false)
                setLoadingMessage('')
            }
        }
    }

    // Reset the form fields after successful submission
    const resetForm = () => {
        setFile(null)
        setLink('')
        setAlias('')
        setPassword('')
        setIsConfidential(false)
    }

    return (
        <>
            <Header />

            {toastMessage && (
                <Toast
                    message={toastMessage}
                    type={toastType}
                    onClose={() => setToastMessage('')}
                />
            )}

            {loading && <Spinner message={loadingMessage} />}

            <div className="w-full max-w-xl mx-auto mt-8 p-6 bg-white rounded-2xl shadow-lg">
                {/* File Upload Form */}
                <form onSubmit={handleFileUpload} className="mb-8">
                    <h2 className="text-lg font-semibold text-gray-800 mb-4">Upload a File</h2>
                    <input
                        type="file"
                        accept=".pdf,.doc,.docx,.txt,.mp3,.mp4,.wav,.m4a"
                        onChange={(e) => setFile(e.target.files?.[0] || null)}
                        className="mb-3 w-full text-sm"
                        required
                    />
                    <input
                        type="text"
                        placeholder="Alias (e.g., Meeting Notes)"
                        value={alias}
                        onChange={(e) => setAlias(e.target.value)}
                        className="w-full p-2 border border-gray-300 rounded mb-3"
                        required
                    />

                    {/* Confidential Option Dropdown */}
                    <div className="mb-3">
                        <label htmlFor="confidentialFile" className="block text-sm text-gray-700 mb-2">
                            Confidential
                        </label>
                        <select
                            id="confidentialFile"
                            value={isConfidential ? "yes" : "no"}  // Set value based on isConfidential state
                            onChange={(e) => setIsConfidential(e.target.value === "yes")}  // Update state based on selected value
                            className="w-full p-2 border border-gray-300 rounded"
                        >
                            <option value="no">No</option>
                            <option value="yes">Yes</option>
                        </select>
                    </div>

                    {/* If confidential, show password input */}
                    {isConfidential && (
                        <input
                            type="password"
                            placeholder="Password for access"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded mb-3"
                            required
                        />
                    )}
                    <button
                        type="submit"
                        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
                    >
                        Upload File
                    </button>
                </form>

                {/* Link Upload Form */}
                <form onSubmit={handleLinkUpload}>
                    <h2 className="text-lg font-semibold text-gray-800 mb-4">Upload via Link</h2>
                    <input
                        type="url"
                        placeholder="File URL"
                        value={link}
                        onChange={(e) => setLink(e.target.value)}
                        className="w-full p-2 border border-gray-300 rounded mb-3"
                        required
                    />
                    <input
                        type="text"
                        placeholder="Alias (e.g., Lecture Recording)"
                        value={alias}
                        onChange={(e) => setAlias(e.target.value)}
                        className="w-full p-2 border border-gray-300 rounded mb-3"
                        required
                    />

                    {/* Confidential Option Dropdown */}
                    <div className="mb-3">
                        <label htmlFor="confidentialLink" className="block text-sm text-gray-700 mb-2">
                            Confidential
                        </label>
                        <select
                            id="confidentialLink"
                            value={isConfidential ? "yes" : "no"}  // Set value based on isConfidential state
                            onChange={(e) => setIsConfidential(e.target.value === "yes")}  // Update state based on selected value
                            className="w-full p-2 border border-gray-300 rounded"
                        >
                            <option value="no">No</option>
                            <option value="yes">Yes</option>
                        </select>
                    </div>

                    {/* If confidential, show password input */}
                    {isConfidential && (
                        <input
                            type="password"
                            placeholder="Password for access"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded mb-3"
                            required
                        />
                    )}
                    <button
                        type="submit"
                        className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition"
                    >
                        Upload Link
                    </button>
                </form>
            </div>
        </>
    )
}

export default Home
