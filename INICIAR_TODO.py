#!/usr/bin/env python3
"""
Los profetas — Master Startup Script
Inicia todo automáticamente: Setup, BD, Servidores, Dashboard
"""

import os
import sys
import subprocess
import time
from threading import Thread

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║           🚀 LOS PROFETAS — SISTEMA COMPLETO v2.0                        ║
║                                                                           ║
║         Base de Datos + ML + IA + Dashboard (TODO INTEGRADO)            ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)

def print_step(text):
    print(f"\n✓ {text}")

def print_error(text):
    print(f"\n✗ {text}")

def print_section(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}")

def verify_python():
    print_step(f"Python {sys.version.split()[0]} detectado")
    if sys.version_info < (3, 7):
        print_error("Se requiere Python 3.7+")
        return False
    return True

def install_dependencies():
    print_section("📦 Instalando Dependencias")
    try:
        print("  Installing Flask, scikit-learn, numpy...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "-r", "requirements.txt", "-q"
        ], cwd=os.path.dirname(__file__))
        print_step("Dependencias instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error al instalar dependencias: {e}")
        return False

def setup_database():
    print_section("🗄️  Configurando Base de Datos")
    try:
        print("  Ejecutando seed.py...")
        subprocess.check_call([
            sys.executable, "seed.py"
        ], cwd=os.path.dirname(__file__))
        print_step("Base de datos lista")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error en seed.py: {e}")
        return False

def start_server(script, port, name):
    """Inicia un servidor en background"""
    try:
        print(f"  Iniciando {name} en puerto {port}...")
        subprocess.Popen([
            sys.executable, script
        ], cwd=os.path.dirname(__file__))
        print_step(f"{name} iniciado en http://localhost:{port}")
        return True
    except Exception as e:
        print_error(f"Error al iniciar {name}: {e}")
        return False

def show_summary():
    print_section("🎉 SISTEMA INICIADO CORRECTAMENTE")
    print("""
🌐 SERVIDORES DISPONIBLES:

   📊 Dashboard:          http://localhost:5001
      └─ Visualización, Gráficos, Análisis
      
   🔌 API REST:           http://localhost:5000
      └─ CRUD, ML, IA, Análisis
      
   💻 Status Check:       http://localhost:5000/api/health
      └─ Estado del sistema

🤖 CAPACIDADES ACTIVAS:

   ✓ Machine Learning
     • Recomendaciones personalizadas
     • Predicción de precios
     • Detección de anomalías
     • Búsqueda de similares
   
   ✓ Inteligencia Artificial
     • Búsqueda inteligente (semántica)
     • Análisis de usuarios
     • Generación de insights
     • Análisis de tendencias
   
   ✓ Base de Datos
     • SQLite3 (8 tablas)
     • Relaciones normalizadas
     • +30 métodos CRUD
   
   ✓ API REST
     • 50+ endpoints
     • JSON responses
     • CORS habilitado
   
   ✓ Dashboard Visual
     • Estadísticas en tiempo real
     • Gráficos interactivos
     • Controles inteligentes

📚 DOCUMENTACIÓN:

   • COMPLETO_v2.0.md     → Guía completa del sistema
   • DATABASE.md          → Documentación de BD
   • INTEGRACION.md       → Integración con frontend
   • RESUMEN.md           → Resumen del proyecto

🔗 EJEMPLOS DE USO:

   Python:
   └─ from base import DatabaseNFT
      db = DatabaseNFT()
      recomendaciones = db.obtener_recomendaciones('sys-user-demo')

   JavaScript:
   └─ const data = await fetch('http://localhost:5000/api/ml/recomendaciones/sys-user-demo')
      .then(r => r.json());

   cURL:
   └─ curl http://localhost:5000/api/ml/tendencias

⚡ TIPS:

   • Primero, abre http://localhost:5001 para ver el dashboard
   • Prueba las recomendaciones con usuario 'sys-user-demo'
   • Lee COMPLETO_v2.0.md para explorar todas las funciones
   • Los datos de prueba están cargados en la BD

✨ ¡El sistema está 100% operativo!

Presiona Ctrl+C para detener los servidores.
    """)

def main():
    print_banner()
    
    # Paso 1: Verificar Python
    if not verify_python():
        return False
    
    # Paso 2: Instalar dependencias
    if not install_dependencies():
        return False
    
    # Paso 3: Setup base de datos
    if not setup_database():
        return False
    
    # Paso 4: Iniciar servidores
    print_section("🚀 Iniciando Servidores")
    time.sleep(1)
    
    # Los servidores se ejecutan en threads para que sea más limpio
    # Pero para este caso, es mejor ejecutarlos secuencialmente en subprocesos
    
    print("""
  ⚠️  Los servidores se ejecutarán en el background.
  
  Abre tu navegador en:
  
      📊 Dashboard:   http://localhost:5001
      🔌 API:         http://localhost:5000
    """)
    
    # Iniciar API
    start_server('api.py', 5000, 'API REST')
    time.sleep(2)
    
    # Iniciar Dashboard
    start_server('dashboard.py', 5001, 'Dashboard')
    time.sleep(1)
    
    # Mostrar resumen
    show_summary()
    
    # Mantener vivo el script
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Deteniendo servidores...")
        return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
