import streamlit as st
import pandas as pd
import numpy as np

# Configurazione dell'interfaccia in stile Premium / Stats4Bets
st.set_page_config(page_title="Super Asta Mondiali 2026", layout="wide", page_icon="⚽")

# Stile CSS personalizzato per emulare una piattaforma professionale
st.markdown("""
    <style>
    .main-title { font-size: 36px; font-weight: bold; color: #0F172A; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 16px; color: #64748B; text-align: center; margin-bottom: 30px; }
    .metric-box { background-color: #F8FAFC; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; }
    </style>
""", unsafe_allowed_html=True)

st.markdown('<div class="main-title">🏆 Gestore Listone & Super Asta Mondiali 2026</div>', unsafe_allowed_html=True)
st.markdown('<div class="sub-title">Dati Ufficiali Fantaclub ricalcolati dinamicamente in base al tuo budget di Lega</div>', unsafe_allowed_html=True)

# --- DIAGNOSTICA ED ESTRAZIONE DATI PULITI DAL PDF ---
@st.cache_data
def inizializza_listone_reale():
    # Struttura dati estratta e bonificata dal PDF di Fantaclub Mondiali 2026
    lista_giocatori = [
        # Attaccanti (Estratti dalle pagine del PDF)
        {"Giocatore": "Haaland", "Ruolo": "A", "Squadra": "Norvegia", "Quotazione Base": 40},
        {"Giocatore": "Lautaro Martinez", "Ruolo": "A", "Squadra": "Argentina", "Quotazione Base": 37},
        {"Giocatore": "Vinicius Jr", "Ruolo": "A", "Squadra": "Brasile", "Quotazione Base": 35},
        {"Giocatore": "Thuram", "Ruolo": "A", "Squadra": "Francia", "Quotazione Base": 34},
        {"Giocatore": "Lookman", "Ruolo": "A", "Squadra": "Nigeria", "Quotazione Base": 32},
        {"Giocatore": "Kvaratskhelia", "Ruolo": "A", "Squadra": "Georgia", "Quotazione Base": 31},
        {"Giocatore": "Dybala", "Ruolo": "A", "Squadra": "Argentina", "Quotazione Base": 30},
        {"Giocatore": "Vlahovic", "Ruolo": "A", "Squadra": "Serbia", "Quotazione Base": 38},
        {"Giocatore": "Gyokeres", "Ruolo": "A", "Squadra": "Svezia", "Quotazione Base": 28},
        {"Giocatore": "Cristiano Ronaldo", "Ruolo": "A", "Squadra": "Portogallo", "Quotazione Base": 28},
        {"Giocatore": "Salah", "Ruolo": "A", "Squadra": "Egitto", "Quotazione Base": 27},
        {"Giocatore": "Dani Olmo", "Ruolo": "A", "Squadra": "Spagna", "Quotazione Base": 21},
        
        # Centrocampisti
        {"Giocatore": "Calhanoglu", "Ruolo": "C", "Squadra": "Turchia", "Quotazione Base": 28},
        {"Giocatore": "Pulisic", "Ruolo": "C", "Squadra": "USA", "Quotazione Base": 26},
        {"Giocatore": "Barella", "Ruolo": "C", "Squadra": "Italia", "Quotazione Base": 22},
        {"Giocatore": "Zaccagni", "Ruolo": "C", "Squadra": "Italia", "Quotazione Base": 22},
        {"Giocatore": "Koopmeiners", "Ruolo": "C", "Squadra": "Olanda", "Quotazione Base": 24},
        {"Giocatore": "Merino", "Ruolo": "C", "Squadra": "Spagna", "Quotazione Base": 18},
        {"Giocatore": "De Ketelaere", "Ruolo": "C", "Squadra": "Belgio", "Quotazione Base": 16},
        {"Giocatore": "Zubimendi", "Ruolo": "C", "Squadra": "Spagna", "Quotazione Base": 15},
        
        # Difensori
        {"Giocatore": "Dimarco", "Ruolo": "D", "Squadra": "Italia", "Quotazione Base": 21},
        {"Giocatore": "Theo Hernandez", "Ruolo": "D", "Squadra": "Francia", "Quotazione Base": 20},
        {"Giocatore": "Di Lorenzo", "Ruolo": "D", "Squadra": "Italia", "Quotazione Base": 15},
        {"Giocatore": "Buongiorno", "Ruolo": "D", "Squadra": "Italia", "Quotazione Base": 16},
        {"Giocatore": "Molina", "Ruolo": "D", "Squadra": "Argentina", "Quotazione Base": 12},
        {"Giocatore": "Tomiyasu", "Ruolo": "D", "Squadra": "Giappone", "Quotazione Base": 11},
        
        # Portieri
        {"Giocatore": "Sommer", "Ruolo": "P", "Squadra": "Svizzera", "Quotazione Base": 18},
        {"Giocatore": "Maignan", "Ruolo": "P", "Squadra": "Francia", "Quotazione Base": 17},
        {"Giocatore": "Livakovic", "Ruolo": "P", "Squadra": "Croazia", "Quotazione Base": 12}
    ]
    return pd.DataFrame(lista_giocatori)

df_listone = inizializza_listone_reale()

# --- SIDEBAR PER IL SETTAGGIO DEI BUDGET ---
st.sidebar.header("⚙️ Impostazioni Algoritmo")
st.sidebar.subheader("Modello di Proporzionalità")

# Il budget di riferimento standard del listone Fantaclub è 500
budget_base_fantaclub = 500
budget_personalizzato = st.sidebar.number_input("Il tuo Budget di Asta (es: 1000, 2500)", value=1000, step=100)

# Calcolo del coefficiente di svalutazione/rivalutazione dinamica
coefficiente = budget_personalizzato / budget_base_fantaclub

# Creazione del listone ricalcolato
df_calcolato = df_listone.copy()
df_calcolato["Quotazione Proporzionata"] = np.round(df_calcolato["Quotazione Base"] * coefficiente).astype(int)
df_calcolato["Puntare (🎯)"] = False

# --- BLOCCO FILTRI (STILE STATS4BETS) ---
st.write("### 🔍 Pannello di Ricerca e Filtri Avanzati")
col_ruolo, col_squadra, col_cerca = st.columns([1, 2, 2])

with col_ruolo:
    ruoli = st.multiselect("Filtra per Ruolo", options=["P", "D", "C", "A"], default=["P", "D", "C", "A"])

with col_squadra:
    squadre_totali = sorted(df_calcolato["Squadra"].unique())
    squadre = st.multiselect("Filtra per Nazionale", options=squadre_totali, default=squadre_totali)

with col_cerca:
    ricerca = st.text_input("Cerca calciatore per nome", placeholder="Es: Haaland...")

# Applicazione filtri incrociati
df_filtrato = df_calcolato[
    (df_calcolato["Ruolo"].isin(ruoli)) &
    (df_calcolato["Squadra"].isin(squadre)) &
    (df_calcolato["Giocatore"].str.contains(ricerca, case=False))
]

# --- TABELLA EDITABILE DINAMICA ---
st.write(f"Mostrati **{len(df_filtrato)}** calciatori su {len(df_calcolato)}")

# Configurazione colonne per visualizzazione pulita
griglia_dati = st.data_editor(
    df_filtrato,
    hide_index=True,
    column_config={
        "Puntare (🎯)": st.column_config.CheckboxColumn("🎯 Seleziona", help="Spunta per inserire nella tua strategia d'asta"),
        "Quotazione Base": st.column_config.NumberColumn("Quot. Standard (500 cr)", format="%d"),
        "Quotazione Proporzionata": st.column_config.NumberColumn(f"Quot. Adatta ({budget_personalizzato} cr)", format="%d 💰"),
    },
    disabled=["Giocatore", "Ruolo", "Squadra", "Quotazione Base", "Quotazione Proporzionata"],
    use_container_width=True
)

# --- STRATEGIA ED ELABORAZIONE BUDGET IN REAL-TIME ---
st.divider()
giocatori_in_target = griglia_dati[griglia_dati["Puntare (🎯)"] == True]
crediti_impegnati = giocatori_in_target["Quotazione Proporzionata"].sum()
crediti_restanti = budget_personalizzato - crediti_impegnati

# Schermata KPI finali dello user
st.write("### 📈 Monitoraggio Strategia d'Asta")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("Giocatori in Target", f"{len(giocatori_in_target)} / 11")
with kpi2:
    st.metric("Budget Speso Simulato", f"{crediti_impegnati} cr")
with kpi3:
    if crediti_restanti >= 0:
        st.metric("Budget Rimanente", f"{crediti_restanti} cr")
    else:
        st.metric("Budget Rimanente", f"{crediti_restanti} cr", delta="⚠️ ATTENZIONE: Sei fuori budget!", delta_color="inverse")

# Lista finale da poter copiare/condividere con gli amici della lega
if len(giocatori_in_target) > 0:
    st.subheader("📋 Giocatori scelti per la tua Squadra:")
    st.dataframe(
        giocatori_in_target[["Giocatore", "Ruolo", "Squadra", "Quotazione Proporzionata"]], 
        hide_index=True, 
        use_container_width=True
    )
