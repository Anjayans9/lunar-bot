import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# Switching to Mistral-7B - a heavily active and stable free cloud brain
HF_API_URL = "https://huggingface.co"

def get_bot_response(user_text):
    try:
        payload = {
            "inputs": f"<s>[INST] You are Lunar AI, an ultra-intelligent, space-themed AI chatbot built from scratch. Answer this short question briefly: {user_text} [/INST]",
            "parameters": {"max_new_tokens": 250, "return_full_text": False}
        }
        
        response = requests.post(HF_API_URL, json=payload)
        
        # SAFETY CHECK: If the server sends back an error code, catch it safely
        if response.status_code != 200:
            return "Lunar AI cloud brain is currently calibrating in orbit. Please wait 10 seconds and retry transmission!"
            
        output = response.json()
        
        # Parse the JSON response text carefully
        if isinstance(output, list) and len(output) > 0:
            return output[0].get('generated_text', 'Transmission blank. Try re-sending.')
        elif isinstance(output, dict) and 'generated_text' in output:
            return output['generated_text']
        else:
            return "Lunar AI Cloud uplink experienced a brief processing anomaly. Try again!"
            
    except Exception as e:
        # Prevents the "Expecting value" text from ever crashing your browser window again
        return "Uplink congested. Re-entering transmission orbit, please try sending your message again."

# Cyberpunk Layout
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Lunar AI Chatbot</title>
    <script src="https://jsdelivr.net"></script>
    <style>
        body { font-family: 'Courier New', Courier, monospace; background: #05070a; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .chat-container { width: 440px; height: 600px; background: #0d1117; border-radius: 16px; box-shadow: 0 0 30px rgba(69, 243, 255, 0.15); display: flex; flex-direction: column; overflow: hidden; border: 2px solid #00f0ff; }
        .chat-header { background: #07090e; padding: 18px 20px; display: flex; flex-direction: column; gap: 8px; border-bottom: 2px solid #00f0ff; box-shadow: 0 4px 15px rgba(0, 240, 255, 0.1); position: relative; }
        .header-top { display: flex; justify-content: space-between; align-items: center; }
        .logo-area { display: flex; align-items: center; gap: 8px; color: #00f0ff; font-weight: bold; font-size: 19px; letter-spacing: 3px; text-shadow: 0 0 10px rgba(0, 240, 255, 0.6); }
        .pulse-dot { width: 8px; height: 8px; background: #00f0ff; border-radius: 50%; display: inline-block; animation: core-glow 1.5s infinite; }
        .clear-btn { background: rgba(255, 0, 85, 0.1); border: 1px solid #ff0055; color: #ff0055; cursor: pointer; padding: 6px 14px; font-family: inherit; font-size: 11px; font-weight: bold; border-radius: 4px; letter-spacing: 1px; transition: all 0.3s; box-shadow: 0 0 8px rgba(255, 0, 85, 0.2); }
        .clear-btn:hover { background: #ff0055; color: #05070a; box-shadow: 0 0 15px #ff0055; transform: scale(1.05); }
        .status-bar { display: flex; justify-content: space-between; font-size: 10px; color: #8b949e; border-top: 1px solid rgba(0, 240, 255, 0.2); padding-top: 6px; margin-top: 2px; }
        .status-item { display: flex; align-items: center; gap: 4px; }
        .status-active { color: #00ff66; font-weight: bold; text-shadow: 0 0 5px rgba(0, 255, 102, 0.5); }
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; background: #0b0e14; }
        .message { padding: 12px; border-radius: 8px; max-width: 75%; word-wrap: break-word; font-size: 14px; line-height: 1.4; box-shadow: inset 0 0 5px rgba(255,255,255,0.02); }
        .user { background: rgba(0, 240, 255, 0.15); color: #00f0ff; align-self: flex-end; font-weight: bold; border: 1px solid #00f0ff; box-shadow: 0 0 10px rgba(0, 240, 255, 0.2); }
        .bot { background: #161b22; color: #c9d1d9; align-self: flex-start; border: 1px solid #30363d; }
        .bot a { color: #00f0ff; font-weight: bold; text-decoration: underline; }
        .bot a:hover { color: #7dfcff; text-shadow: 0 0 5px #00f0ff; }
        .input-area { display: flex; border-top: 2px solid #00f0ff; background: #07090e; }
        .input-area input { flex: 1; padding: 16px; border: none; outline: none; font-size: 14px; background: #07090e; color: #fff; font-family: inherit; }
        .input-area button { padding: 16px 28px; background: #00f0ff; color: #05070a; border: none; cursor: pointer; font-weight: bold; font-family: inherit; transition: all 0.2s; letter-spacing: 1px; }
        .input-area button:hover { background: #7dfcff; box-shadow: inset 0 0 10px #fff; }
        .loading { background: #0d1117; color: #ff0055; align-self: flex-start; border: 1px dashed #ff0055; font-weight: bold; animation: blink 1.2s infinite; display: none; }
        @keyframes blink { 0% { opacity: 0.4; } 50% { opacity: 1.0; } 100% { opacity: 0.4; } }
        @keyframes core-glow { 0% { box-shadow: 0 0 2px #00f0ff; } 50% { box-shadow: 0 0 12px #00f0ff, 0 0 18px #00f0ff; } 100% { box-shadow: 0 0 2px #00f0ff; } }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="header-top">
                <div class="logo-area">
                    <span class="pulse-dot"></span>
                    <span>LUNAR//AI_</span>
                </div>
                <button class="clear-btn" onclick="location.reload()">SYS_REBOOT</button>
            </div>
            <div class="status-bar">
                <div class="status-item">SYS_STATUS: <span class="status-active">ONLINE</span></div>
                <div class="status-item">CORE: <span style="color: #00f0ff;">MISTRAL_7B</span></div>
                <div class="status-item">SECURE: <span style="color: #00f0ff;">SSL_CLOUD</span></div>
            </div>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="message bot">System active. Global cloud pathways synced. Enter transmission...</div>
            <div class="message loading" id="loadingIndicator">>>> LUNAR AI IS THINKING...</div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Enter cloud directive..." onkeypress="handleKeyPress(event)" autocomplete="off">
            <button onclick="sendMessage()">SEND</button>
        </div>
    </div>
    <script>
        function sendMessage() {
            const input = document.getElementById("userInput");
            const messageText = input.value.trim();
            if (!messageText) return;
            appendMessage(messageText, "user", false);
            input.value = "";
            const loader = document.getElementById("loadingIndicator");
            const chatBox = document.getElementById("chatBox");
            chatBox.appendChild(loader); 
            loader.style.display = "block";
            chatBox.scrollTop = chatBox.scrollHeight;
            fetch("/get_response", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: messageText })
            })
            .then(res => res.json())
            .then(data => {
                loader.style.display = "none";
                appendMessage(data.reply, "bot", true);
            })
            .catch(err => {
                loader.style.display = "none";
                appendMessage("Cloud uplink interrupted.", "bot", false);
            });
        }
        function appendMessage(text, sender, useMarkdown) {
            const chatBox = document.getElementById("chatBox");
            const msgDiv = document.createElement("div");
            msgDiv.className = `message ${sender}`;
            if (useMarkdown) {
                try {
                    marked.setOptions({ gfm: true, breaks: true });
                    msgDiv.innerHTML = marked.parse(text);
                } catch (e) {
                    msgDiv.innerText = text;
                }
            } else {
                msgDiv.innerText = text;
            }
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        function handleKeyPress(e) { if (e.key === "Enter") sendMessage(); }
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
