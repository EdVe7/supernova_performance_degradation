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

# --- Colori e Stili (Ispirazione Supernova) ---
# Verde scuro (Teal)
COLOR_PRIMARY = "#0b1d22" 
# Oro
COLOR_ACCENT = "#d4af37" 
# Bianco
COLOR_TEXT = "#ffffff"

# Stile custom per Streamlit (solo alcuni elementi, il resto è gestito dal tema)
# Non è HTML puro, ma si inserisce in Streamlit con st.markdown
st.markdown(
    f"""
    <style>
    .reportview-container .main .block-container {{
        max-width: 800px;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }}
    .sidebar .sidebar-content {{
        background-color: {COLOR_PRIMARY};
        color: {COLOR_TEXT};
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {COLOR_ACCENT};
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }}
    .stButton>button {{
        background-color: {COLOR_ACCENT};
        color: {COLOR_PRIMARY};
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }}
    .stTextInput>div>div>input {{
        border: 1px solid {COLOR_ACCENT};
        border-radius: 5px;
        padding: 8px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Logo Supernova (Semplice, da migliorare con un'immagine) ---
# Per un logo immagine: st.image("path/to/tuo_logo.png", width=100)
st.markdown(
    f"<h1 style='text-align: center; color: {COLOR_TEXT}; font-size: 2.5em;'><span style='color: {COLOR_ACCENT};'>Supernova</span> Performance Predictor ⚡</h1>", 
    unsafe_allow_html=True
)
st.markdown(
    f"<p style='text-align: center; color: {COLOR_ACCENT}; font-size: 1.2em;'><i>Decodifichiamo la fatica, ottimizziamo il picco.</i></p>", 
    unsafe_allow_html=True
)

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

# --- Analisi del Punto di Degradaione Critica ---
st.subheader("Previsione del Punto Critico")
soglia_degradazione = st.number_input(
    "Soglia di accettabilità (es. se la deviazione supera X metri, la performance è degradata)", 
    deviazione_iniziale + 0.5, 
    deviazione_iniziale + degradazione_per_ripetizione * num_ripetizioni, 
    deviazione_iniziale + degradazione_per_ripetizione * num_ripetizioni / 2
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
