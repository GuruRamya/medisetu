import { Link, useLocation } from 'react-router-dom'
import { Activity, Droplets, Scan, Pill, Microscope, Menu, X } from 'lucide-react'
import { useState, useEffect } from 'react'
const NAV_ITEMS = [
  { to: '/blood',        label: 'Blood',        Icon: Droplets  },
  { to: '/radiology',   label: 'Radiology',    Icon: Scan      },
  { to: '/prescription',label: 'Prescription', Icon: Pill      },
  { to: '/skin',        label: 'Skin',         Icon: Microscope},
]
export default function Navbar() {
  const { pathname } = useLocation()
  const [isOpen, setIsOpen] = useState(false)
  const [isScrolled, setIsScrolled] = useState(false)
  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 10)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])
  return (
    <header className={`sticky top-0 z-50 transition-all duration-500 ${
      isScrolled 
        ? 'border-b border-neutral-200 bg-white/95 backdrop-blur-2xl shadow-neo-md' 
        : 'border-b border-neutral-100 bg-white/40 backdrop-blur-xl'
    }`}>
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo with subtle shadow */}
        <Link to="/" className="group relative z-10">
          <div className="absolute -inset-2 bg-maroon-500 rounded-xl opacity-0 group-hover:opacity-5 blur-xl transition-opacity duration-500" />
          <div className="relative flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-maroon-600 flex items-center justify-center group-hover:shadow-neo-md transition-all duration-300">
              <Activity size={16} className="text-white" />
            </div>
            <span className="font-display text-lg font-bold tracking-tight">
              <span className="text-neutral-900">Medi</span><span className="text-maroon-600">Setu</span>
            </span>
          </div>
        </Link>
        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-1.5">
          {NAV_ITEMS.map(({ to, label, Icon }) => {
            const active = pathname === to
            return (
              <Link
                key={to}
                to={to}
                className={`group relative px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 flex items-center gap-1.5 ${
                  active
                    ? 'text-maroon-600'
                    : 'text-neutral-600 hover:text-neutral-900'
                }`}
              >
                {/* Neomorphic background for active */}
                {active && (
                  <div className="absolute inset-0 bg-neutral-100 rounded-lg shadow-neo-sm" />
                )}
                {/* Hover effect */}
                <div className="absolute inset-0 bg-neutral-50 group-hover:bg-neutral-100 rounded-lg transition-all duration-300 opacity-0 group-hover:opacity-100" />
                <Icon size={14} className={active ? 'text-maroon-600' : 'group-hover:text-maroon-600 transition-colors'} />
                <span className="relative">{label}</span>
                {/* Underline animation */}
                {active && (
                  <div className="absolute bottom-1 left-4 right-4 h-0.5 bg-maroon-600" />
                )}
              </Link>
            )
          })}
        </nav>
        {/* Mobile Menu Button */}
        <button 
          onClick={() => setIsOpen(!isOpen)}
          className="md:hidden relative z-20 p-2 rounded-lg hover:bg-neutral-100 transition-colors text-neutral-900"
        >
          {isOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
        {/* Status badge */}
        <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-neutral-100 border border-neutral-200 backdrop-blur-sm shadow-neo-sm">
          <span className="w-1.5 h-1.5 rounded-full bg-maroon-600 animate-pulse shadow-lg shadow-maroon-600/50" />
          <span className="text-xs text-maroon-600 font-semibold">AI Powered</span>
        </div>
      </div>
      {/* Mobile Menu */}
      <div className={`md:hidden absolute top-16 left-0 right-0 bg-white/95 backdrop-blur-xl border-b border-neutral-200 overflow-hidden transition-all duration-300 ${
        isOpen ? 'max-h-96' : 'max-h-0'
      }`}>
        <nav className="p-4 space-y-2">
          {NAV_ITEMS.map(({ to, label, Icon }) => {
            const active = pathname === to
            return (
              <Link
                key={to}
                to={to}
                onClick={() => setIsOpen(false)}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 ${
                  active
                    ? 'bg-neutral-100 text-maroon-600 shadow-neo-sm'
                    : 'text-neutral-600 hover:bg-neutral-50 hover:text-neutral-900'
                }`}
              >
                <Icon size={16} />
                {label}
              </Link>
            )
          })}
        </nav>
      </div>
    </header>
  )
}