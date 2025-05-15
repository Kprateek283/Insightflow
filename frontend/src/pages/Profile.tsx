// src/pages/Profile.tsx
import { useEffect, useState } from 'react'
import axios from 'axios'
import Header from '../components/Header'
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'
import Cookies from 'js-cookie'
import Spinner from '../components/Spinner' // ✅ import Spinner

const COLORS = ['#4F46E5', '#34D399', '#F59E0B'] // Add 3rd color for video

const Profile = () => {
  const [profile, setProfile] = useState<any>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const token = Cookies.get('token')

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/profile`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        setProfile(response.data)
      } catch (error) {
        console.error('Failed to load profile:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchProfile()
  }, [])

  const data = profile ? [
    { name: 'Documents', value: profile.total_documents },
    { name: 'Audio', value: profile.total_audio },
    { name: 'Video', value: profile.total_video },
  ] : []

  return (
    <>
      {console.log(profile)}
      <Header />
      <div className="p-6 max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold mb-4">Profile</h2>
        {loading ? (
          <Spinner message="Loading profile..." />
        ) : profile ? (
          <>
            <p><strong>Name:</strong> {profile.name}</p>
            <p><strong>Email:</strong> {profile.email}</p>
            <p><strong>Total Q&A:</strong> {profile.total_qna}</p>
            <p><strong>Total Uploads:</strong> {profile.total_uploads}</p>

            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-2">Upload Breakdown</h3>
              <PieChart width={320} height={240}>
                <Pie
                  dataKey="value"
                  isAnimationActive
                  data={data}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  fill="#8884d8"
                  label
                >
                  {data.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </div>
          </>
        ) : (
          <p className="text-red-500">Failed to load profile.</p>
        )}
      </div>
    </>
  )
}

export default Profile

