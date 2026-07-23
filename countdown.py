import streamlit as st
from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import requests

def giorni_lavorativi(start_date, end_date):
    inizio_ferie = date(2026, 8, 10)
    fine_ferie = date(2026, 8, 28)
    giorni = 0
    delta = end_date - start_date
    for i in range(delta.days + 1):
        giorno_corrente = start_date + timedelta(days=i)
        if giorno_corrente.weekday() < 5 :  # Lunedì=0, Domenica=6
            if giorno_corrente < inizio_ferie or giorno_corrente > fine_ferie:
                giorni += 1
    return giorni

def ottieni_citazione_del_giorno():
    try:
        response = requests.get("https://zenquotes.io/api/today")
        data = response.json()
        # Ritorna la citazione + l'autore
        return f"🌱**La frase di oggi:**\n\n“{data[0]['q']}” — {data[0]['a']}"
    except:
        # Frase di backup se internet non va
        return "Fai un passo alla volta, la meta si avvicina."

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
DOMANI = date.today() + timedelta(days=1)

# --- CALCOLI ---
giorni_totali = (DATA_FINE_PREAVVISO - DATA_INIZIO_PREAVVISO).days
giorni_totali_feriali = giorni_lavorativi(DATA_INIZIO_PREAVVISO, DATA_FINE_PREAVVISO) #(DATA_FINE_PREAVVISO - DATA_INIZIO_PREAVVISO).days

giorni_passati = (OGGI - DATA_INIZIO_PREAVVISO).days
giorni_passati_feriali = giorni_lavorativi(DATA_INIZIO_PREAVVISO, OGGI) #(OGGI - DATA_INIZIO_PREAVVISO).days

giorni_rimanenti = (DATA_FINE_PREAVVISO - DOMANI).days
giorni_rimanenti_feriali = giorni_lavorativi(DOMANI, DATA_FINE_PREAVVISO) #(DATA_FINE_PREAVVISO - OGGI).days

# Limiti di sicurezza
giorni_passati = max(0, min(giorni_passati_feriali, giorni_totali_feriali))
giorni_rimanenti = max(0, giorni_rimanenti)
percentuale_completata = round((giorni_passati_feriali / giorni_totali_feriali) * 100, 1)

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

# Definizioni periodi speciali
inizio_ferie = date(2026, 8, 10)
fine_ferie = date(2026, 8, 28)

# Creiamo il grafico a linee
fig = px.area(
    df, 
    x="Data", 
    y="Giorni Rimanenti",
    title="Verso quota 0 giorni",
    labels={"Giorni Rimanenti": "Giorni alla fine", "Data": "Calendario"},
    template="plotly_white"
)

# Personalizzazione estetica della linea e dell'area
fig.update_traces(line=dict(color="#2ca02c", width=3), fillcolor="rgba(44, 160, 44, 0.3)")

# Evidenziamo il periodo di ferie con colore di sfondo
fig.add_vrect(
    x0=inizio_ferie, 
    x1=fine_ferie,
    fillcolor="#ff7f0e", 
    opacity=0.2,
    layer="below",
    line_width=0
) 

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
# --- IL BANCO DELLE FRASI (Divise per macro-fasi per rimanere coerenti) ---
FRASI_INIZIO = [
    "“Chi sale sulle montagne più alte ride di tutte le tragedie.” — Friedrich Nietzsche. Tu stai scendendo, quindi rilassati.",
    "Il primo passo non ti porta dove vuoi arrivare, ma ti toglie da dove sei. Focus sul passaggio di consegne.",
    "Zaino in spalla e passo costante. Le prime tappe sono di puro assestamento.",
    "Mantieni la calma, documenta il codice e lascia che il tempo faccia il suo lavoro.",
    "La transizione è iniziata. Un giorno alla volta, con la massima professionalità."
]

FRASI_METÀ = [
    "“Non esistono grandi conquiste che non siano state precedute da un piccolo passo.” — Proverbio. Sei a metà valle!",
    "Il panorama comincia a cambiare. Il vecchio lavoro è quasi alle spalle, il nuovo si intravede all'orizzonte.",
    "Metà del sentiero è andata. Ottimo momento per fare il punto sui task rimasti nella sidebar.",
    "La costanza batte il talento. Ogni giorno completato è un metro di quota guadagnato verso la libertà."
]

FRASI_FINE = [
    "“La fine di un viaggio è solo l'inizio di un altro.” — José Saramago. Prepara gli scatoloni virtuali.",
    "Vedi le luci della valle là in fondo? Manca pochissimo. Lascia un ottimo ricordo dietro di te.",
    "Ultimi tornanti. Respira l'aria fresca del nuovo inizio.",
    "Quota zero in vista. È il momento dei saluti e di ripulire i file locali.",
    "Giro di boa. Da qui in poi la gravità gioca a tuo favore, la discesa accelera.",
    "Il traguardo è dietro la prossima curva. Complimenti per aver gestito il percorso al meglio."
]

if OGGI >= DATA_FINE_PREAVVISO:
    st.balloons()
    st.success("🎉 **Sei arrivato a valle! Il vecchio percorso è concluso, sei arrivato!** 🚀")
#elif percentuale_completata >= 90:
#    st.info("**Ci siamo ormai, ultimi sforzi! Tieni duro!**")
#elif percentuale_completata >= 75:
#    st.info("🏃‍♂️ **Sei all'ultimo chilometro! Manca pochissimo, mantieni alta la professionalità e prepara gli scatoloni.**")
#elif percentuale_completata >= 50:
#    st.info("🌓 **Giro di boa superato! Più di metà strada è alle tue spalle. Il countdown accelera da qui in poi.**")
#elif percentuale_completata >= 35:
#    st.info("🌱 **I motori si stanno scaldando. Stai lasciando tutto in ordine, un giorno alla volta.**")
#elif percentuale_completata >= 20:
#    st.info("🌱 **Forza dai!**")
else:
    if percentuale_completata < 35:
        lista_attiva = FRASI_INIZIO
    elif percentuale_completata < 75:
        lista_attiva = FRASI_METÀ
    else:
        lista_attiva = FRASI_FINE
    
    # Sceglie una frase che cambia ogni giorno in base a 'giorni_passati'
    indice_frase = giorni_passati % len(lista_attiva)
    frase_del_giorno = lista_attiva[indice_frase]
    
    # Mostra la frase in un box carino
    st.info(f"💬 **Il pensiero di oggi:**\n\n{frase_del_giorno}")
    #st.info(f"🏕️ Ti trovi a **{giorni_rimanenti}** metri (giorni) di quota. Il sentiero è tracciato, continua a scendere con passo costante.")

st.success(ottieni_citazione_del_giorno())

# Sidebar standard per i task
#st.sidebar.header("📋 Ricordati di:")
#st.sidebar.checkbox("Documentare i processi più utili")
#st.sidebar.checkbox("Sistemare e pulire i file locali")
#st.sidebar.checkbox("Salutare i colleghi più stretti")
#st.sidebar.checkbox("Cancellare account personali da pc aziendale")
