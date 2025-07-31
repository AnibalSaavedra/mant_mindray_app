import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

st.set_page_config(page_title="🛠️ Registro de Mantenimiento Diario - MINDRAY", page_icon="🧼", layout="centered")
st.title("🛠️ Registro de Mantenimiento Diario - MINDRAY")

EXCEL_FILE = "mant_mindray_registros.xlsx"
RESPALDO_FOLDER = "respaldos"
os.makedirs(RESPALDO_FOLDER, exist_ok=True)

# Cargar o crear DataFrame
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=[
        "Fecha y Hora", "Actividad", "Operador"
    ])

# Formulario
with st.form("registro_mindray"):
    fecha_hora = st.text_input("📅 Fecha y Hora", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    actividad = st.selectbox("🔧 Actividad Realizada", [
        "Eliminacion de Desechos", "Limpieza Sonda de Muestra", "Ab Limp Electrica", "Desobs",
        "Baño WBC", "Baño RBC", "Baño DIFF", "Camara de flujo", "Sonda Muestra"
    ])
    operador = st.selectbox("👤 Operador", [
        "Anibal Saavedra", "Juan Ramos", "Nycole Farias", "Stefanie Maureira", "Maria J.Vera",
        "Felipe Fernandez", "Paula Gutierrez", "Paola Araya", "Maria Rodriguez", "Pamela Montenegro"
    ])
    submit = st.form_submit_button("✅ Guardar Registro")

    if submit:
        nueva_fila = {
            "Fecha y Hora": fecha_hora,
            "Actividad": actividad,
            "Operador": operador
        }
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        st.success("✅ Registro guardado correctamente.")

        # respaldo automático
        fecha_backup = datetime.now().strftime("%Y%m%d_%H%M%S")
        respaldo_path = os.path.join(RESPALDO_FOLDER, f"backup_{fecha_backup}.xlsx")
        df.to_excel(respaldo_path, index=False)

# Filtro por mes
st.markdown("### 🔍 Buscar registros por mes")
if not df.empty:
    df["Fecha_Mes"] = pd.to_datetime(df["Fecha y Hora"]).dt.to_period("M").astype(str)
    meses = sorted(df["Fecha_Mes"].unique())
    mes_seleccionado = st.selectbox("📆 Mes", meses)
    df_filtrado = df[df["Fecha_Mes"] == mes_seleccionado]
    st.dataframe(df_filtrado.drop(columns=["Fecha_Mes"]), use_container_width=True)

    # Descargar registros filtrados
    def to_excel_memory(dataframe):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            dataframe.to_excel(writer, index=False)
        return output.getvalue()

    excel_bytes = to_excel_memory(df_filtrado.drop(columns=["Fecha_Mes"]))

    st.download_button(
        label="📥 Descargar Registros Filtrados",
        data=excel_bytes,
        file_name=f"mant_mindray_{mes_seleccionado}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("📭 No hay registros disponibles.")