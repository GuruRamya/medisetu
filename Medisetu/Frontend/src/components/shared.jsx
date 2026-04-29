import { useState } from 'react'
import { ChevronDown, Upload, Type, Eye, EyeOff, Sparkles } from 'lucide-react'
export function LanguageSelector({ value, onChange }) {
  const langs = ['English', 'Telugu', 'Hindi']
  const getFlag = (lang) => {
    return { English: '🇬🇧', Telugu: '🇮🇳', Hindi: '🇮🇳' }[lang]
  }
  return (
    <div className="flex gap-3 flex-wrap">
      {langs.map(l => (
        <button
          key={l}
          onClick={() => onChange(l)}
          className={`group relative px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300 overflow-hidden ${
            value === l
              ? 'text-white shadow-neo-md bg-maroon-600'
              : 'text-neutral-600 hover:text-neutral-900 bg-neutral-100 hover:shadow-neo-md'
          }`}
        >
          <span className="relative flex items-center gap-2">
            <span>{getFlag(l)}</span>
            {l}
          </span>
        </button>
      ))}
    </div>
  )
}

export function InputMethodTabs({ options, value, onChange }) {
  return (
    <div className="flex gap-2 flex-wrap p-1.5 bg-neutral-100 rounded-2xl border border-neutral-200 w-fit shadow-neo-sm">
      {options.map(opt => {
        const isActive = value === opt
        const getIcon = (o) => {
          if (o.includes('Upload')) return Upload
          if (o.includes('Type') || o.includes('Text')) return Type
          if (o.includes('Camera')) return '📷'
          return null
        }
        const Icon = getIcon(opt)
        return (
          <button
            key={opt}
            onClick={() => onChange(opt)}
            className={`relative px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300 flex items-center gap-2 ${
              isActive
                ? 'text-white bg-maroon-600 shadow-neo-sm'
                : 'text-neutral-600 hover:text-neutral-900 hover:bg-white'
            }`}
          >
            <span className="relative flex items-center gap-2">
              {Icon && (typeof Icon === 'string' ? Icon : <Icon size={16} />)}
              {opt}
            </span>
          </button>
        )
      })}
    </div>
  )
}

export function FileDropZone({ accept, label, sublabel, onChange, fileName }) {
  const [isDragging, setIsDragging] = useState(false)
  return (
    <label className="block cursor-pointer group">
      <div
        onDragEnter={() => setIsDragging(true)}
        onDragLeave={() => setIsDragging(false)}
        onDrop={() => setIsDragging(false)}
        className={`relative border-2 border-dashed rounded-3xl p-12 text-center transition-all duration-300 overflow-hidden ${
          fileName
            ? 'border-maroon-400 bg-maroon-50 shadow-neo-md'
            : isDragging
            ? 'border-maroon-500 bg-neutral-100 scale-102 shadow-neo-md'
            : 'border-neutral-300 hover:border-maroon-500 hover:bg-neutral-50 group-hover:shadow-neo-md'
        }`}
      >
        {/* Animated gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-neutral-50 to-neutral-100 group-hover:from-neutral-100 group-hover:to-neutral-50 transition-all duration-700" />
        <input
          type="file"
          accept={accept}
          className="hidden"
          onChange={e => onChange(e.target.files[0] || null)}
        />
        {fileName ? (
          <div className="relative flex items-center justify-center gap-4 py-2">
            <div className="relative">
              <div className="absolute inset-0 bg-maroon-400 blur-xl rounded-2xl opacity-20" />
              <div className="relative w-12 h-12 rounded-2xl bg-maroon-600 flex items-center justify-center text-white shadow-neo-md">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div className="text-left">
              <p className="text-maroon-600 font-semibold text-sm">{fileName}</p>
              <p className="text-neutral-500 text-xs mt-0.5">✓ Ready to analyse</p>
            </div>
          </div>
        ) : (
          <>
            <div className="relative w-16 h-16 rounded-2xl bg-neutral-200 border border-neutral-300 flex items-center justify-center mx-auto mb-4 group-hover:border-maroon-500 group-hover:shadow-neo-md transition-all duration-300">
              <svg className="w-7 h-7 text-neutral-500 group-hover:text-maroon-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <p className="text-neutral-900 font-semibold text-sm">{label}</p>
            <p className="text-neutral-600 text-xs mt-1">{sublabel}</p>
            <p className="text-neutral-500 text-xs mt-3">Or drag & drop your file here</p>
          </>
        )}
      </div>
    </label>
  )
}

export function TextInput({ value, onChange, placeholder, rows = 6 }) {
  const [isFocused, setIsFocused] = useState(false)
  return (
    <div className="relative">
      <div className={`absolute -inset-0.5 bg-maroon-500 rounded-2xl blur opacity-0 transition-opacity duration-300 ${
        isFocused ? 'opacity-10' : 'opacity-0'
      }`} />
      <textarea
        rows={rows}
        value={value}
        onChange={e => onChange(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholder={placeholder}
        className="relative w-full bg-white border border-neutral-200 rounded-2xl px-4 py-3 text-neutral-900 placeholder-neutral-400 text-sm leading-relaxed font-mono resize-none focus:outline-none focus:border-maroon-500 focus:ring-2 focus:ring-maroon-200 transition-all duration-300 shadow-neo-inset"
      />
    </div>
  )
}

export function AnalyseButton({ onClick, loading, label, icon }) {
  const [isHovering, setIsHovering] = useState(false)
  return (
    <button
      onClick={onClick}
      disabled={loading}
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
      className="w-full relative group py-4 rounded-2xl font-bold text-base text-white overflow-hidden disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 bg-maroon-600 hover:bg-maroon-700 shadow-neo-md hover:shadow-neo-lg active:shadow-neo-sm"
    >
      {/* Shine animation on loading */}
      {loading && (
        <div className="absolute inset-0 bg-gradient-to-r from-maroon-600 via-maroon-500 to-maroon-600 animate-shimmer" />
      )}
      {/* Content */}
      <span className="relative flex items-center justify-center gap-3">
        {loading ? (
          <>
            <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <span>Analysing Medical Report...</span>
          </>
        ) : (
          <>
            <span className="text-lg">{icon}</span>
            <span>{label}</span>
            {isHovering && <Sparkles size={16} className="animate-pulse" />}
          </>
        )}
      </span>
    </button>
  )
}

export function PageHeader({ icon, title, highlight, subtitle }) {
  return (
    <div className="mb-12 relative">
      {/* Background decoration */}
      <div className="absolute -top-20 left-0 right-0 h-64 bg-gradient-to-b from-maroon-100/50 to-transparent blur-3xl pointer-events-none" />
      <div className="relative space-y-3">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="absolute inset-0 bg-maroon-200 rounded-2xl blur-lg opacity-40" />
            <div className="relative w-12 h-12 rounded-2xl bg-maroon-600 flex items-center justify-center text-2xl shadow-neo-md">
              {icon}
            </div>
          </div>
          <h1 className="font-display text-5xl md:text-6xl font-bold text-neutral-900 tracking-tight">
            {title} <span className="text-maroon-600">{highlight}</span>
          </h1>
        </div>
        <p className="text-neutral-600 text-base leading-relaxed max-w-2xl">{subtitle}</p>
      </div>
    </div>
  )
}

export function SectionCard({ icon, title, children, accent }) {
  const accentStyles = {
    maroon: 'border-maroon-200 bg-maroon-50 shadow-neo-md',
    neutral: 'border-neutral-200 bg-neutral-100 shadow-neo-md',
    default: 'border-neutral-200 bg-white shadow-neo-sm',
  }
  return (
    <div className={`group rounded-2xl border p-6 mb-5 transition-all duration-300 hover:shadow-neo-lg ${accentStyles[accent] || accentStyles.default}`}>
      <div className="flex items-start justify-between mb-4 pb-4 border-b border-neutral-200">
        <div className="flex items-center gap-2.5 text-base font-bold text-neutral-900">
          <span className="text-xl">{icon}</span>
          <span>{title}</span>
        </div>
        <Sparkles size={14} className="text-neutral-400 group-hover:text-maroon-600 transition-colors" />
      </div>
      <div className="text-neutral-700 text-sm leading-relaxed whitespace-pre-wrap font-light">{children}</div>
    </div>
  )
}

export function DoctorAdviceCard({ text }) {
  const isImmediate = text.includes('IMMEDIATE')
  const isMonitor = text.includes('MONITOR')
  const styles = isImmediate
    ? 'border-red-300 bg-red-50 shadow-neo-md'
    : isMonitor
    ? 'border-yellow-300 bg-yellow-50 shadow-neo-md'
    : 'border-maroon-200 bg-maroon-50 shadow-neo-md'
  const icon = isImmediate ? '🚨' : isMonitor ? '⚠️' : '✨'
  const accentColor = isImmediate ? 'text-red-700' : isMonitor ? 'text-yellow-700' : 'text-maroon-600'
  return (
    <div className={`rounded-2xl border p-6 mb-5 ${styles}`}>
      <div className={`flex items-center gap-2.5 text-base font-bold mb-4 pb-4 border-b border-neutral-200 ${accentColor}`}>
        <span className="text-xl">{icon}</span>
        <span>Doctor Consultation Advice</span>
      </div>
      <div className="text-neutral-700 text-sm leading-relaxed whitespace-pre-wrap font-light">{text}</div>
    </div>
  )
}

export function RedFlagsCard({ text }) {
  const allClear = text.includes('All values are within normal range') ||
                   text.includes('All findings are within normal range') ||
                   text.includes('No urgent red flags')
  if (allClear) {
    return (
      <div className="rounded-2xl border border-green-300 bg-green-50 p-6 mb-5 shadow-neo-md">
        <div className="flex items-center gap-3 text-base font-bold text-green-700 mb-2">
          <span className="text-2xl">✨</span>
          <span>Perfect Health Report</span>
        </div>
        <p className="text-green-700/70 text-sm leading-relaxed">All values are within the normal range. Your health metrics look great!</p>
      </div>
    )
  }
  const isDanger = text.includes('DANGER')
  const isMonitor = text.includes('MONITOR')
  const icon = isDanger ? '🚨' : isMonitor ? '⚠️' : '🟡'
  const style = isDanger
    ? 'border-red-300 bg-red-50 shadow-neo-md'
    : isMonitor
    ? 'border-yellow-300 bg-yellow-50 shadow-neo-md'
    : 'border-orange-300 bg-orange-50 shadow-neo-md'
  return (
    <div className={`rounded-2xl border p-6 mb-5 ${style}`}>
      <div className="flex items-center gap-2.5 text-base font-bold text-neutral-900 mb-4 pb-4 border-b border-neutral-200">
        <span className="text-xl">{icon}</span>
        <span>Alert Findings</span>
      </div>
      <div className="text-neutral-700 text-sm leading-relaxed whitespace-pre-wrap font-light">{text}</div>
    </div>
  )
}

export function ValueBar({ item }) {
  const { value, min, max, status, name, unit, description } = item
  const safeMax = max > 9000 ? min * 3 : max
  const rangeSpan = safeMax - min || 1
  const clamped = Math.max(min - rangeSpan * 0.2, Math.min(value, safeMax + rangeSpan * 0.2))
  const pct = Math.max(2, Math.min(98,
    ((clamped - (min - rangeSpan * 0.2)) / (rangeSpan * 1.4)) * 100
  ))
  const normalStart = (rangeSpan * 0.2 / (rangeSpan * 1.4)) * 100
  const normalEnd = ((rangeSpan * 0.2 + rangeSpan) / (rangeSpan * 1.4)) * 100
  const color = status === 'NORMAL' ? '#059669'
    : status === 'DANGER' ? '#dc2626'
    : status === 'MONITOR' ? '#d97706'
    : '#f59e0b'
  const emoji = status === 'NORMAL' ? '✨'
    : status === 'DANGER' ? '🚨'
    : status === 'MONITOR' ? '⚠️'
    : '🟡'
  const bgColor = status === 'NORMAL' ? 'bg-green-50 border-green-200'
    : status === 'DANGER' ? 'bg-red-50 border-red-200'
    : status === 'MONITOR' ? 'bg-yellow-50 border-yellow-200'
    : 'bg-orange-50 border-orange-200'
  return (
    <div className={`mb-7 p-4 rounded-xl ${bgColor} border transition-all duration-300 hover:shadow-neo-md shadow-neo-sm`}>
      <div className="flex justify-between items-start mb-2">
        <div>
          <span className="text-sm font-bold text-neutral-900 flex items-center gap-2 mb-1">
            <span className="text-base">{emoji}</span>
            {name}
          </span>
          <span className="text-xs text-neutral-600">{description}</span>
        </div>
        <span className="text-xs font-mono text-neutral-500">
          {min} — {max} {unit}
        </span>
      </div>
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-bold text-neutral-900" style={{ color }}>{value} {unit}</span>
        <span className="text-xs font-semibold px-2.5 py-1 rounded-full text-neutral-900" style={{
          background: color + '20',
          color: color
        }}>{status}</span>
      </div>
      <div className="relative h-3 bg-neutral-300 rounded-full overflow-visible">
        <div
          className="absolute h-full rounded-full transition-all duration-500"
          style={{
            left: `${normalStart}%`,
            width: `${normalEnd - normalStart}%`,
            background: 'rgba(5, 150, 105, 0.25)'
          }}
        />
        <div
          className="absolute w-4 h-4 rounded-full border-2 border-white shadow-neo-md transition-all duration-500"
          style={{
            left: `${pct}%`,
            transform: 'translateX(-50%) translateY(-20%)',
            background: color,
          }}
        />
      </div>
    </div>
  )
}

export function ChatBox({ history, onSend, loading, language }) {
  const [q, setQ] = useState('')
  const [isExpanded, setIsExpanded] = useState(false)
  return (
    <div className="rounded-2xl border border-neutral-200 bg-white p-6 mt-8 shadow-neo-md backdrop-blur-xl">
      <div className="flex items-center justify-between mb-5 pb-4 border-b border-neutral-200">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="absolute inset-0 bg-maroon-400 rounded-full blur-lg opacity-30" />
            <div className="relative w-9 h-9 rounded-full bg-maroon-600 flex items-center justify-center text-white shadow-neo-sm">
              🤖
            </div>
          </div>
          <div>
            <p className="text-neutral-900 font-bold text-sm">Ask MediSetu Anything</p>
            <p className="text-neutral-500 text-xs">Get instant clarifications about your report</p>
          </div>
        </div>
      </div>
      <div className={`space-y-3 mb-4 rounded-xl bg-neutral-50 p-4 border border-neutral-200 transition-all duration-300 ${
        isExpanded ? 'max-h-96 overflow-y-auto' : 'max-h-56 overflow-hidden'
      }`}>
        {history.length === 0 && (
          <p className="text-center text-neutral-500 text-sm py-4">Start a conversation...</p>
        )}
        {history.map((m, i) => (
          <div
            key={i}
            className={`text-sm px-4 py-3 rounded-xl leading-relaxed animate-fadeIn ${
              m.role === 'user'
                ? 'bg-maroon-100 text-maroon-900 ml-8 rounded-br-none border-l-2 border-maroon-500'
                : 'bg-neutral-200 text-neutral-900 mr-8 rounded-bl-none border-l-2 border-neutral-400'
            }`}
          >
            {m.content}
          </div>
        ))}
        {loading && (
          <div className="bg-neutral-200 text-neutral-700 text-sm px-4 py-3 rounded-xl mr-8 rounded-bl-none border-l-2 border-neutral-400">
            <span className="animate-pulse flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-maroon-600 animate-pulse" />
              MediSetu is thinking...
            </span>
          </div>
        )}
      </div>
      {history.length > 2 && !isExpanded && (
        <button
          onClick={() => setIsExpanded(true)}
          className="text-xs text-maroon-600 hover:text-maroon-700 mb-3 transition-colors"
        >
          ↓ Show more messages
        </button>
      )}
      <div className="flex gap-2">
        <textarea
          rows={2}
          value={q}
          onChange={e => setQ(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              if (q.trim()) {
                onSend(q)
                setQ('')
              }
            }
          }}
          placeholder="E.g., What does my hemoglobin mean? What foods should I eat?"
          className="flex-1 bg-neutral-50 border border-neutral-200 rounded-xl px-4 py-2.5 text-neutral-900 placeholder-neutral-500 text-sm resize-none focus:outline-none focus:border-maroon-500 focus:ring-2 focus:ring-maroon-200 transition-all duration-300 shadow-neo-inset"
        />
        <button
          onClick={() => {
            if (q.trim()) {
              onSend(q)
              setQ('')
            }
          }}
          disabled={loading || !q.trim()}
          className="px-4 py-2.5 rounded-xl bg-maroon-600 text-white font-semibold text-sm hover:bg-maroon-700 hover:shadow-neo-md disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 flex items-center justify-center shadow-neo-sm active:shadow-neo-sm"
        >
          Send
        </button>
      </div>
    </div>
  )
}

export const shimmerKeyframes = `
  @keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
`