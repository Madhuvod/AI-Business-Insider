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

def get_script_directory():
    """Get the directory of the current script"""
    return Path(__file__).parent.absolute()

def run_services():
    """Run both FastAPI and Streamlit services"""
    try:

        script_dir = get_script_directory()
        

        api_process = subprocess.Popen([
            sys.executable,
            str(script_dir / "main.py")
        ])

        print("Starting FastAPI server...")
        time.sleep(3)
        
        # Start Streamlit
        streamlit_process = subprocess.Popen([
            sys.executable,
            "-m", "streamlit", "run",
            str(script_dir / "streamlit_app.py")
        ])
        
        print("Both services are running!")
        print("FastAPI: http://localhost:8000")
        print("Streamlit: http://localhost:8501")
        
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
    os.environ["BACKEND_URL"] = "http://localhost:8000"
    run_services() 