import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database setting
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crimegpt_unified.db")

# FastAPI Settings
API_HOST = "127.0.0.1"
API_PORT = 8000

# BNS / BNSS timelines
COGNIZABLE_TIMELINE = [
    "Complaint Submitted",
    "FIR Registered",
    "Cognizance Taken",
    "Investigation Assigned",
    "Evidence Collection",
    "Suspect Identification",
    "Property Recovery",
    "Charge Sheet Filed",
    "Court Trial",
    "Judgment"
]

NON_COGNIZABLE_TIMELINE = [
    "Complaint Submitted",
    "GD Entry Created",
    "NC Entry Registered",
    "Magistrate Referral",
    "Closed"
]

# Progress mapping for timelines
COGNIZABLE_PROGRESS = {
    "Complaint Submitted": 10,
    "FIR Registered": 20,
    "Cognizance Taken": 30,
    "Investigation Assigned": 40,
    "Evidence Collection": 50,
    "Suspect Identification": 60,
    "Property Recovery": 70,
    "Charge Sheet Filed": 80,
    "Court Trial": 90,
    "Judgment": 100
}

NON_COGNIZABLE_PROGRESS = {
    "Complaint Submitted": 20,
    "GD Entry Created": 40,
    "NC Entry Registered": 60,
    "Magistrate Referral": 80,
    "Closed": 100
}
