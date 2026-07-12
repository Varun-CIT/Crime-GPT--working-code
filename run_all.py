import subprocess
import sys
import time
import os

def run_servers():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_dir, "backend")
    citizen_dir = os.path.join(project_dir, "frontend_citizen")
    officer_dir = os.path.join(project_dir, "frontend_officer")

    print("[*] Starting CrimeGPT Unified Stack...")

    # Launch backend (FastAPI)
    print("[-] Launching FastAPI Backend on http://127.0.0.1:8000 ...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=backend_dir
    )
    time.sleep(2)

    # Launch Citizen Frontend (React/Vite on port 8501)
    print("[-] Launching Citizen Portal on http://localhost:8501 ...")
    citizen_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=citizen_dir,
        shell=True
    )

    # Launch Officer Frontend (React/Vite on port 8502)
    print("[-] Launching Officer Command Center on http://localhost:8502 ...")
    officer_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=officer_dir,
        shell=True
    )

    print("\n[SUCCESS] All services are running!")
    print("  Backend API:        http://127.0.0.1:8000")
    print("  API Docs:           http://127.0.0.1:8000/docs")
    print("  Citizen Portal:     http://localhost:8501")
    print("  Officer Dashboard:  http://localhost:8502")
    print("\nPress Ctrl+C to terminate all services.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Shutting down servers...")
    finally:
        citizen_process.terminate()
        officer_process.terminate()
        backend_process.terminate()
        print("[SUCCESS] Services terminated.")

if __name__ == "__main__":
    run_servers()
