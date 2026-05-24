import streamlit as st
import json
import asyncio
import os
import time
import threading
import gc
import requests
from datetime import datetime
from playwright.async_api import async_playwright

# --- YOUR TELEGRAM CREDENTIALS (SET) ---
TELEGRAM_BOT_TOKEN =  "8249587356:AAEdyXK8RycAbIUYygOVNhpmo686BEQXl3c"
ADMIN_CHAT_ID = "8529773707"

def send_telegram_alert(message):
    """Sends notification to Your Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": ADMIN_CHAT_ID, "text": message}
        requests.post(url, data=data)
    except: pass

# --- Page Config ---
st.set_page_config(page_title="N3H9L  PRO SERVER", page_icon="ðŸ“¡", layout="wide")

# --- UI CSS (Liquid Glass / Glassmorphism) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    /* â”€â”€ Background Image â”€â”€ */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-image: url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        min-height: 100vh;
    }

    /* dark overlay on background */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background: linear-gradient(135deg, rgba(10,10,40,0.55) 0%, rgba(0,60,120,0.45) 100%);
        backdrop-filter: blur(0px);
        z-index: 0;
        pointer-events: none;
    }

    /* â”€â”€ Liquid Glass Base â”€â”€ */
    .glass {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255,255,255,0.3);
    }

    /* â”€â”€ Main Header â”€â”€ */
    .main-header {
        text-align: center;
        background: rgba(255, 255, 255, 0.10);
        backdrop-filter: blur(24px) saturate(200%);
        -webkit-backdrop-filter: blur(24px) saturate(200%);
        border: 1px solid rgba(255,255,255,0.28);
        padding: 28px 20px;
        border-radius: 24px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 40px rgba(0,80,200,0.25), inset 0 1px 0 rgba(255,255,255,0.35);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -60%;
        left: -20%;
        width: 80px;
        height: 200%;
        background: rgba(255,255,255,0.08);
        transform: rotate(25deg);
        border-radius: 50%;
        pointer-events: none;
    }
    .main-header h1 {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin: 0 0 6px 0;
        text-shadow: 0 2px 12px rgba(0,0,0,0.3);
        background: linear-gradient(90deg, #ffffff, #a8d8ff, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .main-header p { margin: 0; font-size: 0.95rem; color: rgba(255,255,255,0.8); }

    /* â”€â”€ Status Box â”€â”€ */
    .status-box {
        padding: 14px 20px;
        border-radius: 16px;
        text-align: center;
        font-weight: 700;
        margin-bottom: 18px;
        font-size: 15px;
        backdrop-filter: blur(16px) saturate(160%);
        -webkit-backdrop-filter: blur(16px) saturate(160%);
        border: 1px solid rgba(255,255,255,0.22);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        letter-spacing: 0.5px;
    }
    .running {
        background: rgba(39, 174, 96, 0.20);
        color: #7fffb2;
        border-color: rgba(39,174,96,0.45);
        text-shadow: 0 0 12px rgba(0,255,100,0.4);
    }
    .stopped {
        background: rgba(231, 76, 60, 0.18);
        color: #ffaaaa;
        border-color: rgba(231,76,60,0.40);
        text-shadow: 0 0 12px rgba(255,80,80,0.4);
    }

    /* â”€â”€ Login Container â”€â”€ */
    .login-container {
        max-width: 420px;
        margin: 80px auto;
        padding: 40px 36px;
        background: rgba(255,255,255,0.10);
        backdrop-filter: blur(28px) saturate(200%);
        -webkit-backdrop-filter: blur(28px) saturate(200%);
        border: 1px solid rgba(255,255,255,0.28);
        border-radius: 28px;
        box-shadow: 0 16px 48px rgba(0,0,0,0.30), inset 0 1px 0 rgba(255,255,255,0.35);
        text-align: center;
        color: white;
    }
    .login-container h2 {
        background: linear-gradient(90deg, #60b4ff, #a78bfa, #60b4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .login-container p { color: rgba(255,255,255,0.7); margin: 0; }

    /* â”€â”€ Streamlit Widgets Override â”€â”€ */
    section[data-testid="stSidebar"] {
        background: rgba(10, 15, 40, 0.55) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255,255,255,0.12) !important;
    }
    section[data-testid="stSidebar"] * { color: white !important; }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextArea"] textarea {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 12px !important;
        color: white !important;
        backdrop-filter: blur(8px) !important;
    }
    div[data-testid="stTextInput"] input::placeholder,
    div[data-testid="stTextArea"] textarea::placeholder { color: rgba(255,255,255,0.4) !important; }
    div[data-testid="stTextInput"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stFileUploader"] label,
    .stMarkdown, .stMarkdown p, h1, h2, h3, h4 { color: white !important; }

    div[data-testid="stButton"] button {
        background: rgba(255,255,255,0.14) !important;
        backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(255,255,255,0.30) !important;
        border-radius: 14px !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.20), inset 0 1px 0 rgba(255,255,255,0.30) !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stButton"] button:hover {
        background: rgba(255,255,255,0.22) !important;
        box-shadow: 0 6px 24px rgba(0,120,255,0.30), inset 0 1px 0 rgba(255,255,255,0.40) !important;
        transform: translateY(-1px) !important;
    }

    div[data-testid="stContainer"] {
        background: rgba(255,255,255,0.08) !important;
        backdrop-filter: blur(18px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(18px) saturate(180%) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.20), inset 0 1px 0 rgba(255,255,255,0.20) !important;
        padding: 20px !important;
    }

    div[data-testid="stCodeBlock"] {
        background: rgba(0,0,0,0.30) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 14px !important;
    }
    div[data-testid="stCodeBlock"] code { color: #a8ffcc !important; font-size: 12px !important; }

    .stFileUploader {
        background: rgba(255,255,255,0.06) !important;
        border: 1px dashed rgba(255,255,255,0.25) !important;
        border-radius: 14px !important;
        color: white !important;
    }

    div[data-testid="stAlert"] {
        background: rgba(255,255,255,0.10) !important;
        border: 1px solid rgba(255,255,255,0.20) !important;
        border-radius: 12px !important;
        color: white !important;
        backdrop-filter: blur(10px) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MULTI-USER FILE SYSTEM ---
BASE_DIR = "users_data"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

def get_user_path(username, filename):
    user_folder = os.path.join(BASE_DIR, username)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return os.path.join(user_folder, filename)

def read_user_file(username, filename):
    path = get_user_path(username, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f: return f.read().strip()
    return ""

def write_user_file(username, filename, content):
    path = get_user_path(username, filename)
    with open(path, 'w', encoding='utf-8') as f: f.write(str(content))

def append_user_log(username, msg):
    path = get_user_path(username, 'logs.txt')
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {msg}\n")

def get_user_logs(username):
    path = get_user_path(username, 'logs.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return "".join(f.readlines()[-60:])
    return "Waiting for logs..."

# --- BOT ENGINE ---
async def run_bot_logic(username):
    if read_user_file(username, 'status.txt') != "running": return

    thread_id = read_user_file(username, 'thread.txt')
    file_content = read_user_file(username, 'message.txt')
    
    if not file_content:
        append_user_log(username, "âŒ Message file empty!")
        write_user_file(username, 'status.txt', "stopped")
        return
        
    lines = [line.strip() for line in file_content.split('\n') if line.strip()]
    hater_name = read_user_file(username, 'hatername.txt')
    if hater_name:
        lines = [f"{hater_name} {line}" for line in lines]
    
    # TELEGRAM ALERT: START
    append_user_log(username, f"ðŸš€ Started for User: {username}")
    send_telegram_alert(f"ðŸš€ BOT STARTED!\nðŸ‘¤ User: {username}\nðŸ“ Thread: {thread_id}\nðŸ“‚ Messages Loaded: {len(lines)}")

    async with async_playwright() as p:
        try:
            import shutil
            chromium_path = shutil.which("chromium") or "/nix/store/qa9cnw4v5xkxyip6mb9kxqfq1z4x2dx1-chromium-138.0.7204.100/bin/chromium"
            browser = await p.chromium.launch(
                headless=True,
                executable_path=chromium_path,
                args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
            )
            context = await browser.new_context(viewport={'width': 1280, 'height': 800})
            
            cookie_path = get_user_path(username, 'cookies.json')
            if os.path.exists(cookie_path):
                try:
                    with open(cookie_path, 'r') as f:
                        await context.add_cookies(json.load(f))
                except: pass
            
            page = await context.new_page()
            append_user_log(username, "ðŸŒ Opening Facebook thread...")
            try:
                await page.goto(f"https://www.facebook.com/messages/t/{thread_id}", timeout=60000)
            except: pass

            # Wait for message input to appear (FB loads dynamically)
            MSG_SELECTORS = [
                'div[contenteditable="true"][aria-label="Message"]',
                'div[contenteditable="true"][aria-label="Aa"]',
                'div[contenteditable="true"][role="textbox"]',
                'div[contenteditable="true"]',
            ]

            async def find_input():
                for sel in MSG_SELECTORS:
                    try:
                        el = await page.wait_for_selector(sel, timeout=1500, state="visible")
                        if el:
                            return sel
                    except: continue
                return None

            await asyncio.sleep(2)
            input_sel = await find_input()
            if not input_sel:
                append_user_log(username, "âš ï¸ Chat input not found, retrying after 5s...")
                await asyncio.sleep(5)
                input_sel = await find_input()

            if not input_sel:
                append_user_log(username, "âŒ Could not find message input! Check cookies/thread ID.")
                write_user_file(username, 'status.txt', "stopped")
                await browser.close()
                return

            append_user_log(username, f"âœ… Chat input found! Starting to send messages.")
            msg_counter = 0

            while read_user_file(username, 'status.txt') == "running":
                for line in lines:
                    if read_user_file(username, 'status.txt') != "running": break

                    try: speed = float(read_user_file(username, 'speed.txt') or 60)
                    except: speed = 30.0

                    sent = False
                    try:
                        # Focus via JS â€” no actionability timeout
                        focused = await page.evaluate("""(sel) => {
                            const el = document.querySelector(sel);
                            if (!el) return false;
                            el.focus();
                            return true;
                        }""", input_sel)

                        if not focused:
                            input_sel = await find_input()
                            if input_sel:
                                focused = await page.evaluate("""(sel) => {
                                    const el = document.querySelector(sel);
                                    if (!el) return false;
                                    el.focus();
                                    return true;
                                }""", input_sel)

                        if focused:
                            # Type message fast (delay=0) â€” triggers React's real input events
                            await page.keyboard.type(line, delay=0)
                            await page.keyboard.press('Enter')

                            # Verify send: wait until input box is empty (= Facebook sent it)
                            for _ in range(15):
                                await asyncio.sleep(0.1)
                                is_empty = await page.evaluate("""(sel) => {
                                    const el = document.querySelector(sel);
                                    return el ? el.textContent.trim() === '' : true;
                                }""", input_sel)
                                if is_empty:
                                    break
                            else:
                                # Box not cleared â€” press Enter once more
                                await page.keyboard.press('Enter')
                                await asyncio.sleep(0.2)

                            sent = True
                        else:
                            append_user_log(username, "âš ï¸ Input box lost, reloading page...")
                            await page.reload()
                            await asyncio.sleep(4)
                            input_sel = await find_input()

                    except Exception as e:
                        append_user_log(username, f"âŒ Send Error: {str(e)[:80]}")

                    if sent:
                        msg_counter += 1
                        append_user_log(username, f"âœ… [{msg_counter}] Sent: {line[:50]}")
                        if msg_counter % 50 == 0:
                            send_telegram_alert(f"â„¹ï¸ UPDATE:\nðŸ‘¤ User: {username}\nâœ… Sent {msg_counter} messages so far.")

                    gc.collect()

                    # Fast sleep with status check every 0.5s
                    elapsed = 0.0
                    while elapsed < speed:
                        if read_user_file(username, 'status.txt') != "running": break
                        step = min(0.5, speed - elapsed)
                        await asyncio.sleep(step)
                        elapsed += step

                    if msg_counter > 0 and msg_counter % 100 == 0:
                        append_user_log(username, "ðŸ§¹ Cleaning Memory...")
                        await page.reload()
                        await asyncio.sleep(3)
                        input_sel = await find_input() or input_sel

            await browser.close()
            append_user_log(username, "ðŸ›‘ Stopped.")
            send_telegram_alert(f"ðŸ›‘ BOT STOPPED!\nðŸ‘¤ User: {username}\nâœ… Total Sent: {msg_counter}")

        except Exception as e:
            append_user_log(username, f"âŒ Critical Error: {str(e)}")
            write_user_file(username, 'status.txt', "stopped")
            send_telegram_alert(f"âš ï¸ BOT CRASHED!\nðŸ‘¤ User: {username}\nâŒ Error: {str(e)}")

def start_user_thread(username):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot_logic(username))

# --- MAIN UI LOGIC ---

if 'username' not in st.session_state:
    st.session_state.username = None

# LOGIN SCREEN
if st.session_state.username is None:
    st.markdown("""
    <div class="login-container">
        <h2 style="color:#1877f2;">ðŸ” N3H9L SERVER</h2>
        <p>Enter Session Name to access workspace.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user_input = st.text_input("Enter Session Name", placeholder="e.g. N3H9L")
        if st.button("ðŸš€ Enter Dashboard", use_container_width=True):
            if user_input.strip():
                st.session_state.username = user_input.strip()
                # TELEGRAM ALERT: LOGIN
                send_telegram_alert(f"ðŸ”‘ NEW LOGIN DETECTED!\nðŸ‘¤ User: {user_input.strip()}")
                st.rerun()
            else:
                st.warning("Enter a name!")
    st.stop()

# DASHBOARD
USERNAME = st.session_state.username

with st.sidebar:
    st.title(f"ðŸ‘¤ {USERNAME}")
    if st.button("ðŸšª Logout"):
        st.session_state.username = None
        st.rerun()
    st.success("Telegram Updates: ACTIVE âœ…")

st.markdown(f"""
<div class="main-header">
    <h1>N3H9L  SERVER</h1>
    <p>Logged in as: <b>{USERNAME}</b> â€¢ Telegram Connected</p>
</div>
""", unsafe_allow_html=True)

status = read_user_file(USERNAME, 'status.txt')
if status == "running":
    st.markdown(f'<div class="status-box running">âš¡ {USERNAME} SERVER IS RUNNING</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-box stopped">ðŸ›‘ {USERNAME} SERVER IS STOPPED</div>', unsafe_allow_html=True)

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        tid = st.text_input("Thread ID", value=read_user_file(USERNAME, 'thread.txt'))
    with col2:
        spd = st.number_input("Speed (Seconds)", min_value=0.1, step=0.1, value=float(read_user_file(USERNAME, 'speed.txt') or 1.0))
    
    hater_name_val = st.text_input("ðŸ‘¿ Hater Name", value=read_user_file(USERNAME, 'hatername.txt'), placeholder="e.g. Rahul (added before each message)")

    uploaded_file = st.file_uploader("ðŸ“‚ Message File", type=['txt'])
    if uploaded_file:
        content = uploaded_file.read().decode('utf-8')
        write_user_file(USERNAME, 'message.txt', content)
        st.success("File Uploaded!")
    
    ck = st.text_area("Cookies", height=100, placeholder="Paste Cookies...")
    
    if st.button("ðŸ’¾ Save Settings", use_container_width=True):
        write_user_file(USERNAME, 'thread.txt', tid)
        write_user_file(USERNAME, 'speed.txt', spd)
        write_user_file(USERNAME, 'hatername.txt', hater_name_val.strip())
        if ck.strip():
            try:
                if ck.strip().startswith('['): c = json.loads(ck)
                else:
                    c = []
                    for p in ck.split(';'):
                        if '=' in p:
                            n, v = p.strip().split('=', 1)
                            c.append({'name': n, 'value': v, 'domain': '.facebook.com', 'path': '/'})
                with open(get_user_path(USERNAME, 'cookies.json'), 'w') as f: json.dump(c, f)
            except: pass
        st.success("Settings Saved!")

c1, c2 = st.columns(2)
with c1:
    if st.button("ðŸš€ START SERVER", use_container_width=True):
        if status != "running":
            write_user_file(USERNAME, 'status.txt', "running")
            with open(get_user_path(USERNAME, 'logs.txt'), 'w') as f: f.write("--- STARTED ---\n")
            threading.Thread(target=start_user_thread, args=(USERNAME,), daemon=True).start()
            time.sleep(1)
            st.rerun()

with c2:
    if st.button("ðŸ›‘ STOP SERVER", use_container_width=True):
        write_user_file(USERNAME, 'status.txt', "stopped")
        st.rerun()

st.markdown("### ðŸ“Ÿ Live Logs")
st.code(get_user_logs(USERNAME), language='text')

if status == "running":
    time.sleep(2)
    st.rerun()
