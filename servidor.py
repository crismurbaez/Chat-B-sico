import socket
import sqlite3
from datetime import datetime
import sys

# Configuración del servidor TCP/IP
HOST = "127.0.0.1"  # localhost
PORT = 5000         # Puerto requerido por la consigna
DB_NAME = "chat.db"

# ==========================================
# Inicio la Base de Datos
# ==========================================
def inicializar_db(db_name=DB_NAME):
    """
    Crea la base de datos SQLite y la tabla 'mensajes' si no existe.
    Campos: id, contenido, fecha_envio, ip_cliente.
    Maneja errores si la base de datos no es accesible.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print(f"[DB] Base de datos '{db_name}' inicializada correctamente.")
    except sqlite3.Error as e:
        print(f"[ERROR DB] No se pudo acceder o inicializar la base de datos: {e}")
        sys.exit(1)

# ==========================================
# Guardo el Mensaje en la Base de Datos
# ==========================================
def guardar_mensaje(contenido, ip_cliente, db_name=DB_NAME):
    """
    Inserta un mensaje recibido en la base de datos SQLite.
    Retorna el timestamp formateado en caso de éxito, o None si ocurre un error.
    """
    try:
        fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
            (contenido, fecha_envio, str(ip_cliente))
        )
        conn.commit()
        conn.close()
        return fecha_envio
    except sqlite3.Error as e:
        print(f"[ERROR DB] Error al guardar el mensaje en la BD: {e}")
        return None

# ==========================================
# Inicializo el Socket Servidor
# ==========================================
def inicializar_socket(host=HOST, port=PORT):
    """
    Crea, configura y vincula el socket TCP/IP en localhost:5000.
    Maneja el error de puerto ocupado u OSError.
    """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Permite reutilizar la dirección local si el servidor se reinicia rápidamente
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[SERVIDOR] Servidor escuchando en {host}:{port}...")
        return server_socket
    except OSError as e:
        print(f"[ERROR SOCKET] No se pudo iniciar el socket en {host}:{port}. Puerto ocupado o inaccesible: {e}")
        sys.exit(1)

# ==========================================
# Acepta Conexiones y Procesa Mensajes
# ==========================================
def aceptar_y_procesar(server_socket):
    """
    Acepta conexiones entrantes de clientes, procesa sus mensajes en bucle
    y responde con: 'Mensaje recibido: <timestamp>'.
    """
    try:
        while True:
            conn, addr = server_socket.accept()
            ip_cliente = addr
            print(f"[CONEXIÓN] Cliente conectado desde {addr}")

            with conn:
                while True:
                    datos = conn.recv(1024)
                    if not datos:
                        print(f"[DESCONEXIÓN] Cliente {addr} finalizó la conexión.")
                        break

                    mensaje = datos.decode("utf-8")
                    print(f"[MENSAJE RECOGIDO] De {ip_cliente}: '{mensaje}'")

                    # Persistencia en BD
                    timestamp = guardar_mensaje(mensaje, ip_cliente)

                    if timestamp:
                        respuesta = f"Mensaje recibido: {timestamp}"
                    else:
                        respuesta = "Error: No se pudo almacenar el mensaje en el servidor."

                    conn.sendall(respuesta.encode("utf-8"))
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Deteniendo el servidor de forma segura...")
    finally:
        server_socket.close()

# ==========================================
# Inicio del programa
# ==========================================
if __name__ == "__main__":
    # Inicio la Base de Datos
    inicializar_db()
    # Inicio el Socket
    sock = inicializar_socket()
    # Proceso los mensajes
    aceptar_y_procesar(sock)
