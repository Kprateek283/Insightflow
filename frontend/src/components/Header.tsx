import { useState } from 'react'
//import { useNavigate } from 'react-router-dom'
import HamburgerMenu from './HamburgerMenu'

const Header = () => {
  //const navigate = useNavigate()
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
  }

  return (
    <div>
    <header className="w-full flex justify-between p-4 bg-white shadow-md">
        <div className="font-bold text-xl text-gray-700">AI Q&A Tool</div>
        <button onClick={toggleMenu} className="text-3xl">☰</button>
        <HamburgerMenu isOpen={isMenuOpen} toggleMenu={toggleMenu} />
      </header>
    </div>
  )
}

export default Header
