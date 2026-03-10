import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Supernova - Performance Predictor",
    page_icon="⚡", # Puoi usare un'emoji o un percorso a un'immagine
    layout="centered", # o "wide"
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. CONFIGURAZIONE E DESIGN (Oro, Nero, Bianco)
# ==========================================
st.set_page_config(page_title="Supernova Mind Lab", page_icon="🧠", layout="wide") 

# CSS per pulizia totale e design premium
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .block-container {padding-top: 2rem;}
    
    /* Stile per le metriche (KPI) */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #D4AF37; /* Bordo Oro */
        padding: 5% 10% 5% 10%;
        border-radius: 0px; /* Squadrato, più formale */
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Stile Mission Box (Nero e Oro) */
    .vision-box {
        background: #000000;
        color: #D4AF37;
        padding: 20px;
        border: 2px solid #D4AF37;
        margin-bottom: 20px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Bottoni Oro */
    div.stButton > button:first-child {
        background-color: #D4AF37;
        color: #000000;
        border: None;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #000000;
        color: #D4AF37;
        border: 1px solid #D4AF37;
    }
    </style>
    """, unsafe_allow_html=True) 

st.write("---")

# --- Descrizione del Tool ---
st.header("Analisi Predittiva della Degradaione Performance")
st.markdown(
    """
    Questo strumento Supernova analizza la **variazione dei parametri di performance** su una serie di ripetizioni (es. colpi di golf, lanci). 
    Utilizzando principi di **fatica ingegneristica** applicati al gesto biomeccanico,
    prevediamo il punto oltre il quale la tua precisione e potenza iniziano a degradare significativamente.
    """
)
st.warning("⚠️ **Nota:** I dati attuali sono simulati. L'accuratezza reale richiede dati biomeccanici e fisiologici specifici.")

# --- Input Dati Simulati ---
st.subheader("Inserisci i tuoi Dati Simulati")
num_ripetizioni = st.slider("Numero di ripetizioni (es. colpi, lanci)", 10, 100, 30)
st.info(f"Simuliamo la performance su {num_ripetizioni} ripetizioni.")

# Generazione dati simulati
np.random.seed(42) # Per risultati riproducibili
deviazione_iniziale = st.number_input("Deviazione iniziale media (es. in metri dal target)", 0.5, 5.0, 1.5)
degradazione_per_ripetizione = st.number_input("Tasso di degradazione per ripetizione (aumento deviazione)", 0.01, 0.1, 0.03)

# Calcolo della deviazione simulata
deviazioni = np.linspace(deviazione_iniziale, 
                         deviazione_iniziale + degradazione_per_ripetizione * num_ripetizioni, 
                         num_ripetizioni)
# Aggiungiamo un po' di rumore per realismo
deviazioni += np.random.normal(0, deviazione_iniziale / 5, num_ripetizioni)
df = pd.DataFrame({'Ripetizione': range(1, num_ripetizioni + 1), 'Deviazione (m)': deviazioni})

# --- Visualizzazione ---
st.subheader("Andamento della Performance")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='Ripetizione', y='Deviazione (m)', data=df, ax=ax, color=COLOR_ACCENT)
ax.set_title('Degradazione della Precisione nel Tempo', color=COLOR_TEXT)
ax.set_xlabel('Numero di Ripetizioni', color=COLOR_TEXT)
ax.set_ylabel('Deviazione dal Target (m)', color=COLOR_TEXT)
ax.tick_params(axis='x', colors=COLOR_TEXT)
ax.tick_params(axis='y', colors=COLOR_TEXT)
ax.set_facecolor(COLOR_PRIMARY)
fig.patch.set_facecolor(COLOR_PRIMARY)
plt.grid(True, linestyle='--', alpha=0.6, color=COLOR_ACCENT)
st.pyplot(fig)

# Calcoliamo prima i limiti per sicurezza
minimo_accettabile = deviazione_iniziale + 0.5
massimo_accettabile = deviazione_iniziale + (degradazione_per_ripetizione * num_ripetizioni)
proposta_default = deviazione_iniziale + (degradazione_per_ripetizione * num_ripetizioni / 2)

# Il comando Streamlit corretto:
soglia_degradazione = st.number_input(
    "Soglia di accettabilità (m)",
    min_value=float(minimo_accettabile),
    max_value=float(massimo_accettabile),
    value=float(max(minimo_accettabile, proposta_default)) # <--- Il Fix fondamentale
)

punto_critico = df[df['Deviazione (m)'] > soglia_degradazione]['Ripetizione'].min()

if not pd.isna(punto_critico):
    st.markdown(
        f"<h3 style='color: {COLOR_TEXT};'>Secondo l'analisi, la tua performance degrada significativamente dopo circa <span style='color: {COLOR_ACCENT}; font-size: 1.2em;'>{int(punto_critico)} ripetizioni.</span></h3>", 
        unsafe_allow_html=True
    )
    st.info("Considera un intervallo di riposo o un cambio di focus tecnico dopo questo punto.")
else:
    st.success("La tua performance rientra sempre nei parametri accettabili!")

st.write("---")
st.markdown(
    f"<p style='text-align: center; color: {COLOR_ACCENT};'>⚡ <a href='https://supernovalab.altervista.org' style='color: {COLOR_ACCENT}; text-decoration: none;'>Supernova R&D Lab</a> | Sports Engineering ⚡</p>",
    unsafe_allow_html=True
)
