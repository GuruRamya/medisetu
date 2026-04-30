# MediSetu — Medical Report Explainer

Most people get a medical report and have no idea what it means. They either panic, ignore it, or wait days to ask a doctor a simple question. MediSetu tries to fix that — it takes your report and explains it in plain language, like a knowledgeable friend would.
This is a college project built to solve a real problem I noticed around me.

---

## What It Does

You upload or paste a medical report. The system reads it, validates the values, and explains everything back to you in simple language — what each value means, whether it's normal, what you should watch out for, and what questions to ask your doctor. You can also follow up with questions in a chat interface.
It supports **English, Telugu, and Hindi** because that's who actually needs this — people in India who get reports written in medical jargon they were never taught to read.

---

## Four Modules

### 🩸 Blood Report
Upload a PDF, image, or paste values directly. The system runs a rule-based engine first — it mathematically checks every value against verified reference ranges, flags what's abnormal, and tells the LLM exactly what's wrong before it writes the explanation. This way the AI isn't guessing — it's explaining results that were already validated.

Covers CBC, LFT, KFT, thyroid, lipid panel, HbA1c, hormones, cancer markers, and about 80+ parameters total.

### 🫁 Radiology Report
Upload the written radiology report (the text document, not the scan image). The system scans for concerning keywords — things like "hemorrhage", "malignancy", "aortic dissection" — and flags them by risk level before passing to the LLM for a full plain-language explanation.

### 💊 Prescription
Upload a photo of your prescription or type the medicine names. Every drug gets its own card — purpose, dosage, how it works, side effects, what to avoid. High-risk drugs and controlled substances get flagged automatically.

### 🔬 Skin Analysis
Upload a photo or describe your condition in text. For images, it uses a vision-capable model that's specifically prompted to account for darker South Asian skin tones, since many skin conditions present differently and a lot of AI tools are trained mostly on lighter skin. For text descriptions, a rule-based engine checks for cancer risk signals (ABCDE criteria) before the LLM responds.

---

## How It's Built

**Frontend:** React + Vite + Tailwind CSS  
**Backend:** FastAPI (Python)  
**AI:** Groq API — Llama 3.3 70B for text, Llama 4 Scout for vision  
**OCR:** OCR.space API for extracting text from images and PDFs  
**Rate limiting:** SlowAPI — 25 requests/minute for blood reports, 15/minute for others  

The backend has two layers working together:

1. **Rule-based engine** — pure Python logic with no AI involved. Checks blood values against reference ranges, scans radiology reports for red-flag keywords, identifies high-risk drugs in prescriptions. Fast, deterministic, and always correct on what it knows.
2. **LLM layer** — takes the rule engine's output as ground truth and writes the human explanation. The LLM is explicitly told: "these values are mathematically verified, do not override them — your job is to explain them warmly."

This combination matters. If you only used an LLM, it might get reference ranges slightly wrong or be inconsistent. If you only used rules, you'd get dry clinical output with no context. Together they're more useful than either alone.

---

## OCR Approach

Originally tried pytesseract (local Tesseract installation), but it added complexity to deployment and fragile system dependencies. Switched to OCR.space API instead — stateless, works everywhere, no installation needed.

**Trade-off:** Small cost per OCR request, but cleaner architecture and more reliable in production. You need an OCR API key (free tier available, or premium for higher limits).

---

## Why No Machine Learning Model

The skin module was the obvious candidate for ML — train a classifier, detect diseases from images.
The problem is a trained image classifier can only recognize diseases it was trained on. A decent model might cover 20–50 skin conditions. My rule-based engine covers hundreds of conditions through text descriptions, and the vision LLM can reason about conditions it's seen described in medical literature even if it wasn't trained specifically on those images.
If I added an ML classifier, I'd actually be making the system worse — it would become confident about a narrow set of diseases and miss everything else. The current approach, where a vision LLM describes what it sees and the system reasons from that, handles rare and common conditions equally.
This project is also about **explaining reports, not detecting diseases.** That's a meaningful distinction. I'm not trying to diagnose anyone — I'm trying to help them understand what their doctor already wrote.

---

## Why No Login or Authentication

I considered it. The reason I didn't add it: friction.
When someone gets a confusing medical report, they're already stressed. Making them create an account before they can understand their own health information felt wrong. The value of this tool is that you land on it, paste your report, and get an answer in 30 seconds.
There's also nothing to protect here from a user perspective. The system doesn't store reports. There's no personal health data sitting in a database tied to your account. Each request is stateless — the report goes in, the explanation comes out, nothing is saved.
The only thing I do save is a `feedback.jsonl` file where users can optionally submit feedback. That has no personal information in it.

---

## Why No Database

Same reasoning — this is a read-and-leave tool. People come, get their explanation, maybe ask a couple of follow-up questions, and go. There's no use case where they'd come back and need to see their previous reports.
Adding a database would have required adding authentication (to know whose records are whose), which would have added the friction I was trying to avoid. The complexity wouldn't have added value for the actual use case.

---

## Project Structure

```
MEDISETU/
├── Backend/
│   ├── llm.py
│   ├── main.py
│   ├── medical_engine.py
│   ├── render.yaml
│   ├── requirements.txt
│   └── test_api.py
│
└── Frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   │   ├── Blood.jsx
    │   │   ├── Home.jsx
    │   │   ├── Prescription.jsx
    │   │   ├── Radiology.jsx
    │   │   └── Skin.jsx
    │   ├── api.js
    │   ├── App.jsx
    │   ├── index.css
    │   └── main.jsx
    ├── index.html
    ├── package.json
    ├── postcss.config.js
    ├── tailwind.config.js
    └── vite.config.js
```

---

## Running It Locally

**Backend**

```bash
pip install -r requirements.txt

# Create a .env file
echo "GROQ_API_KEY=your_key_here" > .env
echo "OCR_API_KEY=your_ocr_space_key_here" >> .env

uvicorn main:app --reload
```

**API Keys:**
- **GROQ_API_KEY:** Free from [console.groq.com](https://console.groq.com)
- **OCR_API_KEY:** Free tier at [ocr.space](https://ocr.space/ocrapi), or use the free API without a key (rate limited)

**Frontend**

```bash
npm install
npm run dev
```

The frontend runs on `localhost:5173` and proxies API calls to `localhost:8000`.

---

## Deployment

Currently deployed on Render (see `render.yaml`). The setup is straightforward:

- Set `GROQ_API_KEY` and `OCR_API_KEY` as environment variables in Render
- The `startCommand` runs the FastAPI server on the assigned port

**Docker Note:** Explored Docker for containerization, but Render's free tier doesn't support it without upgrading to a paid plan. Since the current setup works cleanly without it, keeping the simpler deployment path.

---

## Tests

```bash
pip install pytest httpx
pytest test_api.py -v
```

Tests cover all four analysis endpoints, file upload validation, rate limiting, and the chat endpoint.

---

## Limitations

- OCR accuracy depends on image quality. Blurry, skewed, or low-contrast scans may have extraction errors.
- The system explains reports — it does not diagnose. Every response reminds the user to consult a doctor.
- Radiology analysis is NLP on the written report, not computer vision on the actual scan images.
- Responses are only as good as the input. A poorly scanned or unclear report will produce a weaker explanation.
- API calls are rate-limited (25 requests/minute for blood reports, 15/minute for others) to prevent abuse and keep costs stable.

---

## Disclaimer

MediSetu is an educational tool. It explains medical reports in simple language — it is not a substitute for professional medical advice. Always consult a qualified doctor for diagnosis and treatment decisions.

*Built by a CS student who got tired of watching family members stare blankly at lab reports.*  
*No medical reports are permanently stored by the system.*
