import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="KKS Finder",
    layout="centered",
    page_icon="icon-192.png"
)

# === Tema Scuro Sicuro ===
st.markdown("""
<style>
    html, body, .appview-container {
        background-color: #000000 !important; 
        color: #e6e6e6 !important;
    }
    .stButton>button {
        background-color: #0078d4 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #005fa3 !important;
    }
    .stTextInput > div > div > input {
        background-color: #111214 !important;
        color: #e6e6e6 !important;
        border: 2px solid #3793ff !important;
        border-radius: 10px !important;
        height: 50px !important;
        font-size: 20px !important;
    }
    [data-testid="stMarkdown"] h1 {
        color: #e6e6e6 !important;
    }
</style>
""", unsafe_allow_html=True)
# ------------------------------------------------------------
# BARRA BLU STREAMLIT (senza HTML)
# ------------------------------------------------------------
import streamlit as st

# Spazio sopra
st.write("")

# Rettangolo blu come barra
st.markdown(
    """
    <div style='background-color:#0078d4; height:60px; border-radius:0 0 12px 12px;'></div>
    """,
    unsafe_allow_html=True,
)

# Logo + testo centrati in Streamlit
col1, col2, col3 = st.columns([1,2,1])
with col2:
    # Avvicina il logo alla barra blu
    st.markdown("<div style='margin-top:-75px'></div>", unsafe_allow_html=True)
    st.image("icon-192.png", width=110)
    st.markdown("<h2 style='text-align:center; margin-top:-5px;'>KKS Finder</h2>", 
unsafe_allow_html=True)
# ============================================
#  TITOLO
# ============================================
st.markdown("##")
st.markdown("<h1 style='text-align:center;'>Ricerca posizione KKS</h1>", unsafe_allow_html=True)

# ============================================
#  PULSANTE PER APRIRE LA VERSIONE APP
# ============================================
if st.button("📱 Apri versione App"):
    st.markdown(
        "🚀 Clicca qui per aprire la versione App"
    )
# ============================================
#  FIRMA (solo testo e immagine)
# ============================================
st.markdown("###")
colA, colB, colC = st.columns([1,2,1])
with colB:
    st.image("icon-192.png", width=20)
    st.markdown("<p style='text-align:center; font-size:14px; color:#9aa0a6;'>A2A Esercizio Parona | <strong>Marco Canu</strong></p>", unsafe_allow_html=True)

# ============================================
#  CARICAMENTO DATABASE
# ============================================
try:
    df = pd.read_excel("database.xlsx", header=0)
except Exception as e:
    st.error(f"Errore nel caricamento di database.xlsx: {e}")
    st.stop()

df = df.dropna(axis=1, how="all")
df.columns = [str(c).strip().upper() for c in df.columns]

if "KKS" not in df.columns:
    st.error(f"Colonna 'KKS' non trovata. Colonne disponibili: {list(df.columns)}")
    st.stop()

df["KKS"] = df["KKS"].astype(str).str.upper().str.strip()

if "DESCRIZIONE" in df.columns:
    df["DESCRIZIONE"] = df["DESCRIZIONE"].astype(str)

# ============================================
#  INPUT
# ============================================
kks = st.text_input("Inserisci codice KKS (anche parziale)").strip()

# ============================================
#  RICERCA
# ============================================
if kks:
    mask = df["KKS"].str.contains(kks, case=False, regex=False, na=False)
    if "DESCRIZIONE" in df.columns:
        mask |= df["DESCRIZIONE"].str.contains(kks, case=False, regex=False, na=False)

    results = df[mask]

    if results.empty:
        st.error("Nessun risultato trovato.")
    else:
        st.success(f"Trovate {len(results)} occorrenze")
        
        cols = [c for c in ["KKS","SOTTOSTAZIONE ELETTRICA","DESCRIZIONE","P-ID","P&ID","COLONNA","POSIZIONE","NOTE-LINEA","NOTE/LINEA"] if c in df.columns]
        
        st.dataframe(results[cols], use_container_width=True)

        r = results.iloc[0]
        st.subheader("Dettaglio primo risultato")
        box = st.container()
        with box:
            st.markdown(
                '<div style="background-color:#0f1218; padding:15px; border-radius:12px; border:1px solid #2a2f3a;">',
                unsafe_allow_html=True
            )
            for label,field in [
                ("KKS","KKS"),
                ("Sottostazione elettrica","SOTTOSTAZIONE ELETTRICA"),
                ("Descrizione","DESCRIZIONE"),
                ("P&ID","P-ID"),
                ("Colonna","COLONNA"),
                ("Posizione","POSIZIONE"),
                ("Note/Linea","NOTE-LINEA")
            ]:
                if field in df.columns:
                    st.write(f"**{label}:** {r[field]}")
            st.markdown("</div>", unsafe_allow_html=True)