import os
from flask import (
    Flask, 
    render_template_string, 
    request, 
    jsonify
)
import requests

app = Flask(__name__)

# Secure pipeline connecting to a dedicated Llama-3 brain
API_URL = (
    "https://huggingface.co"
    "models/meta-llama/Meta-Llama-3-8B-Instruct"
)

# Grab the secure token from Render's dashboard environment
HF_TOKEN = os.environ.get("HF_TOKEN")

def get_bot_response(user_text):
    if not HF_TOKEN:
        return (
            "Lunar AI Offline: Missing the secure "
            "HF_TOKEN environment variable."
        )
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": (
            f"<|system|>You are Lunar AI, a helpful, conversational "
            f"AI assistant. Answer fluently.<|user|>{user_text}<|assistant|>"
        ),
        "parameters": {
            "max_new_tokens": 300, 
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(
            API_URL, 
            headers=headers, 
            json=payload, 
            timeout=10
        )
        output = response.json()
        
        if isinstance(output, list) and len(output) > 0:
            return output[0].get('generated_text', '').strip()
        elif isinstance(output, dict) and 'error' in output:
            return "Uplink warming up... Try re-sending in 10 seconds."
        else:
            return "Uplink anomaly. Please try re-sending."
    except Exception:
        return "Deep space transmission signal weak. Try again."

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Lunar AI</title>
    <script src="https://jsdelivr.net">
    </script>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: #05070a;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .chat-container {
            width: 440px;
            height: 600px;
            background: #0d1117;
            border-radius: 16px;
            box-shadow: 0 0 25px rgba(0, 240, 255, 0.15);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            border: 2px solid #00f0ff;
        }
        .chat-header {
            background: #07090e;
            padding: 15px 20px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            border-bottom: 2px solid #00f0ff;
        }
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo-area {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #00f0ff;
            font-weight: bold;
            font-size: 19px;
            letter-spacing: 2px;
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            background: #00f0ff;
            border-radius: 50%;
            display: inline-block;
        }
        .clear-btn {
            background: rgba(255,0,85,0.1);
            border: 1px solid #ff0055;
            color: #ff0055;
            cursor: pointer;
            padding: 6px 12px;
            font-size: 11px;
            font-weight: bold;
            border-radius: 4px;
        }
        .status-bar {
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            color: #8b949e;
            border-top: 1px solid rgba(0, 240, 255, 0.2);
            padding-top: 6px;
        }
        .chat-box {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            background: #0b0e14;
        }
        .message {
            padding: 12px;
            border-radius: 8px;
            max-width: 80%;
            display: inline-block;
            box-sizing: border-box;
            font-size: 14px;
            line-height: 1.5;
            overflow-wrap: break-word;
            word-wrap: break-word;
            word-break: break-word;
            white-space: normal;
        }
        .user {
            background: rgba(0,240,255,0.15);
            color: #00f0ff;
            align-self: flex-end;
            border: 1px solid #00f0ff;
        }
        .bot {
            background: #161b22;
            color: #c9d1d9;
            align-self: flex-start;
            border: 1px solid #30363d;
        }
        .bot a {
            color: #00f0ff;
            font-weight: bold;
            text-decoration: underline;
        }
        .input-area {
            display: flex;
            border-top: 2px solid #00f0ff;
            background: #07090e;
        }
        .input-area input {
            flex: 1;
            padding: 16px;
            border: none;
            outline: none;
            background: #07090e;
            color: #fff;
            font-family: inherit;
        }
        .input-area button {
            padding: 16px 24px;
            background: #00f0ff;
            color: #05070a;
            border: none;
            cursor: pointer;
            font-weight: bold;
            font-family: inherit;
        }
        .loading {
            background: #0d1117;
            color: #ff0055;
            align-self: flex-start;
            border: 1px dashed #ff0055;
            display: none;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="header-top">
                <div class="logo-area">
                    <span class="pulse-dot"></span>
                    <span>LUNAR//AI</span>
                </div>
                <button class="clear-btn" onclick="location.reload()">
                    SYS_REBOOT
                </button>
            </div>
            <div class="status-bar">
                <div>STATUS: <span style="color:#00ff66;">ONLINE</span></div>
                <div>CORE: <span style="color:#00f0ff;">CLOUD_AI</span></div>
            </div>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="message bot">
                System active. Cloud neural links online. Ask me anything...
            </div>
            <div class="message loading" id="loader">
                >>> LUNAR AI IS THINKING...
            </div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" 
                   placeholder="Type any command..." 
                   onkeypress="handleKey(event)" autocomplete="off">
            <button onclick="send()">SEND</button>
        </div>
    </div>
    <script>
        window.send = async function() {
            const field = document.getElementById("userInput");
            const text = field.value.trim();
            if (!text) return;

            printMsg(text, "user", false);
            field.value = "";

            const loadBar = document.getElementById("loader");
            const box = document.getElementById("chatBox");
            box.appendChild(loadBar); 
            loadBar.style.display = "block";
            box.scrollTop = box.scrollHeight;

            try {
                const response = await fetch("/get_response", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                loadBar.style.display = "none";
                printMsg(data.reply, "bot", true);
            } catch (err) {
                loadBar.style.display = "none";
                printMsg("Signal dropped. Re-routing...", "bot", false);
            }
        }

        window.printMsg = function(txt, cls, md) {
            const box = document.getElementById("chatBox");
            const div = document.createElement("div");
            div.className = `message ${cls}`;
            if (md) {
                try {
                    marked.setOptions({ gfm:true, breaks:true });
                    div.innerHTML = marked.parse(txt);
                } catch (e) {
                    div.innerText = txt;
                }
            } else {
                div.innerText = txt;
            }
            box.appendChild(div);
            box.scrollTop = box.scrollHeight;
        }

        window.handleKey = function(e) {
            if (e.key === "Enter") send();
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_message = data.get("message", "")
    bot_reply = get_bot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)

