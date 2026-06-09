import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Comarb - Actividad de Chatbot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. BASE DE DATOS CRONOLÓGICA CONSOLIDADA ---
data_historica = {
    "Mes": ["Octubre 2025", "Noviembre 2025", "Diciembre 2025", "Enero 2026", "Febrero 2026", "Marzo 2026", "Abril 2026", "Mayo 2026"],
    "Sesiones_Brutas": [2805, 2593, 1885, 2485, 2774, 4416, 4986, 4999],
    "Tasa_Conversion": [21.00, 21.00, 23.61, 24.62, 24.73, 25.27, 26.58, 25.69],
    "Usuarios_Interactivos": [2805, 2593, 1885, 2485, 2774, 2493, 2137, 2164],
    "Tasa_Rebote": [0.00, 0.00, 0.00, 0.00, 0.00, 43.50, 57.14, 56.71],
    "Consultas_Escritas": [589, 544, 445, 612, 686, 630, 568, 556]
}
df = pd.DataFrame(data_historica)

# --- 2. PERFILES DE DISTRIBUCIÓN TEMPORAL ---
horas_eje = [f"{h:02d}:00" for h in range(24)]
perfiles_horarios = {
    "Octubre 2025": [20,15,10,5,5,2,2,3,5,15,45,90,180,210,195,150,140,160,155,120,90,70,60,40],
    "Noviembre 2025": [18,12,8,4,4,2,2,3,6,12,40,85,170,195,180,145,135,150,140,110,85,65,55,35],
    "Diciembre 2025": [40,38,27,16,12,9,7,5,3,15,36,75,147,205,218,181,145,136,146,119,89,84,72,57],
    "Enero 2026": [60,45,38,23,20,12,11,8,6,9,28,106,192,252,245,226,191,213,212,150,150,118,95,75],
    "Febrero 2026": [51,43,40,29,20,14,8,5,8,13,43,126,224,263,327,252,195,238,236,182,171,99,100,87],
    "Marzo 2026": [92,74,44,30,26,7,4,5,4,14,50,230,415,466,517,413,307,359,366,341,254,150,151,97],
    "Abril 2026": [94,55,59,39,24,9,7,10,6,23,59,257,440,553,537,471,350,433,452,378,299,178,141,112],
    "Mayo 2026": [99,63,70,44,23,21,9,3,9,27,51,253,421,535,573,467,339,410,470,379,262,172,176,123]
}
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
porcentajes_semanales = [0.21, 0.22, 0.22, 0.20, 0.13, 0.015, 0.005]

# --- 3. DATOS CUALITATIVOS Y DISTRIBUCIÓN DE SISTEMAS ---
insights_mes = {
    "Octubre 2025": {
        "contexto": "Mes de mayor actividad del trimestre base, marcando el inicio del período de alta demanda previo al cierre de año.",
        "foco": "Consultas de rutina sobre el uso del chatbot e interacciones bajo niveles normales de operación corporativa.",
        "keywords": {"Convenio": 100, "Sesiones": 85, "Consulta": 60},
        "sistemas": {"Convenio / Padrón": 50, "SIFERE / DDJJ": 30, "SIRCREB": 12, "SIRCUPA": 8, "SIRCIP": 0}
    },
    "Noviembre 2025": {
        "contexto": "Ligera disminución en el volumen bruto de consultas respecto a octubre, manteniendo una tasa de conversión plana del 21%.",
        "foco": "Consultas habituales de mantenimiento de padrón previas al cierre de ejercicio fiscal.",
        "keywords": {"Convenio": 100, "Baja": 80, "Alta": 75},
        "sistemas": {"Convenio / Padrón": 48, "SIFERE / DDJJ": 32, "SIRCREB": 12, "SIRCUPA": 8, "SIRCIP": 0}
    },
    "Diciembre 2025": {
        "contexto": "Desaceleración estacional típica generalizada (-27% de tráfico bruto) provocada por los recesos vacacionales y las fiestas de fin de año.",
        "foco": "Urgencias administrativas de cierre fiscal. Reorganización empresarial (altas/bajas) y fuerte irrupción de consultas críticas sobre el sistema SIRCUPA.",
        "keywords": {"Baja": 59, "DDJJ": 52, "Alta": 51, "Convenio": 48, "Retenciones": 41, "Sistema": 34, "Ingresos": 32, "SIRCREB": 31},
        "sistemas": {"Convenio / Padrón": 30, "SIFERE / DDJJ": 25, "SIRCREB": 20, "SIRCUPA": 25, "SIRCIP": 0}
    },
    "Enero 2026": {
        "contexto": "Recuperación operativa post-receso de Año Nuevo (+31% de crecimiento bruto), marcando el fin de la estacionalidad de las fiestas.",
        "foco": "Reorganización fiscal típica de inicio de ciclo anual. Dominio absoluto de los trámites de alta y baja en el Convenio Multilateral y reclamos por retenciones indebidas (SIRCREB/SIRCUPA).",
        "keywords": {"Alta": 60, "Jurisdicción": 55, "Padrón": 48, "Sistema": 45, "Baja": 40, "Convenio": 38, "Retenciones": 35},
        "sistemas": {"Convenio / Padrón": 45, "SIFERE / DDJJ": 20, "SIRCREB": 20, "SIRCUPA": 15, "SIRCIP": 0}
    },
    "Febrero 2026": {
        "contexto": "Reactivación plena del período comercial y administrativo, alcanzando el máximo volumen del cuatrimestre inicial (+11,6% de incremento respecto a enero).",
        "foco": "Foco crítico en el cierre del ejercicio fiscal: presentación de la DDJJ anual (CM03) en SIFERE Web. Se detectaron fuertes señales de alerta e inconvenientes técnicos externos (la palabra 'error' escaló al 4° lugar general).",
        "keywords": {"DDJJ": 100, "Baja": 87, "Convenio": 82, "Ingresos": 75, "Error": 68, "Actividad": 60, "Alta": 45, "Sistema": 40},
        "sistemas": {"Convenio / Padrón": 25, "SIFERE / DDJJ": 55, "SIRCREB": 12, "SIRCUPA": 8, "SIRCIP": 0}
    },
    "Marzo 2026": {
        "contexto": "Explosión masiva de demanda impulsada por el calendario de vencimientos generales del Convenio Multilateral.",
        "foco": "Consultas complejas sobre reglas de atribución, jurisdicciones de alta y regímenes de recaudación. Disminución drástica de problemas de estabilidad técnica en sistemas.",
        "keywords": {"Convenio": 100, "DDJJ": 88, "Baja": 78, "Multilateral": 72, "Alta": 65, "Ingresos": 58},
        "sistemas": {"Convenio / Padrón": 65, "SIFERE / DDJJ": 20, "SIRCREB": 10, "SIRCUPA": 5, "SIRCIP": 0}
    },
    "Abril 2026": {
        "contexto": "Nuevo pico histórico de tráfico bruto en el canal. Inicio de un período masivo de regularización de contribuyentes.",
        "foco": "Trámites de padrón con paridad exacta entre altas y bajas (68 menciones c/u). Alta demanda de consultas sobre gestión y validación de CUIT y acceso digital al portal corporativo.",
        "keywords": {"Convenio": 100, "Alta": 94, "Baja": 94, "DDJJ": 82, "CUIT": 74, "Retenciones": 66},
        "sistemas": {"Convenio / Padrón": 50, "SIFERE / DDJJ": 25, "SIRCREB": 15, "SIRCUPA": 10, "SIRCIP": 0}
    },
    "Mayo 2026": {
        "contexto": "Estabilización y consolidación de la demanda en la banda más alta registrada del año (~5.000 sesiones totales).",
        "foco": "Persistencia de dudas operativas en DDJJ e irrupción crítica del nuevo régimen local SIRCIP (tarjetas y medios de pago electrónicos), conviviendo directamente con las consultas de SIRCREB.",
        "keywords": {"DDJJ": 100, "Baja": 95, "Convenio": 90, "Alta": 85, "Sircip": 75, "Sircreb": 68},
        "sistemas": {"Convenio / Padrón": 30, "SIFERE / DDJJ": 30, "SIRCREB": 15, "SIRCUPA": 10, "SIRCIP": 15}
    }
}

# --- 4. INTERFAZ DE USUARIO (UI) ---
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_logo = os.path.join(ruta_actual, "comarb_logo.png")

col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    try:
        st.image(ruta_logo, use_container_width=True)
    except Exception:
        st.error("Logo no encontrado.")

with col_titulo:
    st.title("Dashboard Comarb - Actividad de Chatbot")
st.markdown("Análisis dinámico del tráfico, capacidad de contención automática y focos de demanda.")

# --- 5. CONTROLADOR GLOBAL (SIDEBAR) ---
st.sidebar.header("Filtro de Período")
opciones_filtro = ["Total Histórico Consolidado"] + list(insights_mes.keys())
periodo_seleccionado = st.sidebar.selectbox("Seleccionar Período a Diagnosticar:", opciones_filtro)

st.markdown("---")

# Paleta corporativa clara basada estrictamente en los tonos de Comarb
colores_sistemas = ["#00A4E4", "#1E3A8A", "#3B82F6", "#60A5FA", "#93C5FD"]
color_barra_principal = "#00A4E4"
color_linea_conversion = "#10B981"
color_linea_rebote = "#EF4444"

# --- LÓGICA VISTA A: TOTAL HISTÓRICO CONSOLIDADO ---
if periodo_seleccionado == "Total Histórico Consolidado":
    st.subheader("📈 Diagnóstico Macro y Evolución de demanda")
    
    # Cuadrícula expandida a 4 columnas para integrar el Promedio Mensual dinámico
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Pico Máximo Registrado", "4.999 Sesiones", "Mayo 2026")
    k2.metric("Promedio Mensual", f"{df['Sesiones_Brutas'].mean():.0f} Sesiones", "Línea de base operativa")
    k3.metric("Tasa de Conversión Promedio", f"{df['Tasa_Conversion'].mean():.2f}%", "Estabilidad del canal")
    k4.metric("Contención Automatizada Promedio", f"{100 - df['Tasa_Conversion'].mean():.2f}%", "Eficiencia de menús")
    
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Bar(x=df["Mes"], y=df["Sesiones_Brutas"], name="Tráfico Bruto (Sesiones)", marker_color=color_barra_principal))
    fig_hist.add_trace(go.Scatter(x=df["Mes"], y=df["Tasa_Conversion"], name="Tasa de Conversión (%)", yaxis="y2", line=dict(color=color_linea_conversion, width=3)))
    fig_hist.update_layout(
        title="Curva de crecimiento de demanda bruta y tasa de conversión a respuesta por fuera del Bot",
        yaxis=dict(
            title=dict(text="Volumen de Sesiones", font=dict(color="#0F172A")), 
            tickfont=dict(color="#0F172A")
        ),
        yaxis2=dict(
            title=dict(text="Tasa de Conversión (%)", font=dict(color="#0F172A")), 
            overlaying="y", 
            side="right", 
            tickfont=dict(color="#0F172A")
        ),
        template="plotly_white", height=400, legend=dict(x=0.01, y=0.99),
        font=dict(color="#0F172A")
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    col_izq_hist, col_der_hist = st.columns(2)
    
    with col_izq_hist:
        st.subheader("2. Análisis del Fenómeno de Rebote Incidental")
        df_rebote = df[df["Tasa_Rebote"] > 0]
        fig_rebote = px.line(df_rebote, x="Mes", y="Tasa_Rebote", text="Tasa_Rebote", title="Evolución del Rebote por Saturación Externa del Portal", template="plotly_white", markers=True)
        fig_rebote.update_traces(line_color=color_linea_rebote, line_width=3, textposition="top center")
        fig_rebote.update_layout(height=350, font=dict(color="#0F172A"))
        st.plotly_chart(fig_rebote, use_container_width=True)
        
    with col_der_hist:
        st.subheader("3. Share Global de Demandas por Sistema")
        sistemas_global = {"Convenio / Padrón": 0, "SIFERE / DDJJ": 0, "SIRCREB": 0, "SIRCUPA": 0, "SIRCIP": 0}
        for m in insights_mes:
            for sis in insights_mes[m]["sistemas"]:
                sistemas_global[sis] += insights_mes[m]["sistemas"][sis]
        
        df_sis_g = pd.DataFrame(list(sistemas_global.items()), columns=["Sistema", "Volumen_Relativo"])
        fig_pie_g = px.pie(df_sis_g, values="Volumen_Relativo", names="Sistema", hole=0.4, template="plotly_white", color_discrete_sequence=colores_sistemas)
        fig_pie_g.update_layout(height=350, legend=dict(orientation="h", y=-0.1), font=dict(color="#0F172A"))
        st.plotly_chart(fig_pie_g, use_container_width=True)
        
    vector_horas_total = [sum(perfiles_horarios[m][i] for m in perfiles_horarios) for i in range(24)]
    total_sesiones_historicas = df["Sesiones_Brutas"].sum()
    vector_dias_total = [int(total_sesiones_historicas * p) for p in porcentajes_semanales]

# --- LÓGICA VISTA B: CORTE MENSUAL ESPECÍFICO ---
else:
    st.subheader(f"🔍 Diagnóstico Avanzado — Período: {periodo_seleccionado}")
    
    info = insights_mes[periodo_seleccionado]
    datos_mes = df[df["Mes"] == periodo_seleccionado].iloc[0]
    
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Tráfico Bruto", f"{datos_mes['Sesiones_Brutas']} ses.")
    c2.metric("Usuarios Interactivos", f"{datos_mes['Usuarios_Interactivos']} ses.")
    c3.metric("Tasa de Rebote", f"{datos_mes['Tasa_Rebote']}%" if datos_mes['Tasa_Rebote'] > 0 else "N/D")
    c4.metric("Consultas Escritas", f"{datos_mes['Consultas_Escritas']} ses.")
    c5.metric("Tasa de Conversión", f"{datos_mes['Tasa_Conversion']:.2f}%")
    c6.metric("Contención Automatizada", f"{100 - datos_mes['Tasa_Conversion']:.2f}%")
    
    col_textos, col_g_kw, col_g_pie = st.columns([2, 2, 2])
    
    with col_textos:
        st.markdown("### 📌 Contexto de consulta")
        st.info(info["contexto"])
        st.markdown("### 🔍 Foco de Demanda")
        st.warning(info["foco"])
        
    with col_g_kw:
        st.markdown("### 📊 Palabras Clave Dominantes")
        df_kw = pd.DataFrame(list(info["keywords"].items()), columns=["Palabra", "Menciones"]).sort_values(by="Menciones", ascending=True)
        fig_kw = px.bar(df_kw, x="Menciones", y="Palabra", orientation="h", text="Menciones", template="plotly_white")
        fig_kw.update_traces(marker_color=color_barra_principal, textposition="outside")
        fig_kw.update_layout(showlegend=False, height=300, font=dict(color="#0F172A"))
        st.plotly_chart(fig_kw, use_container_width=True)
        
    with col_g_pie:
        st.markdown("### 🍩 Distribución por Sistema")
        df_sis_m = pd.DataFrame(list(info["sistemas"].items()), columns=["Sistema", "Distribución"])
        df_sis_m = df_sis_m[df_sis_m["Distribución"] > 0]
        fig_pie_m = px.pie(df_sis_m, values="Distribución", names="Sistema", hole=0.4, template="plotly_white", color_discrete_sequence=colores_sistemas)
        fig_pie_m.update_layout(height=300, showlegend=True, legend=dict(orientation="h", y=-0.1), font=dict(color="#0F172A"))
        st.plotly_chart(fig_pie_m, use_container_width=True)
        
    vector_horas_total = perfiles_horarios[periodo_seleccionado]
    vector_dias_total = [int(datos_mes["Sesiones_Brutas"] * p) for p in porcentajes_semanales]

# --- 6. MÓDULO INTERACTIVO DE PERFIL TEMPORAL DE CONSULTAS ---
st.sidebar.markdown("---")
st.markdown("### 📅 Análisis de Comportamiento y Hábitos del Contribuyente")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    df_horas = pd.DataFrame({"Hora": horas_eje, "Sesiones": vector_horas_total})
    fig_horas = px.area(df_horas, x="Hora", y="Sesiones", title=f"Distribución Horaria de Consultas ({periodo_seleccionado})", template="plotly_white")
    fig_horas.update_traces(line_color=color_barra_principal, fillcolor="rgba(0, 164, 228, 0.15)")
    fig_horas.update_layout(height=350, font=dict(color="#0F172A"))
    st.plotly_chart(fig_horas, use_container_width=True)

with col_graf2:
    df_dias = pd.DataFrame({"Día": dias_semana, "Sesiones": vector_dias_total})
    fig_dias = px.bar(df_dias, x="Día", y="Sesiones", title=f"Distribución por Día de la Semana ({periodo_seleccionado})", text="Sesiones", template="plotly_white")
    fig_dias.update_traces(marker_color="#10B981", textposition="outside")
    fig_dias.update_layout(height=350, font=dict(color="#0F172A"))
    st.plotly_chart(df_dias, use_container_width=True)

st.markdown("---")
st.caption("Dashboard de Monitoreo Analítico desarrollado bajo lineamientos de análisis de operaciones de canales automatizados.")