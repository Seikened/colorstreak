"""
test_rich_logger.py — Demo de todas las features de RichLogger.

Uso:
    python test_rich.py
"""

import time

from colorstreak import RichLogger

log = RichLogger(style="inline")


def demo_base_levels():
    """P0: Niveles base con metadatos."""
    log.rule("P0 — Base Log Levels")

    log.debug("Esto es un mensaje de debug")
    log.info("Servidor iniciado en puerto 8080")
    log.warning("Cache expirado, regenerando...")
    log.error("No se pudo conectar a la base de datos")
    log.critical("Sistema de archivos lleno — servicio detenido")
    log.success("Deploy completado exitosamente")
    log.library("Cargando módulo: colorstreak v2.2.0")
    log.step("Paso 1/3: Verificando dependencias...")
    log.note("Nota: esto es baja prioridad")
    log.metric("loss=0.1234 acc=0.9876 latency_ms=42")
    log.title("=== Sección: Resultados ===")
    print()


def demo_level_filtering():
    """P0: Filtrado por nivel."""
    log.rule("P0 — Level Filtering")

    filtered_log = RichLogger(level="WARNING", style="inline")
    filtered_log.debug("NO deberías ver esto")
    filtered_log.info("NI esto")
    filtered_log.warning("Esto SÍ se muestra")
    filtered_log.error("Y esto también")
    print()


def demo_table():
    """P0: Tablas hermosas."""
    log.rule("P0 — Tables")

    # Desde lista de dicts
    log.table([
        {"ID": 1, "Nombre": "Carlos", "Rol": "Admin", "Último login": "hace 2 min"},
        {"ID": 2, "Nombre": "María", "Rol": "Editor", "Último login": "hace 1 hora"},
        {"ID": 3, "Nombre": "Juan", "Rol": "Viewer", "Último login": "hace 3 días"},
    ], title="Usuarios activos")

    # Desde columns + rows
    log.table(
        title="Métricas del sistema",
        columns=["Métrica", "Valor", "Estado"],
        rows=[
            ["CPU", "42%", "OK"],
            ["RAM", "78%", "⚠"],
            ["Disco", "91%", "🔴"],
        ],
    )
    print()


def demo_json():
    """P1: JSON con syntax highlighting."""
    log.rule("P1 — JSON")

    log.json({
        "status": "ok",
        "users": 42,
        "cache": True,
        "config": {
            "timeout": 30,
            "retries": 3,
            "endpoints": ["/api/v1", "/api/v2"],
        },
    })
    print()


def demo_exception():
    """P1: Tracebacks hermosos."""
    log.rule("P1 — Exception")

    try:
        result = 1 / 0
    except ZeroDivisionError:
        log.exception("Algo salió mal en el cálculo")
    print()


def demo_benchmark():
    """P1: Medición de tiempos."""
    log.rule("P1 — Benchmark")

    with log.benchmark("Operación rápida", slow_threshold=1.0):
        time.sleep(0.1)

    with log.benchmark("Operación lenta", slow_threshold=0.05):
        time.sleep(0.2)
    print()


def demo_group():
    """P1: Agrupación visual."""
    log.rule("P1 — Groups")

    with log.group("Inicializando servicios"):
        log.info("Conectando a Redis...")
        log.info("Conectando a PostgreSQL...")
        with log.group("Migraciones"):
            log.step("Ejecutando migración 001...")
            log.step("Ejecutando migración 002...")
            log.success("Migraciones completas")
        log.success("Todos los servicios listos")
    print()


def demo_http():
    """P2: HTTP logging."""
    log.rule("P2 — HTTP")

    log.http("GET", "/api/users", status=200, duration=0.045)
    log.http("POST", "/api/login", status=201, duration=0.12)
    log.http("GET", "/api/search", status=304, duration=0.008)
    log.http("PUT", "/api/users/5", status=401, duration=0.05)
    log.http("DELETE", "/api/sessions", status=500, duration=3.2)
    print()


def demo_sql():
    """P2: SQL con syntax highlighting."""
    log.rule("P2 — SQL")

    log.sql("""
        SELECT u.name, u.email, COUNT(o.id) as orders
        FROM users u
        LEFT JOIN orders o ON o.user_id = u.id
        WHERE u.active = true
        GROUP BY u.name, u.email
        ORDER BY orders DESC
        LIMIT 10
    """)
    print()


def demo_header():
    """P2: Banner de inicio."""
    log.rule("P2 — Header")

    log.header(
        "ColorStreak API",
        version="2.2.0",
        env="production",
        port=8080,
        workers=4,
    )
    print()


def demo_env():
    """P2: Variables de entorno."""
    import os
    os.environ["DATABASE_URL"] = "postgres://localhost:5432/mydb"
    os.environ["REDIS_URL"] = "redis://localhost:6379"
    os.environ["SECRET_KEY"] = "sk-super-secret-key-12345678"
    os.environ["DEBUG"] = "true"

    log.rule("P2 — Environment Variables")
    log.env("DATABASE_URL", "REDIS_URL", "SECRET_KEY", "DEBUG", "API_TOKEN")
    print()


def demo_inspect():
    """P3: Inspeccionar objetos."""
    log.rule("P3 — Inspect")

    class User:
        def __init__(self, name: str, age: int, role: str):
            self.name = name
            self.age = age
            self.role = role

        def greet(self) -> str:
            return f"Hola, soy {self.name}"

    user = User("Carlos", 28, "admin")
    log.inspect(user)
    print()


def demo_code():
    """P3: Code snippets."""
    log.rule("P3 — Code")

    log.code("""
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Ejemplo
for i in range(10):
    print(fibonacci(i), end=" ")
    """, title="Fibonacci recursivo")
    print()


def demo_tree():
    """P3: Estructuras jerárquicas."""
    log.rule("P3 — Tree")

    log.tree("Mi Proyecto", {
        "src": {
            "main.py": None,
            "utils.py": None,
            "models": {
                "user.py": None,
                "product.py": None,
            },
        },
        "tests": {
            "test_main.py": None,
            "test_utils.py": None,
        },
        "README.md": None,
        "pyproject.toml": None,
    })
    print()


def demo_diff():
    """P3: Comparación antes/después."""
    log.rule("P3 — Diff")

    old_config = """timeout=30
retries=3
debug=false
log_level=INFO"""

    new_config = """timeout=60
retries=5
debug=true
log_level=DEBUG
cache_ttl=300"""

    log.diff(old_config, new_config, context="config.ini")
    print()


def demo_panel():
    """P3: Panel destacado."""
    log.rule("P3 — Panel")

    log.panel(
        "El servidor se reiniciará en 30 segundos.\nPor favor guarde su trabajo.",
        title="Mantenimiento programado",
        style="warning",
    )
    print()


def demo_count():
    """P3: Contadores."""
    log.rule("P3 — Counters")

    for _ in range(150):
        log.count("requests_processed")
    for _ in range(42):
        log.count("cache_hits")
    for _ in range(7):
        log.count("errors")

    log.count_summary(title="Resumen de operaciones")
    print()


def demo_styles():
    """Comparación de estilos."""
    log.rule("Bonus — Style Comparison")

    for style in ("panel", "inline", "minimal"):
        styled = RichLogger(style=style, timestamp=False)
        print(f"\n  style={style!r}:")
        styled.info("Mensaje de ejemplo")
        styled.warning("Advertencia de ejemplo")
        styled.error("Error de ejemplo")
    print()


def main():
    print("\n")
    log.header("RichLogger Demo", version="1.0.0", features="20")

    demo_base_levels()
    demo_level_filtering()
    demo_table()
    demo_json()
    demo_exception()
    demo_benchmark()
    demo_group()
    demo_http()
    demo_sql()
    demo_header()
    demo_env()
    demo_inspect()
    demo_code()
    demo_tree()
    demo_diff()
    demo_panel()
    demo_count()
    demo_styles()

    log.rule("✔ Demo completo")


if __name__ == "__main__":
    main()
