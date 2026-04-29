import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyseSkin, sendChat, extractSection } from '../api'
import {
  PageHeader, LanguageSelector, InputMethodTabs,
  FileDropZone, TextInput, AnalyseButton,
  SectionCard, RedFlagsCard, ChatBox
} from '../components/shared'
import { ArrowLeft, AlertCircle, Camera } from 'lucide-react'
import { FeedbackButton } from '../components/FeedbackButton'
function TriageCard({ text }) {
  const isImmediate = text.includes('IMMEDIATE')
  const isSoon = text.includes('SOON')
  const isMonitor = text.includes('MONITOR')
  const style = isImmediate
    ? 'border-red-300 bg-red-50 shadow-neo-md'
    : isSoon
    ? 'border-yellow-300 bg-yellow-50 shadow-neo-md'
    : isMonitor
    ? 'border-orange-300 bg-orange-50 shadow-neo-md'
    : 'border-green-300 bg-green-50 shadow-neo-md'
  const icon = isImmediate ? '🚨' : isSoon ? '⚠️' : isMonitor ? '🟡' : '✨'
  const color = isImmediate ? 'text-red-700' : isSoon ? 'text-yellow-700' : isMonitor ? 'text-orange-700' : 'text-green-700'
  return (
    <div className={`rounded-2xl border p-6 mb-5 ${style}`}>
      <div className={`flex items-center gap-2.5 text-base font-bold mb-4 pb-4 border-b border-neutral-200 ${color}`}>
        <span className="text-xl">{icon}</span>
        <span>Should You See a Doctor?</span>
      </div>
      <div className="text-neutral-700 text-sm leading-relaxed whitespace-pre-wrap font-light">{text}</div>
    </div>
  )
}
export default function SkinPage() {
  const nav = useNavigate()
  const [method, setMethod] = useState('Upload Image')
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [text, setText] = useState('')
  const [language, setLanguage] = useState('English')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [chatHistory, setChatHistory] = useState([])
  const [chatLoading, setChatLoading] = useState(false)
  const videoRef = useRef(null)
  const [cameraActive, setCameraActive] = useState(false)
  function handleFileChange(f) {
    setFile(f)
    if (f) setPreview(URL.createObjectURL(f))
  }
  async function startCamera() {
    setCameraActive(true)
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      if (videoRef.current) videoRef.current.srcObject = stream
    } catch {
      setError('Camera access denied. Please allow camera permission.')
      setCameraActive(false)
    }
  }
  function captureCamera() {
    const canvas = document.createElement('canvas')
    canvas.width = videoRef.current.videoWidth
    canvas.height = videoRef.current.videoHeight
    canvas.getContext('2d').drawImage(videoRef.current, 0, 0)
    canvas.toBlob(blob => {
      const f = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' })
      setFile(f)
      setPreview(canvas.toDataURL())
      setCameraActive(false)
      videoRef.current.srcObject?.getTracks().forEach(t => t.stop())
    }, 'image/jpeg')
  }
  async function handleAnalyse() {
    if (!file && !text.trim()) return setError('Please upload an image or describe your condition.')
    setError('')
    setLoading(true)
    setResult(null)
    try {
      const data = await analyseSkin({ file, text: text || undefined, language })
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
      const data = await sendChat({
        reportText: `Skin analysis result: ${result.llm_response?.slice(0, 500)}`,
        question,
        language,
        chatHistory
      })
      setChatHistory([...newHistory, { role: 'bot', content: data.reply }])
    } catch {
      setChatHistory([...newHistory, { role: 'bot', content: 'Sorry, could not process that.' }])
    } finally {
      setChatLoading(false)
    }
  }
  const raw = result?.llm_response || ''
  const plain = extractSection(raw, '---PLAIN_EXPLANATION---', '---RED_FLAGS---')
  const flags = extractSection(raw, '---RED_FLAGS---', '---TRIAGE---')
  const triage = extractSection(raw, '---TRIAGE---', '---SKIN_CARE---')
  const skincare = extractSection(raw, '---SKIN_CARE---')
  return (
    <div className="min-h-screen bg-white relative overflow-hidden">
      {/* Background decoration */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-green-100/20 rounded-full blur-3xl animate-pulse" />
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
          icon="🔬"
          title="Skin"
          highlight="Analysis"
          subtitle="Upload a photo, use live camera, or describe your condition — instant triage and personalized care advice."
        />
        {/* Skin tone note */}
        <div className="rounded-xl border border-green-300 bg-green-50 p-3 text-green-800/80 text-xs mb-6 flex items-start gap-2 shadow-neo-sm">
          <span className="text-sm mt-0.5">🌍</span>
          <span>Skin tone aware — our analysis is optimized for all skin tones including darker South Asian skin.</span>
        </div>
        {!result ? (
          // Input Section
          <div className="space-y-6 mb-12">
            {/* Input Method */}
            <div className="rounded-2xl border border-neutral-200 bg-white p-8 backdrop-blur-xl shadow-neo-md">
              <div className="flex items-center gap-3 mb-6 pb-6 border-b border-neutral-200">
                <div className="w-10 h-10 rounded-lg bg-green-600 flex items-center justify-center text-white font-bold">
                  📤
                </div>
                <h3 className="font-bold text-lg text-neutral-900">Step 1: Provide Your Skin Photo or Description</h3>
              </div>
              <div className="space-y-4">
                <InputMethodTabs
                  options={['Upload Image', 'Live Camera', 'Text Description']}
                  value={method}
                  onChange={m => {
                    setMethod(m)
                    setFile(null)
                    setPreview(null)
                    setText('')
                    setCameraActive(false)
                  }}
                />
                <div className="mt-6">
                  {method === 'Upload Image' && (
                    <>
                      <FileDropZone
                        accept=".jpg,.jpeg,.png"
                        label="Upload a photo of the affected skin area"
                        sublabel="Clear close-up photo in good lighting works best"
                        onChange={handleFileChange}
                        fileName={file?.name}
                      />
                      {preview && (
                        <div className="mt-4 space-y-3">
                          <img
                            src={preview}
                            alt="Preview"
                            className="w-64 rounded-2xl border border-neutral-300 object-cover shadow-neo-md"
                          />
                          <p className="text-maroon-600 text-sm font-semibold">✓ Image ready for analysis</p>
                        </div>
                      )}
                    </>
                  )}
                  {method === 'Live Camera' && (
                    <div className="text-center space-y-4">
                      {!cameraActive && !file && (
                        <button
                          onClick={startCamera}
                          className="inline-flex items-center gap-2 px-6 py-3 bg-maroon-600 text-white font-bold rounded-xl hover:bg-maroon-700 hover:shadow-neo-lg transition-all shadow-neo-md"
                        >
                          <Camera size={18} />
                          Open Camera
                        </button>
                      )}
                      {cameraActive && (
                        <div className="space-y-4">
                          <video
                            ref={videoRef}
                            autoPlay
                            playsInline
                            className="w-full max-w-sm mx-auto rounded-2xl border-2 border-neutral-300 shadow-neo-md"
                          />
                          <button
                            onClick={captureCamera}
                            className="inline-flex items-center gap-2 px-6 py-3 bg-maroon-600 text-white font-bold rounded-xl hover:bg-maroon-700 hover:shadow-neo-lg transition-all shadow-neo-md"
                          >
                            <Camera size={18} />
                            Capture Photo
                          </button>
                        </div>
                      )}
                      {preview && !cameraActive && (
                        <div className="space-y-3">
                          <img
                            src={preview}
                            alt="Captured"
                            className="w-64 mx-auto rounded-2xl border border-neutral-300 shadow-neo-md"
                          />
                          <p className="text-maroon-600 text-sm font-semibold">✓ Photo captured successfully</p>
                          <button
                            onClick={() => {
                              setFile(null)
                              setPreview(null)
                            }}
                            className="text-maroon-600 hover:text-maroon-700 text-sm font-semibold transition-colors"
                          >
                            Retake
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                  {method === 'Text Description' && (
                    <TextInput
                      value={text}
                      onChange={setText}
                      placeholder="Describe your skin condition: Location, size, color, texture, duration, whether it's itchy/painful, any recent changes..."
                      rows={5}
                    />
                  )}
                </div>
              </div>
            </div>
            {/* Language Selection */}
            <div className="rounded-2xl border border-neutral-200 bg-white p-8 backdrop-blur-xl shadow-neo-md">
              <div className="flex items-center gap-3 mb-6 pb-6 border-b border-neutral-200">
                <div className="w-10 h-10 rounded-lg bg-green-600 flex items-center justify-center text-white font-bold">
                  🌐
                </div>
                <h3 className="font-bold text-lg text-neutral-900">Step 2: Choose Your Language</h3>
              </div>
              <LanguageSelector value={language} onChange={setLanguage} />
            </div>
            {error && (
              <div className="rounded-xl border border-green-300 bg-green-50 p-4 text-green-700 text-sm flex items-start gap-3 shadow-neo-sm">
                <AlertCircle size={18} className="flex-shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}
            <AnalyseButton
              onClick={handleAnalyse}
              loading={loading}
              label="Analyse My Skin Condition"
              icon="🔬"
            />
          </div>
        ) : (
          // Results Section
          <div className="space-y-8 mb-12">
            <div className="flex items-center justify-between">
              <h2 className="font-display text-4xl font-bold text-neutral-900 flex items-center gap-3">
                <span className="text-3xl">🔬</span> Your Skin Analysis
              </h2>
              <button
                onClick={() => setResult(null)}
                className="px-4 py-2 rounded-lg text-sm font-semibold text-maroon-600 hover:bg-maroon-50 transition-all shadow-neo-sm"
              >
                ← New Analysis
              </button>
            </div>
            {plain && <SectionCard icon="📋" title="What We Observed" accent="neutral">{plain}</SectionCard>}
            {flags && <RedFlagsCard text={flags} />}
            {triage && <TriageCard text={triage} />}
            {skincare && (
              <SectionCard icon="🧴" title="Skin Care Advice" accent="neutral">
                {skincare}
              </SectionCard>
            )}
            <div className="rounded-xl border border-red-300 bg-red-50 p-4 text-neutral-700 text-xs flex items-start gap-2 shadow-neo-sm">
              <AlertCircle size={14} className="flex-shrink-0 mt-0.5" />
              <span>⚕️ Medical Disclaimer: This is an AI-based observation only and not a medical diagnosis. Please consult a qualified dermatologist for proper diagnosis and treatment.</span>
            </div>
            <ChatBox
              history={chatHistory}
              onSend={handleChat}
              loading={chatLoading}
              language={language}
            />
          </div>
        )}
      </div>
      {result && <FeedbackButton reportType="Skin" />}
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