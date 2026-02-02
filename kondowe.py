import streamlit as st
import streamlit.components.v1 as components

# 1. Sanidi Ukurasa
st.set_page_config(page_title="KONDOWE AI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. KUONDOA BLACK BARS NA KUREKEBISHA BACKGROUND
st.markdown("""
    <style>
        /* Futa kila kitu cha Streamlit kinacholeta kero */
        .block-container { padding: 0 !important; max-width: 100% !important; height: 100vh !important; }
        header, footer { visibility: hidden !important; }
        .stApp { background-color: white !important; }
        
        /* Hakikisha iframe inachukua screen nzima bila mabaki ya chini */
        iframe { 
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw; 
            height: 100vh !important; 
            border: none;
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
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
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

        /* SIDEBAR - Inatokea tu ikiguswa */
        .sidebar {{
            position: fixed;
            left: -300px; /* Inajificha hapa */
            top: 0;
            height: 100%;
            width: var(--sidebar-width);
            background: #f0f4f9;
            z-index: 2000;
            transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            padding: 20px;
            box-shadow: 5px 0 25px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
        }}
        .sidebar.active {{ left: 0; }}

        /* OVERLAY - Inafunika chat sidebar ikiwa wazi */
        .overlay {{
            position: fixed; display: none; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.2); z-index: 1999;
        }}
        .overlay.active {{ display: block; }}

        .main-content {{ 
            flex: 1; display: flex; flex-direction: column; 
            height: 100vh; width: 100%; position: relative;
        }}

        /* HEADER */
        .chat-header {{
            height: 60px; padding: 0 20px; background: white; 
            display: flex; align-items: center; border-bottom: 1px solid #f0f0f0;
            z-index: 100;
        }}
        #menu-btn {{ font-size: 26px; cursor: pointer; border: none; background: none; margin-right: 15px; }}

        /* CHAT CONTAINER - HAPA TU NDIPO PANASCROLL */
        .chat-container {{
            flex: 1; 
            overflow-y: auto; 
            padding: 20px 15% 120px 15%; /* Padding ya chini imeongezwa kwa ajili ya input box */
            scroll-behavior: smooth;
            background: white;
        }}

        /* INPUT AREA - Imepandishwa juu zaidi */
        .input-wrapper {{ 
            position: fixed;
            bottom: 30px; /* Ipawe juu kidogo toka chini kabisa */
            left: 50%;
            transform: translateX(-50%);
            width: 70%;
            max-width: 800px;
            z-index: 1000;
            background: transparent;
        }}
        .input-box {{
            display: flex; background: #f0f4f9; padding: 10px 25px; 
            border-radius: 40px; align-items: center; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #e0e0e0;
        }}
        input {{ flex: 1; border: none; background: transparent; outline: none; font-size: 16px; padding: 10px; }}
        
        .message {{ margin-bottom: 25px; max-width: 85%; line-height: 1.7; font-size: 16px; }}
        .user-message {{ align-self: flex-end; background: #f0f4f9; padding: 15px 22px; border-radius: 22px 22px 4px 22px; }}
        .assistant-message {{ align-self: flex-start; border-left: 4px solid var(--gemini-blue); padding-left: 15px; }}

        @media (max-width: 768px) {{
            .chat-container {{ padding: 20px 5% 120px 5%; }}
            .input-wrapper {{ width: 90%; bottom: 20px; }}
        }}
    </style>
</head>
<body>

    <div class="overlay" id="overlay"></div>
    
    <div class="sidebar" id="sidebar">
        <h3 style="margin-top:0;">Menu</h3>
        <button style="background:white; border:1px solid #ddd; padding:12px; border-radius:25px; cursor:pointer; font-weight:600;" onclick="location.reload()">✨ New Chat</button>
        <div id="history-list" style="margin-top:20px;"></div>
    </div>

    <div class="app-wrapper">
        <div class="main-content">
            <div class="chat-header">
                <button id="menu-btn">☰</button>
                <b style="font-size:1.2rem; background: linear-gradient(to right, #4285F4, #EA4335); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">KONDOWE AI PRO</b>
            </div>

            <div class="chat-container" id="chat-container">
                <div id="welcome-screen" style="text-align:center; margin-top:15vh;">
                    <h1 style="color:#444; font-size:2rem;">Nikupe msaada gani?</h1>
                </div>
            </div>

            <div class="input-wrapper">
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
        const menuBtn = document.getElementById('menu-btn');

        // Fungua/Funga Sidebar
        menuBtn.onclick = () => {{
            sidebar.classList.add('active');
            overlay.classList.add('active');
        }};

        overlay.onclick = () => {{
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        }};

        const _client = supabase.createClient("{SUPABASE_URL}", "{SUPABASE_KEY}");
        
        async function sendMessage() {{
            const input = document.getElementById('user-input');
            const msg = input.value.trim();
            if(!msg) return;

            document.getElementById('welcome-screen').style.display = 'none';
            appendMsg(msg, 'user');
            input.value = '';

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
        document.getElementById('user-input').onkeypress = (e) => {{ if(e.key === 'Enter') sendMessage(); }};
    </script>
</body>
</html>
"""

components.html(html_code, height=1200)
