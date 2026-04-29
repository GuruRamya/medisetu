import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyseRadiology, sendChat, extractSection } from '../api'
import {
  PageHeader, LanguageSelector, InputMethodTabs,
  FileDropZone, TextInput, AnalyseButton,
  SectionCard, RedFlagsCard, DoctorAdviceCard, ChatBox
} from '../components/shared'
import { ArrowLeft, AlertCircle } from 'lucide-react'
import { FeedbackButton } from '../components/FeedbackButton'

export default function RadiologyPage() {
  const nav = useNavigate()
  const [method, setMethod] = useState('Upload PDF')
  const [file, setFile] = useState(null)
  const [text, setText] = useState('')
  const [language, setLanguage] = useState('English')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [chatHistory, setChatHistory] = useState([])
  const [chatLoading, setChatLoading] = useState(false)

  async function handleAnalyse() {
    if (!file && !text.trim()) return setError('Please upload a file or enter report text.')
    setError('')
    setLoading(true)
    setResult(null)
    try {
      const data = await analyseRadiology({ file, text: text || undefined, language })
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
  const doctor = extractSection(raw, '---DOCTOR_ADVICE---', '---LIFESTYLE_SUGGESTIONS---')
  const lifestyle = extractSection(raw, '---LIFESTYLE_SUGGESTIONS---')
  return (
    <div className="min-h-screen bg-white relative overflow-hidden">
      {/* Background decoration */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-100/20 rounded-full blur-3xl animate-pulse" />
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
          icon="🫁"
          title="Radiology"
          highlight="Report"
          subtitle="Complete radiology analysis — X-ray, MRI, CT scan, ultrasound. Every finding explained in simple language."
        />

        {!result ? (
          // Input Section
          <div className="space-y-6 mb-12">
            {/* Input Method */}
            <div className="rounded-2xl border border-neutral-200 bg-white p-8 backdrop-blur-xl shadow-neo-md">
              <div className="flex items-center gap-3 mb-6 pb-6 border-b border-neutral-200">
                <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold">
                  📤
                </div>
                <h3 className="font-bold text-lg text-neutral-900">Step 1: Upload Your Report</h3>
              </div>
              <div className="space-y-4">
                <InputMethodTabs
                  options={['Upload PDF', 'Upload Report Image', 'Type / Paste Text']}
                  value={method}
                  onChange={m => { setMethod(m); setFile(null); setText('') }}
                />
                <div className="mt-6">
                  {method === 'Upload PDF' && (
                    <FileDropZone
                      accept=".pdf"
                      label="Click to upload your radiology report PDF"
                      sublabel="Upload the written report (not the scan image itself)"
                      onChange={setFile}
                      fileName={file?.name}
                    />
                  )}
                  {method === 'Upload Report Image' && (
                    <FileDropZone
                      accept=".jpg,.jpeg,.png"
                      label="Click to upload the report image"
                      sublabel="Upload the written report text (not the scan image)"
                      onChange={setFile}
                      fileName={file?.name}
                    />
                  )}
                  {method === 'Type / Paste Text' && (
                    <TextInput
                      value={text}
                      onChange={setText}
                      placeholder={"Chest X-Ray Report\nFindings: The lung fields appear clear bilaterally.\nThe cardiac silhouette is within normal limits.\nNo evidence of pleural effusion or pneumothorax.\nImpression: Normal chest X-ray."}
                    />
                  )}
                </div>
              </div>
            </div>
            {/* Language Selection */}
            <div className="rounded-2xl border border-neutral-200 bg-white p-8 backdrop-blur-xl shadow-neo-md">
              <div className="flex items-center gap-3 mb-6 pb-6 border-b border-neutral-200">
                <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold">
                  🌐
                </div>
                <h3 className="font-bold text-lg text-neutral-900">Step 2: Choose Your Language</h3>
              </div>
              <LanguageSelector value={language} onChange={setLanguage} />
            </div>
            {error && (
              <div className="rounded-xl border border-blue-300 bg-blue-50 p-4 text-blue-700 text-sm flex items-start gap-3 shadow-neo-sm">
                <AlertCircle size={18} className="flex-shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}
            <AnalyseButton
              onClick={handleAnalyse}
              loading={loading}
              label="Analyse My Radiology Report"
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
            {plain && <SectionCard icon="📋" title="Plain Explanation" accent="neutral">{plain}</SectionCard>}
            {flags && <RedFlagsCard text={flags} />}
            {doctor && <DoctorAdviceCard text={doctor} />}
            {lifestyle && <SectionCard icon="🏃" title="Lifestyle Suggestions" accent="neutral">{lifestyle}</SectionCard>}
            <ChatBox
              history={chatHistory}
              onSend={handleChat}
              loading={chatLoading}
              language={language}
            />
          </div>
        )}
      </div>
      {result && <FeedbackButton reportType="Radiology" />}
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