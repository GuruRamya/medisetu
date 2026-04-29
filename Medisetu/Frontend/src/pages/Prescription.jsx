import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analysePrescription, sendChat } from '../api'
import {
  PageHeader, LanguageSelector, InputMethodTabs,
  FileDropZone, TextInput, AnalyseButton, ChatBox
} from '../components/shared'
import { ArrowLeft, AlertCircle, AlertTriangle } from 'lucide-react'
import { FeedbackButton } from '../components/FeedbackButton'

function DrugCard({ drug, index }) {
  const lines = drug.trim().split('\n')
  const fields = {}
  lines.forEach(line => {
    if (line.includes(':')) {
      const [k, ...v] = line.split(':')
      fields[k.trim()] = v.join(':').trim()
    }
  })
  const { Name, Dosage, Purpose, 'How it works': how, 'Side effects': se, Precautions } = fields
  return (
    <div className="rounded-2xl border border-neutral-200 bg-gradient-to-br from-purple-50 to-white p-6 mb-4 hover:border-maroon-300 hover:shadow-neo-lg hover:from-purple-100 shadow-neo-sm transition-all duration-300">
      <h3 className="text-lg font-bold text-neutral-900 mb-4 pb-3 border-b border-neutral-200 flex items-center gap-2">
        <span className="text-2xl">💊</span>
        {Name || `Medicine ${index + 1}`}
      </h3>
      <div className="space-y-3">
        {[
          { label: 'Dosage', val: Dosage },
          { label: 'Purpose', val: Purpose },
          { label: 'How it works', val: how },
          { label: 'Side effects', val: se },
          { label: 'Precautions', val: Precautions },
        ].map(({ label, val }) => val ? (
          <div key={label} className="flex gap-3 items-start">
            <span className="text-xs font-bold text-maroon-600 uppercase tracking-wider min-w-[100px] pt-1">{label}</span>
            <span className="text-neutral-700 text-sm leading-relaxed">{val}</span>
          </div>
        ) : null)}
      </div>
    </div>
  )
}

export default function PrescriptionPage() {
  const nav = useNavigate()
  const [method, setMethod] = useState('Upload Image')
  const [file, setFile] = useState(null)
  const [text, setText] = useState('')
  const [language, setLanguage] = useState('English')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [chatHistory, setChatHistory] = useState([])
  const [chatLoading, setChatLoading] = useState(false)
  async function handleAnalyse() {
    if (!file && !text.trim()) return setError('Please upload an image or enter prescription text.')
    setError('')
    setLoading(true)
    setResult(null)
    try {
      const data = await analysePrescription({ file, text: text || undefined, language })
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
      setChatHistory([...newHistory, { role: 'bot', content: 'Sorry, could not process that.' }])
    } finally {
      setChatLoading(false)
    }
  }

  const raw = result?.llm_response || ''
  const drugs = raw.split('---DRUG---').slice(1).map(p =>
    p.includes('---END_DRUG---') ? p.split('---END_DRUG---')[0].trim() : p.trim()
  )
  const generalAdvice = raw.includes('---GENERAL_ADVICE---')
    ? raw.split('---GENERAL_ADVICE---')[1].trim()
    : ''
  return (
    <div className="min-h-screen bg-white relative overflow-hidden">
      {/* Background decoration */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-100/20 rounded-full blur-3xl animate-pulse" />
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
          icon="💊"
          title="Prescription"
          highlight="Analyser"
          subtitle="Complete medication guide — Every drug explained separately with purpose, dosage, side effects, and precautions."
        />
        {!result ? (
          // Input Section
          <div className="space-y-6 mb-12">
            <div className="rounded-2xl border border-neutral-200 bg-white p-8 backdrop-blur-xl shadow-neo-md">
              <div className="flex items-center gap-3 mb-6 pb-6 border-b border-neutral-200">
                <div className="w-10 h-10 rounded-lg bg-purple-600 flex items-center justify-center text-white font-bold">
                  📤
                </div>
                <h3 className="font-bold text-lg text-neutral-900">Step 1: Upload Your Prescription</h3>
              </div>
              <div className="space-y-4">
                <InputMethodTabs
                  options={['Upload Image', 'Type / Paste Text']}
                  value={method}
                  onChange={m => { setMethod(m); setFile(null); setText('') }}
                />
                {method === 'Upload Image' && (
                  <>
                    <div className="mt-6">
                      <FileDropZone
                        accept=".jpg,.jpeg,.png"
                        label="Upload a photo of your prescription"
                        sublabel="Take a clear photo of the prescription slip"
                        onChange={setFile}
                        fileName={file?.name}
                      />
                    </div>
                    <div className="rounded-lg border border-yellow-300 bg-yellow-50 p-3 text-yellow-800/80 text-xs flex items-start gap-2 shadow-neo-sm">
                      <AlertTriangle size={16} className="flex-shrink-0 mt-0.5" />
                      <span>Handwritten prescriptions may not read accurately. For best results, type medicines manually.</span>
                    </div>
                  </>
                )}
                {method === 'Type / Paste Text' && (
                  <div className="mt-6">
                    <TextInput
                      value={text}
                      onChange={setText}
                      placeholder={"Tab. Metformin 500mg - 1-0-1 after food\nTab. Atorvastatin 10mg - 0-0-1\nTab. Amlodipine 5mg - 1-0-0\nSyp. Amoxicillin 250mg/5ml - 5ml three times daily for 5 days"}
                    />
                  </div>
                )}
              </div>
            </div>
            {/* Language Selection */}
            <div className="rounded-2xl border border-neutral-200 bg-white p-8 backdrop-blur-xl shadow-neo-md">
              <div className="flex items-center gap-3 mb-6 pb-6 border-b border-neutral-200">
                <div className="w-10 h-10 rounded-lg bg-purple-600 flex items-center justify-center text-white font-bold">
                  🌐
                </div>
                <h3 className="font-bold text-lg text-neutral-900">Step 2: Choose Your Language</h3>
              </div>
              <LanguageSelector value={language} onChange={setLanguage} />
            </div>
            {error && (
              <div className="rounded-xl border border-purple-300 bg-purple-50 p-4 text-purple-700 text-sm flex items-start gap-3 shadow-neo-sm">
                <AlertCircle size={18} className="flex-shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}
            <AnalyseButton
              onClick={handleAnalyse}
              loading={loading}
              label="Explain My Prescription"
              icon="💊"
            />
          </div>
        ) : (
          // Results Section
          <div className="space-y-8 mb-12">
            <div className="flex items-center justify-between">
              <h2 className="font-display text-4xl font-bold text-neutral-900 flex items-center gap-3">
                <span className="text-3xl">💊</span> Your Prescription Explained
              </h2>
              <button
                onClick={() => setResult(null)}
                className="px-4 py-2 rounded-lg text-sm font-semibold text-maroon-600 hover:bg-maroon-50 transition-all shadow-neo-sm"
              >
                ← New Report
              </button>
            </div>

            {drugs.length > 0 ? (
              <div>
                <p className="text-neutral-600 text-sm mb-6">Each medicine explained separately below</p>
                {drugs.map((d, i) => <DrugCard key={i} drug={d} index={i} />)}
              </div>
            ) : (
              <div className="rounded-2xl border border-red-300 bg-red-50 p-6 shadow-neo-md">
                <div className="flex items-center gap-2.5 text-base font-bold text-red-800 mb-4 pb-4 border-b border-red-200">
                  <AlertTriangle size={18} className="text-red-600" />
                  <span>Service Temporarily Unavailable</span>
                </div>
                <p className="text-red-700 text-sm leading-relaxed whitespace-pre-wrap">{raw}</p>
              </div>
            )}

            {generalAdvice && (
              <div className="rounded-2xl border border-neutral-200 bg-gradient-to-br from-purple-50 to-white p-6 shadow-neo-md">
                <div className="flex items-center gap-2.5 text-base font-bold text-neutral-900 mb-4 pb-4 border-b border-neutral-200">
                  <AlertTriangle size={18} className="text-maroon-600" />
                  <span>General Medication Advice</span>
                </div>
                <p className="text-neutral-700 text-sm leading-relaxed whitespace-pre-wrap">{generalAdvice}</p>
              </div>
            )}

            <ChatBox
              history={chatHistory}
              onSend={handleChat}
              loading={chatLoading}
              language={language}
            />
          </div>
        )}
      </div>
      {result && <FeedbackButton reportType="Prescription"/>}
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