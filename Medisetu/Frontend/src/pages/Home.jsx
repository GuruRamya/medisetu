import { Link } from 'react-router-dom'
import { Droplets, Scan, Pill, Microscope, ArrowRight, Zap, Languages, Shield } from 'lucide-react'
import { useState, useEffect } from 'react'
const MODULES = [
  {
    to: '/blood',
    icon: Droplets,
    gradient: 'from-red-100 to-orange-100',
    border: 'border-red-200 hover:border-maroon-400',
    title: 'Blood Report',
    desc: 'CBC, LFT, KFT, thyroid, lipid panel, HbA1c — every value explained.',
    tags: ['PDF', 'Image', 'Text'],
  },
  {
    to: '/radiology',
    gradient: 'from-blue-100 to-cyan-100',
    border: 'border-blue-200 hover:border-maroon-400',
    title: 'Radiology Report',
    desc: 'X-ray, MRI, CT scan, ultrasound — radiologist jargon decoded.',
    tags: ['PDF', 'Image', 'Text'],
  },
  {
    to: '/prescription',
    gradient: 'from-purple-100 to-pink-100',
    border: 'border-purple-200 hover:border-maroon-400',
    title: 'Prescription',
    desc: 'Every drug explained — purpose, dosage, side effects.',
    tags: ['Image', 'Text'],
  },
  {
    to: '/skin',
    gradient: 'from-green-100 to-teal-100',
    border: 'border-green-200 hover:border-maroon-400',
    title: 'Skin Analysis',
    desc: 'Upload photo or describe — instant triage and care advice.',
    tags: ['Camera', 'Image', 'Text'],
  },
]

const FEATURES = [
  { Icon: Languages, title: 'English · Telugu · Hindi', desc: 'Results in your language' },
  { Icon: Shield, title: 'Rule-based Validation', desc: 'Mathematical engine verifies all values' },
  { Icon: Zap, title: 'Instant Analysis', desc: 'Fastest AI inference available' },
]

const STEPS = [
  { num: '01', title: 'Choose Report Type', desc: 'Blood, radiology, prescription or skin' },
  { num: '02', title: 'Upload or Type', desc: 'PDF, image, or paste values directly' },
  { num: '03', title: 'Pick Language', desc: 'English, Telugu or Hindi' },
  { num: '04', title: 'Get Analysis', desc: 'Explanation, alerts, doctor advice' },
]

export default function Home() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })
  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50)
    const handleMouseMove = (e) => {
      setMousePos({ x: e.clientX, y: e.clientY })
    }
    window.addEventListener('scroll', handleScroll)
    window.addEventListener('mousemove', handleMouseMove)
    return () => {
      window.removeEventListener('scroll', handleScroll)
      window.removeEventListener('mousemove', handleMouseMove)
    }
  }, [])

  return (
    <main className="relative overflow-hidden bg-white">
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {/* Subtle gradient blobs */}
        <div className="absolute top-20 left-10 w-96 h-96 bg-maroon-100/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute top-40 right-20 w-80 h-80 bg-neutral-100/30 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute -bottom-20 left-1/2 w-96 h-96 bg-neutral-50/40 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
      </div>
      {/* Dynamic light follow cursor */}
      <div
        className="fixed pointer-events-none w-96 h-96 rounded-full blur-3xl opacity-10 transition-opacity duration-300"
        style={{
          background: 'radial-gradient(circle, rgba(139, 58, 58, 0.2) 0%, transparent 70%)',
          left: `${mousePos.x - 192}px`,
          top: `${mousePos.y - 192}px`,
        }}
      />
      <div className="relative max-w-7xl mx-auto px-6 pt-32 pb-40">
        {/* Hero Section */}
        <div className="text-center mb-32 space-y-8">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-maroon-50 border border-maroon-200 text-maroon-700 text-xs font-bold tracking-widest uppercase animate-fadeIn shadow-neo-sm">
            <span className="w-2 h-2 rounded-full bg-maroon-600 animate-pulse shadow-lg shadow-maroon-600/50" />
            Transforming Medical Literacy
          </div>
          <div className="space-y-4 animate-fadeIn" style={{ animationDelay: '0.1s' }}>
            <h1 className="font-display text-7xl md:text-8xl lg:text-9xl text-neutral-900 leading-none tracking-tight">
              Your Reports,
              <br />
              <span className="text-maroon-600">
                Explained.
              </span>
            </h1>
            <p className="text-neutral-600 text-lg md:text-xl max-w-3xl mx-auto leading-relaxed">
              Medical reports explained in plain language — in English, Telugu, or Hindi.
              <br />
              <span className="text-maroon-700/70">No medical degree needed.</span>
            </p>
          </div>
          <div className="flex items-center justify-center gap-4 pt-4 animate-fadeIn" style={{ animationDelay: '0.2s' }}>
            <Link
              to="/blood"
              className="group relative px-8 py-4 bg-maroon-600 text-white font-bold rounded-xl overflow-hidden shadow-neo-md hover:shadow-neo-lg hover:bg-maroon-700 transition-all duration-300"
            >
              <span className="relative flex items-center gap-2">
                Start Analysing
                <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
              </span>
            </Link>
            <a
              href="#modules"
              className="px-8 py-4 rounded-xl border border-neutral-300 text-neutral-900 font-bold hover:border-maroon-500 hover:bg-maroon-50 transition-all duration-300 shadow-neo-sm hover:shadow-neo-md"
            >
              See All Reports
            </a>
          </div>
        </div>
        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-32 animate-fadeIn" style={{ animationDelay: '0.3s' }}>
          {FEATURES.map(({ Icon, title, desc }, i) => (
            <div
              key={title}
              className="group relative p-6 rounded-2xl border border-neutral-200 bg-neutral-50 hover:border-maroon-300 hover:bg-maroon-50 transition-all duration-300 shadow-neo-sm hover:shadow-neo-md"
              style={{ animationDelay: `${0.3 + i * 0.1}s` }}
            >
              <div className="relative space-y-2">
                <div className="w-10 h-10 rounded-lg bg-maroon-600 flex items-center justify-center group-hover:shadow-neo-md transition-all">
                  <Icon size={16} className="text-white" />
                </div>
                <p className="text-neutral-900 font-bold text-sm">{title}</p>
                <p className="text-neutral-600 text-xs">{desc}</p>
              </div>
            </div>
          ))}
        </div>
        {/* How It Works */}
        <div className="mb-32 space-y-12">
          <div className="text-center space-y-2">
            <p className="text-maroon-700 text-sm font-bold tracking-widest uppercase">Process</p>
            <h2 className="font-display text-5xl text-neutral-900">How MediSetu Works</h2>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {STEPS.map(({ num, title, desc }, i) => (
              <div
                key={num}
                className="relative group animate-fadeIn"
                style={{ animationDelay: `${0.6 + i * 0.1}s` }}
              >
                {/* Connector line */}
                {i < STEPS.length - 1 && (
                  <div className="hidden md:block absolute top-1/2 -right-2 w-4 h-0.5 bg-gradient-to-r from-maroon-400 to-transparent" />
                )}
                <div className="relative p-6 rounded-2xl border border-neutral-200 bg-white hover:border-maroon-300 hover:shadow-neo-lg shadow-neo-sm transition-all duration-300 h-full">
                  <div className="absolute -top-3 left-6 w-6 h-6 rounded-full bg-maroon-600 border-4 border-white flex items-center justify-center text-white text-xs font-bold shadow-neo-md" />
                  <div className="pt-3 space-y-2">
                    <p className="text-neutral-500 text-xs font-mono">{num}</p>
                    <p className="text-neutral-900 font-bold text-sm">{title}</p>
                    <p className="text-neutral-600 text-xs">{desc}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
        {/* Modules Section */}
        <div id="modules" className="space-y-12">
          <div className="text-center space-y-2">
            <p className="text-maroon-700 text-sm font-bold tracking-widest uppercase">Modules</p>
            <h2 className="font-display text-5xl text-neutral-900">Choose Your Report Type</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {MODULES.map(({ to, gradient, border, title, desc, tags }, i) => (
              <Link
                key={to}
                to={to}
                className={`group relative overflow-hidden rounded-3xl border ${border} bg-gradient-to-br ${gradient} p-8 transition-all duration-300 shadow-neo-md hover:shadow-neo-lg animate-fadeIn hover:scale-102`}
                style={{ animationDelay: `${0.9 + i * 0.1}s` }}
              >
                {/* Shine effect on hover */}
                <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/10 to-white/0 -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
                {/* Background gradient line */}
                <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-maroon-400 to-maroon-600" />
                <div className="relative space-y-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-maroon-600 to-maroon-700 flex items-center justify-center group-hover:scale-110 transition-transform duration-300 shadow-neo-md text-white">
                        <Droplets size={24} />
                      </div>
                      <h3 className="font-display text-2xl font-bold text-neutral-900">{title}</h3>
                    </div>
                    <ArrowRight size={20} className="text-neutral-600 group-hover:text-maroon-600 group-hover:translate-x-2 transition-all duration-300 mt-2" />
                  </div>
                  <p className="text-neutral-700 text-sm leading-relaxed">{desc}</p>
                  <div className="flex gap-2 flex-wrap pt-2">
                    {tags.map(t => (
                      <span key={t} className="text-xs px-3 py-1.5 rounded-full bg-white/40 border border-neutral-300 text-neutral-700 group-hover:border-maroon-400 group-hover:bg-white/70 transition-all">
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
        {/* CTA Section */}
        <div className="mt-40 relative rounded-3xl border border-neutral-200 bg-gradient-to-br from-maroon-50 to-white p-12 text-center overflow-hidden shadow-neo-lg">
          <div className="relative space-y-4">
            <h3 className="font-display text-3xl font-bold text-neutral-900">Ready to Understand Your Health?</h3>
            <p className="text-neutral-600 max-w-2xl mx-auto">
              Upload your medical report now and get an instant, detailed explanation in your language.
            </p>
            <Link
              to="/blood"
              className="inline-block px-8 py-4 bg-maroon-600 text-white font-bold rounded-xl hover:bg-maroon-700 hover:shadow-neo-lg transition-all duration-300 shadow-neo-md"
            >
              Get Started Now →
            </Link>
          </div>
        </div>
        {/* Footer */}
        <div className="mt-32 pt-12 border-t border-neutral-200 text-center space-y-3">
          <p className="text-neutral-600 text-sm">
            Built with care by <span className="text-maroon-600 font-bold">MediSetu</span>
          </p>
          <p className="text-xs text-neutral-500">
            Not a substitute for professional medical advice. Always consult a qualified doctor.
          </p>
        </div>
      </div>
      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.8s ease-out forwards;
          opacity: 0;
        }
      `}</style>
    </main>
  )
}