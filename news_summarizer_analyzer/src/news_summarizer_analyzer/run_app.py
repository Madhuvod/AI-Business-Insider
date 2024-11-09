import subprocess
import sys
import os
import time
from pathlib import Path

# Define FastAPI port and let Render handle the Streamlit port
API_PORT = 8000

def get_script_directory():
    return Path(__file__).parent.absolute()

def run_services():
    try:
        script_dir = get_script_directory()

        # Start FastAPI explicitly on port 8000
        api_process = subprocess.Popen([
            sys.executable,
            str(script_dir / "main.py"),
            "--port", str(API_PORT)
        ])
        print(f"Starting FastAPI server on port {API_PORT}")
        time.sleep(3)

        # Start Streamlit without explicitly setting the port, letting Render handle it
        streamlit_process = subprocess.Popen([
            sys.executable,
            "-m", "streamlit", "run",
            str(script_dir / "streamlit_app.py"),
            "--server.address", "0.0.0.0"
        ])
        print("Both services are running!")
        print(f"FastAPI: http://localhost:{API_PORT}")
        print("Streamlit will use the Render-assigned primary port")

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
