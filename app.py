import streamlit as st
import requests
import uuid
import random
from supabase import create_client

# ─── CONFIG ───
st.set_page_config(page_title="AfterShow", layout="wide", initial_sidebar_state="collapsed")


for key in ["user", "pagina", "splash", "injetado", "wiki_result", "supabase_client", "amigo_id", "conversa_amigo"]:
    if key not in st.session_state:
        if key == "user":
            st.session_state.user = None
        elif key == "pagina":
            st.session_state.pagina = "Inicio"
        elif key == "splash":
            st.session_state.splash = True
        elif key == "injetado":
            st.session_state.injetado = False
        elif key == "wiki_result":
            st.session_state.wiki_result = None
        elif key == "supabase_client":
            st.session_state.supabase_client = None
        elif key == "amigo_id":
            st.session_state.amigo_id = None
        elif key == "conversa_amigo":
            st.session_state.conversa_amigo = None


SUPABASE_URL = st.secrets.get("supabase_url", "https://ntxqfaqskorbxbaswdsl.supabase.co")
SUPABASE_KEY = st.secrets.get("supabase_key", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im50eHFmYXFza29yYnhiYXN3ZHNsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkyNjYyMjEsImV4cCI6MjA5NDg0MjIyMX0.sQjACD4u2hv_c7HkILvI5fshxkvvUNMKvlaony0ag2c")

if st.session_state.supabase_client is None:
    st.session_state.supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
supabase = st.session_state.supabase_client


random.seed(42)
estrelas_html = ""
for _ in range(60):
    l = random.randint(0, 100)
    t = random.randint(0, 100)
    sz = random.choice([1, 2, 3])
    d = random.choice([2, 3, 4, 5])
    delay = round(random.uniform(0, 6), 1)
    op = round(random.uniform(0.3, 0.9), 2)
    estrelas_html += (
        f'<span style="left:{l}%;top:{t}%;width:{sz}px;height:{sz}px;'
        f"--d:{d}s;animation-delay:{delay}s;opacity:{op}\"></span>\n"
    )

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;900&family=Montserrat:wght@300;400;500;600;700&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html, body, [class*="css"] {{
    font-family: 'Montserrat', sans-serif;
    color: #FFF8E7;
}}

.stApp {{
    background: linear-gradient(170deg, #0d0a08 0%, #1a1510 30%, #0d0a08 100%) !important;
}}

/* Force dark background on all Streamlit containers */
[data-testid="stAppViewContainer"] {{
    background: transparent !important;
}}
.main, .block-container, .st-emotion-cache-z5fcl4, .st-emotion-cache-1wmy9hl {{
    background: transparent !important;
}}
section[data-testid="stAppViewContainer"] > div:first-child {{
    background: transparent !important;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

/* keep content width consistent whether sidebar is open or closed */
[data-testid="stAppViewContainer"] > .main {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 clamp(16px, 3vw, 40px);
    transition: none !important;
}}

/* ===== VIGNETTE / GLOW OVERLAY ===== */
.stApp::before {{
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 100% 60% at 50% 0%, #C9A84C15 0%, transparent 70%),
        radial-gradient(ellipse 70% 50% at 30% 80%, #C9A84C10 0%, transparent 60%),
        radial-gradient(ellipse 60% 60% at 70% 20%, #C9A84C08 0%, transparent 50%),
        radial-gradient(ellipse 40% 40% at 50% 50%, #C9A84C05 0%, transparent 40%);
    pointer-events: none;
    z-index: 0;
}}

.stApp::after {{
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    background-repeat: repeat;
    background-size: 256px 256px;
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}}

.starfield {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}}
.starfield span {{
    position: absolute;
    background: #C9A84C;
    border-radius: 50%;
    animation: twinkle var(--d, 3s) ease-in-out infinite;
    box-shadow: 0 0 4px #C9A84C44, 0 0 8px #C9A84C22;
}}
@keyframes twinkle {{
    0%, 100% {{ opacity: 0.15; transform: scale(0.8); }}
    50% {{ opacity: 1; transform: scale(1.3); }}
}}

.splash-section {{
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: radial-gradient(ellipse at center, #1a1510 0%, #0d0a08 80%);
    border-radius: 24px;
    margin: 20px 0;
    position: relative;
    z-index: 1;
    box-shadow: inset 0 0 100px #C9A84C08, 0 0 60px #00000055;
}}
.splash-content {{
    text-align: center;
    animation: splashIn 1.2s ease-out forwards;
    padding: 40px;
    border: 1px solid #C9A84C22;
    border-radius: 24px;
    background: radial-gradient(ellipse at center, #1a1510cc, #0d0a08cc);
    backdrop-filter: blur(20px);
    max-width: 600px;
}}
@keyframes splashIn {{
    0% {{ opacity: 0; transform: scale(0.85) translateY(30px); }}
    100% {{ opacity: 1; transform: scale(1) translateY(0); }}
}}
.splash-star {{
    font-size: 60px;
    display: block;
    margin-bottom: 10px;
    animation: spinStar 4s linear infinite;
}}
@keyframes spinStar {{
    0% {{ transform: rotate(0deg) scale(1); }}
    50% {{ transform: rotate(180deg) scale(1.1); }}
    100% {{ transform: rotate(360deg) scale(1); }}
}}
.splash-title {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(48px, 10vw, 90px);
    font-weight: 900;
    color: #C9A84C;
    letter-spacing: 4px;
    text-shadow: 0 0 40px #C9A84C33, 0 0 80px #C9A84C11;
    line-height: 1;
}}
.splash-subtitle {{
    font-family: 'Montserrat', sans-serif;
    font-size: clamp(14px, 2.5vw, 20px);
    color: #C9A84C;
    letter-spacing: 8px;
    text-transform: uppercase;
    margin-top: 15px;
    font-weight: 300;
}}
    margin-top: 10px;
}}
.splash-btn button {{
    background: linear-gradient(135deg, #C9A84C, #a8872e) !important;
    color: #0d0a08 !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 14px 48px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    transition: all 0.4s !important;
    box-shadow: 0 0 30px #C9A84C33 !important;
    cursor: pointer !important;
}}
.splash-btn button:hover {{
    transform: scale(1.05) !important;
    box-shadow: 0 0 50px #C9A84C55 !important;
}}

h1 {{
    font-family: 'Playfair Display', serif !important;
    color: #C9A84C !important;
    font-size: 48px !important;
    letter-spacing: 1px;
    margin-bottom: 20px !important;
    text-shadow: 0 0 30px #C9A84C22;
    position: relative;
    display: inline-block;
    padding-bottom: 12px;
    border-bottom: 2px solid #C9A84C !important;
}}
h2 {{
    font-family: 'Playfair Display', serif !important;
    color: #F5E6C8 !important;
    font-size: 32px !important;
    letter-spacing: 0.5px;
    text-shadow: 0 0 20px #C9A84C33;
    margin-bottom: 8px !important;
    position: relative;
    display: inline-block;
    padding-bottom: 6px;
    border-bottom: 1px solid #C9A84C55 !important;
}}
h3 {{
    font-family: 'Playfair Display', serif !important;
    color: #F5E6C8 !important;
    font-weight: 600 !important;
    font-size: 20px !important;
    letter-spacing: 0.3px;
    margin-bottom: 14px !important;
}}
p, li, .stMarkdown {{
    color: #FFF8E7 !important;
}}
a, a:visited, a:hover, a:active {{
    color: #C9A84C !important;
}}

section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0d0a08 0%, #120e0a 100%);
    border-right: 1px solid #C9A84C22;
    padding-top: 10px;
    position: relative;
    z-index: 1;
}}
section[data-testid="stSidebar"] > div {{
    padding: 0 !important;
}}
.sidebar-brand {{
    text-align: center;
    padding: 25px 15px 20px;
    border-bottom: 1px solid #C9A84C22;
    margin-bottom: 10px;
}}
.sidebar-brand h2 {{
    font-family: 'Playfair Display', serif !important;
    color: #C9A84C !important;
    font-size: 22px !important;
    margin: 0 !important;
}}
.sidebar-brand p {{
    font-size: 11px;
    color: #C9A84C;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 4px;
}}
.sidebar-user {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 15px 16px;
    background: linear-gradient(135deg, #C9A84C08, #C9A84C15);
    border: 1px solid #C9A84C33;
    border-radius: 12px;
    margin: 0 12px 15px;
    transition: all 0.3s;
}}
.sidebar-user:hover {{
    border-color: #C9A84C33;
    box-shadow: 0 4px 20px #00000044;
}}
.sidebar-user .avatares {{
    width: 40px; height: 40px;
    border-radius: 50%;
    border: 2px solid #C9A84C;
    object-fit: cover;
}}
.sidebar-user-info h4 {{
    font-size: 14px;
    margin: 0;
    color: #C9A84C;
}}
.sidebar-user-info p {{
    font-size: 11px;
    color: #C9A84C;
    margin: 0;
}}

.nav-section {{
    padding: 0 8px;
}}
.nav-section button {{
    background: transparent !important;
    border: none !important;
    color: #C9A84C !important;
    text-align: left !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    width: 100% !important;
    transition: all 0.25s !important;
    margin: 1px 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}}
.nav-section button:hover {{
    background: #C9A84C15 !important;
    color: #C9A84C !important;
    transform: translateX(4px) !important;
}}
.nav-section button:focus {{
    box-shadow: none !important;
}}
.nav-active button {{
    background: #C9A84C20 !important;
    color: #C9A84C !important;
    font-weight: 600 !important;
    border-left: 3px solid #C9A84C !important;
}}

/* ===== BUTTONS ===== */
.stButton > button {{
    background: linear-gradient(135deg, #C9A84C, #a8872e) !important;
    color: #0d0a08 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 15px #C9A84C22 !important;
    position: relative;
    z-index: 1;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px #C9A84C44 !important;
}}
.stButton > button:active {{
    transform: translateY(0) !important;
    box-shadow: 0 2px 10px #C9A84C22 !important;
}}

/* secondary buttons */
.stButton > button[data-secondary="true"],
button.secondary {{
    background: transparent !important;
    color: #C9A84C !important;
    border: 1px solid #C9A84C55 !important;
    box-shadow: none !important;
}}
.stButton > button[data-secondary="true"]:hover,
button.secondary:hover {{
    background: #C9A84C15 !important;
    box-shadow: 0 4px 20px #C9A84C22 !important;
}}

/* ===== PAGE CONTENT ===== */
.page-content {{
    position: relative;
    z-index: 1;
    background: radial-gradient(ellipse 80% 60% at 50% 0%, #C9A84C08, transparent 80%);
    border-radius: 20px;
    padding: 32px;
    backdrop-filter: blur(6px);
    box-shadow: 0 0 60px #C9A84C22, inset 0 0 60px #C9A84C08;
    margin-bottom: 20px;
}}
.card {{
    background: linear-gradient(145deg, #1c1612, #0d0a08);
    border: 1px solid #C9A84C33;
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.4s;
    box-shadow: 0 4px 20px #00000033, inset 0 1px 0 #C9A84C11;
    position: relative;
    overflow: hidden;
}}
.card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #C9A84C55, transparent);
}}
.card:hover {{
    border-color: #C9A84C55;
    box-shadow: 0 8px 40px #00000066, 0 0 30px #C9A84C15, inset 0 1px 0 #C9A84C22;
    transform: translateY(-3px);
}}

/* ===== DIVIDER ===== */
.stDivider {{
    height: 0 !important;
    margin: 0 !important;
    border: none !important;
    background: transparent !important;
}}
.login-card {{
    background: linear-gradient(145deg, #1c1612, #0d0a08);
    border: 1px solid #C9A84C33;
    border-radius: 24px;
    padding: 40px 36px;
    box-shadow: 0 20px 60px #00000066, 0 0 40px #C9A84C15;
    position: relative;
    overflow: hidden;
}}
.login-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 25%; right: 25%;
    height: 1px;
    background: linear-gradient(90deg, transparent, #C9A84C, transparent);
}}
.login-title {{
    text-align: center;
    margin-bottom: 30px;
}}
.login-title h1 {{
    font-size: 36px !important;
    margin-bottom: 4px !important;
}}
.login-title p {{
    color: #C9A84C;
    font-size: 13px;
    letter-spacing: 2px;
    text-transform: uppercase;
}}
.login-tabs {{
    display: flex;
    gap: 0;
    margin-bottom: 25px;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #C9A84C22;
}}
.login-tab {{
    padding: 12px 24px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.3s;
    background: transparent;
    color: #C9A84C;
    border: none;
}}
.login-tab.active {{
    background: #C9A84C;
    color: #0d0a08;
}}

/* ===== FORM FIELDS ===== */
.stSelectbox label, .stTextInput label, .stTextArea label,
[data-testid="stSelectbox"] p, [data-testid="stTextInput"] p, [data-testid="stTextArea"] p {{
    color: #C9A84C !important;
    font-weight: 600 !important;
}}
.stTextInput input, .stTextArea textarea, .stSelectbox div, .stSlider {{
    background: #0d0a08 !important;
    border: 1px solid #C9A84C33 !important;
    border-radius: 8px !important;
    color: #C9A84C !important;
    transition: all 0.3s !important;
}}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {{
    color: #C9A84C !important;
    opacity: 1 !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: #C9A84C66 !important;
    box-shadow: 0 0 20px #C9A84C22, inset 0 0 0 1px #C9A84C22 !important;
}}
.stSelectbox div:focus-within {{
    border-color: #C9A84C66 !important;
    box-shadow: 0 0 20px #C9A84C22 !important;
}}
.stSelectbox [data-baseweb="select"] > div {{
    background: #0d0a08 !important;
    border: 1px solid #C9A84C15 !important;
}}
[role="option"] {{
    color: #C9A84C !important;
}}
.stSelectbox ul {{
    background: #1a1510 !important;
    border: 1px solid #C9A84C33 !important;
}}
.stSelectbox li,
.stSelectbox [role="option"],
.stSelectbox [data-baseweb="menu-item"] {{
    color: #C9A84C !important;
}}
.stSelectbox li:hover,
.stSelectbox [role="option"]:hover {{
    background: #C9A84C20 !important;
}}

.stRadio div[role="radiogroup"] {{
    gap: 4px !important;
}}
.stRadio label {{
    color: #C9A84C !important;
}}

.loading-spinner {{
    text-align: center;
    padding: 40px;
}}
.spinner-star {{
    display: inline-block;
    font-size: 32px;
    animation: spinStar 1.5s linear infinite;
    color: #C9A84C;
}}

::-webkit-scrollbar {{
    width: 6px;
}}
::-webkit-scrollbar-track {{
    background: #0d0a08;
}}
::-webkit-scrollbar-thumb {{
    background: #C9A84C44;
    border-radius: 3px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: #C9A84C66;
}}

.fade-in {{
    animation: fadeIn 0.6s ease-out forwards;
}}
@keyframes fadeIn {{
    0% {{ opacity: 0; transform: translateY(10px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}


.poster-frame {{
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 30px #C9A84C22, 0 10px 40px #00000066;
    transition: 0.4s;
}}
.poster-frame:hover {{
    box-shadow: 0 0 50px #C9A84C44, 0 15px 60px #00000088;
    transform: translateY(-5px);
}}

.tag {{
    display: inline-block;
    background: #C9A84C20;
    color: #C9A84C;
    font-size: 12px;
    padding: 3px 12px;
    border-radius: 20px;
    border: 1px solid #C9A84C33;
}}
.tag-streaming {{
    background: #C9A84C15;
    color: #C9A84C;
    border-color: #C9A84C33;
}}

.wiki-card {{
    background: linear-gradient(145deg, #1a1510, #0d0a08);
    border: 1px solid #C9A84C33;
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    backdrop-filter: blur(12px);
    transition: all 0.3s;
}}
.wiki-card h3 {{
    color: #C9A84C !important;
    margin-bottom: 8px;
}}
.wiki-card:hover {{
    border-color: #C9A84C33;
    box-shadow: 0 8px 30px #00000055;
}}


.mt-0 {{ margin-top: 0 !important; }}
.mb-0 {{ margin-bottom: 0 !important; }}
.text-center {{ text-align: center; }}
.text-gold {{ color: #C9A84C !important; }}
</style>
"""

# ─── INJECT CSS + STARS ───
st.markdown(CSS, unsafe_allow_html=True)
if not st.session_state.injetado:
    st.markdown(
        f'<div class="starfield">{estrelas_html}</div>',
        unsafe_allow_html=True,
    )
    st.session_state.injetado = True


def login(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email, "password": password
        })
        st.session_state.user = response.user
        return True
    except Exception as e:
        st.error(str(e))
        return False

def signup(email, password, bio):
    try:
        response = supabase.auth.sign_up({
            "email": email, "password": password
        })
        supabase.table("profiles").insert({
            "id": response.user.id,
            "username": email.split("@")[0],
            "bio": bio
        }).execute()
        st.success("Conta criada! Agora faça login.")
        return True
    except Exception as e:
        st.error(str(e))
        return False


def search_wikipedia(query, categoria="", lang="pt"):
    import urllib.parse
    headers = {"User-Agent": "AfterShow/1.0 (aftershow-app@example.com)"}
    try:
        termos = query.strip()
        if categoria == "musical":
            termos = f"{query} (musical)"
        elif categoria == "teatro":
            termos = f"{query} (peça de teatro)"

        params = {
            "action": "query",
            "list": "search",
            "srsearch": termos,
            "format": "json",
            "srlimit": 3,
            "srprop": "snippet",
        }
        r = requests.get(
            f"https://{lang}.wikipedia.org/w/api.php",
            params=params, headers=headers, timeout=12,
        )
        data = r.json()
        results = data.get("query", {}).get("search", [])

        if not results:
            if lang == "pt":
                return search_wikipedia(query, categoria, "en")
            return None

        page_title = results[0]["title"]
        detail_params = {
            "action": "query",
            "prop": "extracts|pageimages|info",
            "exintro": True,
            "explaintext": True,
            "pithumbsize": 600,
            "titles": page_title,
            "format": "json",
            "inprop": "url",
        }
        r2 = requests.get(
            f"https://{lang}.wikipedia.org/w/api.php",
            params=detail_params, headers=headers, timeout=12,
        )
        detail_data = r2.json()
        pages = detail_data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid != "-1":
                return {
                    "title": page.get("title", ""),
                    "extract": page.get("extract", "")[:2500],
                    "image": page.get("thumbnail", {}).get("source", ""),
                    "url": page.get("canonicalurl", ""),
                    "lang": lang,
                }
    except Exception:
        pass
    return None

def render_splash():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.markdown("""
    <div class="splash-section">
        <div style="text-align:center; animation: splashIn 1.2s ease-out forwards;">
            <span class="splash-star">✦</span>
            <div class="splash-title">AfterShow</div>
            <div class="splash-subtitle">O seu mundo cultural</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="splash-btn" style="text-align:center;">', unsafe_allow_html=True)
        if st.button("✦ ENTRAR ✦", use_container_width=True):
            st.session_state.splash = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_login_page():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-card">
                <div class="login-title">
                    <h1>AfterShow</h1>
                    <p>Faça parte do mundo cultural</p>
                </div>
        """, unsafe_allow_html=True)

        modo = st.radio("Acesso", ["Login", "Cadastro"], horizontal=True, label_visibility="collapsed")
        email = st.text_input("Email", placeholder="seu@email.com")
        password = st.text_input("Senha", type="password", placeholder="••••••••")

        bio = None
        if modo == "Cadastro":
            bio = st.text_area("Bio", placeholder="Nos conte sobre você...", height=100)

        if modo == "Login":
            if st.button("Entrar", use_container_width=True):
                if login(email, password):
                    st.success("Login realizado com sucesso!")
                    st.rerun()
        else:
            if st.button("Criar Conta", use_container_width=True):
                signup(email, password, bio or "")

        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar():
    dados_perfil = None
    try:
        perfil = supabase.table("profiles").select("*").eq(
            "id", st.session_state.user.id
        ).execute()
        if perfil.data:
            dados_perfil = perfil.data[0]
    except Exception:
        pass

    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <h2>✦ AfterShow</h2>
            <p>Plataforma Cultural</p>
        </div>
        """, unsafe_allow_html=True)

        if dados_perfil:
            avatar = dados_perfil.get("avatar_url", "")
            username = dados_perfil.get("username", "Usuário")
            bio = dados_perfil.get("bio", "")
            st.markdown(f"""
            <div class="sidebar-user">
                <div>
                    {"<div style='width:40px;height:40px;border-radius:50%;overflow:hidden;border:2px solid #C9A84C;flex-shrink:0;'><img src='" + avatar + "' style='width:100%;height:100%;object-fit:cover;display:block;'></div>" if avatar else "<div style='width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#C9A84C,#a8872e);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:18px;color:#0d0a08;flex-shrink:0;'>" + username[0].upper() + "</div>"}
                </div>
                <div class="sidebar-user-info">
                    <h4>@{username}</h4>
                    <p>{bio[:40] + '...' if len(bio) > 40 else bio}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        if st.button("Sair", key="nav_sair"):
            try:
                supabase.auth.sign_out()
            except Exception:
                pass
            st.session_state.user = None
            st.session_state.supabase_client = None
            st.session_state.pagina = "Inicio"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def render_top_nav():
    pages = [
        ("Inicio", "Inicio"),
        ("Perfil", "Meu Perfil"),
        ("Filmes", "Filmes"),
        ("Teatro", "Teatro"),
        ("Musicais", "Musicais"),
        ("Favoritos", "Favoritos"),
        ("Pastas", "Pastas"),
        ("Amigos", "Amigos"),
        ("Chat", "Conversas"),
    ]

    cols = st.columns(len(pages), gap="small")
    for i, (display, page) in enumerate(pages):
        with cols[i]:
            if st.button(display, key=f"tnav_{page}", use_container_width=False):
                st.session_state.amigo_id = None
                st.session_state.conversa_amigo = None
                st.session_state.pagina = page
                st.rerun()


def render_home():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        <div style="padding: 40px 0;">
            <div style="font-size: 14px; color: #C9A84C; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px;">
                ✦ Bem-vindo ao
            </div>
            <h1 style="font-size: clamp(42px, 6vw, 72px) !important; text-align: left !important;">
                AfterShow
            </h1>
            <div style="width: 60px; height: 2px; background: #C9A84C; margin: 20px 0;"></div>
            <p style="font-size: 18px; line-height: 1.8; color: #C9A84C;">
                Descubra filmes, peças teatrais e musicais. <br>
                Avalie obras, conecte-se com amigos e <br>
                explore o mundo da cultura.
            </p>
        </div>
        """, unsafe_allow_html=True)

        g1, g2, g3 = st.columns(3)
        with g1:
            st.markdown("""
            <div class="card text-center" style="padding: 20px 12px;">
                <div style="font-size: 13px; color: #C9A84C; font-weight: 600; margin-top: 8px;">Filmes</div>
            </div>
            """, unsafe_allow_html=True)
        with g2:
            st.markdown("""
            <div class="card text-center" style="padding: 20px 12px;">
                <div style="font-size: 13px; color: #C9A84C; font-weight: 600; margin-top: 8px;">Teatro</div>
            </div>
            """, unsafe_allow_html=True)
        with g3:
            st.markdown("""
            <div class="card text-center" style="padding: 20px 12px;">
                <div style="font-size: 13px; color: #C9A84C; font-weight: 600; margin-top: 8px;">Musicais</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 30px;">
            <div style="font-size: 120px; opacity: 0.6; line-height: 1;">✦</div>
            <div style="margin-top: -15px; font-family: 'Playfair Display', serif; font-size: 20px; color: #C9A84C66;">
                "Who lives, who dies,<br>who tells your story?"
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_movies():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.header("Filmes")

    tipo_busca = st.radio("Buscar por:", ["Filme", "Ator", "Diretor"], horizontal=True)
    api_key = st.secrets.get("tmdb_api_key", "ca20f980dcf5f16b3082b78b4bd754cc")
    pesquisa = st.text_input("Digite sua pesquisa:", placeholder="Ex: O Poderoso Chefão, Hamilton, ...")

    if pesquisa:
        with st.spinner("Buscando..."):
            if tipo_busca == "Filme":
                url_filme = (
                    f"https://api.themoviedb.org/3/search/movie"
                    f"?api_key={api_key}&query={pesquisa}&language=pt-BR"
                )
                resposta = requests.get(url_filme)
                dados = resposta.json()

                if dados.get("results"):
                    resultado = dados["results"][0]
                    titulo = resultado["title"]
                    descricao = resultado["overview"]
                    nota = resultado["vote_average"]
                    poster = resultado["poster_path"]
                    filme_id = resultado["id"]
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster}" if poster else ""

                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if poster_url:
                            st.markdown(
                                f'<div class="poster-frame">'
                                f'<img src="{poster_url}" style="width:100%;display:block;">'
                                f'</div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown("""
                            <div class="poster-frame" style="background: linear-gradient(135deg, #1a1510, #0d0a08); aspect-ratio: 2/3; display: flex; align-items: center; justify-content: center; color: #C9A84C44; font-size: 20px;">
                                Sem imagem
                            </div>
                            """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"<h2 style='margin-top:0!important;'>{titulo}</h2>", unsafe_allow_html=True)

                        stars = int(nota // 2)
                        half = 1 if nota % 2 >= 1 else 0
                        empty = 5 - stars - half
                        star_display = "★" * stars + "⯪" * half + "☆" * empty
                        st.markdown(
                            f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">'
                            f'<span style="font-size:22px;color:#C9A84C;">{star_display}</span>'
                            f'<span class="tag">{nota}/10</span>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                        st.markdown(f'<p style="line-height:1.7;">{descricao}</p>', unsafe_allow_html=True)
                        st.divider()

                        creditos_url = (
                            f"https://api.themoviedb.org/3/movie/{filme_id}/credits"
                            f"?api_key={api_key}&language=pt-BR"
                        )
                        creditos = requests.get(creditos_url).json()

                        col_e, col_d = st.columns(2)
                        with col_e:
                            st.markdown("**Elenco Principal**")
                            for ator in creditos.get("cast", [])[:5]:
                                st.markdown(f'<span style="font-size:14px;">• {ator["name"]}</span>', unsafe_allow_html=True)
                        with col_d:
                            st.markdown("**Diretor**")
                            for equipe in creditos.get("crew", []):
                                if equipe["job"] == "Director":
                                    st.markdown(f'<span style="font-size:14px;color:#C9A84C;">{equipe["name"]}</span>', unsafe_allow_html=True)
                        st.divider()

                        providers_url = (
                            f"https://api.themoviedb.org/3/movie/{filme_id}/watch/providers"
                            f"?api_key={api_key}"
                        )
                        providers = requests.get(providers_url).json()

                        st.markdown("**Onde assistir**")
                        if "BR" in providers.get("results", {}):
                            brasil = providers["results"]["BR"]
                            if "flatrate" in brasil:
                                for plataforma in brasil["flatrate"]:
                                    st.markdown(f'<span class="tag tag-streaming">• {plataforma["provider_name"]}</span>', unsafe_allow_html=True)
                            else:
                                st.markdown('<span style="color:#C9A84C;">Streaming não disponível no Brasil.</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span style="color:#C9A84C;">Informações indisponíveis.</span>', unsafe_allow_html=True)
                        st.divider()

                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("Favoritar", use_container_width=True):
                                try:
                                    supabase.table("favoritos").insert({
                                        "filme": titulo, "tipo": "Filme",
                                        "usuario_id": st.session_state.user.id
                                    }).execute()
                                    st.success("Adicionado aos favoritos!")
                                except Exception as e:
                                    st.error(e)
                        with c2:
                            try:
                                dados_pastas = supabase.table("Pastas").select("*").eq(
                                    "usuario_id", st.session_state.user.id
                                ).execute()
                                pastas = dados_pastas.data
                                nomes_pastas = [p["nome"] for p in pastas]
                                if nomes_pastas:
                                    pasta_escolhida = st.selectbox("Salvar em:", nomes_pastas, label_visibility="collapsed", placeholder="Escolha uma pasta")
                                    if st.button("Adicionar à Pasta", use_container_width=True):
                                        supabase.table("filmes_pastas").insert({
                                            "pasta": pasta_escolhida, "filme": titulo,
                                            "usuario_id": st.session_state.user.id
                                        }).execute()
                                        st.success("Adicionado à pasta!")
                                else:
                                    st.info("Crie uma pasta primeiro.")
                            except Exception as e:
                                st.error(e)

                    st.divider()

                    st.markdown("### Sua Crítica")
                    comentario = st.text_area("O que você achou do filme?", placeholder="Escreva sua crítica...", height=100)
                    nota_usuario = st.slider("Nota", 0, 10, 5)
                    if st.button("Enviar Crítica", use_container_width=True):
                        try:
                            supabase.table("criticas").insert({
                                "filme": titulo, "comentario": comentario, "nota": nota_usuario,
                                "usuario_id": st.session_state.user.id
                            }).execute()
                            st.success("Crítica enviada!")
                        except Exception as e:
                            st.error(e)

                    st.divider()

                    st.markdown("### Se esse filme fosse...")
                    st.markdown('<p style="color:#C9A84C;font-size:14px;">Atribua sensações ao filme</p>', unsafe_allow_html=True)
                    ce1, ce2, ce3 = st.columns(3)
                    with ce1:
                        cor = st.text_input("Uma cor", placeholder="Ex: Vermelho")
                        estacao = st.text_input("Uma estação", placeholder="Ex: Outono")
                    with ce2:
                        cidade = st.text_input("Uma cidade", placeholder="Ex: Paris")
                        cheiro = st.text_input("Um cheiro", placeholder="Ex: Chuva")
                    with ce3:
                        musica = st.text_input("Uma música", placeholder="Ex: Bohemian Rhapsody")

                    if st.button("Salvar Sensações", use_container_width=True):
                        try:
                            supabase.table("sensacoes_filmes").insert({
                                "filme": titulo, "cor": cor, "estacao": estacao,
                                "cidade": cidade, "cheiro": cheiro, "musica": musica
                            }).execute()
                            st.success("Sensações salvas!")
                        except Exception as e:
                            st.error(e)
                else:
                    st.error("Filme não encontrado. Tente outro nome.")

            elif tipo_busca in ("Ator", "Diretor"):
                url_pessoa = (
                    f"https://api.themoviedb.org/3/search/person"
                    f"?api_key={api_key}&query={pesquisa}&language=pt-BR"
                )
                resp_pessoa = requests.get(url_pessoa)
                dados_pessoa = resp_pessoa.json()

                if dados_pessoa.get("results"):
                    pessoa = dados_pessoa["results"][0]
                    nome = pessoa["name"]
                    foto = pessoa.get("profile_path", "")

                    bio_url = (
                        f"https://api.themoviedb.org/3/person/{pessoa['id']}"
                        f"?api_key={api_key}&language=pt-BR"
                    )
                    bio_dados = requests.get(bio_url).json()
                    biografia = bio_dados.get("biography", "")

                    foto_url = f"https://image.tmdb.org/t/p/w500{foto}" if foto else ""

                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if foto_url:
                            st.markdown(
                                f'<div class="poster-frame">'
                                f'<img src="{foto_url}" style="width:100%;display:block;">'
                                f'</div>', unsafe_allow_html=True,
                            )
                        else:
                            st.markdown("""
                            <div class="poster-frame" style="aspect-ratio:2/3;display:flex;
                                align-items:center;justify-content:center;
                                background:linear-gradient(135deg,#1a1510,#0d0a08);
                                color:#C9A84C44;font-size:14px;">Sem foto</div>
                            """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"<h2 style='margin-top:0!important;'>{nome}</h2>", unsafe_allow_html=True)
                        if biografia:
                            texto_bio = biografia[:600] + ("..." if len(biografia) > 600 else "")
                            st.markdown(f'<p style="line-height:1.7;font-size:14px;">{texto_bio}</p>', unsafe_allow_html=True)
                        else:
                            st.markdown('<p style="color:#C9A84C;">Biografia não disponível.</p>', unsafe_allow_html=True)

                        st.divider()
                        st.markdown("**Conhecido por**")
                        for trabalho in pessoa.get("known_for", [])[:8]:
                            titulo = trabalho.get("title") or trabalho.get("name", "")
                            ano = ""
                            if trabalho.get("release_date"):
                                ano = f" ({trabalho['release_date'][:4]})"
                            elif trabalho.get("first_air_date"):
                                ano = f" ({trabalho['first_air_date'][:4]})"
                            midia = trabalho.get("media_type", "").title()
                            st.markdown(
                                f'<span style="font-size:14px;">• {titulo}{ano} '
                                f'<span style="color:#C9A84C;font-size:12px;">[{midia}]</span></span>',
                                unsafe_allow_html=True,
                            )
                else:
                    st.error(f"{tipo_busca} não encontrado. Tente outro nome.")

    st.markdown("</div>", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def fetch_em_cartaz():
    url = "https://theatromunicipal.org.br/wp-json/wp/v2/eventos?_embed&per_page=50"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        eventos = resp.json()
        resultados = []
        for e in eventos:
            cats = [c for c in e.get("class_list", []) if c.startswith("categorias-eventos-")]
            img_url = ""
            if "_embedded" in e and "wp:featuredmedia" in e["_embedded"]:
                media = e["_embedded"]["wp:featuredmedia"][0]
                sizes = media.get("media_details", {}).get("sizes", {})
                img_url = sizes.get("medium", sizes.get("full", {})).get("source_url", "")
            resultados.append({
                "titulo": e["title"]["rendered"],
                "data": e["date"][:10],
                "link": e["link"],
                "categorias": [c.replace("categorias-eventos-", "").replace("-", " ") for c in cats],
                "imagem": img_url,
            })
        return resultados
    except:
        return "ERRO"

def render_theater():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.header("Teatro")

    st.markdown("""
    <p style="color:#C9A84C;font-size:14px;margin-bottom:24px;">
        Descubra espetáculos em cartaz no Theatro Municipal de São Paulo ou pesquise qualquer peça na Wikipedia.
    </p>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("### Em Cartaz")

    cat_map = {
        "Todos": None,
        "Teatro": "teatro",
        "Espetáculos": "espetaculos",
        "Dança": "danca",
        "Ópera": "opera",
        "Música": "musica",
        "Concertos": "concertos",
    }

    filtro = st.radio("Filtrar por categoria", list(cat_map.keys()), horizontal=True, label_visibility="collapsed")

    with st.spinner("Carregando programação..."):
        eventos = fetch_em_cartaz()

    if eventos is None or eventos == "ERRO":
        if eventos == "ERRO":
            st.error("Erro de conexão com a API do Theatro Municipal.")
        st.markdown("""
        <div class="card text-center" style="padding:30px;">
            <p style="color:#C9A84C;">Não foi possível carregar a programação no momento.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        slug = cat_map[filtro]
        eventos_filtrados = [e for e in eventos if slug is None or slug in e["categorias"]]

        if not eventos_filtrados:
            st.markdown("""
            <div class="card text-center" style="padding:40px;">
                <p style="color:#C9A84C;">Nenhum evento encontrado nesta categoria.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for i in range(0, len(eventos_filtrados), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(eventos_filtrados):
                        ev = eventos_filtrados[i + j]
                        with cols[j]:
                            img_html = (
                                f'<img src="{ev["imagem"]}" style="width:100%;height:150px;object-fit:cover;display:block;">'
                                if ev["imagem"]
                                else '<div style="width:100%;height:150px;background:linear-gradient(135deg,#1a1510,#0d0a08);display:flex;align-items:center;justify-content:center;color:#C9A84C33;font-size:36px;">✦</div>'
                            )
                            cat_tag = ev["categorias"][0] if ev["categorias"] else ""
                            st.markdown(f"""
                            <div class="card" style="margin-bottom:16px;overflow:hidden;padding:0;">
                                {img_html}
                                <div style="padding:12px 16px;">
                                    <span class="tag">{cat_tag}</span>
                                    <p style="margin:8px 0 4px;font-weight:600;font-size:14px;color:#C9A84C;line-height:1.3;">{ev['titulo']}</p>
                                    <p style="font-size:12px;color:#C9A84C;margin:0 0 6px;">{ev['data']}</p>
                                    <a href="{ev['link']}" target="_blank" style="color:#C9A84C;font-size:13px;">Ver detalhes →</a>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)


    st.divider()
    st.markdown("### Pesquisar peça")

    pesquisa = st.text_input("Pesquise uma peça de teatro:", placeholder="Ex: Hamlet, O Auto da Compadecida, ...")
    st.markdown('<p style="color:#C9A84C;font-size:13px;">Os resultados são obtidos via Wikipedia.</p>', unsafe_allow_html=True)

    if pesquisa:
        with st.spinner("Buscando peça..."):
            resultado = search_wikipedia(pesquisa, "teatro")

        if resultado:
            st.markdown(f"""
            <div class="wiki-card">
                <div style="display:flex;gap:20px;flex-wrap:wrap;">
                    {"<div style='flex:0 0 280px;'><img src='" + resultado['image'] + "' style='width:100%;border-radius:12px;'></div>" if resultado['image'] else ""}
                    <div style="flex:1;min-width:250px;">
                        <h3 style="margin-top:0!important;">{resultado["title"]}</h3>
                        <p style="line-height:1.7;">{resultado["extract"][:1200]}{"..." if len(resultado["extract"]) > 1200 else ""}</p>
                        <a href="{resultado["url"]}" target="_blank" style="color:#C9A84C;font-size:13px;">Ler mais na Wikipedia →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Favoritar", use_container_width=True):
                    try:
                        supabase.table("favoritos").insert({
                            "filme": resultado["title"], "tipo": "Teatro",
                            "usuario_id": st.session_state.user.id
                        }).execute()
                        st.success("Adicionado aos favoritos!")
                    except Exception as e:
                        st.error(e)
            with c2:
                if st.button("Fazer crítica", use_container_width=True):
                    st.session_state["critica_page"] = resultado["title"]
        else:
            st.markdown("""
            <div class="card text-center" style="padding:40px;">
                <p>Peça não encontrada. Tente com outro nome ou busque em inglês.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card text-center" style="padding: 60px 20px;">
            <p style="color:#C9A84C;">Digite o nome de uma peça de teatro para explorar.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_musicals():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.header("Musicais")

    st.markdown("""
    <p style="color:#C9A84C;font-size:14px;margin-bottom:24px;">
        Conheça os grandes musicais da história ou pesquise qualquer musical na Wikipedia.
    </p>
    """, unsafe_allow_html=True)

    # ── GRANDES MUSICAIS ──
    st.divider()
    st.markdown("### Grandes Musicais")

    MUSICAIS = [
        "Hamilton (musical)", "O Fantasma da Ópera", "Les Misérables",
        "Chicago (musical)", "O Rei Leão (musical)", "Wicked",
        "Mamma Mia!", "Cats", "Miss Saigon", "Rent",
        "West Side Story", "My Fair Lady", "A Noviça Rebelde",
        "Cabaret", "Beauty and the Beast (musical)", "Aladdin (musical)",
        "Matilda (musical)", "Six (musical)", "Dear Evan Hansen",
        "Hairspray (musical)",
    ]

    with st.spinner("Carregando..."):
        resultados = []
        for nome in MUSICAIS:
            info = search_wikipedia(nome, "musical")
            if info:
                resultados.append(info)

    if resultados:
        for i in range(0, len(resultados), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(resultados):
                    mus = resultados[i + j]
                    with cols[j]:
                        img_html = (
                            f'<img src="{mus["image"]}" style="width:100%;height:150px;object-fit:cover;display:block;border-radius:10px 10px 0 0;">'
                            if mus["image"]
                            else '<div style="width:100%;height:150px;background:linear-gradient(135deg,#C9A84C22,#a8872e11);display:flex;align-items:center;justify-content:center;border-radius:10px 10px 0 0;color:#C9A84C33;font-size:36px;font-family:serif;">♪</div>'
                        )
                        extract = mus["extract"][:120] + "..." if len(mus["extract"]) > 120 else mus["extract"]
                        st.markdown(f"""
                        <div class="card" style="margin-bottom:16px;overflow:hidden;padding:0;">
                            {img_html}
                            <div style="padding:12px 16px;">
                                <p style="margin:0 0 6px;font-weight:700;font-size:15px;color:#C9A84C;line-height:1.3;">{mus['title']}</p>
                                <p style="font-size:13px;color:#C9A84C;line-height:1.5;margin:0 0 8px;">{extract}</p>
                                <a href="{mus['url']}" target="_blank" style="color:#C9A84C;font-size:12px;">Ler mais →</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card text-center" style="padding:30px;">
            <p style="color:#C9A84C;">Não foi possível carregar a lista de musicais.</p>
        </div>
        """, unsafe_allow_html=True)

    # ── PESQUISAR NA WIKIPEDIA ──
    st.divider()
    st.markdown("### Pesquisar musical")

    pesquisa = st.text_input("Pesquise um musical:", placeholder="Ex: Hamilton, Les Misérables, O Fantasma da Ópera, ...")
    st.markdown('<p style="color:#C9A84C;font-size:13px;">Os resultados são obtidos via Wikipedia.</p>', unsafe_allow_html=True)

    if pesquisa:
        with st.spinner("Buscando musical..."):
            resultado = search_wikipedia(pesquisa, "musical")

        if resultado:
            st.markdown(f"""
            <div class="wiki-card">
                <div style="display:flex;gap:20px;flex-wrap:wrap;">
                    {"<div style='flex:0 0 280px;'><img src='" + resultado['image'] + "' style='width:100%;border-radius:12px;'></div>" if resultado['image'] else ""}
                    <div style="flex:1;min-width:250px;">
                        <h3 style="margin-top:0!important;">{resultado["title"]}</h3>
                        <p style="line-height:1.7;">{resultado["extract"][:1200]}{"..." if len(resultado["extract"]) > 1200 else ""}</p>
                        <a href="{resultado["url"]}" target="_blank" style="color:#C9A84C;font-size:13px;">Ler mais na Wikipedia →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Favoritar", use_container_width=True):
                    try:
                        supabase.table("favoritos").insert({
                            "filme": resultado["title"], "tipo": "Musical",
                            "usuario_id": st.session_state.user.id
                        }).execute()
                        st.success("Adicionado aos favoritos!")
                    except Exception as e:
                        st.error(e)
            with c2:
                if st.button("Fazer crítica", use_container_width=True):
                    st.session_state["critica_page"] = resultado["title"]
        else:
            st.markdown("""
            <div class="card text-center" style="padding:40px;">
                <p>Musical não encontrado. Tente com outro nome ou busque em inglês.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card text-center" style="padding: 60px 20px;">
            <p style="color:#C9A84C;">Digite o nome de um musical para explorar.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def render_profile():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.header("Meu Perfil")

    try:
        perfil = supabase.table("profiles").select("*").eq(
            "id", st.session_state.user.id
        ).execute()
        if not perfil.data:
            email = st.session_state.user.email or ""
            base_username = email.split("@")[0]
            username = base_username
            suffix = 1
            criado = False
            ultimo_erro = None
            while suffix < 20:
                try:
                    supabase.table("profiles").insert({
                        "id": st.session_state.user.id,
                        "username": username, "bio": "",
                    }).execute()
                    criado = True
                    break
                except Exception as e:
                    ultimo_erro = str(e)
                    username = f"{base_username}{suffix}"
                    suffix += 1
            if not criado:
                st.error(f"Nao foi possivel criar o perfil: {ultimo_erro}")
                return
            st.rerun()
            return
        dados_perfil = perfil.data[0]

        col_img, col_info = st.columns([1, 2])
        with col_img:
            avatar_url = dados_perfil.get("avatar_url", "")
            if avatar_url:
                st.markdown(
                    f'<div style="width:120px;height:120px;border-radius:50%;overflow:hidden;border:3px solid #C9A84C;margin:0 auto;">'
                    f'<img src="{avatar_url}" style="width:100%;height:100%;object-fit:cover;display:block;">'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="width:120px;height:120px;border-radius:50%;background:linear-gradient(135deg,#C9A84C,#a8872e);display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:42px;font-weight:700;color:#0d0a08;">'
                    f'{dados_perfil.get("username", "U")[0].upper()}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        with col_info:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            username = st.text_input("Username", value=dados_perfil.get("username", ""))
            bio = st.text_area("Bio", value=dados_perfil.get("bio", ""), height=80)
            st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("### Favoritos")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        filme = st.text_input("Filme favorito", value=dados_perfil.get("filme_favorito", ""))
        musical = st.text_input("Musical favorito", value=dados_perfil.get("musical_favorito", ""))
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("### Local")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        cidade = st.text_input("Cidade", value=dados_perfil.get("cidade", ""))
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("### Inspiração")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        frase = st.text_area("Frase favorita", value=dados_perfil.get("frase", ""), height=80)
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("### Avatar")
        foto = st.file_uploader("Escolha uma foto de perfil", type=["png", "jpg", "jpeg"])

        if st.button("Salvar Perfil", use_container_width=True):
            avatar_url = dados_perfil.get("avatar_url", "")
            if foto:
                nome_arquivo = f"{st.session_state.user.id}/{uuid.uuid4()}.png"
                supabase.storage.from_("avatars").upload(nome_arquivo, foto.getvalue())
                avatar_url = f"{SUPABASE_URL}/storage/v1/object/public/avatars/{nome_arquivo}"

            supabase.table("profiles").update({
                "username": username, "bio": bio,
                "filme_favorito": filme, "musical_favorito": musical,
                "cidade": cidade, "frase": frase, "avatar_url": avatar_url
            }).eq("id", st.session_state.user.id).execute()
            st.success("Perfil atualizado!")
            st.rerun()

    except Exception as e:
        st.error(e)

    st.markdown("</div>", unsafe_allow_html=True)

def render_favorites():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.header("Meus Favoritos")

    try:
        dados = supabase.table("favoritos").select("*").eq(
            "usuario_id", st.session_state.user.id
        ).execute()
        favoritos = dados.data

        if favoritos:
            for item in favoritos:
                st.markdown(f"""
                <div class="card" style="margin-bottom:12px;padding:16px 20px;display:flex;align-items:center;justify-content:space-between;">
                    <div>
                        <strong style="font-size:16px;color:#C9A84C;">{item['filme']}</strong>
                        <span class="tag" style="margin-left:10px;">{item['tipo']}</span>
                    </div>
                    <div style="font-size:18px;opacity:0.5;">--</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card text-center" style="padding:60px 20px;">
                <p style="color:#C9A84C;">Nenhum item favoritado ainda.</p>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(e)

    st.markdown("</div>", unsafe_allow_html=True)


def render_folders():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.header("Pastas")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    nome_pasta = st.text_input("Nome da nova pasta", placeholder="Ex: Favoritos do mês")
    if st.button("Criar Pasta", use_container_width=True):
        try:
            supabase.table("Pastas").insert({
                "nome": nome_pasta, "usuario_id": st.session_state.user.id
            }).execute()
            st.success("Pasta criada!")
            st.rerun()
        except Exception as e:
            st.error(e)
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    try:
        dados = supabase.table("Pastas").select("*").eq(
            "usuario_id", st.session_state.user.id
        ).execute()
        pastas = dados.data

        if pastas:
            for pasta in pastas:
                dados_filmes = supabase.table("filmes_pastas").select("*").eq(
                    "pasta", pasta["nome"]
                ).eq("usuario_id", st.session_state.user.id).execute()
                filmes = dados_filmes.data

                st.markdown(f"""
                <div class="card" style="margin-bottom:16px;">
                    <h3 style="margin-top:0!important;display:flex;align-items:center;gap:8px;">
                        {pasta['nome']}
                        <span class="tag">{len(filmes)} itens</span>
                    </h3>
                """, unsafe_allow_html=True)

                if filmes:
                    for filme in filmes:
                        st.markdown(f'<p style="margin:4px 0;">• {filme["filme"]}</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color:#C9A84C;">Nenhum filme nesta pasta.</p>', unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card text-center" style="padding:40px;">
                <p style="color:#C9A84C;">Nenhuma pasta criada ainda.</p>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(e)

    st.markdown("</div>", unsafe_allow_html=True)


def render_friends():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    col_amigos, col_busca = st.columns([2, 1])

    with col_amigos:
        st.header("Amigos")

        try:
            amizades = supabase.table("amigos").select("*").eq(
                "usuario_id", st.session_state.user.id
            ).execute()

            if amizades.data:
                for amizade in amizades.data:
                    amigo = supabase.table("profiles").select("*").eq(
                        "id", amizade["amigo_id"]
                    ).execute()
                    if amigo.data:
                        perfil = amigo.data[0]
                        inicial = perfil.get("username", "?")[0].upper()
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:14px;padding:14px 16px;
                            border-bottom:1px solid #C9A84C22;transition:all 0.25s;cursor:pointer;">
                            <div style="width:38px;height:38px;border-radius:50%;
                                background:linear-gradient(135deg,#C9A84C,#a8872e);
                                display:flex;align-items:center;justify-content:center;
                                font-weight:700;font-size:16px;color:#0d0a08;flex-shrink:0;">
                                {inicial}
                            </div>
                            <div style="flex:1;min-width:0;">
                                <div style="font-size:14px;font-weight:600;color:#C9A84C;">
                                    @{perfil['username']}
                                </div>
                                <div style="font-size:12px;color:#C9A84C;margin-top:2px;
                                    overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                                    {perfil.get('bio', '')[:60] or 'Sem bio'}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("Ver Perfil", key=f"view_friend_{perfil['id']}",
                                     use_container_width=True):
                            st.session_state.amigo_id = perfil["id"]
                            st.session_state.pagina = "Perfil do Amigo"
                            st.rerun()
            else:
                st.markdown("""
                <div style="text-align:center;padding:60px 20px;">
                    <p style="color:#C9A84C;font-size:15px;">
                        Voce ainda nao tem amigos.<br>
                        Busque usuarios ao lado para adicionar!
                    </p>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(e)

    with col_busca:
        st.markdown("""
        <div style="background:linear-gradient(145deg,#1a1510,#0d0a08);
            border:1px solid #C9A84C33;border-radius:16px;padding:20px 18px;
            backdrop-filter:blur(12px);margin-bottom:16px;">
            <h4 style="margin:0 0 12px;color:#C9A84C;font-size:14px;font-weight:600;
                letter-spacing:0.5px;">ADICIONAR AMIGOS</h4>
        """, unsafe_allow_html=True)
        busca = st.text_input("", placeholder="Buscar por username...",
                              label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        if busca:
            try:
                usuarios = supabase.table("profiles").select("*").ilike(
                    "username", f"%{busca}%"
                ).execute()

                if usuarios.data:
                    for usuario in usuarios.data:
                        if usuario["id"] == st.session_state.user.id:
                            continue
                        inicial = usuario["username"][0].upper()
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:10px;padding:10px 14px;
                            border-bottom:1px solid #C9A84C22;">
                            <div style="width:32px;height:32px;border-radius:50%;
                                background:linear-gradient(135deg,#C9A84C,#a8872e);
                                display:flex;align-items:center;justify-content:center;
                                font-weight:700;font-size:13px;color:#0d0a08;flex-shrink:0;">
                                {inicial}
                            </div>
                            <div style="flex:1;min-width:0;">
                                <div style="font-size:13px;font-weight:500;color:#C9A84C;">
                                    @{usuario['username']}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("+", key=f"add_{usuario['id']}",
                                     use_container_width=True):
                            try:
                                supabase.table("amigos").insert({
                                    "usuario_id": st.session_state.user.id,
                                    "amigo_id": usuario["id"]
                                }).execute()
                                st.success("Adicionado!")
                                st.rerun()
                            except Exception as e:
                                st.error(e)
                else:
                    st.markdown("""
                    <div style="text-align:center;padding:20px;">
                        <p style="color:#C9A84C;font-size:13px;">Nenhum usuario encontrado</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(e)

    st.markdown("</div>", unsafe_allow_html=True)


def render_friend_profile():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    amigo_id = st.session_state.get("amigo_id")
    if not amigo_id:
        st.warning("Nenhum amigo selecionado.")
        if st.button("← Voltar para Amigos"):
            st.session_state.pagina = "Amigos"
            st.rerun()
        return

    try:
        perfil = supabase.table("profiles").select("*").eq("id", amigo_id).execute()
        if not perfil.data:
            st.error("Perfil não encontrado.")
            if st.button("← Voltar"):
                st.session_state.pagina = "Amigos"
                st.rerun()
            return
        dados = perfil.data[0]
    except Exception as e:
        st.error(e)
        return

    # Avatar e info
    col_img, col_info = st.columns([1, 2])
    with col_img:
        avatar_url = dados.get("avatar_url", "")
        if avatar_url:
            st.markdown(
                f'<div style="width:120px;height:120px;border-radius:50%;overflow:hidden;border:3px solid #C9A84C;margin:0 auto;">'
                f'<img src="{avatar_url}" style="width:100%;height:100%;object-fit:cover;display:block;">'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="width:120px;height:120px;border-radius:50%;background:linear-gradient(135deg,#C9A84C,#a8872e);display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:42px;font-weight:700;color:#0d0a08;">'
                f'{dados.get("username", "?")[0].upper()}'
                f'</div>',
                unsafe_allow_html=True,
            )

    with col_info:
        st.markdown(f'<h2 style="margin-top:0!important;">@{dados["username"]}</h2>', unsafe_allow_html=True)
        if dados.get("bio"):
            st.markdown(f'<p style="color:#C9A84C;line-height:1.6;">{dados["bio"]}</p>', unsafe_allow_html=True)

    # Detalhes do perfil
    st.divider()
    st.markdown("### Sobre")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    campos = []
    if dados.get("filme_favorito"):
        campos.append(("Filme favorito", dados["filme_favorito"]))
    if dados.get("musical_favorito"):
        campos.append(("Musical favorito", dados["musical_favorito"]))
    if dados.get("cidade"):
        campos.append(("Cidade", dados["cidade"]))
    if dados.get("frase"):
        campos.append(("Frase favorita", dados["frase"]))
    if campos:
        for label, valor in campos:
            st.markdown(f'<p><strong style="color:#C9A84C;">{label}:</strong> {valor}</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#C9A84C;">Nenhuma informação adicional.</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Favoritos do amigo
    st.divider()
    st.markdown("### Favoritos")
    try:
        favs = supabase.table("favoritos").select("*").eq("usuario_id", amigo_id).execute()
        if favs.data:
            for item in favs.data:
                st.markdown(f"""
                <div class="card" style="margin-bottom:8px;padding:14px 18px;display:flex;align-items:center;justify-content:space-between;">
                    <div>
                        <strong style="font-size:15px;color:#C9A84C;">{item['filme']}</strong>
                        <span class="tag" style="margin-left:8px;">{item['tipo']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#C9A84C;">Nenhum favorito ainda.</p>', unsafe_allow_html=True)
    except Exception as e:
        st.error(e)

    # Pastas do amigo
    st.divider()
    st.markdown("### Pastas")
    try:
        pastas = supabase.table("Pastas").select("*").eq("usuario_id", amigo_id).execute()
        if pastas.data:
            for pasta in pastas.data:
                filmes_pasta = supabase.table("filmes_pastas").select("*").eq(
                    "pasta", pasta["nome"]
                ).eq("usuario_id", amigo_id).execute()
                filmes = filmes_pasta.data
                st.markdown(f"""
                <div class="card" style="margin-bottom:12px;">
                    <h4 style="margin-top:0!important;display:flex;align-items:center;gap:8px;">
                        {pasta['nome']}
                        <span class="tag">{len(filmes)} itens</span>
                    </h4>
                """, unsafe_allow_html=True)
                if filmes:
                    for f in filmes:
                        st.markdown(f'<p style="margin:3px 0;">• {f["filme"]}</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color:#C9A84C;">Pasta vazia.</p>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#C9A84C;">Nenhuma pasta criada.</p>', unsafe_allow_html=True)
    except Exception as e:
        st.error(e)

    # Críticas do amigo
    st.divider()
    st.markdown("### Críticas")
    try:
        crits = supabase.table("criticas").select("*").eq("usuario_id", amigo_id).execute()
        if crits.data:
            for c in crits.data:
                estrelas = "★" * (c["nota"] // 2) + "☆" * (5 - c["nota"] // 2)
                st.markdown(f"""
                <div class="card" style="margin-bottom:10px;padding:14px 18px;">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
                        <strong style="color:#C9A84C;font-size:15px;">{c['filme']}</strong>
                        <span style="color:#C9A84C;font-size:16px;">{estrelas}</span>
                    </div>
                    <p style="margin:0;color:#C9A84C;font-size:14px;line-height:1.5;">{c.get('comentario', '')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#C9A84C;">Nenhuma crítica ainda.</p>', unsafe_allow_html=True)
    except Exception as e:
        st.error(e)

    st.divider()
    if st.button("← Voltar para Amigos", use_container_width=True):
        st.session_state.amigo_id = None
        st.session_state.pagina = "Amigos"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_conversas():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    amigo_chat = st.session_state.get("conversa_amigo")

    if amigo_chat:
        # ── CHAT ──
        try:
            perfil = supabase.table("profiles").select("*").eq("id", amigo_chat).execute()
            if not perfil.data:
                st.error("Amigo nao encontrado.")
                st.session_state.conversa_amigo = None
                st.rerun()
                return
            amigo = perfil.data[0]
        except Exception as e:
            st.error(e)
            return

        col_voltar, col_nome = st.columns([0.2, 0.8])
        with col_voltar:
            if st.button("← Voltar", use_container_width=True):
                st.session_state.conversa_amigo = None
                st.rerun()
        with col_nome:
            st.markdown(f'<h3 style="margin:0;">@{amigo["username"]}</h3>', unsafe_allow_html=True)

        st.divider()

        try:
            msgs = supabase.table("mensagens").select("*").or_(
                f"and(remetente_id.eq.{st.session_state.user.id},destinatario_id.eq.{amigo_chat}),"
                f"and(remetente_id.eq.{amigo_chat},destinatario_id.eq.{st.session_state.user.id})"
            ).order("data_envio").execute()

            if msgs.data:
                for m in msgs.data:
                    sou_eu = m["remetente_id"] == st.session_state.user.id
                    lado = "right" if sou_eu else "left"
                    cor = "#C9A84C" if sou_eu else "#C9A84C15"
                    texto_cor = "#0d0a08" if sou_eu else "#C9A84C"
                    is_critica = m["conteudo"].startswith("CRITICA:")
                    critica_style = "border-left:3px solid #C9A84C;" if is_critica else ""
                    st.markdown(
                        f'<div style="display:flex;justify-content:{lado};margin-bottom:8px;">'
                        f'<div style="background:{cor};color:{texto_cor};padding:10px 16px;'
                        f'border-radius:16px;max-width:75%;font-size:14px;line-height:1.4;{critica_style}'
                        f'white-space:pre-wrap;">{m["conteudo"]}</div></div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    '<p style="color:#C9A84C;text-align:center;padding:20px 0;">'
                    'Nenhuma mensagem ainda. Envie algo ou compartilhe uma critica!</p>',
                    unsafe_allow_html=True,
                )
        except Exception as e:
            st.error(e)

    
        st.divider()
        with st.form("envio_msg", clear_on_submit=True):
            texto = st.text_input("", placeholder="Digite sua mensagem...", label_visibility="collapsed")
            if st.form_submit_button("Enviar", use_container_width=True):
                if texto.strip():
                    try:
                        supabase.table("mensagens").insert({
                            "remetente_id": st.session_state.user.id,
                            "destinatario_id": amigo_chat,
                            "conteudo": texto.strip(),
                        }).execute()
                        st.rerun()
                    except Exception as e:
                        st.error(e)

        st.divider()
        st.markdown("### Compartilhar Critica")
        try:
            minhas_criticas = supabase.table("criticas").select("*").eq(
                "usuario_id", st.session_state.user.id
            ).order("id", desc=True).execute()

            if minhas_criticas.data:
                opcoes = {
                    f'{c["filme"]} — {c["nota"]}/10': c
                    for c in minhas_criticas.data
                }
                escolha = st.selectbox(
                    "Selecione uma critica", list(opcoes.keys()),
                    label_visibility="collapsed",
                )
                if st.button("Enviar Critica para @" + amigo["username"], use_container_width=True):
                    c = opcoes[escolha]
                    estrelas = "★" * (c["nota"] // 2) + "☆" * (5 - c["nota"] // 2)
                    texto_critica = (
                        f"CRITICA: {c['filme']}\n"
                        f"Nota: {c['nota']}/10 {estrelas}\n"
                        f"{c.get('comentario', '')}"
                    ).strip()
                    try:
                        supabase.table("mensagens").insert({
                            "remetente_id": st.session_state.user.id,
                            "destinatario_id": amigo_chat,
                            "conteudo": texto_critica,
                        }).execute()
                        st.success("Critica enviada!")
                        st.rerun()
                    except Exception as e:
                        st.error(e)
            else:
                st.markdown(
                    '<p style="color:#C9A84C;">Voce ainda nao fez nenhuma critica. '
                    'Avalie filmes, teatro ou musicais primeiro!</p>',
                    unsafe_allow_html=True,
                )
        except Exception as e:
            st.error(e)

    else:
        
        st.header("Conversas")
        try:
            amizades = supabase.table("amigos").select("*").eq(
                "usuario_id", st.session_state.user.id
            ).execute()
            amigos_ids = {a["amigo_id"] for a in amizades.data}

            if amigos_ids:
                for aid in sorted(amigos_ids):
                    try:
                        p = supabase.table("profiles").select("id,username,avatar_url,bio").eq("id", aid).execute()
                        if not p.data:
                            continue
                        amigo = p.data[0]

                        ultima = supabase.table("mensagens").select("conteudo,data_envio").or_(
                            f"and(remetente_id.eq.{st.session_state.user.id},destinatario_id.eq.{aid}),"
                            f"and(remetente_id.eq.{aid},destinatario_id.eq.{st.session_state.user.id})"
                        ).order("data_envio", desc=True).limit(1).execute()

                        preview = "Iniciar conversa..."
                        tem_msg = False
                        if ultima.data:
                            preview = ultima.data[0]["conteudo"][:60]
                            if len(ultima.data[0]["conteudo"]) > 60:
                                preview += "..."
                            tem_msg = True

                        inicial = amigo["username"][0].upper()
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:12px;
                            background:#1a1510;border:1px solid #C9A84C33;
                            border-radius:12px;padding:12px 16px;margin-bottom:8px;">
                            <div style="width:40px;height:40px;border-radius:50%;
                                background:linear-gradient(135deg,#C9A84C,#a8872e);
                                display:flex;align-items:center;justify-content:center;
                                font-weight:700;color:#0d0a08;font-size:18px;flex-shrink:0;">
                                {inicial}
                            </div>
                            <div style="flex:1;min-width:0;">
                                <div style="font-size:15px;font-weight:600;color:#C9A84C;">
                                    @{amigo['username']}
                                </div>
                                <div style="font-size:13px;color:#C9A84C;overflow:hidden;
                                    text-overflow:ellipsis;white-space:nowrap;">
                                    {preview}
                                </div>
                            </div>
                            {f'<span style="font-size:10px;color:#C9A84C55;">msg</span>' if tem_msg else ''}
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("Conversar", key=f"chat_{aid}", use_container_width=True):
                            st.session_state.conversa_amigo = aid
                            st.rerun()
                    except:
                        continue
            else:
                st.markdown("""
                <div class="card text-center" style="padding:60px 20px;">
                    <p style="color:#C9A84C;font-size:16px;">
                        Nenhum amigo ainda.<br>Adicione amigos para conversar!
                    </p>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erro ao carregar conversas: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.splash:
    render_splash()
else:
    if not st.session_state.user:
        render_login_page()
    else:
        render_sidebar()
        render_top_nav()

        pages_map = {
            "Inicio": render_home,
            "Meu Perfil": render_profile,
            "Filmes": render_movies,
            "Teatro": render_theater,
            "Musicais": render_musicals,
            "Favoritos": render_favorites,
            "Pastas": render_folders,
            "Amigos": render_friends,
            "Perfil do Amigo": render_friend_profile,
            "Conversas": render_conversas,
        }

        page = st.session_state.pagina
        if page in pages_map:
            st.markdown(
                '<div class="page-content">',
                unsafe_allow_html=True,
            )
            pages_map[page]()
            st.markdown("</div>", unsafe_allow_html=True)
