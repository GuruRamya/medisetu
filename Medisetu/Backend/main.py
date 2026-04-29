from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
import os
from fastapi.middleware.cors import CORSMiddleware
import fitz
import pytesseract
import shutil
tesseract_path = shutil.which('tesseract')
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
from PIL import Image
import io
import json
from datetime import datetime
import base64
from typing import Optional
import logging
logging.basicConfig(level=logging.DEBUG)
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from llm import analyse_report, analyse_prescription, analyse_radiology, analyse_skin, chat_with_report
from medical_engine import (
    analyse_blood_report_engine,
    format_engine_results_for_llm,
    analyse_radiology_engine,
    analyse_prescription_engine,
    analyse_skin_engine
)
app = FastAPI(title="MediSetu API", version="1.0.0")
from uuid import uuid4
def custom_key_func(request: Request):
    client_id = getattr(request.state, "client_id", None)
    if client_id:
        return f"user:{client_id}"
    return f"ip:{get_remote_address(request)}"
limiter = Limiter(
    key_func=custom_key_func,
    default_limits=["30/minute"]   
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = logging.getLogger(__name__)
@app.middleware("http")

async def add_anonymous_id(request: Request, call_next):
    client_id = request.cookies.get("client_id")
    if not client_id:
        client_id = str(uuid4())
    request.state.client_id = client_id
    start_time = datetime.now()
    try:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.set_cookie(
            key="client_id",
            value=client_id,
            httponly=True,
            secure=True,  
            samesite="Lax",
            max_age=60 * 60 * 24 * 365
        )
        return response
    finally:
        duration = (datetime.now() - start_time).total_seconds()
        log_data = {
            "event": "request",
            "client_id": client_id,
            "path": request.url.path,
            "method": request.method,
            "duration_sec": duration
        }
        logger.info(f"REQUEST_LOG {json.dumps(log_data)}")  
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_MIME_TYPES = {"application/pdf", "image/jpeg", "image/png", "image/webp", "image/tiff"}

async def validate_and_read_file(file: UploadFile) -> bytes:
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Upload PDF or image only.")
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 5 MB.")
    return file_bytes
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please slow down."}
    )
def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception:
        raise HTTPException(status_code=400, detail="PDF reading failed")   


def extract_text_from_image(file_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        if not text or not text.strip():
            logger.warning("Tesseract returned empty text")
            raise HTTPException(status_code=400, detail="No text found in image. Try a clearer image.")
        return text.strip()
    except pytesseract.TesseractNotFoundError as e:
        logger.error(f"Tesseract NOT FOUND: {str(e)}")
        raise HTTPException(status_code=500, detail="OCR engine not available")
    except pytesseract.TesseractCommandNotFound as e:
        logger.error(f"Tesseract command failed: {str(e)}")
        raise HTTPException(status_code=500, detail="OCR engine error")
    except Exception as e:
        logger.error(f"OCR Exception: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"OCR processing failed: {str(e)}")  


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "MediSetu API"}


@app.post("/api/blood/analyse")
@limiter.limit("25/minute")
async def analyse_blood(
    request: Request,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    gender: str = Form("default"),
    language: str = Form("English"),
):
    report_text = ""
    if file:
        file_bytes = await validate_and_read_file(file)
        if file.content_type == "application/pdf":
            report_text = extract_text_from_pdf(file_bytes)
            if not report_text:
                raise HTTPException(status_code=400, detail="PDF appears to be scanned. Please upload an image or type values.")
        elif file.content_type.startswith("image/"):
            report_text = extract_text_from_image(file_bytes)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    elif text:
        report_text = text
    else:
        raise HTTPException(status_code=400, detail="No input provided")
    if not report_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from the provided file")
    engine = analyse_blood_report_engine(report_text)
    try:
        result = analyse_report(report_text, "Blood Report", language, gender)
        llm_response = result.get("llm_response", "")
    except Exception:
        llm_response = "AI analysis failed. Showing basic medical insights."
    return {
        "report_text": report_text,
        "llm_response": llm_response,
        "engine_results": engine,
    } 
    
@app.post("/api/radiology/analyse")
@limiter.limit("15/minute")
async def analyse_radiology_report(
    request: Request,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    language: str = Form("English"),
):
    try:
        report_text = ""
        if file:
            file_bytes = await validate_and_read_file(file)
            if file.content_type == "application/pdf":
                report_text = extract_text_from_pdf(file_bytes)
            elif file.content_type.startswith("image/"):
                report_text = extract_text_from_image(file_bytes)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF or image.")
        elif text:
            report_text = text
        else:
            raise HTTPException(status_code=400, detail="No input provided.")
        if not report_text or not report_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the report.")
        engine = analyse_radiology_engine(report_text)
        try:
            llm_response = analyse_radiology(report_text, language)
        except Exception:
            llm_response = "AI analysis failed. Showing basic radiology insights."
        return {
            "report_text": report_text,
            "llm_response": llm_response,
            "engine_results": engine
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Report format invalid. Make sure it has clear medical findings.")
         
@app.post("/api/prescription/analyse")
@limiter.limit("15/minute")
async def analyse_prescription_route(
    request: Request,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    language: str = Form("English"),
):
    try:
        report_text = ""
        if file:
            file_bytes = await validate_and_read_file(file)
            if file.content_type.startswith("image/"):
                report_text = extract_text_from_image(file_bytes)
            else:
                raise HTTPException(status_code=400, detail="Only image files are supported for prescriptions.")
        elif text:
            report_text = text
        else:
            raise HTTPException(status_code=400, detail="No input provided.")
        if not report_text or not report_text.strip():
            raise HTTPException(status_code=400, detail="Could not read the prescription.")
        engine = analyse_prescription_engine(report_text)
        try:
            llm_response = analyse_prescription(report_text, language)
        except Exception:
            llm_response = "AI analysis failed. Showing basic prescription insights."
        return {
            "report_text": report_text,
            "llm_response": llm_response,
            "engine_results": engine
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Report format invalid. Make sure it has clear medical findings.")
        
@app.post("/api/skin/analyse")
@limiter.limit("15/minute")
async def analyse_skin_route(
    request: Request,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    language: str = Form("English"),
):
    try:
        if file:
            file_bytes = await validate_and_read_file(file)
            try:
                llm_response = analyse_skin(file_bytes, language)
            except Exception:
                llm_response = "AI image analysis failed. Please try again with a clearer image."
            return {
                "mode": "image",
                "llm_response": llm_response
            }
        elif text:
            if not text.strip():
                raise HTTPException(status_code=400, detail="Skin description cannot be empty.")
            engine = analyse_skin_engine(text)
            try:
                llm_response = analyse_skin(text, language)
            except Exception:
                llm_response = "AI analysis failed. Showing basic skin insights."
            return {
                "mode": "text",
                "llm_response": llm_response,
                "engine_results": engine
            }
        else:
            raise HTTPException(status_code=400, detail="No input provided. Please upload image or enter description.")
    except Exception:
        raise HTTPException(status_code=500, detail="Report format invalid. Make sure it has clear medical findings.")


@app.post("/api/chat")
@limiter.limit("15/minute")
async def chat(
    request: Request,
    report_text: str = Form(...),
    question: str = Form(...),
    language: str = Form("English"),
    chat_history: str = Form("[]"),
):
    import json
    try:
        history = json.loads(chat_history)
    except Exception:
        history = []

    reply = chat_with_report(report_text, question, language, history)
    return {"reply": reply}

@app.post("/api/feedback")
@limiter.limit("30/minute")
async def submit_feedback(
    request: Request,
    report_type: str = Form(...),
    feedback_type: str = Form(...),
    feedback_text: str = Form(...)
):
    """Save user feedback to file"""
    try:
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "report_type": report_type,
            "feedback_type": feedback_type,
            "text": feedback_text
        }
        
        feedback_file = "/tmp/feedback.jsonl"
        with open(feedback_file, "a") as f:
            f.write(json.dumps(feedback_entry) + "\n")
        print(f"✓ Feedback saved: {feedback_type} for {report_type}")
        return {
            "status": "success",
            "message": "Thank you for your feedback!"
        }
    except Exception as e:
        print(f"✗ Error saving feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not save feedback")
