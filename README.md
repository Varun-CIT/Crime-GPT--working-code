# 🚔 CrimeGPT Unified

**AI-Assisted FIR Generation & Officer Review System**  
*KANAD Shield Gujarat Hackathon Prototype*

## Features
- 👤 Citizen complaint submission (Text/Voice)
- 📍 Complaint status tracking
- 👮 Officer dashboard with complaint queue
- 🤖 AI-generated FIR drafting
- ✅ Human review & approval workflow
- 📚 Citation verification

## Tech Stack
- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** Python, FastAPI
- **Database:** SQLite
- **AI:** LLM-based FIR generation & speech-to-text

## Project Structure

```text
CrimeGPT-Unified/
├── backend/
├── frontend_citizen/
├── frontend_officer/
├── requirements.txt
├── run_all.py
└── README.md
```

## Installation

```bash
pip install -r requirements.txt

cd frontend_citizen
npm install

cd ../frontend_officer
npm install
```

## Run

```bash
python run_all.py
```

## Disclaimer

This is a hackathon prototype built for the **KANAD Shield Gujarat Hackathon**. AI assists in drafting FIRs, while the final decision always remains with the officer.
