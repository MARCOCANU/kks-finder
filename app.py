import streamlit as st
import pandas as pd

st.set_page_config(page_title="KKS Finder", layout="centered")
# --- STILE ---
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Titolo */
h1 {
    text-align: center !important;
    font-size: 42px !important;
    margin-top: 40px !important;
    margin-bottom: 20px !important;
    font-weight: 700 !important;
    color: #003366 !important;
}

/* Barra di ricerca */
.stTextInput > div > div > input {
    font-size: 22px !important;
    height: 55px !important;
    border-radius: 12px !important;
    border: 2px solid #0078d4 !important;
    background-color: #eef6ff !important;
    padding-left: 14px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #005fa3 !important;
    background-color: #ffffff !important;
    box-shadow: 0 0 8px rgba(0,120,212,0.4) !important;
}

/* Card risultato */
.result-box {
    padding: 18px;
    border-radius: 14px;
    background-color: #f3f7fb;
    border: 1px solid #cfd6e0;
    margin-top: 25px;
    margin-bottom: 25px;
}

/* Tabella */
[data-testid="dataframe"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid #d6d9df !important;
}

/* Layout */
.block-container {
    max-width: 850px !important;
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
}

/* --- Barra superiore colorata --- */
.topbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 42px;
    background: #0078d4; /* blu A2A-style */
    z-index: 999;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}

/* Spazio extra all'inizio della pagina per non far coprire il contenuto dalla topbar */
.block-container {
    padding-top: 5rem !important; /* aumenta se serve più spazio */
}
</style>
""", unsafe_allow_html=True)


st.markdown(
    '<h1 style="text-align:center; font-size:42px; margin-top:40px; margin-bottom:12px; color:#003366;">Ricerca posizione KKS</h1>',
    unsafe_allow_html=True
)
# Barra superiore colorata
st.markdown('<div class="topbar"></div>', unsafe_allow_html=True)
# ------------------------------------------------------------
# 1) CARICA IL FILE EXCEL
# ------------------------------------------------------------
try:
    df = pd.read_excel("database.xlsx", header=0)
except Exception as e:
    st.error(f"Errore nel caricamento del file Excel: {e}")
    st.stop()

# Rimuove colonne completamente vuote
df = df.dropna(axis=1, how="all")

# Normalizza nomi colonne
df.columns = [str(c).strip().upper() for c in df.columns]

# Controllo colonna KKS
if "KKS" not in df.columns:
    st.error(f"Colonna 'KKS' non trovata. Colonne presenti: {list(df.columns)}")
    st.stop()

# Normalizza valori KKS
df["KKS"] = df["KKS"].astype(str).str.upper().str.strip()

# Normalizza descrizione (se presente)
if "DESCRIZIONE" in df.columns:
    df["DESCRIZIONE"] = df["DESCRIZIONE"].astype(str)

# ------------------------------------------------------------
# 2) INPUT UTENTE
# ------------------------------------------------------------
kks = st.text_input("Inserisci codice KKS (anche parziale)").strip()

# ------------------------------------------------------------
# 3) RICERCA PARZIALE
# ------------------------------------------------------------
if kks:
    # Ricerca in KKS
    filtro = df["KKS"].str.contains(kks, case=False, regex=False, na=False)

    # Ricerca anche nella descrizione, se esiste
    if "DESCRIZIONE" in df.columns:
        filtro = filtro | df["DESCRIZIONE"].str.contains(kks, case=False, regex=False, na=False)

    risultati = df[filtro]

    if risultati.empty:
        st.error("Nessun risultato trovato.")
    else:
        st.success(f"Trovate {len(risultati)} occorrenze")

        # Colonne da mostrare
        colonne_utili = [
            c for c in [
                "KKS", "SOTTOSTAZIONE ELETTRICA", "DESCRIZIONE",
                "P-ID", "COLONNA", "POSIZIONE", "NOTE-LINEA"
            ] if c in df.columns
        ]

        # Tabella risultati
        st.dataframe(risultati[colonne_utili], use_container_width=True)

        # Mostra il primo risultato
        r = risultati.iloc[0]
        st.subheader("Dettaglio primo risultato:")

        if "SOTTOSTAZIONE ELETTRICA" in risultati.columns:
            st.write("**Sottostazione elettrica:**", r["SOTTOSTAZIONE ELETTRICA"])
        if "DESCRIZIONE" in risultati.columns:
            st.write("**Descrizione:**", r["DESCRIZIONE"])
        if "P-ID" in risultati.columns:
            st.write("**P&ID:**", r["P-ID"])
        if "COLONNA" in risultati.columns:
            st.write("**Colonna:**", r["COLONNA"])
        if "POSIZIONE" in risultati.columns:
            st.write("**Posizione:**", r["POSIZIONE"])
        if "NOTE-LINEA" in risultati.columns:
            st.write("**Note/Linea:**", r["NOTE-LINEA"])