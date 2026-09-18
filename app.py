import streamlit as st
from deep_translator import GoogleTranslator
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import base64

# Configurazione della pagina futuristica
st.set_page_config(page_title="A.T.O.M. System", page_icon="🤖", layout="centered")

# CSS personalizzato per trasformare l'interfaccia in stile Jarvis / Sci-Fi
st.markdown("""
    <style>
    .stApp {
        background-color: #030712;
        font-family: 'Courier New', Courier, monospace;
    }
    .jarvis-title {
        color: #00f0ff;
        text-shadow: 0 0 10px #00f0ff, 0 0 20px #00d8ff;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        text-align: center;
        letter-spacing: 3px;
        margin-bottom: 5px;
    }
    .jarvis-subtitle {
        color: #38bdf8;
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .hud-box {
        background: rgba(0, 240, 255, 0.05);
        border: 1px solid #00f0ff;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
        border-radius: 8px;
        padding: 20px;
        color: #e2e8f0;
        margin-top: 15px;
    }
    .hud-label {
        color: #38bdf8;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="jarvis-title">🤖 A.T.O.M. v1.1</h1>', unsafe_allow_html=True)
st.markdown('<div class="jarvis-subtitle">Automatic Translator Operative Machine</div>', unsafe_allow_html=True)
st.write("---")

direzione = st.radio(
    "SELEZIONA FLUSSO DATI (OPERATIONAL CORE):",
    ("ITALIANO ➔ INGLESE (Data Link Alpha)", "INGLESE ➔ ITALIANO (Data Link Beta)")
)

if "ITALIANO" in direzione:
    lingua_partenza, lingua_arrivo = "it", "en"
    codice_voce = "it"
    placeholder_testo = "Iniezione dati testo (IT)..."
    label_bottone = "⚡ ATTIVA ACCESSO VOCALE (ITALIANO)"
else:
    lingua_partenza, lingua_arrivo = "en", "it"
    codice_voce = "en"
    placeholder_testo = "Iniezione dati testo (EN)..."
    label_bottone = "⚡ ATTIVA ACCESSO VOCALE (INGLESE)"

# Usiamo un motore di riserva MyMemory se Google fallisce per evitare l'errore di rete dei server
try:
    from deep_translator import MyMemoryTranslator
    traduttore = MyMemoryTranslator(source=lingua_partenza, target=lingua_arrivo)
except:
    traduttore = GoogleTranslator(source=lingua_partenza, target=lingua_arrivo)

st.write("")
st.markdown("<div class='hud-label'>[INPUT MATRIX] Rilevamento Audio Vocale</div>", unsafe_allow_html=True)

testo_vocale = speech_to_text(
    start_prompt=label_bottone,
    stop_prompt="🔴 CORE IN ASCOLTO... PARLA ORA",
    language=codice_voce,
    use_container_width=True,
    key='atom_speech'
)

st.markdown("<div class='hud-label'>[MANUAL OVERRIDE] Inserimento Testuale</div>", unsafe_allow_html=True)
testo_scritto = st.text_input("", placeholder=placeholder_testo, label_visibility="collapsed")

testo_finale = testo_vocale if testo_vocale else testo_scritto

if testo_finale:
    st.write("")
    st.markdown(f"""
    <div class="hud-box">
        <div class="hud-label">> INPUT RILEVATO:</div>
        <div style="font-size: 1.2rem; color: #ffffff;">{testo_finale}</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Elaborazione algoritmi di traduzione..."):
        try:
            traduzione = traduttore.translate(testo_finale)
            
            st.markdown(f"""
            <div class="hud-box" style="border-color: #38bdf8; background: rgba(56, 189, 248, 0.07);">
                <div class="hud-label" style="color: #38bdf8;">> TRADUZIONE DECODIFICATA:</div>
                <div style="font-size: 1.3rem; color: #00f0ff; font-weight: bold; text-shadow: 0 0 5px rgba(0,240,255,0.5);">{traduzione}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- MODULO VOCALE AUDIO ---
            # Genera il file audio della traduzione nella lingua di arrivo
            tts = gTTS(text=traduzione, lang=lingua_arrivo)
            tts.save("output.mp3")
            
            # Inserisce il player audio nascosto con autoplay automatico
            with open("output.mp3", "rb") as f:
                audio_bytes = f.read()
            b64_audio = base64.b64encode(audio_bytes).decode()
            
            st.markdown("<div class='hud-label' style='margin-top:10px;'>[AUDIO OUTPUT] Sintesi Vocale Attiva</div>", unsafe_allow_html=True)
            # Mostra il lettore e fa partire l'audio in automatico appena la traduzione è pronta
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
            
        except Exception as e:
            st.error("ERRORE DI DECODIFICA CORE: Riprova a inviare il messaggio.")
