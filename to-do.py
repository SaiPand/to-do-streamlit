import streamlit as st
import mysql.connector
from mysql.connector import Error
import time


###### Configuration de MySQL #######


def conectar_db():
    try:
        conn = mysql.connector.connect(
            host=st.secrets.connections.mysql.host,
            port=st.secrets.connections.mysql.port,
            database=st.secrets.connections.mysql.database,
            user=st.secrets.connections.mysql.username,
            password=st.secrets.connections.mysql.password,
        )
        return conn
    except Error as e:
        st.error(f"Error de conexion: {e}")
        return None


#### CRUD ###
def obtener():
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tareas")
        tareas = cursor.fetchall()
        conn.close()
        return tareas
    return []


def agregar(texto):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tarea (texto) VALUES (%s)", (texto,))
        conn.commit()
        conn.close()
        return True
    return False


def actualizar(id, texto):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tarea SET texto=%s WHERE id=%s", (texto, id))
        conn.commit()
        conn.close()
        return True
    return False


def eliminar(id):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tarea WHERE id=%s", (id,))
        conn.commit()
        conn.close()
        return True
    return False


## Codigo ##
def page2():
    st.title("_Lista de tarea_")


pg = st.navigation(
    [
        st.Page(page2, title="To-Do", icon=":material/favorite:"),
    ]
)
pg.run()


if "tarea" not in st.session_state:
    st.session_state.tareas = obtener()

with st.form("formulario_agregar_texto"):
    nuevo_texto = st.text_input("", placeholder="Escribe tu siguiente tarea")
    if st.form_submit_button("_Agregar_", type="secondary"):
        if nuevo_texto:
            agregar(nuevo_texto)
            st.session_state.tareas = obtener()
            st.toast("Tarea agregar")
            time.sleep(0.5)
        else:
            st.toast("Debes introducir una tarea", icon="🚨")
            time.sleep(0.5)
    else:
        pass


for i, tarea in enumerate(st.session_state.tareas):

    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        check = st.checkbox(tarea[1], key=f"check_{tarea[0]}")
    with col2:
        with st.popover(f"✍️ Edictar {tarea[1]}"):
            nuevo_texto = st.text_input(
                "Texto", value=tarea[1], key=f"edictar_{tarea[0]}"
            )
            if st.button("💾 Guardar Cambio", key=f"guardar_{tarea[0]}"):
                if actualizar(tarea[0], nuevo_texto):
                    st.session_state.tareas = obtener()
                    st.success("Tarea actualizada")
                else:
                    st.error("Error al actualizar")

                # st.session_state.anadir_tarea[i] = nuevo_texto
                # st.toast("Tarea actualizada", icon="✅")
                # time.sleep(0)

    with col3:
        if st.button("🗑️ Borrar", key=f"del_{tarea[0]}"):
            if eliminar(tarea[0]):
                st.session_state.tareas = obtener()
                st.success("Tarea eliminada")
            else:
                st.error("Error al eliminar")

bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://as1.ftcdn.net/jpg/02/74/70/20/1000_F_274702029_dC9sFwkI5xpuHuHvGFcma0zmYTSrE16i.webp");
background-size: cover;
}
[data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
}
.caption-style{
    color: black;
    text-align: justify;
    font-size: 20px;
}
.prediction-style{
    color: black;
    text-align: justify;
    font-size: 20px;
}

.description-style{
    color: black;
    text-align: justify;
    font-size: 20px;
}

.block-container {
    background-color: #FAFAFA;
    margin: 25px;
    border: 2px solid grey;
    border-radius: 25px;
    padding-top: 25px;
}


</style>
"""
st.markdown(bg_img, unsafe_allow_html=True)
