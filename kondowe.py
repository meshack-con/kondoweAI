import streamlit as st
import streamlit.components.v1 as components

# 1. Sanidi Ukurasa
st.set_page_config(page_title="KONDOWE AI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. Safisha Streamlit Background (Dawa ya Black/Grey interface)
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; height: 100vh !important; }
        header, footer { visibility: hidden !important; }
        .stHtml { background-color: white !important; }
        iframe { height: 100vh !important; width: 100vw !important; border: none; }
    </style>
""", unsafe_allow_html=True)

# 3. Credentials
SUPABASE_URL = "https://xickklzlmwaobzobwyws.supabase.co"
SUPABASE_KEY = "sb_publishable_6L6eHvGEeEaVwICwCVZpXg_WV5zaRog"
GROQ_API_KEY = "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"

# 4. HTML/CSS/JS Interface iliyoboreshwa
html_code = f"""
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --gemini-blue: #4285F4;
            --gemini-red: #EA4335;
            --gemini-yellow: #FBBC05;
            --gemini-green: #34A853;
            --sidebar-bg: #f0f4f9;
        }}

        body, html {{ 
            margin: 0; padding: 0; height: 100vh; width: 100vw; 
            overflow: hidden; font-family: 'Outfit', sans-serif; 
            background-color: #ffffff;
        }}

        .app-wrapper {{ display: flex; height: 100vh; width: 100vw; overflow: hidden; }}

        /* Sidebar Responsive */
        .sidebar {{
            width: 270px; background: var(--sidebar-bg); padding: 20px;
            display: flex; flex-direction: column; border-right: 1px solid #e3e3e3;
            transition: 0.3s ease; flex-shrink: 0; z-index: 1001;
        }}

        .main-content {{ 
            flex: 1; display: flex; flex-direction: column; 
            height: 100vh; position: relative; background: white;
        }}

        /* Header - Fixed */
        .chat-header {{
            height: 60px; padding: 0 25px; background: white; 
            border-bottom: 1px solid #f0f0f0; display: flex; 
            align-items: center; gap: 15px; flex-shrink: 0;
        }}

        .logo-text {{ 
            font-weight: 800; font-size: 1.3rem; 
            background: linear-gradient(to right, var(--gemini-blue), var(--gemini-red), var(--gemini-yellow), var(--gemini-green));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}

        /* CHAT CONTAINER - HAPA TU NDIPO PANASCROLL */
        .chat-container {{
            flex: 1; overflow-y: auto; padding: 20px 15%; 
            display: flex; flex-direction: column; background: white;
            scroll-behavior: smooth;
        }}

        /* Message Styling */
        .message {{ margin-bottom: 25px; max-width: 85%; line-height: 1.7; font-size: 16px; color: #1f1f1f; }}
        .user-message {{ 
            align-self: flex-end; background: #f0f4f9; padding: 15px 22px; 
            border-radius: 22px 22px 4px 22px; border-left: 4px solid var(--gemini-blue);
        }}
        .assistant-message {{ 
            align-self: flex-start; padding-left: 15px; border-left: 4px solid transparent;
            border-image: linear-gradient(to bottom, var(--gemini-blue), var(--gemini-red), var(--gemini-yellow), var(--gemini-green)) 1;
        }}

        /* INPUT AREA - Fixed at bottom */
        .input-wrapper {{ 
            padding: 20px 15% 30px 15%; background: white; flex-shrink: 0;
        }}
        .input-box {{
            display: flex; background: #f0f4f9; padding: 8px 25px; 
            border-radius: 35px; align-items: center; border: 1px solid transparent;
        }}
        .input-box:focus-within {{ background: white; border-color: #d1d5db; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        
        input {{ flex: 1; border: none; background: transparent; outline: none; font-size: 16px; padding: 12px; }}
        #send-btn {{ cursor: pointer; font-size: 26px; color: var(--gemini-blue); border: none; background: none; }}

        /* Menu Button for Mobile */
        #menu-toggle {{ display: none; font-size: 24px; cursor: pointer; background: none; border: none; color: #444; }}

        /* RESPONSIVE DESIGN */
        @media (max-width: 768px) {{
            #menu-toggle {{ display: block; }}
            .sidebar {{ position: absolute; left: -270px; height: 100%; box-shadow: 5px 0 15px rgba(0,0,0,0.05); }}
            .sidebar.active {{ left: 0; }}
            .chat-container {{ padding: 20px 5%; }}
            .input-wrapper {{ padding: 15px 5% 25px 5%; }}
            .message {{ max-width: 92%; font-size: 15px; }}
            .logo-text {{ font-size: 1.1rem; }}
        }}
    </style>
</head>
<body>

    <div class="app-wrapper">
        <div class="sidebar" id="sidebar">
            <button style="background:white; border:1px solid #ddd; padding:12px; border-radius:25px; cursor:pointer; font-weight:600; margin-bottom:20px;" onclick="location.reload()">✨ New Chat</button>
            <div id="history-list"></div>
        </div>

        <div class="main-content">
            <div class="chat-header">
                <button id="menu-toggle">☰</button>
                <span class="logo-text">KONDOWE AI PRO</span>
            </div>

            <div class="chat-container" id="chat-container">
                <div id="welcome-screen" style="text-align:center; margin-top:10vh;">
                    <h1 style="font-size: 2.2rem; background: linear-gradient(90deg, #4285F4, #9b72cb, #d96570, #FBBC05); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight:700;">Nikupe msaada gani leo?</h1>
                </div>
            </div>

            <div class="input-wrapper">
                <div class="input-box">
                    <input type="text" id="user-input" placeholder="Uliza chochote..." autocomplete="off">
                    <button id="send-btn">➤</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const sidebar = document.getElementById('sidebar');
        document.getElementById('menu-toggle').onclick = () => sidebar.classList.toggle('active');

        const _client = supabase.createClient("{SUPABASE_URL}", "{SUPABASE_KEY}");
        
        async function sendMessage() {{
            const input = document.getElementById('user-input');
            const msg = input.value.trim();
            if(!msg) return;

            document.getElementById('welcome-screen').style.display = 'none';
            appendMsg(msg, 'user');
            input.value = '';
            
            // Ficha sidebar kwenye simu baada ya kutuma
            if(window.innerWidth < 768) sidebar.classList.remove('active');

            try {{
                const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {{
                    method: "POST",
                    headers: {{ "Authorization": "Bearer {GROQ_API_KEY}", "Content-Type": "application/json" }},
                    body: JSON.stringify({{ model: "llama-3.3-70b-versatile", messages: [{{ role: "user", content: msg }}], stream: true }})
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
                                if (content) {{ 
                                    fullText += content; 
                                    botDiv.innerText = fullText; 
                                }}
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
        document.getElementById('user-input').onkeypress = (e) => {{ if(e.key === 'Enter') sendMessage(); }};
    </script>
</body>
</html>
"""

components.html(html_code, height=1200)
