import streamlit as st
import streamlit.components.v1 as components

# 1. Sanidi Ukurasa
st.set_page_config(page_title="KONDOWE AI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. Ficha vitu vya Streamlit
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; height: 100vh !important; overflow: hidden !important; }
        header, footer { visibility: hidden !important; }
        iframe { height: 100vh !important; width: 100vw !important; border: none; }
    </style>
""", unsafe_allow_html=True)

# 3. Credentials (Hardcoded kwa usalama wako wa sasa hivi)
SUPABASE_URL = "https://xickklzlmwaobzobwyws.supabase.co"
SUPABASE_KEY = "sb_publishable_6L6eHvGEeEaVwICwCVZpXg_WV5zaRog"
GROQ_API_KEY = "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"

# 4. HTML/CSS/JS Interface na Responsive Design
html_code = f"""
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --gemini-blue: #4285F4; --sidebar-bg: #f0f4f9;
        }}

        body, html {{ 
            margin: 0; padding: 0; height: 100vh; width: 100vw; 
            overflow: hidden; font-family: 'Outfit', sans-serif; 
        }}

        .app-wrapper {{ display: flex; height: 100vh; width: 100vw; position: relative; }}

        /* Sidebar Responsive */
        .sidebar {{
            width: 280px; background: var(--sidebar-bg); padding: 20px;
            display: flex; flex-direction: column; border-right: 1px solid #e3e3e3;
            transition: all 0.3s ease; z-index: 1000;
        }}

        /* Main Content */
        .main-content {{ flex: 1; display: flex; flex-direction: column; height: 100vh; width: 100%; }}

        .chat-header {{
            padding: 10px 20px; background: white; border-bottom: 1px solid #f0f0f0;
            display: flex; align-items: center; justify-content: space-between;
        }}

        .logo-text {{ font-weight: 800; font-size: 1.2rem; background: linear-gradient(to right, #4285F4, #EA4335, #FBBC05, #34A853); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}

        /* Menu Button kwa ajili ya Simu */
        #menu-toggle {{ display: none; font-size: 24px; cursor: pointer; background: none; border: none; }}

        .chat-container {{ flex: 1; overflow-y: auto; padding: 20px 5%; display: flex; flex-direction: column; }}

        .message {{ margin-bottom: 20px; max-width: 90%; line-height: 1.5; font-size: 15px; }}
        .user-message {{ align-self: flex-end; background: #f0f4f9; padding: 12px 18px; border-radius: 18px 18px 0 18px; }}
        .assistant-message {{ align-self: flex-start; padding: 10px; border-left: 3px solid var(--gemini-blue); }}

        .input-wrapper {{ padding: 15px; background: white; }}
        .input-box {{ display: flex; background: #f0f4f9; padding: 5px 20px; border-radius: 30px; align-items: center; }}
        input {{ flex: 1; border: none; background: transparent; outline: none; padding: 10px; font-size: 16px; }}

        /* MEDIA QUERIES KWA SIMU */
        @media (max-width: 768px) {{
            #menu-toggle {{ display: block; }}
            .sidebar {{
                position: absolute; left: -280px; height: 100%;
            }}
            .sidebar.active {{ left: 0; shadow: 5px 0 15px rgba(0,0,0,0.1); }}
            .chat-container {{ padding: 20px 3%; }}
            .welcome-screen h1 {{ font-size: 1.8rem; }}
        }}
    </style>
</head>
<body>

    <div class="app-wrapper">
        <div class="sidebar" id="sidebar">
            <button style="align-self:flex-end; display:none;" id="close-menu">✕</button>
            <button class="new-chat-btn" onclick="location.reload()">✨ New Chat</button>
            <div id="history-list"></div>
        </div>

        <div class="main-content">
            <div class="chat-header">
                <button id="menu-toggle">☰</button>
                <span class="logo-text">KONDOWE AI PRO</span>
                <div style="width:24px;"></div> </div>

            <div class="chat-container" id="chat-container">
                <div id="welcome-screen" style="text-align:center; margin-top:15vh;">
                    <h1 style="background: linear-gradient(90deg, #4285F4, #9b72cb, #d96570, #FBBC05); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Habari, Kondowe AI Hapa</h1>
                </div>
            </div>

            <div class="input-wrapper">
                <div class="input-box">
                    <input type="text" id="user-input" placeholder="Andika hapa...">
                    <button id="send-btn" style="border:none; background:none; color:var(--gemini-blue); font-size:24px;">➤</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Toggle Sidebar Logic
        const menuBtn = document.getElementById('menu-toggle');
        const sidebar = document.getElementById('sidebar');
        menuBtn.onclick = () => sidebar.classList.toggle('active');

        const _client = supabase.createClient("{SUPABASE_URL}", "{SUPABASE_KEY}");
        
        async function sendMessage() {{
            const input = document.getElementById('user-input');
            const msg = input.value.trim();
            if(!msg) return;

            appendMsg(msg, 'user');
            input.value = '';
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
                                if (content) botDiv.innerText += content;
                            }} catch(e) {{}}
                        }}
                    }});
                    document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;
                }}
            }} catch(e) {{}}
        }}

        function appendMsg(txt, role) {{
            const div = document.createElement('div');
            div.className = `message ${{role}}-message`;
            div.innerText = txt;
            document.getElementById('chat-container').appendChild(div);
            document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;
            return div;
        }}

        document.getElementById('send-btn').onclick = sendMessage;
        document.getElementById('user-input').onkeypress = (e) => {{ if(e.key === 'Enter') sendMessage(); }};
    </script>
</body>
</html>
"""

components.html(html_code, height=1200)
