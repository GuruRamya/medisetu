import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyseBlood, sendChat, extractSection } from '../api'
import {
  PageHeader, LanguageSelector, InputMethodTabs,
  FileDropZone, TextInput, AnalyseButton,
  SectionCard, RedFlagsCard, DoctorAdviceCard,
  ValueBar, ChatBox
} from '../components/shared'
import { ArrowLeft, TrendingUp, AlertCircle } from 'lucide-react'
import { FeedbackButton } from '../components/FeedbackButton'
export default function BloodPage() {
  const nav = useNavigate()
  const [method, setMethod] = useState('Upload PDF')
  const [file, setFile] = useState(null)
  const [text, setText] = useState('')
  const [gender, setGender] = useState('female')
  const [language, setLanguage] = useState('English')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [chatHistory, setChatHistory] = useState([])
  const [chatLoading, setChatLoading] = useState(false)
  const [expandedSection, setExpandedSection] = useState('values')

  async function handleAnalyse() {
    if (!file && !text.trim()) return setError('Please upload a file or enter report text.')
    setError('')
    setLoading(true)
    setResult(null)
    try {
      const data = await analyseBlood({ file, text: text || undefined, gender, language })
      setResult(data)
      setChatHistory([])
    } catch (e) {
      setError(e?.response?.data?.detail || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  async function handleChat(question) {
    if (!result) return
    setChatLoading(true)
    const newHistory = [...chatHistory, { role: 'user', content: question }]
    setChatHistory(newHistory)
    try {
      const data = await sendChat({ reportText: result.report_text, question, language, chatHistory })
      setChatHistory([...newHistory, { role: 'bot', content: data.reply }])
    } catch {
      setChatHistory([...newHistory, { role: 'bot', content: 'Sorry, I could not process that. Please try again.' }])
    } finally {
      setChatLoading(false)
    }
  }

  const raw = result?.llm_response || ''
  const plain = extractSection(raw, '---PLAIN_EXPLANATION---', '---RED_FLAGS---')
  const flags = extractSection(raw, '---RED_FLAGS---', '---DOCTOR_ADVICE---')
  const doctor = extractSection(raw, '---DOCTOR_ADVICE---', '---DIET_SUGGESTIONS---')
  const diet = extractSection(raw, '---DIET_SUGGESTIONS---')
  const engine = result?.engine_results
  return (
    <div className="min-h-screen bg-white relative overflow-hidden">
      {/* Background decoration */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-red-100/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-1/4 w-96 h-96 bg-neutral-100/30 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>
      <div className="relative max-w-5xl mx-auto px-6 py-12">
        {/* Back Button */}
        <button
          onClick={() => nav('/')}
          className="group mb-8 flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold text-neutral-600 hover:text-maroon-600 hover:bg-maroon-50 transition-all duration-300 shadow-neo-sm"
        >
          <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" />
          Back to Home
        </button>

        <PageHeader
          icon="🩸"
          title="Blood"
          highlight="Report"
          subtitle="Complete blood analysis — CBC, LFT, KFT, thyroid, lipid panel, glucose. Every value explained with accurate ranges."
        />
        {!result ? (
          // Input Section
          <div className="space-y-6 mb-12">
            {/* Input Method */}
            <div className="rounded-2xl border border-neutral-200 bg-white p-8 backdrop-blur-xl shadow-neo-md">
              <div className="flex items-center gap-3 mb-6 pb-6 border-b border-neutral-200">
                <div className="w-10 h-10 rounded-lg bg-red-600 flex items-center justify-center text-white font-bold">
                  📤
                </div>
                <h3 className="font-bold text-lg text-neutral-900">Step 1: Upload Your Report</h3>
              </div>
              <div className="space-y-4">
                <InputMethodTabs
                  options={['Upload PDF', 'Upload Image', 'Type / Paste Text']}
                  value={method}
                  onChange={m => { setMethod(m); setFile(null); setText('') }}
                />
                <div className="mt-6">
                  {method === 'Upload PDF' && (
                    <FileDropZone
                      accept=".pdf"
                      label="Click to upload your blood report PDF"
                      sublabel="Supports Apollo, Thyrocare, SRL, Diagnostic Labs, etc."
                      onChange={setFile}
                      fileName={file?.name}
                    />
                  )}
                  {method === 'Upload Image' && (
                    <FileDropZone
                      accept=".jpg,.jpeg,.png"
                      label="Click to upload an image of your report"
                      sublabel="Take a clear photo in good lighting"
                      onChange={setFile}
                      fileName={file?.name}
                    />
                  )}
                  {method === 'Type / Paste Text' && (
                    <TextInput
                      value={text}
                      onChange={setText}
                      placeholder={"Hemoglobin: 10.2 g/dL\nWBC: 11,000 cells/mcL\nPlatelets: 1.8 lakh\nFasting Glucose: 126 mg/dL\nTSH: 5.2 mIU/L"}
                    />
                  )}
                </div>
              </div>
            </div>
            {/* Gender Selection */}
            <div className="rounded-2xl border border-neutral-200 bg-white p-8 backdrop-blur-xl shadow-neo-md">
              <div className="flex items-center gap-3 mb-6 pb-6 border-b border-neutral-200">
                <div className="w-10 h-10 rounded-lg bg-red-600 flex items-center justify-center text-white font-bold">
                  👤
                </div>
                <h3 className="font-bold text-lg text-neutral-900">Step 2: Select Gender</h3>
              </div>
              <div className="flex gap-4">
                {[
                  { value: 'male', label: '♂ Male', icon: '👨' },
                  { value: 'female', label: '♀ Female', icon: '👩' }
                ].map(g => (
                  <button
                    key={g.value}
                    onClick={() => setGender(g.value)}
                    className={`flex-1 px-6 py-4 rounded-xl font-bold transition-all duration-300 shadow-neo-sm hover:shadow-neo-md ${
                      gender === g.value
                        ? 'bg-maroon-600 text-white'
                        : 'bg-neutral-100 text-neutral-700 hover:text-neutral-900 border border-neutral-200'
                    }`}
                  >
                    <span className="text-xl mr-2">{g.icon}</span>
                    {g.label}
                  </button>
                ))}
              </div>
            </div>
            {/* Language Selection */}
            <div className="rounded-2xl border border-neutral-200 bg-white p-8 backdrop-blur-xl shadow-neo-md">
              <div className="flex items-center gap-3 mb-6 pb-6 border-b border-neutral-200">
                <div className="w-10 h-10 rounded-lg bg-red-600 flex items-center justify-center text-white font-bold">
                  🌐
                </div>
                <h3 className="font-bold text-lg text-neutral-900">Step 3: Choose Your Language</h3>
              </div>
              <LanguageSelector value={language} onChange={setLanguage} />
            </div>
            {error && (
              <div className="rounded-xl border border-red-300 bg-red-50 p-4 text-red-700 text-sm flex items-start gap-3 shadow-neo-sm">
                <AlertCircle size={18} className="flex-shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}
            <AnalyseButton
              onClick={handleAnalyse}
              loading={loading}
              label="Analyse My Blood Report"
              icon="🔍"
            />
          </div>
        ) : (
          // Results Section
          <div className="space-y-8 mb-12">
            <div className="flex items-center justify-between">
              <h2 className="font-display text-4xl font-bold text-neutral-900 flex items-center gap-3">
                <span className="text-3xl">📊</span> Your Analysis Results
              </h2>
              <button
                onClick={() => setResult(null)}
                className="px-4 py-2 rounded-lg text-sm font-semibold text-maroon-600 hover:bg-maroon-50 transition-all shadow-neo-sm"
              >
                ← New Report
              </button>
            </div>
            {/* Value Bars */}
            {engine?.all_values?.length > 0 && (
              <div className="rounded-2xl border border-neutral-200 bg-white p-8 backdrop-blur-xl shadow-neo-md">
                <button
                  onClick={() => setExpandedSection(expandedSection === 'values' ? null : 'values')}
                  className="w-full flex items-center justify-between mb-6 pb-6 border-b border-neutral-200 hover:opacity-80 transition-opacity"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-red-600 flex items-center justify-center text-white">
                      📈
                    </div>
                    <h3 className="font-bold text-lg text-neutral-900">Your Values at a Glance</h3>
                  </div>
                  <span className="text-2xl text-neutral-600">{expandedSection === 'values' ? '−' : '+'}</span>
                </button>
                {expandedSection === 'values' && (
                  <div className="space-y-2">
                    {engine.all_values.map((item, i) => (
                      <ValueBar key={i} item={item} />
                    ))}
                  </div>
                )}
              </div>
            )}
            {plain && <SectionCard icon="📋" title="Plain Explanation" accent="neutral">{plain}</SectionCard>}
            {flags && <RedFlagsCard text={flags} />}
            {doctor && <DoctorAdviceCard text={doctor} />}
            {diet && <SectionCard icon="🥗" title="Diet & Lifestyle Suggestions" accent="neutral">{diet}</SectionCard>}
            <ChatBox
              history={chatHistory}
              onSend={handleChat}
              loading={chatLoading}
              language={language}
            />
          </div>
        )}
      </div>
      {/* Feedback Button - Show this after analysis is done */}
      {result && <FeedbackButton reportType="Blood" />}
      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        div {
          animation: fadeIn 0.5s ease-out;
        }
      `}</style>
    </div>
  )
}