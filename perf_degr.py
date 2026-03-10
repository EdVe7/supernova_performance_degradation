import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

# --- 1. CONFIGURAZIONE PAGINA & STILE ---
st.set_page_config(page_title="Supernova - Performance Predictor", layout="centered")

# Colori Brand Supernova
COLOR_BG = "#0b1d22"    # Teal Scuro
COLOR_GOLD = "#d4af37"  # Oro
COLOR_TEXT = "#ffffff"  # Bianco

st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BG}; color: {COLOR_TEXT}; }}
    h1, h2, h3 {{ color: {COLOR_GOLD} !important; }}
    .stButton>button {{ background-color: {COLOR_GOLD}; color: {COLOR_BG}; font-weight: bold; border: none; }}
    .stTextInput>div>div>input {{ background-color: #1a2e35; color: white; border: 1px solid {COLOR_GOLD}; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA DI ACCESSO (PASSWORD) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align:center;'>Accesso Lab Supernova</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Inserisci Password Ingegneria", type="password")
        if st.button("Entra"):
            if pwd == "supernova2026": # CAMBIA QUESTA PASSWORD SE VUOI
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Password errata.")
        return False
    return True

if check_password():

    # --- 3. HEADER ---
    st.markdown(f"<h1 style='text-align: center;'>SUPERNOVA <span style='color:{COLOR_GOLD}'>PREDICTOR</span> ⚡</h1>", unsafe_allow_html=True)
    st.write("---")

    # --- 4. INPUT DATI ---
    st.sidebar.header("Parametri Analisi")
    atleta = st.sidebar.text_input("Nome Atleta", "Atleta Alpha")
    n_shots = st.sidebar.slider("Numero Ripetizioni", 10, 50, 25)
    base_error = st.sidebar.slider("Errore Base (metri)", 0.5, 3.0, 1.2)
    fatigue_rate = st.sidebar.slider("Tasso di Fatica", 0.01, 0.10, 0.04)

    # --- 5. GENERAZIONE DATI & GRAFICO ---
    np.random.seed(42)
    # Simulazione: l'errore aumenta con le ripetizioni + rumore casuale
    errors = [base_error + (i * fatigue_rate) + np.random.normal(0, 0.2) for i in range(n_shots)]
    df = pd.DataFrame({"Colpo": range(1, n_shots + 1), "Errore (m)": errors})

    st.subheader(f"Analisi Degradaione: {atleta}")
    
    # Creazione Grafico con Seaborn
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor("#122a30")
    
    sns.lineplot(data=df, x="Colpo", y="Errore (m)", color=COLOR_GOLD, linewidth=2, marker='o', ax=ax)
    
    # Styling assi
    ax.tick_params(colors=COLOR_TEXT)
    ax.xaxis.label.set_color(COLOR_TEXT)
    ax.yaxis.label.set_color(COLOR_TEXT)
    for spine in ax.spines.values(): spine.set_edgecolor(COLOR_GOLD)
    
    st.pyplot(fig)

    # --- 6. LOGICA DI CALCOLO PUNTO CRITICO ---
    threshold = base_error * 1.5
    critical_hit = df[df["Errore (m)"] > threshold]["Colpo"].min()

    if not pd.isna(critical_hit):
        st.warning(f"⚠️ PUNTO CRITICO RILEVATO: Dopo il colpo {int(critical_hit)} la precisione decade oltre il 50%.")
    else:
        st.success("✅ Performance stabile per tutta la sessione.")

    # --- 7. GENERAZIONE PDF ---
    def create_pdf(name, shots, crit):
        # Salviamo il grafico come immagine temporanea
        img_path = "temp_chart.png"
        fig.savefig(img_path, dpi=150, bbox_inches='tight')
        
        pdf = FPDF()
        pdf.add_page()
        
        # Header PDF
        pdf.set_fill_color(11, 29, 34) # Teal Supernova
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_font("Arial", 'B', 24)
        pdf.set_text_color(212, 175, 55) # Oro
        pdf.cell(0, 20, "SUPERNOVA R&D REPORT", ln=True, align='C')
        
        # Info Atleta
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 14)
        pdf.ln(25)
        pdf.cell(0, 10, f"Analisi Performance Atleta: {name}", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Sessione di {shots} ripetizioni.", ln=True)
        
        # Inserimento Immagine Grafico
        pdf.image(img_path, x=15, y=85, w=180)
        
        # Conclusioni
        pdf.set_y(180)
        pdf.set_font("Arial", 'B', 12)
        msg = f"Soglia critica individuata al colpo: {int(crit)}" if not pd.isna(crit) else "Nessuna anomalia rilevata."
        pdf.multi_cell(0, 10, f"RISULTATO TECNICO: {msg}")
        
        pdf_name = f"Report_{name}.pdf"
        pdf.output(pdf_name)
        return pdf_name

    # Bottone per scaricare
    if st.button("Genera e Scarica Report PDF"):
        file_path = create_pdf(atleta, n_shots, critical_hit)
        with open(file_path, "rb") as f:
            st.download_button(
                label="Clicca qui per il download",
                data=f,
                file_name=file_path,
                mime="application/pdf"
            )
        # Pulizia file temporanei
        if os.path.exists("temp_chart.png"): os.remove("temp_chart.png")

    st.write("---")
    st.caption("Supernova Lab © 2026 - Ingegneria Meccanica Applicata")
