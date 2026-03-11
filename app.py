import streamlit as st
import pandas as pd

st.set_page_config(page_title="KKS Finder", layout="centered")
st.title("Ricerca posizione KKS")

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