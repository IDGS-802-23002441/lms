import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import re

# URL de tu API desplegada en MonsterASP
API_URL = "https://lmsidgs902.runasp.net/api/sensores"

def formatear_fecha(fecha_raw):
    """
    Intenta limpiar y formatear la fecha recibida para que sea legible.
    Soporta formato ISO o timestamps numéricos largos.
    """
    if not fecha_raw:
        return "-"
    
    # Si la fecha viene como string pero contiene un timestamp largo ej: "1780001501312 (ISO...)"
    # Extraemos solo los dígitos del inicio
    match_timestamp = re.match(r"^(\d+)", str(fecha_raw).strip())
    
    if match_timestamp:
        try:
            # Los timestamps de JS/Mongo vienen en milisegundos, pasamos a segundos (/1000)
            ms = int(match_timestamp.group(1))
            dt = datetime.fromtimestamp(ms / 1000.0)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass

    # Si no es numérico, intentamos tratarlo como texto ISO directo limpiando paréntesis
    try:
        texto_limpio = str(fecha_raw).split('(')[-1].replace(')', '').strip()
        # Cortamos microsegundos/zonas horarias si existen para parseo simple
        if 'T' in texto_limpio:
            texto_limpio = texto_limpio.split('.')[0].replace('T', ' ')
            return texto_limpio
    except Exception:
        pass

    return str(fecha_raw)

def consultar_datos():
    # Limpiar tabla antes de cargar nuevos datos
    for fila in tabla.get_children():
        tabla.delete(fila)
        
    try:
        # Petición GET a la API de .NET
        respuesta = requests.get(API_URL, timeout=10)
        
        if respuesta.status_code == 200:
            lecturas = respuesta.json()
            for lectura in lecturas:
                # Se extraen los datos como strings sin asumir tipos numéricos para el ID
                id_sensor = str(lectura.get("id", "")) or str(lectura.get("_id", "-"))
                sensor_name = lectura.get("sensor", "-")
                valor_sensor = lectura.get("valor", 0.0)
                fecha_raw = lectura.get("fecha", "-")
                
                # Formatear el valor decimal de manera segura
                try:
                    valor_formateado = f"{float(valor_sensor):.2f}"
                except (ValueError, TypeError):
                    valor_formateado = str(valor_sensor)

                # Formatear la fecha
                fecha_formateada = formatear_fecha(fecha_raw)

                # Insertar en la tabla visual
                tabla.insert("", "end", values=(
                    id_sensor,
                    sensor_name,
                    valor_formateado,
                    fecha_formateada
                ))
        else:
            messagebox.showerror("Error", f"Error de servidor: {respuesta.status_code}")
            
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la API:\n{e}")

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Monitoreo de Sensores - LMS")
ventana.geometry("750x450") # Un poco más ancha para desplegar bien los IDs largos

# Botón de actualización
btn_actualizar = tk.Button(ventana, text="Consultar Base de Datos", command=consultar_datos, bg="#0078D4", fg="white", font=("Arial", 10, "bold"))
btn_actualizar.pack(pady=10)

# Contenedor para la tabla
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

# Definición de columnas de la tabla
columnas = ("ID", "Sensor", "Valor", "Fecha/Hora")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

# Ajuste de anchos para dar espacio a los hashes de ID y fechas largas
tabla.heading("ID", text="ID Registro")
tabla.column("ID", width=220, anchor="w") # Alineado a la izquierda por longitud del ID

tabla.heading("Sensor", text="Sensor")
tabla.column("Sensor", width=100, anchor="center")

tabla.heading("Valor", text="Valor")
tabla.column("Valor", width=80, anchor="center")

tabla.heading("Fecha/Hora", text="Fecha/Hora")
tabla.column("Fecha/Hora", width=180, anchor="center")

# Barra de desplazamiento
scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scroll.set)

tabla.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

# Carga inicial automática
consultar_datos()

ventana.mainloop()
