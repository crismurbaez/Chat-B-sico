# Chat Básico Cliente-Servidor con Sockets y SQLite

\## 📌 Información General - \*\*Materia:\*\* Programación sobre Redes - \*\*Estudiante:\*\* [Tu Nombre y Apellido] - \*\*Profesor:\*\* [Nombre del Profesor] - \*\*Cátedra / Comisión:\*\* [Número de Comisión o Universidad] - \*\*Año:\*\* 2026

Este proyecto es una implementación en Python de una arquitectura **Cliente-Servidor** utilizando sockets TCP/IP, concurrencia mediante hilos (`threading`) y almacenamiento persistente en una base de datos **SQLite3**.

## 🚀 Características
- **Servidor TCP (`servidor.py`):** Escucha en `localhost:5000`, gestiona conexiones concurrentes de múltiples clientes, almacena cada mensaje recibido en la base de datos `chat.db` y responde con una confirmación con *timestamp*.
- **Cliente TCP (`cliente.py`):** Permite enviar mensajes continuos al servidor e interactuar por consola hasta enviar la palabra clave `éxito`.
- **Base de Datos SQLite (`chat.db`):** Persiste los campos `id`, `contenido`, `fecha_envio` e `ip_cliente`.
- **Manejo de Errores:** Captura excepciones de sockets (puerto ocupado) y de base de datos.

## 📋 Requisitos
- Python 3.8 o superior.
- No requiere instalar dependencias externas (utiliza la biblioteca estándar de Python).

## 🛠️ Ejecución Local

### Paso 1: Iniciar el Servidor
Abre una terminal y ejecuta:
```bash
python3 servidor.py
```
*El servidor creará la base de datos `chat.db` (si no existe) y quedará a la espera de conexiones en `127.0.0.1:5000`.*

### Paso 2: Iniciar el Cliente
Abre **otra terminal distinta** y ejecuta:
```bash
python3 cliente.py
```

### Paso 3: Probar la comunicación
1. Escribe mensajes desde el cliente y presiona `Enter`. Verás la confirmación devuelta por el servidor con la fecha y hora.
2. Para finalizar la conexión del cliente, escribe `éxito`.

---

## 🗄️ Verificación de la Base de Datos
Puedes consultar los mensajes almacenados en la base de datos usando SQLite desde la consola:

```bash
sqlite3 chat.db "SELECT * FROM mensajes;"
```
