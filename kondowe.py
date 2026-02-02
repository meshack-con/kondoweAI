import streamlit as st
import streamlit.components.v1 as components

# 1. Sanidi Ukurasa
st.set_page_config(page_title="KONDOWE AI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. KUONDOA BLACK BARS NA KUREKEBISHA BACKGROUND
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; height: 100vh !important; }
        header, footer { visibility: hidden !important; }
        .stApp { background-color: white !important; }
        iframe { 
            position: fixed; top: 0; left: 0; width: 100vw; 
            height: 100vh !important; border: none;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Credentials
SUPABASE_URL = "https://xickklzlmwaobzobwyws.supabase.co"
SUPABASE_KEY = "sb_publishable_6L6eHvGEeEaVwICwCVZpXg_WV5zaRog"
GROQ_API_KEY = "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"

# 4. HTML/CSS/JS Interface
html_code = f"""
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --gemini-blue: #4285F4;
            --sidebar-width: 280px;
        }}

        body, html {{ 
            margin: 0; padding: 0; height: 100vh; width: 100vw; 
            overflow: hidden; font-family: 'Outfit', sans-serif; 
            background-color: #ffffff;
        }}

        .app-wrapper {{ display: flex; height: 100vh; width: 100vw; position: relative; }}

        /* SIDEBAR */
        .sidebar {{
            position: fixed; left: -300px; top: 0; height: 100%;
            width: var(--sidebar-width); background: #f0f4f9; z-index: 2000;
            transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1); padding: 20px;
            box-shadow: 5px 0 25px rgba(0,0,0,0.1); display: flex; flex-direction: column;
        }}
        .sidebar.active {{ left: 0; }}

        .overlay {{
            position: fixed; display: none; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.2); z-index: 1999;
        }}
        .overlay.active {{ display: block; }}

        .main-content {{ flex: 1; display: flex; flex-direction: column; height: 100vh; width: 100%; position: relative; }}

        /* HEADER */
        .chat-header {{
            height: 60px; padding: 0 20px; background: white; 
            display: flex; align-items: center; border-bottom: 1px solid #f0f0f0; z-index: 100;
        }}
        #menu-btn {{ font-size: 26px; cursor: pointer; border: none; background: none; margin-right: 15px; }}

        /* CHAT CONTAINER */
        .chat-container {{
            flex: 1; overflow-y: auto; padding: 20px 15% 150px 15%; 
            scroll-behavior: smooth; background: white;
        }}

        /* WELCOME TEXT */
        .welcome-title {{
            font-size: 3.5rem; font-weight: 700; margin-bottom: 5px;
            background: linear-gradient(90deg, #4285F4, #9b72cb, #d96570, #FBBC05);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .welcome-subtitle {{ font-size: 1.2rem; color: #757575; font-weight: 400; }}

        /* INPUT AREA */
        .input-wrapper {{ 
            position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
            width: 75%; max-width: 800px; z-index: 1000; transition: bottom 0.3s ease;
        }}

        .input-box {{
            display: flex; background: #f0f4f9; padding: 10px 25px; 
            border-radius: 40px; align-items: center; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;
        }}
        input {{ flex: 1; border: none; background: transparent; outline: none; font-size: 16px; padding: 10px; }}
        
        .message {{ margin-bottom: 25px; max-width: 85%; line-height: 1.7; font-size: 16px; }}
        .user-message {{ align-self: flex-end; background: #f0f4f9; padding: 15px 22px; border-radius: 22px 22px 4px 22px; }}
        .assistant-message {{ align-self: flex-start; border-left: 4px solid var(--gemini-blue); padding-left: 15px; }}

        @media (max-width: 768px) {{
            .welcome-title {{ font-size: 2.2rem; }}
            .chat-container {{ padding: 20px 5% 180px 5%; }}
            .input-wrapper {{ width: 92%; }}
        }}
    </style>
</head>
<body>
    <div class="overlay" id="overlay"></div>
    <div class="sidebar" id="sidebar">
        <h3 style="margin-top:0;">Menu</h3>
        <button style="background:white; border:1px solid #ddd; padding:12px; border-radius:25px; cursor:pointer; font-weight:600;" onclick="location.reload()">✨ New Chat</button>
    </div>

    <div class="app-wrapper">
        <div class="main-content">
            <div class="chat-header">
                <button id="menu-btn">☰</button>
                <b style="font-size:1.1rem; color:#444;">KONDOWE AI</b>
            </div>

            <div class="chat-container" id="chat-container">
                <div id="welcome-screen" style="text-align:center; margin-top:18vh;">
                    <div class="welcome-title">mimi ni kondowe ai</div>
                    <div class="welcome-subtitle">naweza kukusaidia nini?</div>
                </div>
            </div>

            <div class="input-wrapper" id="input-wrap">
                <div class="input-box">
                    <input type="text" id="user-input" placeholder="Uliza chochote..." autocomplete="off">
                    <button id="send-btn" style="border:none; background:none; color:var(--gemini-blue); font-size:26px; cursor:pointer;">➤</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('overlay');
        const inputWrap = document.getElementById('input-wrap');
        const userInput = document.getElementById('user-input');

        document.getElementById('menu-btn').onclick = () => {{ sidebar.classList.add('active'); overlay.classList.add('active'); }};
        overlay.onclick = () => {{ sidebar.classList.remove('active'); overlay.classList.remove('active'); }};

        // KEYBOARD LOGIC: Inapanda kwenye SIMU TU
        userInput.addEventListener('focus', () => {{
            if (window.innerWidth <= 768) {{
                inputWrap.style.bottom = '300px'; 
            }}
        }});

        userInput.addEventListener('blur', () => {{
            inputWrap.style.bottom = '30vh'; // Inarudi sehemu yake ya asili 30px
            if (window.innerWidth <= 768) {{
                inputWrap.style.bottom = '20px';
            }} else {{
                inputWrap.style.bottom = '30px';
            }}
        }});

        const _client = supabase.createClient("{SUPABASE_URL}", "{SUPABASE_KEY}");
        
        async function sendMessage() {{
            const msg = userInput.value.trim();
            if(!msg) return;

            document.getElementById('welcome-screen').style.display = 'none';
            appendMsg(msg, 'user');
            userInput.value = '';
            userInput.blur();

            try {{
                const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {{
                    method: "POST",
                    headers: {{ "Authorization": "Bearer {GROQ_API_KEY}", "Content-Type": "application/json" }},
                    body: JSON.stringify({{ 
                        model: "llama-3.3-70b-versatile", 
                        messages: [
                            {{ role: "system", content: "Wewe unaitwa KONDOWE AI. Kila unapoulizwa wewe ni nani, jitambulishe kama KONDOWE AI. Jibu maswali kwa ufasaha na upendo." }},
                            {{ role: "user", content: msg }}
                        ], 
                        stream: true 
                    }})
                }});

                const reader = res.body.getReader();
                const decoder = new TextDecoder();
                let botDiv = appendMsg('', 'assistant');
                let fullText = "";

                while (true) {{
                    const {{ done, value }} = await reader.read();
                    if (done) break;
                    const chunk = decoder.decode(value);
                    const lines = chunk.split("\\n");
                    lines.forEach(line => {{
                        if (line.startsWith("data: ") && line !== "data: [DONE]") {{
                            try {{
                                const json = JSON.parse(line.substring(6));
                                const content = json.choices[0].delta.content;
                                if (content) {{ fullText += content; botDiv.innerText = fullText; }}
                            }} catch(e) {{}}
                        }}
                    }});
                    const cc = document.getElementById('chat-container');
                    cc.scrollTop = cc.scrollHeight;
                }}
            }} catch(e) {{}}
        }}

        function appendMsg(txt, role) {{
            const container = document.getElementById('chat-container');
            const div = document.createElement('div');
            div.className = `message ${{role}}-message`;
            div.innerText = txt;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
            return div;
        }}

        document.getElementById('send-btn').onclick = sendMessage;
        userInput.onkeypress = (e) => {{ if(e.key === 'Enter') sendMessage(); }};
    </script>
</body>
</html>
"""

components.html(html_code, height=1200)
