import streamlit as st
from datetime import date, timedelta
import pandas as pd
import plotly.express as px

def giorni_lavorativi(start_date, end_date):
    giorni = 0
    delta = end_date - start_date
    for i in range(delta.days + 1):
        giorno_corrente = start_date + timedelta(days=i)
        if giorno_corrente.weekday() < 5:  # Lunedì=0, Domenica=6
            giorni += 1
    return giorni


# Configurazione pagina
st.set_page_config(page_title="The Descent - Next Chapter", page_icon="🏔️", layout="centered")

# --- TITOLO E INTRO ---
st.title("🏔️ La Discesa della Montagna")
st.subheader("Ogni giorno un passo in meno verso la vetta, un passo in più verso la valle.")
st.markdown("---")

# --- CONFIGURAZIONE DATE ---
DATA_INIZIO_PREAVVISO = date(2026, 6, 1)  
DATA_FINE_PREAVVISO = date(2026, 10, 2)  
OGGI = date.today()

# --- CALCOLI ---
giorni_totali = (DATA_FINE_PREAVVISO - DATA_INIZIO_PREAVVISO).days
giorni_totali_feriali = giorni_lavorativi(DATA_INIZIO_PREAVVISO, DATA_FINE_PREAVVISO) #(DATA_FINE_PREAVVISO - DATA_INIZIO_PREAVVISO).days

giorni_passati = (OGGI - DATA_INIZIO_PREAVVISO).days
giorni_passati_feriali = giorni_lavorativi(DATA_INIZIO_PREAVVISO, OGGI) #(OGGI - DATA_INIZIO_PREAVVISO).days

giorni_rimanenti = (DATA_FINE_PREAVVISO - OGGI).days
giorni_rimanenti_feriali = giorni_lavorativi(OGGI, DATA_FINE_PREAVVISO) #(DATA_FINE_PREAVVISO - OGGI).days

# Limiti di sicurezza
giorni_passati = max(0, min(giorni_passati_feriali, giorni_totali_feriali))
giorni_rimanenti = max(0, giorni_rimanenti)
percentuale_completata = round((giorni_passati_feriali / giorni_totali_feriali) * 100, 2)

# --- METRICHE IN EVIDENZA ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Quota di partenza (gg lav)", value=giorni_totali_feriali)
with col2:
    st.metric(label="Quota attuale (gg lav)📉", value=giorni_rimanenti_feriali)
with col3:
    st.metric(label="Scalini scesi (gg lav)", value=giorni_passati_feriali)
with col4:
    st.metric(label="Discesa completata", value=f"{percentuale_completata}%")

st.markdown("---")

# --- COSTRUZIONE DEL GRAFICO "DISCESA" ---
st.write("### 📉 Il profilo della tua discesa")

# Generiamo la cronologia dei giorni per il grafico
date_intervallo = [DATA_INIZIO_PREAVVISO + timedelta(days=x) for x in range(giorni_totali + 1)]
giorni_mancanti_storia = [giorni_totali - x for x in range(giorni_totali + 1)]

# Creiamo un DataFrame per Plotly
df = pd.DataFrame({
    "Data": date_intervallo,
    "Giorni Rimanenti": giorni_mancanti_storia
})

# Creiamo il grafico a linee
fig = px.area(
    df, 
    x="Data", 
    y="Giorni Rimanenti",
    title="Verso quota 0 giorni",
    labels={"Giorni Rimanenti cal.": "Giorni alla fine cal.", "Data": "Calendario"},
    template="plotly_white"
)

# Personalizzazione estetica della linea (stile sentiero di montagna)
fig.update_traces(line=dict(color="#2ca02c", width=3)) 

# Evidenziamo il punto "OGGI" sulla mappa per capire a che punto della discesa ti trovi
fig.add_scatter(
    x=[OGGI], 
    y=[giorni_rimanenti], 
    mode="markers+text", 
    name="Tu sei qui",
    text=["📍 Tu sei qui"],
    textposition="top right",
    marker=dict(color="red", size=12)
)

# Render del grafico in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- INTERFACCIA PSICOLOGICA ---
if OGGI >= DATA_FINE_PREAVVISO:
    st.balloons()
    st.success("🎉 **Sei arrivato a valle! Il vecchio percorso è concluso, sei arrivato!** 🚀")
elif percentuale_completata >= 90:
    st.info("**Ci siamo ormai, ultimi sforzi! Tieni duro!**")
elif percentuale_completata >= 75:
    st.info("🏃‍♂️ **Sei all'ultimo chilometro! Manca pochissimo, mantieni alta la professionalità e prepara gli scatoloni.**")
elif percentuale_completata >= 50:
    st.info("🌓 **Giro di boa superato! Più di metà strada è alle tue spalle. Il countdown accelera da qui in poi.**")
elif percentuale_completata >= 35:
    st.success("🌱 **I motori si stanno scaldando. Stai lasciando tutto in ordine, un giorno alla volta.**")
elif percentuale_completata >= 20:
    st.success("🌱 **Forza dai!**")
else:
    st.info(f"🏕️ Ti trovi a **{giorni_rimanenti}** metri (giorni) di quota. Il sentiero è tracciato, continua a scendere con passo costante.")

# Sidebar standard per i task
st.sidebar.header("📋 Ricordati di:")
st.sidebar.checkbox("Documentare i processi più utili")
st.sidebar.checkbox("Sistemare e pulire i file locali")
st.sidebar.checkbox("Salutare i colleghi più stretti")
st.sidebar.checkbox("Cancellare account personali da pc aziendale")
