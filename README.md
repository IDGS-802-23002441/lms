# Sistema de Monitoreo de Sensores (LMS)

Este proyecto es un sistema integral de monitoreo de sensores compuesto por tres componentes principales:

- **Backend (.NET)**: API REST que gestiona y almacena lecturas de sensores
- **Firmware (C++)**: Código para ESP32 que recopila datos de sensores
- **Ejecutable (Python)**: Aplicación cliente de Windows que interactúa con el sistema

---

## 📋 Componentes

### 1. ApiSensores - Backend .NET

Backend desarrollado en **ASP.NET Core 9.0** que proporciona una API REST para gestionar sensores y sus lecturas.

#### Requisitos
- .NET 9.0 SDK
- Base de datos (configurar en `appsettings.json`)

#### Estructura
```
ApiSensores/
├── Program.cs              # Configuración principal
├── Controller/
│   └── SensoresController.cs   # Endpoints de la API
├── Models/
│   └── Lectura.cs          # Modelo de datos
├── Data/
│   └── AppDbContext.cs     # Contexto de base de datos
├── appsettings.json        # Configuración
└── ApiSensores.csproj      # Proyecto
```

#### Compilación
```bash
cd ApiSensores
dotnet build
```

#### Ejecución (Desarrollo)
```bash
cd ApiSensores
dotnet run
```
La API estará disponible en `https://localhost:5001` o `http://localhost:5000`

#### Ejecución (Producción)
```bash
cd ApiSensores
dotnet publish -c Release
# Los archivos compilados estarán en: bin/Release/net9.0/publish/
```

#### Endpoints Disponibles
- `GET /api/sensores` - Obtener lista de sensores
- `GET /api/sensores/{id}` - Obtener sensor específico
- `GET /api/sensores/{id}/lecturas` - Obtener lecturas de un sensor
- `POST /api/sensores` - Crear nuevo sensor
- `POST /api/lecturas` - Registrar nueva lectura

#### Configuración
Editar `appsettings.Development.json` para desarrollo:
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    }
  },
  "ConnectionStrings": {
    "DefaultConnection": "tu_conexion_sql_aqui"
  }
}
```

---

### 2. Sketch ESP32 - Firmware C++

Código Arduino para la placa **ESP32** que recopila datos de sensores y los envía al backend.

#### Requisitos
- Arduino IDE o PlatformIO
- Librerías necesarias (ver en el sketch)

#### Estructura
```
sketch_may22a/
└── sketch_may22a.ino   # Código principal del ESP32
```

#### Compilación y Carga

**Opción 1: Con Arduino IDE**
1. Abrir Arduino IDE
2. Ir a `Archivo → Abrir` y seleccionar `sketch_may22a.ino`
3. Seleccionar placa: `Herramientas → Placa → ESP32 DEV MODULE`
4. Seleccionar puerto: `Herramientas → Puerto → [Tu puerto COM]`
5. Presionar `Subir` (Upload) o `Ctrl + U`

**Opción 2: Con PlatformIO**
```bash
cd sketch_may22a
platformio run --target upload
```

#### Configuración
Editar el archivo `sketch_may22a.ino` para:
- Configurar credenciales WiFi
- Establecer la URL del backend
- Ajustar intervalos de lectura

---

### 3. Ejecutable Python - Cliente Windows

Aplicación Python que actúa como cliente de Windows para interactuar con el sistema.

#### Requisitos
- Python 3.8 o superior
- Librerías: `requests`, `tkinter` (incluido en Python)

#### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

Si no existe `requirements.txt`, instalar manualmente:
```bash
pip install requests
```

#### Ejecución
```bash
python ejecutable.py
```

#### Funcionalidades
- Visualizar sensores disponibles
- Consultar lecturas históricas
- Registrar nuevas lecturas
- Configurar parámetros del sistema

---

## 🚀 Inicio Rápido

### 1. Iniciar el Backend
```bash
cd ApiSensores
dotnet run
```

### 2. Programar el ESP32
```bash
# Usar Arduino IDE siguiendo los pasos en la sección de Sketch ESP32
```

### 3. Ejecutar Cliente Python
```bash
python ejecutable.py
```

---

## 📋 Flujo de Datos

```
ESP32 (Sensores)
    ↓
API REST (.NET)
    ↓
Base de Datos
    ↑
Cliente Python (Windows)
```

1. El **ESP32** recopila datos de sensores
2. Envía los datos a la **API REST**
3. La API almacena en la **Base de Datos**
4. El **cliente Python** consulta y visualiza los datos

---

## 🔧 Desarrollo

### Agregar Nueva Funcionalidad

**Backend:**
```bash
cd ApiSensores
dotnet add package [nombre_paquete]
```

**Python:**
```bash
pip install [nombre_paquete]
pip freeze > requirements.txt
```

---

## 📝 Notas Importantes

- Asegurar que el ESP32 esté conectado a la misma red que el PC
- Configurar correctamente la URL del backend en el ESP32
- Revisar los logs de la API para diagnosticar problemas
- Mantener actualizada la base de datos

---

## 📧 Contacto

Para problemas o preguntas sobre el proyecto, consultar con el desarrollador.

---

**Versión:** 1.0  
**Última actualización:** Mayo 2026
