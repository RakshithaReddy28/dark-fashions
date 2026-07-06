import subprocess
import threading
import time
import urllib.request
import json
import sys

def start_flask():
    subprocess.run([sys.executable, "app.py"])

def start_ngrok():
    try:
        from pyngrok import ngrok
        public_url = ngrok.connect(5000, bind_tls=True)
        print(f"\n{'='*60}")
        print(f"  PUBLIC URL: {public_url}")
        print(f"{'='*60}")
        print(f"  Share this link with anyone to access your site!")
        print(f"{'='*60}\n")
        ngrok_process = ngrok.get_ngrok_process()
        try:
            ngrok_process.proc.wait()
        except KeyboardInterrupt:
            ngrok.kill()
    except Exception as e:
        print(f"ngrok error: {e}")
        print("\nTrying alternative method...")
        try:
            result = subprocess.run(
                ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:5000", "nokey@localhost.run"],
                capture_output=True, text=True, timeout=30
            )
            print(result.stdout)
            print(result.stderr)
        except:
            print("Could not establish tunnel. Run Flask app manually and visit http://127.0.0.1:5000")

if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    time.sleep(3)
    start_ngrok()
