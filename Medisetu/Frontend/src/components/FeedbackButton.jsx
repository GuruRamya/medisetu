import { useState } from 'react'
import { MessageCircle, X } from 'lucide-react'
export function FeedbackButton({ reportType }) {
  const [showModal, setShowModal] = useState(false)
  const [feedbackType, setFeedbackType] = useState('suggestion')
  const [feedbackText, setFeedbackText] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  async function handleSubmit() {
    if (!feedbackText.trim()) {
      alert('Please write some feedback')
      return
    }
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('report_type', reportType)
      formData.append('feedback_type', feedbackType)
      formData.append('feedback_text', feedbackText)
      const response = await fetch('/api/feedback', {
        method: 'POST',
        body: formData
      })
      if (response.ok) {
        setSuccess(true)
        setFeedbackText('')
        setTimeout(() => {
          setSuccess(false)
          setShowModal(false)
        }, 2000)
      } else {
        alert('Failed to submit feedback')
      }
    } catch (e) {
      alert('Error: ' + e.message)
    } finally {
      setLoading(false)
    }
  }
  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setShowModal(true)}
        className="fixed bottom-6 right-6 bg-maroon-600 text-white px-5 py-3 rounded-full shadow-neo-lg hover:bg-maroon-700 transition-all duration-300 hover:scale-105 z-40 flex items-center gap-2"
        title="Send feedback"
      >
        <MessageCircle size={20} />
        <span>Feedback</span>
      </button>
      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-neo-lg max-w-md w-full p-6 border border-neutral-200">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-bold text-lg text-neutral-900">Send Feedback</h2>
              <button
                onClick={() => setShowModal(false)}
                className="text-neutral-500 hover:text-neutral-900 transition"
              >
                <X size={18} />
              </button>
            </div>
            {/* Success Message */}
            {success ? (
              <div className="text-center py-8">
                <p className="text-4xl mb-2">🙏</p>
                <p className="text-green-600 font-semibold">Thank you for your feedback!</p>
                <p className="text-neutral-500 text-sm mt-2">We'll improve based on what you said</p>
              </div>
            ) : (
              <>
                {/* Feedback Type Dropdown */}
                <div className="mb-4">
                  <label className="text-sm font-semibold text-neutral-700 mb-2 block">
                    What's your feedback about?
                  </label>
                  <select
                    value={feedbackType}
                    onChange={(e) => setFeedbackType(e.target.value)}
                    className="w-full px-3 py-2 border border-neutral-200 rounded-lg text-neutral-900 bg-white text-sm focus:outline-none focus:border-maroon-500 focus:ring-2 focus:ring-maroon-100"
                  >
                    <option value="bug">🐛 Report a bug</option>
                    <option value="wrong">❌ Wrong analysis</option>
                    <option value="suggestion">💡 Feature suggestion</option>
                    <option value="compliment">⭐ Something great</option>
                    <option value="other">💬 Other</option>
                  </select>
                </div>
                {/* Feedback Text */}
                <div className="mb-4">
                  <label className="text-sm font-semibold text-neutral-700 mb-2 block">
                    Your feedback
                  </label>
                  <textarea
                    value={feedbackText}
                    onChange={(e) => setFeedbackText(e.target.value)}
                    placeholder="Tell us what you think... (be specific)"
                    className="w-full p-3 border border-neutral-200 rounded-lg text-neutral-900 text-sm focus:outline-none focus:border-maroon-500 focus:ring-2 focus:ring-maroon-100 resize-none"
                    rows="4"
                  />
                </div>
                {/* Submit Button */}
                <button
                  onClick={handleSubmit}
                  disabled={loading || !feedbackText.trim()}
                  className="w-full bg-maroon-600 text-white py-2.5 rounded-lg font-semibold text-sm hover:bg-maroon-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  {loading ? 'Sending...' : 'Send Feedback'}
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </>
  )
}