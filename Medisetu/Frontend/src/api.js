import axios from 'axios'
const BASE = import.meta.env.VITE_API_URL || '/api'

export async function analyseBlood({ file, text, gender, language }) {
  const fd = new FormData()
  if (file) fd.append('file', file)
  if (text) fd.append('text', text)
  fd.append('gender', gender || 'default')
  fd.append('language', language || 'English')
  const { data } = await axios.post(`${BASE}/blood/analyse`, fd)
  return data
}

export async function analyseRadiology({ file, text, language }) {
  const fd = new FormData()
  if (file) fd.append('file', file)
  if (text) fd.append('text', text)
  fd.append('language', language || 'English')
  const { data } = await axios.post(`${BASE}/radiology/analyse`, fd)
  return data
}

export async function analysePrescription({ file, text, language }) {
  const fd = new FormData()
  if (file) fd.append('file', file)
  if (text) fd.append('text', text)
  fd.append('language', language || 'English')
  const { data } = await axios.post(`${BASE}/prescription/analyse`, fd)
  return data
}

export async function analyseSkin({ file, text, language }) {
  const fd = new FormData()
  if (file) fd.append('file', file)
  if (text) fd.append('text', text)
  fd.append('language', language || 'English')
  const { data } = await axios.post(`${BASE}/skin/analyse`, fd)
  return data
}

export async function sendChat({ reportText, question, language, chatHistory }) {
  const fd = new FormData()
  fd.append('report_text', reportText)
  fd.append('question', question)
  fd.append('language', language || 'English')
  fd.append('chat_history', JSON.stringify(chatHistory || []))
  const { data } = await axios.post(`${BASE}/chat`, fd)
  return data
}

export function extractSection(raw, start, end) {
  try {
    if (!raw || typeof raw !== 'string') return raw || ''
    const startIdx = raw.indexOf(start)
    if (startIdx === -1) return raw.trim()
    const contentStart = startIdx + start.length
    if (end) {
      const endIdx = raw.indexOf(end, contentStart)
      if (endIdx === -1) return raw.slice(contentStart).trim()
      return raw.slice(contentStart, endIdx).trim()
    }
    return raw.slice(contentStart).trim()
  } catch {
    return raw || ''
  }
}