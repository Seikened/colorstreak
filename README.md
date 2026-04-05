
# colorstreak

Minimal color logging for Python terminals. Two loggers in one package:

- **`Logger`** — zero-dependency ANSI logger that works like `print()`
- **`RichLogger`** — feature-rich logger powered by [Rich](https://github.com/Textualize/rich) with tables, JSON, trees, benchmarks, and more

## Instalacion

```bash
pip install colorstreak
```

---

## Logger (basico)

ANSI puro, sin dependencias. Se siente como `print()`.

```python
from colorstreak import Logger

Logger.info("Servidor arriba")
Logger.warning("Cache fria")
Logger.error("No se pudo conectar")
Logger.success("Deploy OK")
```

### Niveles disponibles

| Metodo | Color |
|---|---|
| `Logger.debug()` | Verde |
| `Logger.info()` | Azul |
| `Logger.warning()` | Amarillo |
| `Logger.error()` | Rojo |
| `Logger.success()` | Verde |
| `Logger.library()` | Magenta |
| `Logger.step()` | Cyan |
| `Logger.note()` | Gris |
| `Logger.title()` | Azul bold |
| `Logger.metric()` | Magenta |

### Estilos

```python
Logger.configure(style="soft")  # "full" (default) | "prefix" | "soft"
```

O por variable de entorno:

```bash
export COLORSTREAK_STYLE=prefix
```

### Compatible con print()

```python
Logger.info("Multiple", "args", 123, sep=" | ")
Logger.warning("Sin salto...", end="")
```

### Desactivar colores

```bash
export NO_COLOR=1
```

---

## RichLogger (avanzado)

Logger con Rich para output profesional en terminal.

```python
from colorstreak import RichLogger

log = RichLogger(style="inline")
```

### Configuracion

```python
log = RichLogger(
    level="DEBUG",       # nivel minimo: DEBUG, INFO, WARNING, ERROR, CRITICAL
    style="inline",      # "panel" | "inline" | "minimal"
    metadata=True,       # muestra archivo:linea en cada log
    timestamp=True,      # muestra hora
)
```

### Niveles

```python
log.debug("Mensaje de debug")
log.info("Servidor iniciado en puerto 8080")
log.warning("Cache expirado")
log.error("No se pudo conectar a la DB")
log.critical("Sistema de archivos lleno")
log.success("Deploy completado")
log.library("Cargando modulo: colorstreak")
log.step("Paso 1/3: Verificando...")
log.note("Nota de baja prioridad")
log.metric("loss=0.1234 acc=0.9876")
log.title("=== Seccion: Resultados ===")
```

### Filtrado por nivel

```python
log = RichLogger(level="WARNING")
log.debug("No se muestra")
log.warning("Esto si")
```

### Tablas

```python
# Desde lista de dicts
log.table([
    {"ID": 1, "Nombre": "Carlos", "Rol": "Admin"},
    {"ID": 2, "Nombre": "Maria", "Rol": "Editor"},
], title="Usuarios")

# Desde columns + rows
log.table(
    columns=["Metrica", "Valor"],
    rows=[["CPU", "42%"], ["RAM", "78%"]],
)
```

### JSON

```python
log.json({
    "status": "ok",
    "config": {"timeout": 30, "retries": 3},
})
```

### Excepciones

```python
try:
    result = 1 / 0
except ZeroDivisionError:
    log.exception("Algo salio mal")
```

### Benchmark

```python
with log.benchmark("Operacion pesada", slow_threshold=1.0):
    time.sleep(0.5)
```

### Grupos

```python
with log.group("Inicializando servicios"):
    log.info("Conectando a Redis...")
    log.success("Listo")
```

### HTTP

```python
log.http("GET", "/api/users", status=200, duration=0.045)
log.http("POST", "/api/login", status=201, duration=0.12)
log.http("DELETE", "/api/sessions", status=500, duration=3.2)
```

### SQL

```python
log.sql("""
    SELECT u.name, COUNT(o.id) as orders
    FROM users u
    LEFT JOIN orders o ON o.user_id = u.id
    WHERE u.active = true
    LIMIT 10
""")
```

### Header (banner de inicio)

```python
log.header(
    "Mi API",
    version="1.0.0",
    env="production",
    port=8080,
)
```

### Variables de entorno

```python
# Explicito: muestra solo las que pidas
log.env("DATABASE_URL", "REDIS_URL", "SECRET_KEY")

# Auto-discover: lee las variables de los archivos .env* del proyecto
log.env()
```

El auto-discover parsea todos los archivos `.env`, `.env.local`, `.env.secret`, etc. del root del proyecto. Las variables con nombres como `SECRET`, `KEY`, `TOKEN`, `PASSWORD` se enmascaran automaticamente.

### Tree (estructura de directorios)

```python
# Manual: pasa tu propio dict
log.tree("Mi Proyecto", {
    "src": {"main.py": None, "utils.py": None},
    "tests": {"test_main.py": None},
    "README.md": None,
})

# Auto-discover: escanea el proyecto desde el root
log.tree()

# Con profundidad maxima
log.tree(max_depth=2)
```

El auto-discover detecta el root del proyecto buscando `pyproject.toml`, `package.json`, `.git`, etc. Ignora carpetas como `.git`, `__pycache__`, `.venv`, `node_modules`.

### Inspect

```python
log.inspect(mi_objeto)
log.inspect(mi_objeto, methods=True)
```

### Code

```python
log.code("""
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
""", title="Fibonacci", language="python")
```

### Diff

```python
log.diff(old_text, new_text, context="config.ini")
```

### Panel

```python
log.panel(
    "El servidor se reiniciara en 30 segundos.",
    title="Mantenimiento",
    style="warning",  # "info" | "warning" | "error" | "success"
)
```

### Contadores

```python
for request in requests:
    log.count("requests_processed")

log.count_summary(title="Resumen")
```

### Log a archivo

```python
log.to_file("output.log")
# A partir de aqui, todo se escribe tambien al archivo (sin colores)
```

### Regla visual

```python
log.rule("Seccion importante")
```

---

## Requisitos

- Python >= 3.10
- `rich` (se instala automaticamente)
