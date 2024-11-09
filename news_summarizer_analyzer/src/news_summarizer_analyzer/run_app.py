import subprocess
import sys
import os
import time
from pathlib import Path

try:
    import sqlite3
except ImportError:
    print("sqlite3 is not available in your Python installation")
    sys.exit(1)

# Override Render's PORT with our desired ports
os.environ["PORT"] = "8501"  # Force Streamlit port
API_PORT = 8000  # FastAPI port

def get_script_directory():
    """Get the directory of the current script"""
    return Path(__file__).parent.absolute()

def run_services():
    """Run both FastAPI and Streamlit services"""
    try:
        script_dir = get_script_directory()
        
        # Start FastAPI on port 8000
        api_process = subprocess.Popen([
            sys.executable,
            str(script_dir / "main.py"),
            "--port", str(API_PORT)
        ])
        print(f"Starting FastAPI server on port {API_PORT}")
        time.sleep(3)
        
        # Force Streamlit to use port 8501
        streamlit_process = subprocess.Popen([
            sys.executable,
            "-m", "streamlit", "run",
            str(script_dir / "streamlit_app.py"),
            "--server.port", "8501",  # Hardcode the port
            "--server.address", "0.0.0.0"
        ])
        print("Both services are running!")
        print(f"FastAPI: http://localhost:{API_PORT}")
        print(f"Streamlit: http://localhost:8501")
        
        try:
            streamlit_process.wait()
            api_process.wait()
        except KeyboardInterrupt:
            print("\nShutting down services...")
            streamlit_process.terminate()
            api_process.terminate()
            streamlit_process.wait()
            api_process.wait()
            print("Services stopped.")
            
    except Exception as e:
        print(f"Error starting services: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_services()