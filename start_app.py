"""
Convenience launcher for the Business-for-Sale Aggregator & Scraper Prototype.
Runs both the FastAPI backend and Vite frontend concurrently.
"""
import subprocess
import sys
import os
import time

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")

    print("=" * 65)
    print("  🚀 Starting DealFlowHub: Business-for-Sale Scraper Prototype")
    print("=" * 65)
    print("• Backend API: http://127.0.0.1:8000 (Swagger docs: http://127.0.0.1:8000/docs)")
    print("• Frontend App: http://localhost:5173")
    print("=" * 65)

    # Start FastAPI Backend
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=backend_dir
    )

    # Start Vite Frontend
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    frontend_proc = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=frontend_dir
    )

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down DealFlowHub prototype servers...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    main()
