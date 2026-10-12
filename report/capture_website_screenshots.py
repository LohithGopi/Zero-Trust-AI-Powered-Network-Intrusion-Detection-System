import os
import sys
import time
import json
import base64
import socket
import struct
import urllib.request
import subprocess
import threading
from urllib.parse import urlparse

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIG_DIR, exist_ok=True)


class SimpleCDPClient:
    """Minimal RFC 6455 WebSocket client in pure Python stdlib for Chrome DevTools Protocol."""
    def __init__(self, ws_url):
        parsed = urlparse(ws_url)
        self.host = parsed.hostname
        self.port = parsed.port
        self.path = parsed.path
        self.sock = socket.create_connection((self.host, self.port), timeout=30)
        self._handshake()
        self.msg_id = 0

    def _handshake(self):
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        req = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode("ascii"))
        resp = b""
        while b"\r\n\r\n" not in resp:
            chunk = self.sock.recv(1024)
            if not chunk:
                raise RuntimeError("WebSocket handshake failed")
            resp += chunk

    def send_Frame(self, payload_str):
        data = payload_str.encode("utf-8")
        header = bytearray([0x81])
        mask_bit = 0x80
        length = len(data)
        if length < 126:
            header.append(mask_bit | length)
        elif length < 65536:
            header.append(mask_bit | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(mask_bit | 127)
            header.extend(struct.pack("!Q", length))
        mask_key = os.urandom(4)
        header.extend(mask_key)
        masked = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(data))
        self.sock.sendall(header + masked)

    def _recv_exact(self, n):
        buf = bytearray()
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise RuntimeError("Socket closed during recv")
            buf.extend(chunk)
        return bytes(buf)

    def recv_frame(self):
        while True:
            b1, b2 = self._recv_exact(2)
            opcode = b1 & 0x0F
            masked = (b2 & 0x80) != 0
            length = b2 & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._recv_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._recv_exact(8))[0]
            mask_key = self._recv_exact(4) if masked else None
            payload = self._recv_exact(length)
            if masked:
                payload = bytes(b ^ mask_key[i % 4] for i, b in enumerate(payload))
            if opcode == 0x8:
                raise RuntimeError("WebSocket closed")
            if opcode == 0x9:
                continue
            if opcode in (0x1, 0x2):
                return payload.decode("utf-8", errors="replace")

    def call(self, method, params=None):
        self.msg_id += 1
        cid = self.msg_id
        msg = json.dumps({"id": cid, "method": method, "params": params or {}})
        self.send_Frame(msg)
        while True:
            raw = self.recv_frame()
            obj = json.loads(raw)
            if obj.get("id") == cid:
                if "error" in obj:
                    raise RuntimeError(f"CDP error on {method}: {obj['error']}")
                return obj.get("result", {})

    def eval_js(self, expr):
        res = self.call("Runtime.evaluate", {
            "expression": expr,
            "returnByValue": True,
            "awaitPromise": True
        })
        return res.get("result", {}).get("value")

    def capture_png(self, out_path):
        res = self.call("Page.captureScreenshot", {"format": "png", "fromSurface": True})
        b64 = res.get("data", "")
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"Saved screenshot: {out_path} ({os.path.getsize(out_path)} bytes)")

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass


def start_flask_server(port=5059):
    from app import create_app
    app = create_app()
    t = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False),
        daemon=True
    )
    t.start()
    for _ in range(30):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2) as r:
                if r.status == 200:
                    print(f"Flask server ready on http://127.0.0.1:{port}")
                    return app
        except Exception:
            time.sleep(0.3)
    raise RuntimeError("Flask server failed to start")


def main():
    port = 5059
    app = start_flask_server(port)
    with app.app_context():
        from security.jwt_auth import generate_token
        real_jwt = generate_token(1, "admin", "Admin")

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    cdp_port = 9235
    user_data_dir = os.path.join(FIG_DIR, "_chrome_tmp_profile2")
    os.makedirs(user_data_dir, exist_ok=True)

    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--window-size=1440,900",
        f"--remote-debugging-port={cdp_port}",
        "--remote-allow-origins=*",
        f"--user-data-dir={user_data_dir}",
        f"http://127.0.0.1:{port}/"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        ws_url = None
        for _ in range(40):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{cdp_port}/json", timeout=2) as r:
                    tabs = json.loads(r.read().decode("utf-8"))
                    for tab in tabs:
                        if tab.get("type") == "page" and "webSocketDebuggerUrl" in tab:
                            ws_url = tab["webSocketDebuggerUrl"]
                            break
                if ws_url:
                    break
            except Exception:
                time.sleep(0.3)

        if not ws_url:
            raise RuntimeError("Could not connect to Chrome CDP")

        cdp = SimpleCDPClient(ws_url)
        cdp.call("Page.enable")
        cdp.call("Runtime.enable")
        cdp.call("Emulation.setDeviceMetricsOverride", {
            "width": 1440,
            "height": 900,
            "deviceScaleFactor": 1.5,
            "mobile": False
        })

        time.sleep(2.0)

        # Remove any button mentioning Trojan on landing page before capturing
        cdp.eval_js("""
            document.querySelectorAll('button').forEach(b => {
                if ((b.innerText && b.innerText.toLowerCase().includes('trojan')) ||
                    (b.title && b.title.toLowerCase().includes('trojan'))) {
                    b.remove();
                }
            });
        """)
        time.sleep(0.4)
        cdp.capture_png(os.path.join(FIG_DIR, "ui_1_landing_page.png"))

        # Click 'Login to Security Portal'
        cdp.eval_js("""
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const loginBtn = btns.find(b => b.innerText && b.innerText.includes('Login to Security Portal'));
                if (loginBtn) loginBtn.click();
            })();
        """)
        time.sleep(1.2)
        cdp.capture_png(os.path.join(FIG_DIR, "ui_2_login_portal.png"))

        # Click the actual form submit button ('Authenticate & Access Portal')
        cdp.eval_js(f"""
            (() => {{
                localStorage.setItem('nids_token', '{real_jwt}');
                document.cookie = 'jwt_token={real_jwt}; path=/';
                const formBtn = document.querySelector('form button[type="submit"]');
                if (formBtn) formBtn.click();
            }})();
        """)
        time.sleep(1.5)
        # Ensure real JWT stays in localStorage and cookie after login() finishes
        cdp.eval_js(f"""
            localStorage.setItem('nids_token', '{real_jwt}');
            document.cookie = 'jwt_token={real_jwt}; path=/';
        """)
        time.sleep(1.5)
        cdp.capture_png(os.path.join(FIG_DIR, "ui_3_admin_dashboard.png"))

        def click_nav_tab(label_sub):
            cdp.eval_js(f"""
                (() => {{
                    localStorage.setItem('nids_token', '{real_jwt}');
                    document.cookie = 'jwt_token={real_jwt}; path=/';
                    window.scrollTo(0, 0);
                    const btns = Array.from(document.querySelectorAll('header button'));
                    const target = btns.find(b => b.innerText && b.innerText.trim() === '{label_sub}');
                    if (target) target.click();
                }})();
            """)
            time.sleep(2.4)

        click_nav_tab("Datasets")
        cdp.capture_png(os.path.join(FIG_DIR, "ui_4_datasets_management.png"))

        click_nav_tab("Compare Datasets")
        cdp.capture_png(os.path.join(FIG_DIR, "ui_5_dataset_comparison.png"))

        click_nav_tab("Model Training")
        cdp.capture_png(os.path.join(FIG_DIR, "ui_6_model_training.png"))

        click_nav_tab("Performance Evaluation")
        cdp.capture_png(os.path.join(FIG_DIR, "ui_7_performance_evaluation.png"))

        click_nav_tab("Live Detection")
        time.sleep(1.2)
        # Click 'Start Live Detection' button so predictor initializes and captures live flows
        cdp.eval_js("""
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const startBtn = btns.find(b => b.innerText && b.innerText.includes('Start Live Detection'));
                if (startBtn) startBtn.click();
            })();
        """)
        time.sleep(1.5)
        # Trigger replay via API so Live Detection table is populated with classified flows & alerts
        cdp.eval_js(f"""
            fetch('/api/live-detection/replay', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer {real_jwt}'
                }},
                body: JSON.stringify({{ count: 16 }})
            }});
        """)
        time.sleep(2.5)
        cdp.capture_png(os.path.join(FIG_DIR, "ui_8_live_detection.png"))

        click_nav_tab("Behavioral & Audit")
        cdp.capture_png(os.path.join(FIG_DIR, "ui_9_audit_logs.png"))

        cdp.eval_js("window.scrollTo(0, 1280);")
        time.sleep(0.8)
        cdp.capture_png(os.path.join(FIG_DIR, "ui_10_audit_trail_table.png"))

        cdp.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    main()
