import socket
import sys

# Configuración de conexión al servidor
HOST = "127.0.0.1"  # localhost
PORT = 5000         # Puerto del servidor

def ejecutar_cliente(host=HOST, port=PORT):
    """
    Cliente TCP/IP que se conecta al servidor en localhost:5000,
    envía mensajes continuos y finaliza al escribir 'éxito'.
    """
    try:
        # Configuración del socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"[CLIENTE] Conectado exitosamente al servidor en {host}:{port}")
        print("Escriba sus mensajes. Para finalizar la sesión, ingrese 'éxito'.\n")

        while True:
            mensaje = input("Ingrese mensaje: ")

            # Condición de salida estipulada en la consigna
            if mensaje.strip().lower() == "éxito":
                print("[CLIENTE] Finalizando sesión de chat...")
                break

            if not mensaje.strip():
                continue

            # Enviar mensaje al servidor
            client_socket.sendall(mensaje.encode("utf-8"))

            # Recibir la respuesta de confirmación del servidor
            respuesta = client_socket.recv(1024).decode("utf-8")
            print(f"[RESPUESTA DEL SERVIDOR]: {respuesta}\n")

    except ConnectionRefusedError:
        print(f"[ERROR CONEXIÓN] No se pudo conectar al servidor en {host}:{port}. Verifique que el servidor esté ejecutándose.")
    except Exception as e:
        print(f"[ERROR CLIENTE] Ocurrió un error inesperado: {e}")
    finally:
        client_socket.close()
        print("[CLIENTE] Conexión cerrada.")

if __name__ == "__main__":
    ejecutar_cliente()

