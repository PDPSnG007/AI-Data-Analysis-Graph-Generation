# run.py
import subprocess
import sys
import time
import webbrowser

# Paths
backend_path = "backend"
frontend_path = "frontend"
backend_port = 8000

# Step 1: Start backend (FastAPI)
backend_cmd = [
    sys.executable, "-m", "uvicorn", "api:app",
    "--reload", "--host", "127.0.0.1", f"--port={backend_port}"
]
backend_proc = subprocess.Popen(
    backend_cmd, cwd=backend_path
)
print(f"Backend started at http://127.0.0.1:{backend_port}")

# Step 2: Wait a few seconds for backend to start
time.sleep(5)

# Step 3: Start frontend (Streamlit)
frontend_cmd = [
    sys.executable, "-m", "streamlit", "run", "main.py"
]
frontend_proc = subprocess.Popen(
    frontend_cmd, cwd=frontend_path
)
print("Frontend started...")

# Step 4: Open Streamlit in browser automatically
time.sleep(3)
webbrowser.open("http://localhost:8501")  # default Streamlit port

# Keep script running until Ctrl+C
try:
    backend_proc.wait()
    frontend_proc.wait()
except KeyboardInterrupt:
    print("Stopping servers...")
    backend_proc.terminate()
    frontend_proc.terminate()
