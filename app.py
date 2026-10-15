import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import plotly.io as pio

# Tipografía institucional para todos los gráficos Plotly
_tpl = pio.templates["plotly_white"]
_tpl.layout.font.family = "Helvetica Neue, Helvetica, Arial, sans-serif"
_tpl.layout.font.color = "#2D3748"

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Comarb - Actividad de Chatbot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INYECCIÓN DE CSS ESTILO INTEGRAL www.ca.gob.ar ---
st.markdown(
    """
    <style>
        /* Tipografía oficial */
        html, body, [class*="css"], .stMarkdown p {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            color: #2D3748 !important;
        }
        
        .stApp {
            background-color: #FFFFFF !important;
        }
        
        /* Barra lateral institucional */
        [data-testid="stSidebar"] {
            background-color: #F8FAFC !important;
            border-right: 1px solid #E2E8F0 !important;
        }
        
        /* Títulos en Azul Eléctrico (#0022c3) */
        [data-testid="stSidebar"] h2 {
            font-size: 1.1rem !important;
            color: #0022c3 !important;
            font-weight: 700 !important;
            margin-bottom: 0.5rem !important;
        }

        /* Rediseño de Tarjetas de Métrica */
        [data-testid="stMetricContainer"] {
            background-color: #F8FAFC !important;
            border: 1px solid #E2E8F0 !important;
            border-left: 4px solid #039ee2 !important; 
            padding: 1rem !important;
            border-radius: 4px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        }
        
        /* Etiquetas de KPI */
        [data-testid="stMetricLabel"] p {
            font-size: 0.82rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: #4A5568 !important;
            font-weight: 600 !important;
        }
        
        /* Números en Azul Eléctrico (#0022c3) */
        [data-testid="stMetricValue"] div {
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            color: #0022c3 !important;
        }

        /* Paneles de alerta con Contexto */
        .stElementContainer div[data-testid="stNotificationV2"]:has(div[data-testid="stHeading"] + div) {
            border-left-color: #039ee2 !important;
        }

        /* Paneles de alerta con Salmón Oficial (#ff7870) */
        div[data-testid="stAlert"] {
            background-color: #FFF5F5 !important;
            border: 1px solid #FED7D7 !important;
            border-left: 4px solid #ff7870 !important; 
            color: #2D3748 !important;
        }

        /* Estilo para el selector de meses */
        div[data-baseweb="select"] {
            font-size: 0.85rem !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 4px !important;
        }
        
        /* Línea divisoria principal en color Salmón Oficial */
        hr {
            margin: 1.5rem 0 !important;
            border: 0 !important;
            border-top: 2px solid #ff7870 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 1. BASE DE DATOS CRONOLÓGICA CONSOLIDADA ---
data_historica = {
    "Mes": ["Octubre 2025", "Noviembre 2025", "Diciembre 2025", "Enero 2026", "Febrero 2026", "Marzo 2026", "Abril 2026", "Mayo 2026", "Junio 2026", "Julio 2026", "Agosto 2026", "Septiembre 2026"],
    "Sesiones_Brutas": [2808, 2595, 1885, 2485, 2774, 4416, 4986, 4999, 5299, 4043, 4247, 4122],
    "Tasa_Conversion": [19.42, 24.82, 24.79, 25.84, 26.43, 25.27, 26.58, 25.69, 25.62, 26.11, 23.43, 23.63],
    "Usuarios_Interactivos": [2673, 2498, 1795, 2368, 2596, 2493, 2137, 2164, 2334, 1796, 1818, 1807],
    "Tasa_Rebote": [4.81, 3.74, 4.77, 4.71, 6.42, 43.55, 57.14, 56.71, 55.95, 55.58, 57.19, 56.16],
    "Consultas_Escritas": [519, 620, 445, 612, 686, 630, 568, 556, 598, 469, 426, 427]
}
df = pd.DataFrame(data_historica)

# --- 2. PERFILES DE DISTRIBUCIÓN TEMPORAL (UTC) ---
horas_eje = [f"{h:02d}:00" for h in range(24)]
perfiles_horarios = {
    "Octubre 2025": [76, 53, 65, 39, 21, 10, 15, 12, 13, 19, 51, 117, 198, 253, 318, 252, 190, 262, 222, 187, 148, 114, 84, 89],
    "Noviembre 2025": [59, 48, 40, 32, 18, 10, 14, 6, 8, 16, 18, 106, 190, 267, 385, 263, 191, 190, 210, 158, 114, 92, 83, 77],
    "Diciembre 2025": [50, 35, 33, 22, 15, 9, 3, 5, 3, 14, 34, 76, 133, 184, 217, 181, 142, 142, 150, 122, 96, 86, 72, 61],
    "Enero 2026": [60, 45, 38, 23, 20, 12, 11, 8, 6, 9, 28, 106, 192, 252, 245, 226, 191, 213, 212, 150, 150, 118, 95, 75],
    "Febrero 2026": [51, 43, 40, 29, 20, 14, 8, 5, 8, 13, 43, 126, 224, 263, 327, 252, 195, 238, 236, 182, 171, 99, 100, 87],
    "Marzo 2026": [92, 74, 44, 30, 26, 7, 4, 5, 4, 14, 50, 230, 415, 466, 517, 413, 307, 359, 366, 341, 254, 150, 151, 97],
    "Abril 2026": [94, 55, 59, 39, 24, 9, 7, 10, 6, 23, 59, 257, 440, 553, 537, 471, 350, 433, 452, 378, 299, 178, 141, 112],
    "Mayo 2026": [99, 63, 70, 44, 23, 21, 9, 3, 9, 27, 51, 253, 421, 535, 573, 467, 339, 410, 470, 379, 262, 172, 176, 123],
    "Junio 2026": [80, 69, 65, 37, 20, 10, 10, 5, 5, 20, 68, 261, 492, 587, 558, 523, 362, 402, 493, 414, 292, 207, 180, 139],
    "Julio 2026": [70, 60, 45, 41, 15, 12, 12, 6, 8, 21, 42, 192, 374, 451, 485, 401, 311, 319, 329, 261, 213, 148, 117, 110],
    "Agosto 2026": [91, 66, 46, 33, 26, 12, 10, 6, 7, 14, 44, 211, 414, 447, 499, 367, 279, 363, 360, 312, 243, 157, 129, 111],
    "Septiembre 2026": [70, 63, 51, 33, 16, 9, 4, 3, 3, 15, 45, 228, 406, 474, 473, 404, 250, 307, 373, 318, 223, 144, 112, 98]
}
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
porcentajes_semanales = [0.21, 0.22, 0.22, 0.20, 0.13, 0.015, 0.005]
# Conteos reales por día de la semana (sesiones brutas, UTC, lunes primero).
dias_semana_reales = {
    "Octubre 2025": [380, 410, 599, 732, 480, 115, 92],
    "Noviembre 2025": [528, 482, 419, 451, 474, 132, 109],
    "Diciembre 2025": [352, 433, 302, 306, 346, 90, 56],
    "Enero 2026": [456, 444, 412, 459, 510, 141, 63],
    "Febrero 2026": [361, 439, 560, 591, 603, 123, 97],
    "Marzo 2026": [736, 863, 837, 852, 841, 151, 136],
    "Abril 2026": [946, 918, 1127, 966, 734, 166, 129],
    "Mayo 2026": [799, 975, 909, 953, 981, 216, 166],
    "Junio 2026": [878, 1255, 1059, 928, 948, 151, 80],
    "Julio 2026": [720, 730, 836, 755, 749, 160, 93],
    "Agosto 2026": [852, 833, 777, 741, 775, 163, 106],
    "Septiembre 2026": [684, 906, 935, 705, 675, 138, 79]
}

# --- 3. DATOS CUALITATIVOS Y SISTEMAS ---
insights_mes = {
    "Octubre 2025": {
        "contexto": "Mes de mayor actividad del trimestre base, marcando el inicio del período de alta demanda previo al cierre de año.",
        "foco": "Consultas de rutina sobre el uso del chatbot e interacciones bajo niveles normales de operación corporativa.",
        "keywords": {"Baja": 85, "DDJJ": 68, "Convenio": 67, "Sircreb": 53, "Ingresos": 49, "Retenciones": 48, "Alta": 45},
        "sistemas": {"Otros": 12, "Convenio / Padrón": 20, "SIFERE / DDJJ": 24, "SIRCAR": 6, "SIRCREB": 20, "SIRCUPA": 18}
    },
    "Noviembre 2025": {
        "contexto": "Ligera disminución en el volumen bruto de consultas respecto a octubre, con una tasa de conversión de 24,82% (se incrementa frente a octubre).",
        "foco": "Consultas habituales de mantenimiento de padrón previas al cierre de ejercicio fiscal.",
        "keywords": {"DDJJ": 81, "Convenio": 77, "Baja": 74, "Sifere": 60, "Pago": 55, "Alta": 55, "Retenciones": 55},
        "sistemas": {"Otros": 11, "Convenio / Padrón": 14, "SIFERE / DDJJ": 36, "SIRCAR": 7, "SIRCREB": 16, "SIRCUPA": 16}
    },
    "Diciembre 2025": {
        "contexto": "Desaceleración estacional típica generalizada (-27% de tráfico bruto) provocada por los recesos vacacionales y las fiestas de fin de año.",
        "foco": "Urgencias administrativas de cierre fiscal. Reorganización empresarial (altas/bajas) y fuerte irrupción de consultas críticas sobre el sistema SIRCUPA.",
        "keywords": {"Baja": 59, "DDJJ": 53, "Alta": 51, "Convenio": 48, "Retenciones": 41, "Pago": 37, "Ingresos": 32},
        "sistemas": {"Otros": 14, "Convenio / Padrón": 17, "SIFERE / DDJJ": 28, "SIRCAR": 9, "SIRCREB": 20, "SIRCUPA": 12}
    },
    "Enero 2026": {
        "contexto": "Recuperación operativa post-receso de Año Nuevo (+31% de crecimiento bruto), marcando el fin de la estacionalidad de las fiestas.",
        "foco": "Reorganización fiscal típica de inicio de ciclo anual. Dominio absoluto de los trámites de alta y baja en el Convenio Multilateral y reclamos por retenciones indebidas (SIRCREB/SIRCUPA).",
        "keywords": {"Convenio": 103, "Baja": 99, "Multilateral": 72, "DDJJ": 68, "Alta": 62, "Ingresos": 58, "Brutos": 53},
        "sistemas": {"Otros": 13, "Convenio / Padrón": 22, "SIFERE / DDJJ": 29, "SIRCAR": 9, "SIRCREB": 17, "SIRCUPA": 10}
    },
    "Febrero 2026": {
        "contexto": "Reactivación plena del período comercial y administrativo, alcanzando el máximo volumen del cuatrimestre inicial (+11,6% de incremento respecto a enero).",
        "foco": "Foco crítico en el cierre del ejercicio fiscal: presentación de la DDJJ anual (CM03) en SIFERE Web. Se detectaron fuertes señales de alerta e inconvenientes técnicos externos (la palabra 'error' escaló al 4° lugar general).",
        "keywords": {"DDJJ": 140, "Baja": 93, "Convenio": 87, "Error": 83, "Ingresos": 67, "Actividad": 65, "Presentar": 64},
        "sistemas": {"Otros": 13, "Convenio / Padrón": 16, "SIFERE / DDJJ": 40, "SIRCAR": 7, "SIRCIP": 2, "SIRCREB": 14, "SIRCUPA": 8}
    },
    "Marzo 2026": {
        "contexto": "Explosión masiva de demanda impulsada por el calendario de vencimientos generales del Convenio Multilateral.",
        "foco": "Consultas complejas sobre reglas de atribución, jurisdicciones de alta y regímenes de recaudación. Disminución drástica de problemas de estabilidad técnica en sistemas.",
        "keywords": {"Convenio": 96, "DDJJ": 77, "Baja": 67, "Multilateral": 65, "Alta": 65, "Ingresos": 61, "Actividad": 57},
        "sistemas": {"Otros": 15, "Convenio / Padrón": 17, "SIFERE / DDJJ": 30, "SIRCAR": 7, "SIRCIP": 5, "SIRCREB": 18, "SIRCUPA": 8}
    },
    "Abril 2026": {
        "contexto": "Nuevo pico histórico de tráfico bruto en el canal. Inicio de un período masivo de regularización de contribuyentes.",
        "foco": "Trámites de padrón con paridad exacta entre altas y bajas (68 menciones c/u). Alta demanda de consultas sobre gestión y validación de CUIT y acceso digital al portal corporativo.",
        "keywords": {"Convenio": 69, "Alta": 68, "Baja": 68, "DDJJ": 56, "Retenciones": 50, "Sircreb": 49, "Multilateral": 47},
        "sistemas": {"Otros": 15, "Convenio / Padrón": 17, "SIFERE / DDJJ": 28, "SIRCAR": 7, "SIRCIP": 5, "SIRCREB": 20, "SIRCUPA": 8}
    },
    "Mayo 2026": {
        "contexto": "Estabilización y consolidación de la demanda en la banda más alta registrada del año (~5.000 sesiones totales).",
        "foco": "Persistencia de dudas operativas en DDJJ e irrupción crítica del nuevo régimen local SIRCIP (tarjetas y medios de pago electrónicos), conviviendo directamente con las consultas de SIRCREB.",
        "keywords": {"DDJJ": 70, "Baja": 65, "Convenio": 65, "Alta": 62, "Sircip": 53, "Sircreb": 51, "Ingresos": 50},
        "sistemas": {"Otros": 11, "Convenio / Padrón": 14, "SIFERE / DDJJ": 30, "SIRCAR": 7, "SIRCIP": 11, "SIRCREB": 19, "SIRCUPA": 8}
    },
    "Junio 2026": {
        "contexto": "Cierre del primer semestre consolidando el pico histórico de demanda del canal con casi 5.300 sesiones brutas ingresadas.",
        "foco": "Urgencia de liquidación de obligaciones anuales combinada con los trámites de rutina fiscal, dominando las consultas sobre DDJJ, ingresos y presentaciones.",
        "keywords": {"DDJJ": 73, "Baja": 61, "Convenio": 59, "Ingresos": 55, "Retenciones": 53, "Alta": 49, "Multilateral": 47},
        "sistemas": {"Otros": 11, "Convenio / Padrón": 15, "SIFERE / DDJJ": 31, "SIRCAR": 6, "SIRCIP": 10, "SIRCREB": 17, "SIRCUPA": 10}
    },
    "Julio 2026": {
        "contexto": "Disminución del tráfico tras los picos estacionales de vencimientos. Recientes interacciones del sistema muestran pruebas de QA activas para el SUMA BOT.",
        "foco": "Identificación de CUIT y validación de registros dentro del padrón federal, observándose un peso relativo alto en consultas sobre retenciones bancarias.",
        "keywords": {"Baja": 72, "Alta": 58, "DDJJ": 55, "Convenio": 47, "Sircreb": 46, "Pago": 38, "Multilateral": 34},
        "sistemas": {"Otros": 13, "Convenio / Padrón": 15, "SIFERE / DDJJ": 29, "SIRCAR": 6, "SIRCIP": 3, "SIRCREB": 20, "SIRCUPA": 14}
    },
    "Agosto 2026": {
        "contexto": "Recuperación leve del volumen bruto post-ferias de julio (4.247 sesiones). Se logró la tasa de contención automatizada más eficiente del semestre, alcanzando el 76,57%.",
        "foco": "Prevalencia equilibrada entre los trámites de DDJJ en SIFERE y retenciones de SIRCREB, acompañados de un volumen masivo de gestión de Padrón (altas y bajas de contribuyentes).",
        "keywords": {"Baja": 64, "Convenio": 53, "Alta": 48, "DDJJ": 47, "Sircreb": 43, "Retenciones": 39, "Multilateral": 37},
        "sistemas": {"Otros": 13, "Convenio / Padrón": 19, "SIFERE / DDJJ": 25, "SIRCAR": 8, "SIRCIP": 5, "SIRCREB": 22, "SIRCUPA": 8}
    },
    "Septiembre 2026": {
        "contexto": "Caída leve del tráfico bruto (4.122 sesiones, -2,9% frente a agosto), con la demanda concentrada de lunes a viernes. Conversión a consulta estable (23,63%) y contención automatizada del 76,37%.",
        "foco": "Trámites de padrón (baja, convenio, alta) y consultas sobre retenciones bancarias de SIRCREB, con presencia constante de DDJJ y Convenio Multilateral. SIRCAR aparece como sistema demandado (9%).",
        "keywords": {"Baja": 68, "Convenio": 54, "Alta": 50, "Sircreb": 41, "DDJJ": 38, "Multilateral": 37, "Retenciones": 33},
        "sistemas": {"Otros": 14, "Convenio / Padrón": 16, "SIFERE / DDJJ": 23, "SIRCAR": 9, "SIRCIP": 7, "SIRCREB": 24, "SIRCUPA": 7}
    }
}


# --- 4. UI ---
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_logo = os.path.join(ruta_actual, "comarb_logo.png")

col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    try:
        st.image(ruta_logo, width="stretch")
    except Exception:
        st.error("Logo no encontrado.")

with col_titulo:
    st.title("Dashboard Comarb - Actividad de Chatbot")
st.markdown("Análisis dinámico del tráfico, contención y focos de demanda bajo lineamientos institucionales.")

# --- 5. CONTROLADOR GLOBAL ---
periodo_seleccionado = st.sidebar.selectbox("Seleccionar Período a Diagnosticar:", ["Total Histórico Consolidado"] + list(insights_mes.keys()))

st.markdown("---")

# Paleta ca.gob.ar Oficial definitiva
colores_sistemas = ["#039ee2", "#0022c3", "#1E3A8A", "#60A5FA", "#93C5FD"]
color_sistema_map = {
    "SIRCREB": "#0022c3",
    "SIFERE / DDJJ": "#039ee2",
    "Convenio / Padrón": "#1E3A8A",
    "SIRCAR": "#60A5FA",
    "SIRCIP": "#93C5FD",
    "SIRCUPA": "#ff7870",
    "Otros": "#A0AEC0",
}
color_barra_principal = "#039ee2"
color_linea_conversion = "#ff7870"
color_linea_rebote = "#0022c3"

# --- LÓGICA VISTA A: TOTAL HISTÓRICO CONSOLIDADO ---
if periodo_seleccionado == "Total Histórico Consolidado":
    st.subheader("Diagnóstico Macro y Evolución de demanda")
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Pico Máximo Registrado", f"{df['Sesiones_Brutas'].max():.0f} Sesiones")
    k2.metric("Promedio Mensual", f"{df['Sesiones_Brutas'].mean():.0f} Sesiones")
    k3.metric("Tasa de Conversión Promedio", f"{df['Tasa_Conversion'].mean():.2f}%")
    k4.metric("Contención Automatizada Promedio", f"{100 - df['Tasa_Conversion'].mean():.2f}%")
    
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Bar(x=df["Mes"], y=df["Sesiones_Brutas"], name="Tráfico Bruto", marker_color=color_barra_principal))
    fig_hist.add_trace(go.Scatter(x=df["Mes"], y=df["Tasa_Conversion"], name="Conversión (%)", yaxis="y2", line=dict(color=color_linea_conversion, width=3)))
    fig_hist.update_layout(
        title="Crecimiento de demanda bruta y tasa de conversión",
        yaxis=dict(title=dict(text="Sesiones", font=dict(color="#2D3748")), tickfont=dict(color="#2D3748")),
        yaxis2=dict(title=dict(text="Tasa de Conversión (%)", font=dict(color="#2D3748")), overlaying="y", side="right", tickfont=dict(color="#2D3748")),
        template="plotly_white", height=400, legend=dict(x=0.01, y=0.99), font=dict(color="#2D3748")
    )
    st.plotly_chart(fig_hist, width="stretch")
    
    col_izq_hist, col_der_hist = st.columns(2)
    with col_izq_hist:
        st.subheader("2. Rebote Incidental (Portal)")
        df_rebote = df[df["Tasa_Rebote"] > 0]
        fig_rebote = px.line(df_rebote, x="Mes", y="Tasa_Rebote", text="Tasa_Rebote", title="Evolución del Rebote", template="plotly_white", markers=True)
        fig_rebote.update_traces(line_color=color_linea_rebote, line_width=3, textposition="top center")
        fig_rebote.update_layout(height=350)
        st.plotly_chart(fig_rebote, width="stretch")
        
    with col_der_hist:
        st.subheader("3. Share de Demandas por Sistema")
        sistemas_global = {}
        for m in insights_mes:
            for sis, val in insights_mes[m]["sistemas"].items():
                sistemas_global[sis] = sistemas_global.get(sis, 0) + val
        df_sis_g = pd.DataFrame(list(sistemas_global.items()), columns=["Sistema", "Volumen"])
        fig_pie_g = px.pie(df_sis_g, values="Volumen", names="Sistema", hole=0.4, template="plotly_white", color="Sistema", color_discrete_map=color_sistema_map)
        fig_pie_g.update_traces(textinfo="label+percent", textposition="outside")
        fig_pie_g.update_layout(height=350, showlegend=False, margin=dict(l=10, r=10, t=30, b=30))
        st.plotly_chart(fig_pie_g, width="stretch")
        
    vector_horas_total = [sum(perfiles_horarios[m][i] for m in perfiles_horarios) for i in range(24)]
    vector_dias_total = [int(df["Sesiones_Brutas"].sum() * p) for p in porcentajes_semanales]

# --- LÓGICA VISTA B: CORTE MENSUAL ---
else:
    st.subheader(f"Diagnóstico Avanzado — Período: {periodo_seleccionado}")
    datos_mes = df[df["Mes"] == periodo_seleccionado].iloc[0]
    info = insights_mes[periodo_seleccionado]
    
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Tráfico Bruto", f"{datos_mes['Sesiones_Brutas']} ses.")
    c2.metric("Usuarios Interactivos", f"{datos_mes['Usuarios_Interactivos']} ses.")
    c3.metric("Tasa de Rebote", f"{datos_mes['Tasa_Rebote']}%" if datos_mes['Tasa_Rebote'] > 0 else "N/D")
    c4.metric("Consultas Escritas", f"{datos_mes['Consultas_Escritas']} ses.")
    c5.metric("Tasa de Conversión", f"{datos_mes['Tasa_Conversion']:.2f}%")
    c6.metric("Contención Automatizada", f"{100 - datos_mes['Tasa_Conversion']:.2f}%")
    
    col_textos, col_g_kw, col_g_pie = st.columns([2, 2, 2])
    with col_textos:
        st.markdown("### Contexto de consulta")
        st.info(info["contexto"])
        st.markdown("### Foco de Demanda")
        st.warning(info["foco"])
    with col_g_kw:
        st.markdown("### Palabras Dominantes")
        df_kw = pd.DataFrame(list(info["keywords"].items()), columns=["Palabra", "Menciones"]).sort_values(by="Menciones", ascending=True)
        fig_kw = px.bar(df_kw, x="Menciones", y="Palabra", orientation="h", text="Menciones", template="plotly_white", color_discrete_sequence=[color_barra_principal])
        fig_kw.update_layout(showlegend=False, height=300, margin=dict(l=10, r=30, t=10, b=10))
        st.plotly_chart(fig_kw, width="stretch")
    with col_g_pie:
        st.markdown("### Por Sistema")
        df_sis_m = pd.DataFrame(list(info["sistemas"].items()), columns=["Sistema", "Dist"]).query("Dist > 0")
        fig_pie_m = px.pie(df_sis_m, values="Dist", names="Sistema", hole=0.4, template="plotly_white", color="Sistema", color_discrete_map=color_sistema_map)
        fig_pie_m.update_traces(textinfo="label+percent", textposition="outside")
        fig_pie_m.update_layout(height=300, showlegend=False, margin=dict(l=10, r=10, t=30, b=30))
        st.plotly_chart(fig_pie_m, width="stretch")
        
    vector_horas_total = perfiles_horarios[periodo_seleccionado]
    if periodo_seleccionado in dias_semana_reales:
        vector_dias_total = dias_semana_reales[periodo_seleccionado]
    else:
        vector_dias_total = [int(datos_mes["Sesiones_Brutas"] * p) for p in porcentajes_semanales]

# --- 6. ANÁLISIS TEMPORAL ---
st.markdown("### Análisis de Comportamiento y Hábitos del Contribuyente")
col_graf1, col_graf2 = st.columns(2)
with col_graf1:
    df_horas = pd.DataFrame({"Hora": horas_eje, "Sesiones": vector_horas_total})
    fig_horas = px.area(df_horas, x="Hora", y="Sesiones", title=f"Distribución Horaria en UTC ({periodo_seleccionado})", template="plotly_white")
    fig_horas.update_traces(line_color=color_barra_principal, fillcolor="rgba(3, 158, 226, 0.15)")
    st.plotly_chart(fig_horas, width="stretch")
with col_graf2:
    df_dias = pd.DataFrame({"Día": dias_semana, "Sesiones": vector_dias_total})
    fig_dias = px.bar(df_dias, x="Día", y="Sesiones", title=f"Distribución Semanal ({periodo_seleccionado})", text="Sesiones", template="plotly_white")
    fig_dias.update_traces(marker_color="#039ee2", textposition="outside")
    st.plotly_chart(fig_dias, width="stretch")

st.markdown("---")
st.caption("Dashboard de Monitoreo desarrollado bajo lineamientos institucionales ca.gob.ar.")