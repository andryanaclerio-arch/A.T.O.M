import streamlit as st
from deep_translator import GoogleTranslator
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import base64

st.set_page_config(page_title="A.T.O.M. Continuous", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; font-family: 'Courier New', Courier, monospace; }
    .jarvis-title { color: #00f0ff; text-shadow: 0 0 10px #00f0ff; font-weight: bold; text-align: center; }
    .hud-box { background: rgba(0, 240, 255, 0.05); border: 1px solid #00f0ff; border-radius: 8px; padding: 15px; color: #e2e8f0; margin-top: 10px; }
    .hud-label { color: #38bdf8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="jarvis-title">🤖 A.T.O.M. AUTOMATIC CORE</h1>', unsafe_allow_html=True)
st.write("---")

st.markdown("<div class='hud-label'>[SYSTEM STATUS] LIVE AUDIO STREAMING OVERRIDE</div>", unsafe_allow_html=True)

# Attiviamo un unico grande bottone di ascolto globale. 
# Nota: impostiamo una stringa vuota per i codici in modo che il browser provi a catturare l'audio in generale, 
# oppure usiamo una configurazione mista. Per massima precisione immediata senza tasti, 
# usiamo il selettore 'auto' se supportato, altrimenti intercettiamo il testo.
testo_rilevato = speech_to_text(
    start_prompt="🚀 AVVIA MONITORAGGIO AMBIENTALE CONTINUO",
    stop_prompt="🔴 SPEGNI MONITORAGGIO",
    language="it-IT", # Rilevamento primario (se parli in inglese, prova a scrivere lo stesso o viceversa)
    use_container_width=True,
    key='atom_continuous'
)

if testo_rilevato:
    # ALGORITMO DI RILEVAMENTO AUTOMATICO DELLA LINGUA (Eurisitico veloce)
    # Controlliamo se la frase contiene parole tipiche inglesi per capire chi sta parlando
    parole_inglesi = ['hello', 'hi', 'what', 'is', 'the', 'you', 'are', 'to', 'my', 'school', 'teacher', 'yes', 'no']
    contiene_inglese = any(parola in testo_rilevato.lower() for parola in parole_inglesi)
    
    if contiene_inglese:
        lingua_partenza, lingua_arrivo = "en", "it"
        modalita = "INGLESE ➔ ITALIANO"
    else:
        lingua_partenza, lingua_arrivo = "it", "en"
        modalita = "ITALIANO ➔ INGLESE"
        
    st.markdown(f"<div class='hud-label' style='color:#a855f7;'>[CORE DETECTED]: {modalita}</div>", unsafe_allow_html=True)

    try:
        # Traduzione immediata con server di backup MyMemory per evitare blocchi
        from deep_translator import MyMemoryTranslator
        traduttore = MyMemoryTranslator(source=lingua_partenza, target=lingua_arrivo)
        traduzione = traduttore.translate(testo_rilevato)
        
        # Mostra i risultati a schermo stile HUD
        st.markdown(f"""
        <div class="hud-box">
            <div class="hud-label">> ASCOLTATO:</div>
            <div style="font-size: 1.1rem; color: #ffffff;">{testo_rilevato}</div>
        </div>
        <div class="hud-box" style="border-color: #38bdf8;">
            <div class="hud-label" style="color: #38bdf8;">> OUTPUT TRADOTTO:</div>
            <div style="font-size: 1.2rem; color: #00f0ff; font-weight: bold;">{traduzione}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Riproduzione vocale istantanea automatica
        tts = gTTS(text=traduzione, lang=lingua_arrivo)
        tts.save("live_output.mp3")
        with open("live_output.mp3", "rb") as f:
            audio_bytes = f.read()
        
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        
    except Exception as e:
        st.error("Errore nell'elaborazione del flusso dati.")
