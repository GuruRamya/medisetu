import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> str:
    """Simple LLM call with basic error handling"""
    if not prompt or not prompt.strip():
        return "Sorry, the input was empty. Please provide the medical report."
    try:
        if not os.getenv("GROQ_API_KEY"):
            return "GROQ API key is missing. Please check your .env file."
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        content = response.choices[0].message.content.strip()
        return content if content else "Sorry, I couldn't generate a response. Please try again."
    except Exception as e:
        err = str(e).lower()
        if "api key" in err or "401" in err:
            return "API key error. Please check your GROQ key in .env file."
        elif "429" in err or "rate limit" in err:
            return "AI service is busy. Please wait a few seconds and try again."
        elif "timeout" in err or "connection" in err:
            return "Connection problem. Please check internet and try again."
        else:
            return "Something went wrong. Please try again."


def analyse_report(report_text: str, report_type: str, language: str, gender: str = "default") -> dict:
    lang_instruction = {
        "English": "Respond ONLY in English.",
        "Telugu": "Respond ONLY in Telugu.",
        "Hindi": "Respond ONLY in Hindi (Devanagari script). Do NOT use English. Do NOT mix languages."
    }.get(language, "Respond in English.")
    engine_results = None
    engine_summary = ""
    if report_type == "Blood Report":
        from medical_engine import analyse_blood_report_engine, format_engine_results_for_llm
        engine_results = analyse_blood_report_engine(report_text, gender)
        engine_summary = format_engine_results_for_llm(engine_results)

    prompt = f"""
You are MediSetu — a compassionate medical AI assistant that explains medical reports 
to patients in simple, warm, human language like a trusted friend who happens to 
know medicine. Never sound robotic or clinical.

{lang_instruction}

Report Type: {report_type}

{f"RULE-BASED VALIDATION RESULTS (these are mathematically verified — trust these fully):{chr(10)}{engine_summary}{chr(10)}" if engine_summary else ""}

Original Report Data:
{report_text}

IMPORTANT: If rule-based validation results are provided above, use them as the 
ground truth for all values and statuses. Do NOT override these with your own 
judgment on normal ranges. Your job is to EXPLAIN these results warmly, not to 
re-evaluate them.

Now provide a COMPLETE analysis in this EXACT structure:

---PLAIN_EXPLANATION---
Explain what this report means in simple language. For each value/finding:
- What it is (in simple words)
- The normal minimum and maximum range
- Where this patient stands (low/normal/high)
- What this means for their body right now
- Why they might have gotten this value (causes)
- What they should do about it (lifestyle, diet, habits)
Write this warmly, like explaining to a family member.

---RED_FLAGS---
List ONLY the abnormal values. For each one:
- Value name and patient's result
- Normal range
- Danger level: DANGER / MONITOR / MILD
- What this means and why it needs attention
If nothing is abnormal, write: "All values are within normal range."

---DOCTOR_ADVICE---
Based on the overall report, clearly state ONE of these:
- IMMEDIATE: Must see a doctor within 24-48 hours (explain why)
- MONITOR: Can manage for now, consult within 6-12 months (explain why)
- STABLE: No doctor visit needed right now (explain why)
Then list 5 smart questions they should ask their doctor if they visit.

---DIET_SUGGESTIONS---
Based on their specific values, suggest:
- Foods to eat more of (with reasons)
- Foods to avoid (with reasons)
- Simple lifestyle changes
Write this practically for an Indian household.
"""

    llm_response = call_llm(prompt)
    return {
        "llm_response": llm_response,
        "engine_results": engine_results
    }


def analyse_prescription(report_text: str, language: str) -> str:
    lang_instruction = {
        "English": "Respond in English.",
        "Telugu": "Respond in Telugu language.",
        "Hindi": "Respond in Hindi language."
    }.get(language, "Respond in English.")
    from medical_engine import analyse_prescription_engine
    engine = analyse_prescription_engine(report_text)
    engine_note = ""
    if engine["high_risk_drugs"]:
        engine_note += f"RULE-BASED ALERT: High risk drugs detected: {', '.join(engine['high_risk_drugs'])}. These need careful monitoring.\n"
    if engine["controlled_substances"]:
        engine_note += f"RULE-BASED ALERT: Controlled substances detected: {', '.join(engine['controlled_substances'])}. Warn patient about dependency risk.\n"
    if engine["pregnancy_caution"]:
        engine_note += f"RULE-BASED ALERT: Pregnancy caution drugs detected: {', '.join(engine['pregnancy_caution'])}. Warn if patient is pregnant.\n"
    if not engine_note:
        engine_note = "RULE-BASED SCAN: No high risk drugs detected in this prescription.\n"

    prompt = f"""
You are MediSetu — a compassionate medical AI that explains prescriptions to patients 
in simple, warm language.

{lang_instruction}

{engine_note}

Prescription Data:
{report_text}

IMPORTANT: If rule-based alerts are mentioned above, make sure to include 
appropriate warnings in the relevant drug cards. Do not ignore flagged drugs.

List EACH drug separately. For every drug use this format EXACTLY:

---DRUG---
Name: [drug name]
Dosage: [dosage and timing]
Purpose: [what this drug is for in simple words]
How it works: [simple explanation]
Side effects: [common side effects to watch for]
Precautions: [what to avoid while taking this]
---END_DRUG---

After all drugs, add:
---GENERAL_ADVICE---
Any general advice about taking these medicines together.
"""
    return call_llm(prompt)


def chat_with_report(report_text: str, user_question: str, language: str, chat_history: list) -> str:
    lang_instruction = {
        "English": "Respond in English.",
        "Telugu": "Respond in Telugu language.",
        "Hindi": "Respond in Hindi language."
    }.get(language, "Respond in English.")
    history_text = "\n".join([
        f"{m['role'].upper()}: {m['content']}" 
        for m in chat_history[-6:]
    ])

    prompt = f"""
You are MediSetu — a warm, helpful medical AI assistant. The patient has uploaded 
their medical report and is asking questions about it. Answer based on THEIR specific 
data only. Be warm, simple, never scary.

{lang_instruction}

Their Report:
{report_text}

Conversation so far:
{history_text}

Patient's question: {user_question}

Answer their question based on their report data. Keep it simple and reassuring.
"""
    return call_llm(prompt)

def analyse_radiology(report_text: str, language: str) -> str:
    lang_instruction = {
        "English": "Respond in English.",
        "Telugu": "Respond in Telugu language.",
        "Hindi": "Respond in Hindi language."
    }.get(language, "Respond in English.")
    from medical_engine import analyse_radiology_engine
    engine = analyse_radiology_engine(report_text)
    engine_note = ""
    if engine["DANGER"]:
        engine_note = f"RULE-BASED SCAN DETECTED HIGH RISK KEYWORDS: {', '.join(engine['DANGER'])}. Overall risk: {engine['overall_risk']}. Treat these findings seriously.\n"
    elif engine["MONITOR"]:
        engine_note = f"RULE-BASED SCAN DETECTED NOTABLE KEYWORDS: {', '.join(engine['MONITOR'])}. Overall risk: {engine['overall_risk']}. Monitor these findings.\n"
    elif engine["MILD"]:
        engine_note = f"RULE-BASED SCAN DETECTED MILD KEYWORDS: {', '.join(engine['MILD'])}. Overall risk: {engine['overall_risk']}.\n"
    else:
        engine_note = "RULE-BASED SCAN: No concerning keywords detected. Report appears normal.\n"

    prompt = f"""
You are MediSetu — a compassionate medical AI assistant that explains radiology 
reports to patients in simple, warm, human language like a trusted friend.
Never use scary medical jargon. Always be reassuring but honest.

{lang_instruction}

{engine_note}

Radiology Report:
{report_text}

IMPORTANT: Use the rule-based scan results above as a guide for risk level.
Do not downplay findings that the rule-based scan flagged as high risk.

Provide a COMPLETE analysis in this EXACT structure:

---PLAIN_EXPLANATION---
Explain what this radiology report means in simple language:
- What body part was examined and why
- What the radiologist found (in simple words)
- What is normal vs what was observed
- What these findings mean for the patient's body
- Why they might have these findings (possible causes)
Write this warmly like explaining to a worried family member.

---RED_FLAGS---
List ONLY the concerning findings. For each one:
- Finding name in simple words
- What it means
- Danger level: DANGER / MONITOR / MILD
- Why it needs attention
If nothing is concerning write: "All findings are within normal range."

---DOCTOR_ADVICE---
Based on the overall report clearly state ONE of:
- IMMEDIATE: Must see a doctor within 24-48 hours (explain why)
- MONITOR: Can manage for now, consult within 6-12 months (explain why)
- STABLE: No doctor visit needed right now (explain why)
Then list 5 smart questions they should ask their doctor if they visit.

---LIFESTYLE_SUGGESTIONS---
Based on the findings suggest:
- Activities to do or avoid
- Breathing exercises if relevant
- Posture or movement tips
- General wellness advice
Write practically for an Indian lifestyle.
"""
    return call_llm(prompt)

def analyse_skin(input_data, language: str) -> str:
    lang_instruction = {
        "English": "Respond in English.",
        "Telugu": "Respond in Telugu language.",
        "Hindi": "Respond in Hindi language."
    }.get(language, "Respond in English.")
    if isinstance(input_data, bytes):
        import base64
        base64_image = base64.b64encode(input_data).decode('utf-8')
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": f"""You are MediSetu — a compassionate medical AI that analyses skin conditions 
and explains them to patients in simple warm language like a trusted friend.

{lang_instruction}

IMPORTANT: This patient may have a darker South Asian skin tone. Make sure your 
analysis is accurate for ALL skin tones including dark brown and black skin tones. 
Many skin conditions present differently on darker skin — account for this carefully.
Also specifically check for any signs of skin cancer — asymmetry, border irregularity, 
color variation, diameter, evolution over time.

Analyse this skin image and provide a COMPLETE response in this EXACT structure:

---PLAIN_EXPLANATION---
Explain what you observe in simple language:
- What type of skin condition this appears to be
- What it looks like and where it appears
- How common this condition is
- What typically causes this condition
- Whether this is related to darker skin tone specifically
Write warmly like explaining to a family member.

---RED_FLAGS---
List concerning signs. For each one:
- What you observed
- Why it is concerning
- Danger level: DANGER / MONITOR / MILD
If nothing concerning write: "No urgent red flags observed."

---TRIAGE---
Clearly state ONE of:
- IMMEDIATE: Must see a dermatologist within 24-48 hours
- SOON: See a doctor within 2-4 weeks
- MONITOR: Watch for changes, no rush
- STABLE: Likely harmless, no doctor needed
Then list 5 smart questions to ask the dermatologist.

---SKIN_CARE---
Suggest:
- How to care for this at home
- What to avoid
- Safe home remedies for Indian household
- Warning signs that mean it is getting worse

Always remind this is AI observation only — not a medical diagnosis."""
                        }
                    ]
                }
            ],
            max_tokens=4000,
            temperature=0.7
        )
        return response.choices[0].message.content
    else:
        from medical_engine import analyse_skin_engine
        engine = analyse_skin_engine(input_data)
        engine_note = ""
        if engine["overall_risk"] == "HIGH":
            engine_note = f"RULE-BASED CANCER SCREENING ALERT: High risk signals detected: {', '.join(engine['high_risk_signals'])}. ABCDE flags: {list(engine['abcde_flags'].keys())}. This needs immediate dermatologist attention.\n"
        elif engine["overall_risk"] == "MEDIUM":
            engine_note = f"RULE-BASED SCAN: Medium risk signals detected: {', '.join(engine['medium_risk_signals'])}. Monitor carefully.\n"
        else:
            engine_note = "RULE-BASED SCAN: No high risk signals detected from description.\n"
        prompt = f"""You are MediSetu — a compassionate medical AI that analyses skin conditions 
and explains them to patients in simple warm language like a trusted friend.

{lang_instruction}

{engine_note}

Patient's skin condition description:
{input_data}

IMPORTANT: Use the rule-based scan results above as a guide for risk level.
If high risk signals were detected, do not downplay them. Be honest but kind.
This patient may have a darker South Asian skin tone — account for this carefully.

Provide a COMPLETE response in this EXACT structure:

---PLAIN_EXPLANATION---
Explain what this condition likely is:
- Most likely skin condition based on description
- What it means for the patient
- How common it is and what causes it
- Whether darker skin tone affects presentation
Write warmly like explaining to a worried family member.

---RED_FLAGS---
List any concerning signs. For each:
- What the concerning sign is
- Why it needs attention
- Danger level: DANGER / MONITOR / MILD
If nothing concerning write: "No urgent red flags observed."

---TRIAGE---
Clearly state ONE of:
- IMMEDIATE: Must see a dermatologist within 24-48 hours
- SOON: See a doctor within 2-4 weeks
- MONITOR: Watch for changes, no rush
- STABLE: Likely harmless, no doctor needed
Then list 5 smart questions to ask the dermatologist.

---SKIN_CARE---
Suggest:
- Home care tips
- What to avoid
- Safe home remedies for Indian household
- Warning signs that mean it is getting worse

Always remind this is AI observation only — not a medical diagnosis."""

        return call_llm(prompt)