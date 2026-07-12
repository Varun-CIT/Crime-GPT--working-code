import os
import json
import shutil
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Form, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime

from database import init_db, db_cursor, get_case, get_all_cases
from auth import authenticate_user, create_access_token, get_current_user, require_role
from hash_chain import compute_hash, GENESIS_HASH
from citation_verification import verify_citation

from ai.whisper_service import transcribe_audio_bytes
from ai.llm_service import generate_fir_draft

app = FastAPI(title="CrimeGPT Unified API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.on_event("startup")
def startup():
    init_db()

# --- AUTH ---
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(user["username"], user["role"])
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}

@app.get("/me")
def read_current_user(user: dict = Depends(get_current_user)):
    return user

# --- AUDIT HELPER ---
def _write_audit_entry(case_id: str, actor_username: str, actor_role: str, action: str, data_snapshot: dict):
    with db_cursor() as cur:
        cur.execute("SELECT record_hash FROM audit_log WHERE case_id = ? ORDER BY id DESC LIMIT 1", (case_id,))
        row = cur.fetchone()
        prev_hash = row["record_hash"] if row else GENESIS_HASH

        cur.execute("SELECT datetime('now') as ts")
        timestamp = cur.fetchone()["ts"]

        record_hash = compute_hash(prev_hash, actor_username, action, data_snapshot, timestamp)

        cur.execute("""
            INSERT INTO audit_log (case_id, actor_username, actor_role, action, data_snapshot, timestamp, prev_hash, record_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (case_id, actor_username, actor_role, action, json.dumps(data_snapshot, sort_keys=True), timestamp, prev_hash, record_hash))

# --- CITIZEN INTAKE ---
@app.post("/api/cases", status_code=status.HTTP_201_CREATED)
async def create_new_case(
    citizen_username: str = Form(...),
    citizen_phone: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    audio: Optional[UploadFile] = File(None)
):
    # Generate unique case ID
    year = datetime.now().year
    with db_cursor() as cur:
        cur.execute("SELECT case_id FROM fir_records ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        next_num = 1
        if row:
            try:
                next_num = int(row["case_id"].split("-")[-1]) + 1
            except:
                pass
        case_id = f"CGPT-{year}-{next_num:04d}"

    # Handle Audio / Transcription
    saved_audio_name = None
    transcript_text = description
    if audio and audio.filename:
        ext = os.path.splitext(audio.filename)[1]
        saved_audio_name = f"{case_id}_voice{ext}"
        dest_path = os.path.join(UPLOAD_DIR, saved_audio_name)
        content = await audio.read()
        with open(dest_path, "wb") as buffer:
            buffer.write(content)
        
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            transcript_text = transcribe_audio_bytes(content, audio.filename, api_key=api_key)
        except Exception as e:
            print(f"Transcription failed: {e}")

    # Generate FIR Draft via AI
    fir_draft = None
    suggested_section = None
    cognizable = 1
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        fir_draft = generate_fir_draft(transcript_text, api_key=api_key)
        suggested_section = ", ".join(fir_draft.get("suggested_bns_sections", []))
        cognizable = 1 if fir_draft.get("cognizable", True) else 0
    except Exception as e:
        print(f"FIR Generation failed: {e}")

    # Save to DB
    with db_cursor() as cur:
        cur.execute("""
            INSERT INTO fir_records 
            (case_id, citizen_username, citizen_phone, subject, description, audio_file, category, suggested_section, cognizable, fir_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (case_id, citizen_username, citizen_phone, subject, transcript_text, saved_audio_name, category, suggested_section, cognizable, json.dumps(fir_draft) if fir_draft else None))

    data_snapshot = {
        "case_id": case_id, "subject": subject, "description": transcript_text, "category": category
    }
    _write_audit_entry(case_id, citizen_username, "citizen", "FIR_SUBMITTED", data_snapshot)
    
    return {"case_id": case_id, "status": "Submitted"}

# --- OFFICER QUEUE & REVIEW ---
@app.get("/api/cases")
def read_all_cases():
    return get_all_cases()

class ReviewPayload(BaseModel):
    status: str
    remarks: str
    officer_username: str

@app.post("/api/cases/{case_id}/review")
def review_case(case_id: str, payload: ReviewPayload):
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    with db_cursor() as cur:
        cur.execute("""
            UPDATE fir_records 
            SET status = ?, officer_username = ?, updated_at = datetime('now')
            WHERE case_id = ?
        """, (payload.status, payload.officer_username, case_id))

    data_snapshot = {"status": payload.status, "remarks": payload.remarks}
    _write_audit_entry(case_id, payload.officer_username, "officer", f"OFFICER_REVIEW:{payload.status}", data_snapshot)

    return {"success": True, "case_id": case_id}

# --- CITATIONS ---
class CitationRequest(BaseModel):
    citation_text: str
    quoted_paragraph: Optional[str] = ""

@app.post("/api/verify_citation")
def check_citation(payload: CitationRequest):
    return verify_citation(payload.citation_text, payload.quoted_paragraph)
