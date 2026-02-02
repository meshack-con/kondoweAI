import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Sanidi Ukurasa (Page Config)
st.set_page_config(page_title="KONDOWE AI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. Ficha Header na Footer ya Streamlit ili kupata muonekano safi
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; height: 100vh !important; overflow: hidden !important; }
        header, footer { visibility: hidden !important; }
        iframe { height: 100vh !important; width: 100vw !important; border: none; overflow: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# 3. KUSOMA SECRETS (Hapa ndipo penye marekebisho muhimu)
try:
    # Tunakagua kama keys zipo kwenye st.secrets (ambazo zinatoka kwenye secrets.toml yako)
    if "GROQ_API_KEY" in st.secrets:
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    else:
        st.error("❌ File la 'secrets.toml' limeonekana lakini halina data sahihi ndani yake!")
        st.info("Hakikisha ndani ya file la secrets.toml kodi imeandikwa hivi:\n\nGROQ_API_KEY = '...' \nSUPABASE_URL = '...' \nSUPABASE_KEY = '...' ")
        st.stop()
except Exception as e:
    st.error("❌ Duh! Streamlit haioni file lako la siri (secrets.toml).")
    st.markdown(f"**Tatizo:** `{str(e)}`")
    st.info("Hakikisha folder la `.streamlit` liko sehemu moja na hili file la `app.py`.")
    st.stop()

# 4. KODI YA INTERFACE (HTML/CSS/JS)
html_code = f"""
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --gemini-blue: #4285F4; --gemini-red: #EA4335;
            --gemini-yellow: #FBBC05; --gemini-green: #34A853;
            --sidebar-bg: #f0f4f9;
        }}

        body, html {{ 
            margin: 0; padding: 0; height: 100vh; width: 100vw; 
            overflow: hidden; font-family: 'Outfit', sans-serif; 
            background-color: #ffffff;
        }}

        .app-wrapper {{ display: flex; height: 100vh; width: 100vw; }}

        /* Sidebar */
        .sidebar {{
            width: 270px; background: var(--sidebar-bg); padding: 20px;
            display: flex; flex-direction: column; border-right: 1px solid #e3e3e3;
            flex-shrink: 0;
        }}

        .new-chat-btn {{
            background: linear-gradient(135deg, #4285F4, #1a73e8); 
            color: white; border: none; padding: 14px; 
            border-radius: 25px; font-weight: 600; cursor: pointer; 
            margin-bottom: 25px; transition: 0.3s;
            box-shadow: 0 4px 10px rgba(66, 133, 244, 0.2);
        }}

        /* Main Area */
        .main-content {{ flex: 1; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }}

        .chat-header {{
            padding: 15px 30px; background: white; border-bottom: 1px solid #f0f0f0;
            display: flex; align-items: center;
        }}

        .logo-text {{ 
            font-weight: 800; font-size: 1.4rem; 
            background: linear-gradient(to right, var(--gemini-blue), var(--gemini-red), var(--gemini-yellow), var(--gemini-green));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}

        /* Chat Container (Scrolling Area) */
        .chat-container {{
            flex: 1; overflow-y: auto; padding: 20px 15%; 
            display: flex; flex-direction: column; background: white;
        }}

        .message {{ margin-bottom: 30px; max-width: 85%; line-height: 1.7; font-size: 16px; }}
        
        .user-message {{ 
            align-self: flex-end; background: #f0f4f9; color: #1f1f1f; 
            padding: 15px 25px; border-radius: 25px 25px 4px 25px;
            border-left: 4px solid var(--gemini-blue);
        }}

        .assistant-message {{ 
            align-self: flex-start; color: #1f1f1f; padding-left: 15px;
            border-left: 4px solid transparent;
            border-image: linear-gradient(to bottom, var(--gemini-blue), var(--gemini-red), var(--gemini-yellow), var(--gemini-green)) 1;
        }}

        /* Input Box */
        .input-wrapper {{ padding: 20px 15%; background: white; }}
        .input-box {{
            display: flex; background: #f0f4f9; padding: 10px 25px; 
            border-radius: 35px; align-items: center; border: 1px solid transparent;
        }}
        .input-box:focus-within {{ background: white; border-color: #d1d5db; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        
        input {{ flex: 1; border: none; background: transparent; outline: none; font-size: 16px; padding: 10px; color: #111; }}
        #send-btn {{ cursor: pointer; font-size: 26px; color: var(--gemini-blue); border: none; background: none; }}

        /* Colorful Spinner */
        #loader {{ display: none; margin-bottom: 15px; padding-left: 15%; }}
        .gemini-loader {{
            width: 25px; height: 25px; border: 4px solid #f3f3f3;
            border-top: 4px solid var(--gemini-blue); border-right: 4px solid var(--gemini-red);
            border-bottom: 4px solid var(--gemini-yellow); border-left: 4px solid var(--gemini-green);
            border-radius: 50%; animation: spin 1s linear infinite;
        }}
        @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}

        .history-item {{ padding: 12px; cursor: pointer; border-radius: 12px; font-size: 14px; margin-bottom: 5px; }}
        .history-item:hover {{ background: #e2e7ed; }}
    </style>
</head>
<body>
    <div class="app-wrapper">
        <div class="sidebar">
            <button class="new-chat-btn" id="new-chat-btn">✨ New Chat</button>
            <div id="history-list"></div>
        </div>

        <div class="main-content">
            <div class="chat-header"><span class="logo-text">KONDOWE AI PRO</span></div>
            <div class="chat-container" id="chat-container">
                <div id="welcome-screen" style="text-align:center; margin-top:10vh;">
                    <h1 style="background: linear-gradient(90deg, #4285F4, #9b72cb, #d96570, #FBBC05); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.8rem; font-weight:700;">Habari, Naitwa Kondowe AI</h1>
                    <p style="color: #5f6368; font-size: 1.2rem;">Mimi ni msaidizi wako, nikupe msaada gani?</p>
                </div>
            </div>
            <div id="loader"><div class="gemini-loader"></div></div>
            <div class="input-wrapper">
                <div class="input-box">
                    <input type="text" id="user-input" placeholder="Uliza chochote hapa..." autocomplete="off">
                    <button id="send-btn">➤</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const _client = supabase.createClient("{SUPABASE_URL}", "{SUPABASE_KEY}");
        let currentChatId = null;

        async function startNewChat() {{
            currentChatId = null;
            document.getElementById('chat-container').innerHTML = `<div style="text-align:center; margin-top:10vh;"><h1 style="color:#444;">Chat Mpya</h1><p>Nipe swali lako la kwanza.</p></div>`;
        }}

        async function sendMessage() {{
            const input = document.getElementById('user-input');
            const msg = input.value.trim();
            if (!msg) return;

            if (!currentChatId) {{
                document.getElementById('chat-container').innerHTML = '';
                const {{ data }} = await _client.from('chats').insert([{{ title: msg.substring(0, 30) }}]).select().single();
                currentChatId = data.id;
            }}

            appendMsg(msg, 'user');
            input.value = '';
            document.getElementById('loader').style.display = 'block';

            try {{
                const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {{
                    method: "POST",
                    headers: {{ "Authorization": "Bearer {GROQ_API_KEY}", "Content-Type": "application/json" }},
                    body: JSON.stringify({{ model: "llama-3.3-70b-versatile", messages: [{{ role: "user", content: msg }}], stream: true }})
                }});

                document.getElementById('loader').style.display = 'none';
                const reader = response.body.getReader();
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
                await _client.from('messages').insert([{{ chat_id: currentChatId, role: 'user', content: msg }}, {{ chat_id: currentChatId, role: 'assistant', content: fullText }}]);
                loadHistory();
            }} catch (e) {{ document.getElementById('loader').style.display = 'none'; }}
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

        async function loadHistory() {{
            const {{ data }} = await _client.from('chats').select('*').order('created_at', {{ ascending: false }});
            document.getElementById('history-list').innerHTML = data.map(c => `<div class="history-item" onclick="loadChat('${{c.id}}')">${{c.title}}</div>`).join('');
        }}

        async function loadChat(id) {{
            currentChatId = id;
            document.getElementById('chat-container').innerHTML = '';
            const {{ data }} = await _client.from('messages').select('*').eq('chat_id', id).order('created_at', {{ ascending: true }});
            data.forEach(m => appendMsg(m.content, m.role));
        }}

        document.getElementById('send-btn').onclick = sendMessage;
        document.getElementById('new-chat-btn').onclick = startNewChat;
        document.getElementById('user-input').onkeypress = (e) => {{ if(e.key === 'Enter') sendMessage(); }};
        loadHistory();
    </script>
</body>
</html>
"""

# 5. Onyesha Kazi (Render HTML)
components.html(html_code, height=1200)
