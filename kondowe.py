import streamlit as st
import streamlit.components.v1 as components

# 1. Sanidi Ukurasa - Tunatumia "wide" ili kuzuia margin kubwa pembeni
st.set_page_config(page_title="KONDOWE AI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. HII NDIO DAWA: Inafuta background ya Streamlit na kuifanya nyeupe kabisa
st.markdown("""
    <style>
        /* Inafuta padding zote za Streamlit */
        .block-container { padding: 0 !important; max-width: 100% !important; height: 100vh !important; }
        
        /* Inazuia scroll ya nje ya Streamlit */
        header, footer { visibility: hidden !important; }
        
        /* Inalazimisha sehemu ya HTML iwe nyeupe na ijae screen */
        .stHtml { background-color: white !important; height: 100vh !important; }
        
        iframe { height: 100vh !important; width: 100vw !important; border: none; }
    </style>
""", unsafe_allow_html=True)

# 3. Credentials (Zimebaki vilevile)
SUPABASE_URL = "https://xickklzlmwaobzobwyws.supabase.co"
SUPABASE_KEY = "sb_publishable_6L6eHvGEeEaVwICwCVZpXg_WV5zaRog"
GROQ_API_KEY = "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"

# 4. HTML Interface (Imerekebishwa kuondoa giza)
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
            --sidebar-bg: #f8fafd;
        }}

        /* Tunahakikisha kila kitu ni cheupe na kinavyoonekana */
        body, html {{ 
            margin: 0; padding: 0; height: 100vh; width: 100vw; 
            font-family: 'Outfit', sans-serif; 
            background-color: #ffffff !important;
            color: #1f1f1f;
        }}

        .app-wrapper {{ display: flex; height: 100vh; width: 100vw; position: relative; overflow: hidden; }}

        /* Sidebar inakaa pembeni kwa uzuri */
        .sidebar {{
            width: 260px; background: var(--sidebar-bg); padding: 20px;
            display: flex; flex-direction: column; border-right: 1px solid #e3e3e3;
            transition: 0.3s; flex-shrink: 0;
        }}

        .main-content {{ 
            flex: 1; display: flex; flex-direction: column; 
            height: 100vh; background: white; position: relative;
        }}

        .chat-header {{
            padding: 12px 20px; background: white; border-bottom: 1px solid #f0f0f0;
            display: flex; align-items: center; gap: 15px;
        }}

        #menu-toggle {{ display: none; font-size: 22px; cursor: pointer; background: none; border: none; }}

        /* Sehemu ya Chat - Scrollable */
        .chat-container {{ 
            flex: 1; overflow-y: auto; padding: 20px 10%; 
            display: flex; flex-direction: column; gap: 20px;
        }}

        .message {{ max-width: 85%; line-height: 1.6; font-size: 16px; padding: 12px 18px; border-radius: 18px; }}
        .user-message {{ align-self: flex-end; background: #f0f4f9; border-bottom-right-radius: 4px; }}
        .assistant-message {{ align-self: flex-start; background: transparent; border-left: 3px solid var(--gemini-blue); }}

        /* Sehemu ya Kuandikia (Siku zote inakaa chini) */
        .input-wrapper {{ 
            padding: 20px 10%; background: white; border-top: 1px solid #f5f5f5;
        }}
        .input-box {{ 
            display: flex; background: #f0f4f9; padding: 5px 20px; 
            border-radius: 30px; align-items: center; gap: 10px;
        }}
        input {{ 
            flex: 1; border: none; background: transparent; outline: none; 
            padding: 12px; font-size: 16px; color: #1f1f1f;
        }}

        /* RESPONSIVE KWA SIMU */
        @media (max-width: 768px) {{
            #menu-toggle {{ display: block; }}
            .sidebar {{ position: absolute; left: -260px; height: 100%; z-index: 999; }}
            .sidebar.active {{ left: 0; box-shadow: 10px 0 20px rgba(0,0,0,0.05); }}
            .chat-container {{ padding: 20px 5%; }}
            .input-wrapper {{ padding: 15px 5%; }}
            .message {{ max-width: 90%; font-size: 15px; }}
        }}
    </style>
</head>
<body>

    <div class="app-wrapper">
        <div class="sidebar" id="sidebar">
            <button style="margin-bottom:20px; padding:10px; border-radius:20px; border:1px solid #ccc; background:white; cursor:pointer;" onclick="location.reload()">+ New Chat</button>
            <div id="history-list"></div>
        </div>

        <div class="main-content">
            <div class="chat-header">
                <button id="menu-toggle">☰</button>
                <b style="font-size:1.2rem; color:var(--gemini-blue);">KONDOWE AI PRO</b>
            </div>

            <div class="chat-container" id="chat-container">
                <div id="welcome" style="text-align:center; margin-top:15vh; color:#5f6368;">
                    <h2>Je, nikupe msaada gani leo?</h2>
                </div>
            </div>

            <div class="input-wrapper">
                <div class="input-box">
                    <input type="text" id="user-input" placeholder="Uliza chochote..." autocomplete="off">
                    <button id="send-btn" style="border:none; background:none; color:var(--gemini-blue); font-size:24px; cursor:pointer;">➤</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Sidebar Toggle
        const sidebar = document.getElementById('sidebar');
        document.getElementById('menu-toggle').onclick = () => sidebar.classList.toggle('active');

        const _client = supabase.createClient("{SUPABASE_URL}", "{SUPABASE_KEY}");
        
        async function sendMessage() {{
            const input = document.getElementById('user-input');
            const msg = input.value.trim();
            if(!msg) return;

            document.getElementById('welcome').style.display = 'none';
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

components.html(html_code, height=1500)
