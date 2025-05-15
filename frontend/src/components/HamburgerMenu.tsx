import React from 'react'
import { useNavigate } from 'react-router-dom'

interface HamburgerMenuProps {
  isOpen: boolean
  toggleMenu: () => void
}

const HamburgerMenu: React.FC<HamburgerMenuProps> = ({ isOpen, toggleMenu }) => {
  const navigate = useNavigate()

  const menuButtons = [
    { label: 'Home', onClick: () => navigate('/home') },
    { label: 'Profile', onClick: () => navigate('/profile') },
    { label: 'My Uploads', onClick: () => navigate('/myUploads') },
    { label: 'Logout', onClick: () => navigate('/logout') }
  ]

  return (
    <div className={`fixed top-0 right-0 z-50 bg-gray-800 text-white ${isOpen ? 'block' : 'hidden'} p-4`}>
      <button onClick={toggleMenu} className="text-white text-3xl">&times;</button>
      <div className="space-y-4 mt-6">
        {menuButtons.map((button, index) => (
          <button
            key={index}
            onClick={button.onClick}
            className="w-full text-left px-4 py-2 hover:bg-gray-700 rounded-md"
          >
            {button.label}
          </button>
        ))}
      </div>
    </div>
  )
}

export default HamburgerMenu
