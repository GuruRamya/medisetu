import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import BloodPage from './pages/Blood'
import RadiologyPage from './pages/Radiology'
import PrescriptionPage from './pages/Prescription'
import SkinPage from './pages/Skin'
import Navbar from './components/Navbar'

export default function App() {
  return (
    <div className="min-h-screen bg-slate-950">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/blood" element={<BloodPage />} />
        <Route path="/radiology" element={<RadiologyPage />} />
        <Route path="/prescription" element={<PrescriptionPage />} />
        <Route path="/skin" element={<SkinPage />} />
      </Routes>
    </div>
  )
}