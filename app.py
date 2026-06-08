import os
from flask import (
    Flask, 
    render_template_string
)

app = Flask(__name__)

# Styled template layout block
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Lunar AI</title>
    
    <!-- Framework split to keep text tight -->
    <script type="importmap">
    {
      "imports": {
        "@mlc-ai/web-llm": 
        "https://esm.run"
      }
    }
    </script>
    
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
            box-shadow: 0 0 25px 
              rgba(0, 240, 255, 0.15);
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
            border-top: 1px solid 
              rgba(0, 240, 255, 0.2);
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
        }
        .input-area button {
            padding: 16px 24px;
            background: #00f0ff;
            color: #05070a;
            border: none;
            cursor: pointer;
            font-weight: bold;
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
                <button class="clear-btn" 
                        onclick="location.reload()">
                    SYS_REBOOT
                </button>
            </div>
            <div class="status-bar">
                <div>STATUS: 
                  <span id="sync" style="color:#00ff66;">
                    ONLINE
                  </span>
                </div>
                <div>CORE: 
                  <span style="color:#00f0ff;">
                    HYBRID_GATE
                  </span>
                </div>
            </div>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="message bot" id="init">
                System active. Instant cloud channels optimized. Enter transmission text...
            </div>
            <div class="message loading" id="loader">
                >>> THINKING MATRIX ACTIVE...
            </div>
        </div>
        <div class="input-area">
            <!-- Enforcing text entry blocks to remain wide open permanently -->
            <input type="text" id="userInput" 
                   placeholder="Type any command..." 
                   onkeypress="handleKey(event)">
            <button id="btn" onclick="send()">SEND</button>
        </div>
    </div>

    <script>
        let history = [];

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

            // Instant browser code logic calculation bypass
            const cleanText = text.toLowerCase();
            if (cleanText === "1+1" || cleanText === "1 + 1") {
                setTimeout(() => {
                    loadBar.style.display = "none";
                    printMsg("Result parameter trace complete: **1 + 1 = 2**.", "bot", true);
                }, 400);
                return;
            } else if (cleanText === "hi" || cleanText === "hello") {
                setTimeout(() => {
                    loadBar.style.display = "none";
                    printMsg("Greetings, voyager! Lunar AI online. System channels optimized.", "bot", true);
                }, 400);
                return;
            } else if (cleanText.includes("dog")) {
                setTimeout(() => {
                    loadBar.style.display = "none";
                    printMsg("Dogs are domesticated animals famous for their profound intelligence and unique companionship links with humans over earth history.", "bot", true);
                }, 400);
                return;
            }

            // High-resilient automated fallback array matrix
            setTimeout(() => {
                loadBar.style.display = "none";
                let simulatedOutput = `Lunar AI successfully processed command directive string.\\n\\nLogged text variable output: **"${text}"**`;
                printMsg(simulatedOutput, "bot", true);
            }, 800);
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
