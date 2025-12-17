import os
import subprocess
import time
import threading
import json
import http.server
import socketserver
import urllib.request
import sys

# Configuration
MOCK_PORT = 9000
BACKEND_PORT = 7860
N8N_URL = f"http://localhost:{MOCK_PORT}/webhook"
UPLOAD_ENDPOINT = f"http://localhost:{BACKEND_PORT}/generate-catalog"
TEST_IMAGE = "test_image.jpg"

# Global capture for webhook data
received_webhooks = []

class MockWebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        received_webhooks.append(data)
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    
    def log_message(self, format, *args):
        pass # Silence logs


def start_mock_server():
    print(f"Starting Mock N8n Server on port {MOCK_PORT}...")
    with socketserver.TCPServer(("localhost", MOCK_PORT), MockWebhookHandler) as httpd:
        httpd.serve_forever()

def wait_for_server(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(1)
    return False

def run_test():
    # 1. Start Mock Server in Thread
    server_thread = threading.Thread(target=start_mock_server, daemon=True)
    server_thread.start()
    
    # 2. Start Backend Server
    print("Starting Backend Server...")
    env = os.environ.copy()
    env["N8N_WEBHOOK_URL"] = N8N_URL
    env["PYTHONUNBUFFERED"] = "1"
    
    # Force UTF-8 for subprocess to handle emojis from main.py
    # Use venv python
    venv_python = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        print(f"Warning: venv python not found at {venv_python}, using sys.executable")
        venv_python = sys.executable

    process = subprocess.Popen(
        [venv_python, "main.py"],
        env=env,
        cwd=os.getcwd(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    try:
        # 3. Wait for Backend
        print("Waiting for backend to be ready...")
        if not wait_for_server(f"http://localhost:{BACKEND_PORT}/"):
            print("Backend failed to start.")
            # Print stdout/stderr
            out, err = process.communicate(timeout=5)
            print(f"STDOUT:\n{out}")
            print(f"STDERR:\n{err}")
            return
            
        print("Backend is Ready.")
        
        # 4. Send Request
        print(f"Sending request to {UPLOAD_ENDPOINT} with {TEST_IMAGE}...")
        
        # Determine boundary
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        
        # Read image
        with open(TEST_IMAGE, "rb") as f:
            image_data = f.read()
            
        # Construct Multipart Body manually
        body = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="{TEST_IMAGE}"\r\n'
            'Content-Type: image/jpeg\r\n\r\n'
        ).encode('utf-8') + image_data + (
            f'\r\n--{boundary}--\r\n'
        ).encode('utf-8')
        
        req = urllib.request.Request(UPLOAD_ENDPOINT, data=body)
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
        
        try:
            with urllib.request.urlopen(req) as response:
                response_data = json.load(response)
                print("Received success response from Backend.")
        except urllib.error.HTTPError as e:
            print(f"Backend returned error: {e.code}")
            print(e.read().decode())
            return
        except Exception as e:
            print(f"Request failed: {e}")
            return
            
        # 5. Verify Webhook
        print("Verifying Webhook Receipt...")
        time.sleep(2)
        
        if len(received_webhooks) > 0:
            print("Mock Server Received Webhook!")
            data = received_webhooks[0]
            if "visual_data" in data and "listing" in data:
                print("Webhook payload structure looks correct.")
            else:
                print("Webhook payload missing keys.")
                # print(json.dumps(data, indent=2))
        else:
            print("No Webhook received by Mock Server.")
            
    finally:
        print("Stopping Backend...")
        process.terminate()
        try:
            out, err = process.communicate(timeout=5)
            # print("--- Backend Logs ---")
            # print(out)
        except:
            process.kill()


if __name__ == "__main__":
    run_test()
